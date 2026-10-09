import argparse
import ast
import csv
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal, localcontext
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from threadpoolctl import threadpool_limits


ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / ".agent/qa/phase2b2-20261009"
RUN = ROOT / "models/runs/20261009-phase2b2-a"
ML = ROOT / "data/ml/runs/20261009-phase2a-a"
CANDIDATE = ROOT / "models/runs/20261009-phase2b1-a2"
FINAL = ROOT / "models/final/hgb-uci-hourly-v1.0-train-only"
sys.path.insert(0, str(ROOT / "forecasting"))
from predictor import POLICY, nonnegative, predict_bundle

CHECKS = []
FIT_CALLS = 0
META = ["target_hour", "prediction_origin", "target_end", "latest_observed_hour", "target_energy_kwh"]


def now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check(name, passed, details=None):
    CHECKS.append(dict(name=name, passed=bool(passed), details=details))
    if not passed:
        raise AssertionError(name)


def protect():
    def reject(*args, **kwargs):
        global FIT_CALLS
        FIT_CALLS += 1
        raise PermissionError("No training in final verification")

    HistGradientBoostingRegressor.fit = reject
    frozen = read_json(QA / "preservation-before.json")["files"]
    protected_files = {str(Path(p).absolute()) for p in frozen}
    protected_roots = [ROOT / p for p in ("data", "pipeline", "models/runs/20261009-phase2b1-a2",
                       "models/runs/20261009-phase2b1-b", ".agent/qa/phase2b1-20261009")]

    def audit(event, arguments):
        if event != "open" or not isinstance(arguments[0], (str, bytes)):
            return
        path = Path(os.fsdecode(arguments[0])).absolute()
        if arguments[2] & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
            if str(path) in protected_files or any(base == path or base in path.parents for base in protected_roots):
                raise PermissionError("Accepted artifacts are immutable")

    sys.addaudithook(audit)


def preservation():
    prior = read_json(QA / "preservation-before.json")
    changed = []
    cache = []
    matched = 0
    for path, expected in prior["files"].items():
        actual = sha256(path) if Path(path).is_file() else None
        if actual == expected:
            matched += 1
        elif "/flink-tmp/" in path:
            cache.append(dict(path=path, expected=expected, actual=actual))
        else:
            changed.append(dict(path=path, expected=expected, actual=actual))
    return dict(captured_at=now(), count=prior["count"], matched=matched,
                changed_products=changed, current_new_cache_exceptions=cache,
                inherited_runtime_exceptions=prior["current_runtime_exceptions"],
                historical_68=prior["historical_68"], inherited_933_matched=prior["inherited_matched"])


def array_hash(values):
    return hashlib.sha256(np.asarray(values, dtype="<f8").tobytes()).hexdigest()


def cold(model_path, output_path):
    protect()
    bundle = joblib.load(model_path)
    frame = pd.read_csv(ML / "holdout/test.csv", float_precision="round_trip")
    saved = pd.read_csv(RUN / "predictions-test.csv", float_precision="round_trip")
    with threadpool_limits(limits=2):
        raw, final = predict_bundle(bundle, frame[bundle["feature_columns"]])
    result = dict(captured_at=now(), pid=os.getpid(), python=platform.python_version(),
                  model_sha256=sha256(model_path), feature_columns=bundle["feature_columns"],
                  n=len(raw), fit_calls=FIT_CALLS, labels_passed_to_predict=False,
                  exact_raw=np.array_equal(raw, saved["hgb_raw_kwh"].to_numpy()),
                  exact_final=np.array_equal(final, saved["hgb_final_kwh"].to_numpy()),
                  maximum_difference_kwh=float(np.max(abs(raw-saved["hgb_raw_kwh"].to_numpy()))),
                  raw_sha256=array_hash(raw), final_sha256=array_hash(final),
                  estimator_fingerprint=joblib.hash(bundle["estimator"], hash_name="sha1"),
                  evaluated_again=False, note="Fixed-model inference only; no scoring, fit or model selection")
    write_json(output_path, result)
    print(json.dumps(result))


def run_cold(model, name):
    output = QA / name
    completed = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()),
                                "--cold-model", str(model), "--cold-output", str(output)],
                               text=True, capture_output=True, timeout=60)
    check(name+"_separate_process", completed.returncode == 0, dict(exit_code=completed.returncode,
          stderr=completed.stderr, stdout=completed.stdout))
    witness = read_json(output)
    check(name+"_exact_predictions_no_fit", witness["exact_raw"] and witness["exact_final"] and
          witness["fit_calls"] == 0 and witness["n"] == 4590 and witness["pid"] != os.getpid(), witness)
    return witness


def independent_features(test, lock):
    with (ROOT / lock["flink_source"]["path"]).open(newline="", encoding="utf-8") as handle:
        hourly = list(csv.DictReader(handle))
    reference = {datetime.fromisoformat(r["hour_start"]): None if r["energy_kwh"] == "NULL"
                 else Decimal(r["energy_kwh"]) for r in hourly}
    axis = list(reference)
    hour = timedelta(hours=1)
    check("full_hourly_axis_and_missing_policy", len(reference) == 34589 and
          all(b-a == hour for a, b in zip(axis, axis[1:])) and
          sum(v is None for v in reference.values()) == 504 and
          all((r["energy_kwh"] != "NULL") == (r["is_complete"] == "true") for r in hourly))

    def features_at(stamp, energy):
        expected = {f"lag_{k}_kwh": energy.get(stamp-k*hour) for k in (1, 2, 3, 24, 168)}
        for window in (3, 24):
            values = [energy.get(stamp-k*hour) for k in range(1, window+1)]
            expected[f"rolling_mean_{window}_kwh"] = (sum(values)/Decimal(window)
                if all(v is not None for v in values) else None)
        expected.update(target_hour_of_day=stamp.hour, target_day_of_week=stamp.weekday(),
                        target_month=stamp.month, target_is_weekend=int(stamp.weekday() >= 5))
        return expected

    expected_mask = []
    with localcontext() as ctx:
        ctx.prec = 45
        for stamp in axis[len(axis)*85//100:]:
            values = features_at(stamp, reference)
            if reference[stamp] is not None and all(v is not None for v in values.values()):
                expected_mask.append(stamp)
        times = [datetime.fromisoformat(value) for value in test["target_hour"]]
        check("independent_Test_eligibility_exact_4590_no_mask_change", times == expected_mask and
              len(expected_mask) == 4590, dict(first=str(times[0]), last=str(times[-1]), axis_hours=5189, excluded=599))
        maximum = Decimal(0)
        mismatches = []
        for row in test.to_dict("records"):
            stamp = datetime.fromisoformat(row["target_hour"])
            expected = features_at(stamp, reference)
            expected["target_energy_kwh"] = reference[stamp]
            for name, value in expected.items():
                difference = abs(Decimal(str(row[name]))-Decimal(value))
                maximum = max(maximum, difference)
                if difference > Decimal("2e-14"):
                    mismatches.append([str(stamp), name, str(difference)])
        check("all_11_features_and_targets_independent_timestamp_oracle", not mismatches,
              dict(rows=4590, maximum_difference_kwh=str(maximum), errors=mismatches[:10]))
        check("no_future_measurement_offsets", all(spec["latest_source_offset_hours"] is None or
              spec["latest_source_offset_hours"] < 0 for spec in lock["feature_schema"]["features"]))
        stamp = times[len(times)//2]
        mutated = {s: (v+Decimal(999) if v is not None and s >= stamp else v) for s, v in reference.items()}
        check("target_and_future_hour_perturbation_cannot_change_current_features",
              features_at(stamp, reference) == features_at(stamp, mutated), dict(timestamp=str(stamp)))


def metric_oracle(predictions, metrics):
    with (RUN / "predictions-test.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    result = {}
    with localcontext() as ctx:
        ctx.prec = 45
        for name in ("hgb", "naive", "seasonal_naive_24"):
            values = {}
            for variant in ("raw", "final"):
                errors = [Decimal(row[name+"_"+variant+"_kwh"])-Decimal(row["target_energy_kwh"]) for row in rows]
                mae = sum(abs(v) for v in errors)/Decimal(len(errors))
                rmse = (sum(v*v for v in errors)/Decimal(len(errors))).sqrt()
                values[variant] = dict(mae_kwh=str(mae), rmse_kwh=str(rmse))
                for kind, value in (("mae", mae), ("rmse", rmse)):
                    key = ("raw_" if variant == "raw" else "")+kind+"_kwh"
                    check(name+"_"+variant+"_"+kind+"_Decimal_vs_library",
                          abs(value-Decimal(str(metrics["models"][name][key]))) < Decimal("1e-12"),
                          dict(decimal=str(value), library=metrics["models"][name][key], tolerance_kwh="1e-12"))
            raw = predictions[name+"_raw_kwh"].to_numpy()
            final = predictions[name+"_final_kwh"].to_numpy()
            item = metrics["models"][name]
            check(name+"_D09_all_rows_and_counts", np.array_equal(final, np.maximum(0, raw)) and
                  int((raw < 0).sum()) == item["negative_raw_count"] and
                  int((raw != final).sum()) == item["changed_prediction_count"] and
                  float(raw.min()) == item["minimum_raw_kwh"])
            check(name+"_D09_metric_effect", all(abs(item["raw_"+kind+"_kwh"]-item[kind+"_kwh"]-
                  item["d09_"+kind+"_reduction_kwh"]) < 1e-12 for kind in ("mae", "rmse")))
            result[name] = values
    write_json(QA / "metric-oracle.json", dict(method="Decimal45 from saved CSV; no sklearn metric function", n=4590, models=result))


def main():
    protect()
    lock = read_json(QA / "selection-lock.json")
    pretest = read_json(QA / "pretest-verification.json")
    started = read_json(QA / "evaluation-started.json")
    completed = read_json(QA / "evaluation-completed.json")
    manifest = read_json(RUN / "manifest.json")
    metrics = read_json(RUN / "metrics-test.json")
    runtime = read_json(RUN / "runtime-evidence.json")
    features = lock["feature_schema"]["feature_columns"]
    check("selection_pretest_PASS_before_official_Test_start", lock["status"] == "LOCKED" and
          lock["refit"] is False and pretest["status"] == "VERIFIED" and pretest["passed"] == pretest["total_checks"] == 17 and
          all(item["passed"] for item in pretest["checks"]) and not pretest["test_content_read"] and pretest["fit_calls"] == 0 and
          lock["locked_at"] <= pretest["captured_at"] < started["started_at"] < completed["completed_at"] and
          pretest["selection_lock_sha256"] == started["selection_lock_sha256"] == sha256(QA / "selection-lock.json") and
          started["pretest_sha256"] == sha256(QA / "pretest-verification.json"))
    check("one_official_evaluation_and_runtime_no_fit", started["evaluation_number"] == completed["official_evaluation_number"] ==
          metrics["official_evaluation_number"] == 1 and runtime["state"]["fit_calls"] == 0 and
          runtime["state"]["test_text_opens"] == 1 and runtime["no_fit"] and not runtime["target_passed_to_predict"] and
          runtime["evaluation_started_sha256"] == sha256(QA / "evaluation-started.json"))
    check("candidate_and_Test_hash_exact_approved", sha256(CANDIDATE / "candidate.joblib") == lock["candidate_sha256"] ==
          "94ed8c4e493025ae363a3cc6fb1b0639ef2368264966b5bda190303e98a95c38" and
          sha256(ML / "holdout/test.csv") == lock["test_sha256"] ==
          "f9785b91f46c43bbb22c08c98294cd32739f75e5df0218e355baa53d5fbd3574")
    check("evaluation_output_and_code_hashes", all(sha256(RUN/name) == value for name, value in manifest["outputs_sha256"].items()) and
          all(sha256(ROOT/name) == value for name, value in manifest["code_sha256"].items()) and
          manifest["code_sha256"]["forecasting/evaluate_final.py"] == lock["evaluation_code_sha256"] and
          completed["manifest_sha256"] == sha256(RUN / "manifest.json"))
    check("ML_Flink_lineage_unchanged", sha256(ML / "manifest.json") == lock["source_phase2a_manifest_sha256"] and
          sha256(ML / "verification.json") == lock["source_phase2a_verification_sha256"] and
          all(sha256(ML/name) == expected for name, expected in lock["source_phase2a_outputs"].items()) and
          sha256(ROOT / lock["flink_source"]["path"]) == lock["flink_source"]["sha256"] and
          manifest["flink_source"] == lock["flink_source"])
    check("pinned_runtime_packages", platform.python_version() == lock["python"] == "3.12.3" and
          all(importlib.metadata.version(name) == value for name, value in lock["packages"].items()))
    tree = ast.parse((ROOT / "forecasting/evaluate_final.py").read_text())
    check("evaluation_code_has_no_fit_or_hyperparameter_search_call", not any(isinstance(node, ast.Call) and
          isinstance(node.func, ast.Attribute) and node.func.attr in ("fit", "fit_predict", "fit_transform", "set_params")
          for node in ast.walk(tree)))
    test = pd.read_csv(ML / "holdout/test.csv", float_precision="round_trip")
    predictions = pd.read_csv(RUN / "predictions-test.csv", float_precision="round_trip")
    expected_columns = META+[name+"_"+variant+"_kwh" for name in ("hgb", "naive", "seasonal_naive_24") for variant in ("raw", "final")]
    check("Test_and_prediction_schema_4590_finite_nonnegative_targets", list(test.columns) == META+features and
          list(predictions.columns) == expected_columns and len(test) == len(predictions) == metrics["n"] == 4590 and
          np.isfinite(test[features+["target_energy_kwh"]].to_numpy()).all() and
          np.isfinite(predictions.select_dtypes(include=np.number).to_numpy()).all() and (test["target_energy_kwh"] >= 0).all())
    check("shared_mask_target_origin_end_exact", predictions[META].equals(test[META]) and test["target_hour"].is_unique and
          test["target_hour"].is_monotonic_increasing and all(pd.to_datetime(test[name]).equals(
          pd.to_datetime(test["target_hour"])+pd.Timedelta(hours=offset)) for name, offset in
          (("prediction_origin", 0), ("target_end", 1), ("latest_observed_hour", -1))))
    check("baseline_predictions_are_past_lag1_lag24", np.array_equal(predictions["naive_raw_kwh"], test["lag_1_kwh"]) and
          np.array_equal(predictions["seasonal_naive_24_raw_kwh"], test["lag_24_kwh"]))
    independent_features(test, lock)
    metric_oracle(predictions, metrics)
    bundle = joblib.load(CANDIDATE / "candidate.joblib")
    check("candidate_still_Train_only_22513_no_early_stop", bundle["training_split"] == "train" and not bundle["final_locked"] and
          bundle["feature_columns"] == features and bundle["prediction_policy"] == POLICY and
          lock["fitted_rows"] == 22513 and bundle["estimator"].n_iter_ == 200 and not bundle["estimator"].do_early_stopping_)
    with threadpool_limits(limits=2):
        raw, final = predict_bundle(bundle, test[features])
        changed_labels = test.copy()
        changed_labels["target_energy_kwh"] += 999
        mutated_raw, mutated_final = predict_bundle(bundle, changed_labels[features])
    check("Test_label_perturbation_cannot_change_predictions", np.array_equal(raw, mutated_raw) and np.array_equal(final, mutated_final))
    check("in_process_fixed_candidate_exact_saved_predictions", np.array_equal(raw, predictions["hgb_raw_kwh"]) and
          np.array_equal(final, predictions["hgb_final_kwh"]))
    check("D09_negative_zero_positive_fixture", np.array_equal(nonnegative([-2, -0.0, 0, 2]), [0, 0, 0, 2]))
    rejected = []
    for values in ([np.nan], [np.inf], [[1, 2]]):
        try:
            nonnegative(values)
        except ValueError:
            rejected.append(True)
    check("D09_rejects_nonfinite_and_nonvector", len(rejected) == 3)
    for name, frame in (("feature_order", test[list(reversed(features))]),
                        ("target_column", test[features+["target_energy_kwh"]])):
        did_reject = False
        try:
            predict_bundle(bundle, frame)
        except ValueError:
            did_reject = True
        check(name+"_invalid_inference_schema_rejected", did_reject)
    witness = run_cold(CANDIDATE / "candidate.joblib", "reproducibility-candidate.json")
    preserved = preservation()
    check("accepted_artifacts_preserved_before_final_packaging", not preserved["changed_products"],
          dict(count=preserved["count"], matched=preserved["matched"], cache=len(preserved["current_new_cache_exceptions"])))
    check("no_training_during_independent_QA", FIT_CALLS == 0)
    write_json(QA / "test-verification.json", dict(status="VERIFIED", captured_at=now(), passed=len(CHECKS), total_checks=len(CHECKS),
               checks=list(CHECKS), preservation=preserved, metrics_sha256=sha256(RUN / "metrics-test.json"),
               predictions_sha256=sha256(RUN / "predictions-test.csv"), verifier_sha256=sha256(Path(__file__)), fit_calls=FIT_CALLS))
    FINAL.mkdir(parents=True, exist_ok=False)
    packaged = dict(bundle)
    packaged.update(final_locked=True, model_version=lock["final_version"], selected_candidate_sha256=lock["candidate_sha256"], refit=False)
    joblib.dump(packaged, FINAL / "model.joblib", compress=3, protocol=5)
    loaded = joblib.load(FINAL / "model.joblib")
    check("final_metadata_LOCKED_Train_only_no_refit", loaded["final_locked"] and loaded["refit"] is False and
          loaded["model_version"] == lock["final_version"] and loaded["feature_columns"] == features and
          loaded["prediction_policy"] == POLICY and loaded["training_split"] == "train")
    check("final_estimator_identical_to_candidate_fingerprint", joblib.hash(loaded["estimator"], hash_name="sha1") == witness["estimator_fingerprint"])
    final_witness = run_cold(FINAL / "model.joblib", "reproducibility-final.json")
    check("candidate_final_prediction_digest_exact", witness["raw_sha256"] == final_witness["raw_sha256"] and
          witness["final_sha256"] == final_witness["final_sha256"])
    write_json(FINAL / "manifest.json", dict(status="LOCKED", created_at=now(), version=lock["final_version"],
               model_sha256=sha256(FINAL / "model.joblib"), candidate_path=lock["candidate_path"], candidate_sha256=lock["candidate_sha256"],
               no_refit=True, training_split="train", fitted_rows=22513, feature_columns=features, prediction_policy=POLICY,
               python=lock["python"], packages=lock["packages"], source_phase2a_manifest_sha256=lock["source_phase2a_manifest_sha256"],
               source_phase2a_outputs=lock["source_phase2a_outputs"], flink_source=lock["flink_source"],
               selection_lock_sha256=sha256(QA / "selection-lock.json"), test_verification_sha256=sha256(QA / "test-verification.json"),
               test_metrics=metrics, prediction_path=str((RUN / "predictions-test.csv").relative_to(ROOT)),
               prediction_sha256=sha256(RUN / "predictions-test.csv"), estimator_fingerprint=final_witness["estimator_fingerprint"],
               packaging="Same fitted estimator; wrapper metadata changed only. Final hash differs from candidate because metadata differs.",
               official_evaluation_number=1, protocol=lock["protocol"]))
    check("final_manifest_hash_model_and_verified_Test", read_json(FINAL / "manifest.json")["model_sha256"] == sha256(FINAL / "model.joblib") and
          read_json(FINAL / "manifest.json")["test_verification_sha256"] == sha256(QA / "test-verification.json"))
    preserved = preservation()
    check("accepted_artifacts_preserved_after_packaging_no_fit", not preserved["changed_products"] and FIT_CALLS == 0, preserved)
    write_json(QA / "verification.json", dict(status="VERIFIED", captured_at=now(), passed=len(CHECKS), total_checks=len(CHECKS),
               checks=CHECKS, preservation=preserved, final_model_sha256=sha256(FINAL / "model.joblib"),
               final_manifest_sha256=sha256(FINAL / "manifest.json"), no_refit=True, fit_calls=FIT_CALLS,
               official_evaluation_number=1, verifier_sha256=sha256(Path(__file__))))
    write_json(RUN / "verification.json", dict(status="VERIFIED", captured_at=now(), passed=len(CHECKS), total_checks=len(CHECKS),
               qa_path=str((QA / "verification.json").relative_to(ROOT)), qa_sha256=sha256(QA / "verification.json"),
               final_path=str(FINAL.relative_to(ROOT)), final_model_sha256=sha256(FINAL / "model.joblib")))
    print(json.dumps(dict(status="VERIFIED", checks=len(CHECKS), final_model=str(FINAL / "model.joblib"),
                         final_sha256=sha256(FINAL / "model.joblib"), metrics=metrics["models"], fit_calls=FIT_CALLS)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cold-model")
    parser.add_argument("--cold-output")
    args = parser.parse_args()
    cold(Path(args.cold_model), Path(args.cold_output)) if args.cold_model else main()

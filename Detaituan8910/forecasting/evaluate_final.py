import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from threadpoolctl import threadpool_limits

from predictor import POLICY, nonnegative, predict_bundle


ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / ".agent/qa/phase2b2-20261009"
SOURCE = ROOT / "data/ml/runs/20261009-phase2a-a"
CANDIDATE = ROOT / "models/runs/20261009-phase2b1-a2"
OUTPUT = ROOT / "models/runs/20261009-phase2b2-a"
MODEL_HASH = "94ed8c4e493025ae363a3cc6fb1b0639ef2368264966b5bda190303e98a95c38"
TEST_HASH = "f9785b91f46c43bbb22c08c98294cd32739f75e5df0218e355baa53d5fbd3574"
META = ["target_hour", "prediction_origin", "target_end", "latest_observed_hour", "target_energy_kwh"]
STATE = dict(test_authorized=False, hashing=None, test_text_opens=0, test_hash_opens=0, fit_calls=0)
CHECKS = []


def now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def sha256(path):
    path = Path(path)
    prior = STATE["hashing"]
    STATE["hashing"] = str(path.absolute())
    try:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    finally:
        STATE["hashing"] = prior


def check(name, passed, details=None):
    CHECKS.append(dict(name=name, passed=bool(passed), details=details))
    if not passed:
        raise AssertionError(name)


def install_guards():
    def reject_fit(*args, **kwargs):
        STATE["fit_calls"] += 1
        raise PermissionError("Refit is forbidden in Phase2B2")

    HistGradientBoostingRegressor.fit = reject_fit
    frozen_roots = [ROOT / p for p in ("data/raw", "data/processed", "data/ml", "pipeline",
                    "models/runs/20261009-phase2b1-a2", "models/runs/20261009-phase2b1-b")]
    test_paths = {str((ROOT / "data/ml/runs" / run / "holdout/test.csv").absolute())
                  for run in ("20261009-phase2a-a", "20261009-phase2a-b")}

    def audit(event, arguments):
        if event != "open" or not isinstance(arguments[0], (str, bytes)):
            return
        path = Path(os.fsdecode(arguments[0])).absolute()
        mode, flags = arguments[1], arguments[2]
        writing = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if writing and any(path == base or base in path.parents for base in frozen_roots):
            raise PermissionError("Cannot write accepted source artifacts")
        if str(path) not in test_paths:
            return
        if STATE["hashing"] == str(path) and not writing:
            STATE["test_hash_opens"] += 1
            return
        if not STATE["test_authorized"]:
            raise PermissionError("Test content cannot open before selection lock and pretest PASS")
        if writing:
            raise PermissionError("Test is immutable")
        STATE["test_text_opens"] += 1

    sys.addaudithook(audit)


def source_gate():
    manifest = read_json(CANDIDATE / "manifest.json")
    companion = read_json(CANDIDATE / "verification.json")
    check("candidate_VERIFIED_bound_to_37_checks", companion["status"] == "VERIFIED" and
          companion["passed"] == companion["total_checks"] == 37 and
          sha256(ROOT / companion["qa_path"]) == companion["qa_sha256"])
    check("candidate_exact_approved_hash", sha256(CANDIDATE / "candidate.joblib") == MODEL_HASH)
    check("candidate_outputs_and_code_frozen", all(sha256(CANDIDATE / name) == expected
          for name, expected in manifest["outputs_sha256"].items()) and
          all(sha256(ROOT / "forecasting" / name) == expected for name, expected in manifest["code_sha256"].items()))
    ml = read_json(SOURCE / "manifest.json")
    verified = read_json(SOURCE / "verification.json")
    check("Phase2A_manifest_verification_bound", sha256(SOURCE / "manifest.json") == manifest["source_phase2a_manifest_sha256"] and
          sha256(SOURCE / "verification.json") == manifest["source_phase2a_verification_sha256"] and verified["status"] == "VERIFIED")
    check("all_ML_outputs_unchanged_binary_hashes", ml["outputs_sha256"] == manifest["source_phase2a_outputs"] and
          all(sha256(SOURCE / name) == expected for name, expected in ml["outputs_sha256"].items()))
    source = ml["source"]
    hourly = ROOT / source["path"]
    check("Flink_lineage_hashes", source == manifest["flink_source"] and sha256(hourly) == source["sha256"] and
          sha256(hourly.parent / "manifest.json") == source["manifest_sha256"] and
          sha256(hourly.parent / "verification.json") == source["verification_sha256"])
    seal = read_json(SOURCE / "holdout/seal.json")
    check("Test_seal_4590_and_expected_hash", seal["status"] == "SEALED_FOR_FINAL_EVALUATION" and
          seal["test_evaluated"] is False and seal["eligible_hours"] == 4590 and
          seal["test_sha256"] == TEST_HASH == sha256(SOURCE / "holdout/test.csv"))
    installed = {name: importlib.metadata.version(name) for name in manifest["packages"]}
    check("pinned_Python_and_packages", platform.python_version() == manifest["python"] == "3.12.3" and
          installed == manifest["packages"] and installed["scikit-learn"] == "1.6.1", installed)
    config = read_json(CANDIDATE / "model-config.json")
    schema = read_json(SOURCE / "feature-schema.json")
    features = schema["feature_columns"]
    expected = dict(loss="squared_error", learning_rate=0.05, max_iter=200, max_leaf_nodes=15,
                    min_samples_leaf=30, l2_regularization=1.0, max_bins=255, early_stopping=False, random_state=42)
    check("fixed_config_features_D09_no_refit", config["approved_parameters"] == expected and
          config["feature_columns"] == features and len(features) == 11 and config["prediction_policy"] == POLICY and
          manifest["training_split"] == "train" and manifest["train_n"] == 22513)
    return manifest, schema, config, installed


def load_frame(split, features, count):
    path = SOURCE / ("holdout/test.csv" if split == "test" else "validation.csv")
    frame = pd.read_csv(path, float_precision="round_trip")
    check(split + "_schema_count_finite", list(frame.columns) == META + features and len(frame) == count and
          np.isfinite(frame[features + ["target_energy_kwh"]].to_numpy()).all())
    times = pd.to_datetime(frame["target_hour"], format="%Y-%m-%d %H:%M:%S")
    summary = read_json(SOURCE / "split-summary.json")[split]
    check(split + "_timestamp_mask_boundaries", times.is_unique and times.is_monotonic_increasing and
          frame["target_hour"].iloc[0] == summary["eligible_start"] and frame["target_hour"].iloc[-1] == summary["eligible_end"])
    check(split + "_origin_target_past_contract", all(pd.to_datetime(frame[name]).equals(times + pd.Timedelta(hours=offset))
          for name, offset in (("prediction_origin", 0), ("target_end", 1), ("latest_observed_hour", -1))))
    return frame


def capture_preservation():
    old = read_json(ROOT / ".agent/qa/phase2b1-20261009/preservation-before.json")
    retained, exceptions = {}, []
    for path, expected in old["files"].items():
        actual = sha256(path) if Path(path).is_file() else None
        if actual == expected:
            retained[path] = expected
        elif "/flink-tmp/" in path:
            exceptions.append(dict(path=path, expected=expected, actual=actual))
        else:
            raise ValueError("Product/source drift: " + path)
    check("prior_933_guard_only_runtime_exceptions", len(retained) + len(exceptions) == 933 and
          all("/flink-tmp/" in entry["path"] for entry in exceptions), dict(matched=len(retained), exceptions=exceptions))
    for name in ("models/runs/20261009-phase2b1-a2", "models/runs/20261009-phase2b1-b", ".agent/qa/phase2b1-20261009"):
        for path in sorted((ROOT / name).rglob("*")):
            if path.is_file():
                retained[str(path)] = sha256(path)
    for name in ("forecasting/train_hgb.py", "forecasting/predictor.py", "forecasting/evaluate_final.py",
                 ".agent/scripts/verify_phase2b1.py", ".agent/decisions/20261009-phase2b1-approval.md",
                 ".agent/decisions/20261009-phase2b2-approval.md"):
        path = ROOT / name
        retained[str(path)] = sha256(path)
    write_json(QA / "preservation-before.json", dict(captured_at=now(), files=retained, count=len(retained),
               inherited_count=933, inherited_matched=933-len(exceptions), current_runtime_exceptions=exceptions,
               historical_68=dict(archive=16, blobStorage=52), policy="Only runtime cache exceptions; no product drift"))


def load_candidate(features, config):
    bundle = joblib.load(CANDIDATE / "candidate.joblib")
    estimator = bundle["estimator"]
    check("loaded_candidate_schema_policy_parameters", isinstance(estimator, HistGradientBoostingRegressor) and
          bundle["feature_columns"] == features and bundle["prediction_policy"] == POLICY and
          bundle["training_split"] == "train" and bundle["final_locked"] is False and
          estimator.get_params() == config["actual_parameters"] and estimator.n_iter_ == 200 and
          not estimator.do_early_stopping_)
    return bundle


def preflight():
    if (QA / "selection-lock.json").exists() or (QA / "evaluation-started.json").exists():
        raise FileExistsError("Pretest already exists; do not rewrite locked selection")
    manifest, schema, config, installed = source_gate()
    capture_preservation()
    features = schema["feature_columns"]
    bundle = load_candidate(features, config)
    validation = load_frame("validation", features, 4727)
    saved = pd.read_csv(CANDIDATE / "predictions-validation.csv", float_precision="round_trip")
    with threadpool_limits(limits=2):
        raw, final = predict_bundle(bundle, validation[features])
    check("load_matches_all_Validation_timestamps_targets", saved[META[:3]+["target_energy_kwh"]].equals(validation[META[:3]+["target_energy_kwh"]]))
    check("load_matches_Validation_raw_final_exact", np.array_equal(raw, saved["hgb_raw_kwh"].to_numpy()) and
          np.array_equal(final, saved["hgb_final_kwh"].to_numpy()), dict(n=4727, max_difference_kwh=float(np.max(abs(raw-saved["hgb_raw_kwh"].to_numpy())))))
    check("no_Test_content_or_fit_before_lock", STATE["test_text_opens"] == 0 and STATE["fit_calls"] == 0, dict(STATE))
    write_json(QA / "selection-lock.json", dict(status="LOCKED", locked_at=now(), selected_model="HistGradientBoostingRegressor",
               candidate_path=str((CANDIDATE/"candidate.joblib").relative_to(ROOT)), candidate_sha256=MODEL_HASH,
               selected_version="hgb-uci-hourly-v0.1-candidate", final_version="hgb-uci-hourly-v1.0-train-only",
               refit=False, training_split="train", fitted_rows=22513, feature_schema=schema, model_config=config,
               prediction_policy=POLICY, packages=installed, python=platform.python_version(),
               source_phase2a_manifest_sha256=manifest["source_phase2a_manifest_sha256"],
               source_phase2a_verification_sha256=manifest["source_phase2a_verification_sha256"],
               source_phase2a_outputs=manifest["source_phase2a_outputs"], flink_source=manifest["flink_source"],
               test_sha256=TEST_HASH, test_n=4590, official_evaluation="once; no model selection from Test",
               protocol="one-step rolling origin; observed actual history through s-1; target [s,s+1), origin=s; naive source calendar",
               authorized_request_sha256=sha256(ROOT/".agent/decisions/20261009-phase2b2-approval.md"),
               evaluation_code_sha256=sha256(Path(__file__)), validation_match_exact=True, test_content_read_before_lock=False))
    write_json(QA / "pretest-verification.json", dict(status="VERIFIED", captured_at=now(), passed=len(CHECKS), total_checks=len(CHECKS),
               checks=CHECKS, selection_lock_sha256=sha256(QA/"selection-lock.json"), test_content_read=False, fit_calls=0))
    print(json.dumps(dict(action="preflight", status="VERIFIED", checks=len(CHECKS), test_content_read=False)))


def scores(y, raw):
    final = nonnegative(raw)
    raw_mae, raw_rmse = float(mean_absolute_error(y, raw)), float(root_mean_squared_error(y, raw))
    mae, rmse = float(mean_absolute_error(y, final)), float(root_mean_squared_error(y, final))
    return dict(mae_kwh=mae, rmse_kwh=rmse, raw_mae_kwh=raw_mae, raw_rmse_kwh=raw_rmse,
                negative_raw_count=int(np.sum(raw < 0)), minimum_raw_kwh=float(np.min(raw)),
                changed_prediction_count=int(np.sum(final != raw)), d09_mae_reduction_kwh=raw_mae-mae,
                d09_rmse_reduction_kwh=raw_rmse-rmse)


def evaluate():
    locked = read_json(QA/"selection-lock.json")
    pretest = read_json(QA/"pretest-verification.json")
    check("pretest_PASS_selection_LOCKED_before_Test", pretest["status"] == "VERIFIED" and
          pretest["passed"] == pretest["total_checks"] and all(c["passed"] for c in pretest["checks"]) and
          pretest["selection_lock_sha256"] == sha256(QA/"selection-lock.json") and locked["status"] == "LOCKED" and
          locked["refit"] is False and locked["evaluation_code_sha256"] == sha256(Path(__file__)))
    manifest, schema, config, installed = source_gate()
    check("model_code_and_config_match_pretest_lock", locked["candidate_sha256"] == MODEL_HASH and
          locked["model_config"] == config and locked["feature_schema"] == schema and locked["packages"] == installed)
    bundle = load_candidate(schema["feature_columns"], config)
    if OUTPUT.exists():
        raise FileExistsError("Official Test output already exists")
    write_json(QA/"evaluation-started.json", dict(status="IN_PROGRESS", started_at=now(), evaluation_number=1,
               selection_lock_sha256=sha256(QA/"selection-lock.json"), pretest_sha256=sha256(QA/"pretest-verification.json"),
               candidate_sha256=MODEL_HASH, test_sha256=TEST_HASH, refit=False))
    STATE["test_authorized"] = True
    test = load_frame("test", schema["feature_columns"], 4590)
    with threadpool_limits(limits=2):
        raw, final = predict_bundle(bundle, test[schema["feature_columns"]])
    predictions = test[META].copy()
    predictions["hgb_raw_kwh"], predictions["hgb_final_kwh"] = raw, final
    for name, column in (("naive", "lag_1_kwh"), ("seasonal_naive_24", "lag_24_kwh")):
        values = test[column].to_numpy()
        predictions[name+"_raw_kwh"], predictions[name+"_final_kwh"] = values, nonnegative(values)
    result = {name: scores(test["target_energy_kwh"], predictions[name+"_raw_kwh"].to_numpy())
              for name in ("hgb", "naive", "seasonal_naive_24")}
    check("no_refit_and_Test_only_after_authorization", STATE["fit_calls"] == 0 and STATE["test_text_opens"] == 1, dict(STATE))
    OUTPUT.mkdir(parents=True, exist_ok=False)
    predictions.to_csv(OUTPUT/"predictions-test.csv", index=False, float_format="%.17g", lineterminator="\n")
    write_json(OUTPUT/"metrics-test.json", dict(evaluation_split="test", unit="kWh", n=4590, models=result,
               official_prediction="final", prediction_policy=POLICY, official_evaluation_number=1,
               refit=False, protocol=locked["protocol"], test_evaluated=True))
    write_json(OUTPUT/"runtime-evidence.json", dict(captured_at=now(), state=STATE, no_fit=True,
               model_input_columns=schema["feature_columns"], prediction_rows=len(predictions),
               target_passed_to_predict=False, evaluation_started_sha256=sha256(QA/"evaluation-started.json")))
    write_json(OUTPUT/"manifest.json", dict(status="APPLIED_UNVERIFIED", created_at=now(), run_id=OUTPUT.name,
               candidate_path=locked["candidate_path"], candidate_sha256=MODEL_HASH, selection_lock_sha256=sha256(QA/"selection-lock.json"),
               pretest_sha256=sha256(QA/"pretest-verification.json"), source_phase2a_manifest_sha256=manifest["source_phase2a_manifest_sha256"],
               source_phase2a_outputs=manifest["source_phase2a_outputs"], flink_source=manifest["flink_source"],
               python=platform.python_version(), packages=installed, refit=False, test_evaluated=True,
               feature_columns=schema["feature_columns"], prediction_policy=POLICY,
               code_sha256={"forecasting/evaluate_final.py":sha256(Path(__file__)), "forecasting/predictor.py":sha256(ROOT/"forecasting/predictor.py")},
               outputs_sha256={name:sha256(OUTPUT/name) for name in ("predictions-test.csv", "metrics-test.json", "runtime-evidence.json")}))
    write_json(QA/"evaluation-completed.json", dict(completed_at=now(), status="APPLIED_UNVERIFIED", official_evaluation_number=1,
               run_id=OUTPUT.name, manifest_sha256=sha256(OUTPUT/"manifest.json"), checks=CHECKS, state=STATE,
               note="Independent verification and final packaging still pending; do not repeat evaluation"))
    print(json.dumps(dict(action="evaluate", status="APPLIED_UNVERIFIED", run_id=OUTPUT.name, scores=result)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("preflight", "evaluate"))
    action = parser.parse_args().action
    install_guards()
    preflight() if action == "preflight" else evaluate()

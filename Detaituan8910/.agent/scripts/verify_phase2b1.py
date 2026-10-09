import argparse
import ast
import csv
import hashlib
import json
import math
import runpy
import sys
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from pathlib import Path
from unittest.mock import patch

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from threadpoolctl import threadpool_limits


ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / ".agent/qa/phase2b1-20261009"
SOURCE = ROOT / "data/ml/runs/20261009-phase2a-a"
sys.path.insert(0, str(ROOT / "forecasting"))
from predictor import POLICY, nonnegative, predict_bundle


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def capture():
    destination = QA / "preservation-before.json"
    if destination.exists():
        raise FileExistsError(destination)
    existing = read_json(ROOT / ".agent/qa/phase2a-20261009/preservation-before.json")["files"]
    transient_changes = []
    retained = {}
    for path, expected in existing.items():
        observed = sha256(path) if Path(path).exists() else None
        if observed != expected and "/flink-tmp/" in path:
            transient_changes.append(dict(path=path, expected_sha256=expected, observed_sha256=observed,
                                          reason="Ephemeral Flink runtime state changed before Phase2B1; not an accepted product artifact"))
            continue
        if observed != expected:
            raise ValueError(f"Pre-existing source drift: {path}")
        retained[path] = expected
    files = dict(retained)
    for directory in (ROOT / "data/ml", ROOT / ".agent/qa/phase2a-20261009"):
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                files[str(path)] = sha256(path)
    for name in ("forecasting/prepare_baselines.py", "forecasting/requirements.txt", "forecasting/README.md",
                 ".agent/scripts/verify_phase2a.py", ".agent/scripts/verify_phase2a_documents.py",
                 ".agent/decisions/20261009-phase2a-approval.md"):
        path = ROOT / name
        files[str(path)] = sha256(path)
    write_json(destination, dict(captured_at=datetime.now(timezone.utc).isoformat(), files=files,
                                inherited_frozen_files=len(existing), count=len(files),
                                inherited_retained_files=len(retained), preexisting_transient_changes=transient_changes,
                                holdout_access="binary SHA256 only, never parsed or evaluated"))
    print(json.dumps(dict(captured=len(files), inherited=len(existing))))


def csv_rows(path):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def oracle(rows, column):
    with localcontext() as context:
        context.prec = 45
        residuals = [Decimal(row[column]) - Decimal(row["target_energy_kwh"]) for row in rows]
        n = Decimal(len(residuals))
        return dict(mae_kwh=float(sum(map(abs, residuals)) / n),
                    rmse_kwh=float((sum(value * value for value in residuals) / n).sqrt()))


def expect_value_error(function):
    try:
        function()
    except ValueError:
        return True
    return False


def verify():
    destination = QA / "verification.json"
    if destination.exists():
        raise FileExistsError(destination)
    checks = []

    def check(name, passed, details=None):
        checks.append(dict(name=name, passed=bool(passed), details=details))
        if not passed:
            raise AssertionError(name)

    frozen = read_json(QA / "preservation-before.json")["files"]
    changed_before = [path for path, expected in frozen.items() if sha256(path) != expected]
    check("preserved_before_training_rerun", not changed_before, dict(count=len(frozen), changed=changed_before))
    schema = read_json(SOURCE / "feature-schema.json")["feature_columns"]
    train = pd.read_csv(SOURCE / "train.csv", float_precision="round_trip")
    calls = []
    original_fit = HistGradientBoostingRegressor.fit

    def witnessed_fit(estimator, X, y, *args, **kwargs):
        if not isinstance(X, pd.DataFrame) or not isinstance(y, pd.Series):
            raise AssertionError("Fit must receive approved Train DataFrame and labels")
        same_x = X.equals(train[schema])
        same_y = y.equals(train["target_energy_kwh"])
        if not same_x or not same_y or len(y) != 22513:
            raise AssertionError("Fit inputs differ from accepted Train")
        calls.append(dict(rows=len(y), columns=list(X.columns), exact_train_X=same_x,
                          exact_train_y=same_y, kwargs=kwargs, params=estimator.get_params()))
        return original_fit(estimator, X, y, *args, **kwargs)

    sys.argv = [str(ROOT / "forecasting/train_hgb.py"), "--run-id", "20261009-phase2b1-b"]
    with patch.object(HistGradientBoostingRegressor, "fit", witnessed_fit):
        runpy.run_path(str(ROOT / "forecasting/train_hgb.py"), run_name="__main__")
    write_json(QA / "fit-witness.json", dict(calls=calls, validation_labels_available_to_fit=False,
                                           train_sha256=sha256(SOURCE / "train.csv")))
    check("independent_fit_witness_exact_train_only", len(calls) == 1 and calls[0]["exact_train_X"] and calls[0]["exact_train_y"], calls)
    a = ROOT / "models/runs/20261009-phase2b1-a2"
    b = ROOT / "models/runs/20261009-phase2b1-b"
    validation_rows = csv_rows(SOURCE / "validation.csv")
    baseline_rows = csv_rows(SOURCE / "predictions-validation.csv")
    validation = pd.read_csv(SOURCE / "validation.csv", float_precision="round_trip")
    all_scores = {}
    for directory in (a, b):
        manifest = read_json(directory / "manifest.json")
        config = read_json(directory / "model-config.json")
        runtime = read_json(directory / "runtime-evidence.json")
        scores = read_json(directory / "metrics-validation.json")
        rows = csv_rows(directory / "predictions-validation.csv")
        prefix = directory.name
        check(prefix + ":output_hashes", all(sha256(directory / name) == digest for name, digest in manifest["outputs_sha256"].items()))
        check(prefix + ":source_hashes_and_verified_status", manifest["source_phase2a_verification_sha256"] == sha256(SOURCE / "verification.json") and
              manifest["source_phase2a_manifest_sha256"] == sha256(SOURCE / "manifest.json") and read_json(SOURCE / "verification.json")["status"] == "VERIFIED")
        check(prefix + ":configuration_exact_and_no_early_stopping", all(config["actual_parameters"][key] == value for key, value in config["approved_parameters"].items()) and
              config["approved_parameters"] == dict(loss="squared_error", learning_rate=0.05, max_iter=200, max_leaf_nodes=15,
              min_samples_leaf=30, l2_regularization=1.0, max_bins=255, early_stopping=False, random_state=42) and
              runtime["n_iter"] == 200 and runtime["do_early_stopping"] is False)
        check(prefix + ":feature_order_train_count_and_fit_digests", config["feature_columns"] == schema and runtime["fitted_rows"] == 22513 and
              runtime["feature_count"] == 11 and runtime["fit_X_sha256"] == hashlib.sha256(train[schema].to_numpy(dtype=np.float64).tobytes()).hexdigest() and
              runtime["fit_y_sha256"] == hashlib.sha256(train["target_energy_kwh"].to_numpy(dtype=np.float64).tobytes()).hexdigest())
        check(prefix + ":no_test_or_final_model", manifest["test_evaluated"] is False and manifest["final_locked"] is False and
              scores["evaluation_split"] == "validation" and scores["test_evaluated"] is False and not any("test" in p.name for p in directory.iterdir()))
        reads = runtime["audit"]["dataset_opens"]
        check(prefix + ":runtime_dataset_read_gate", runtime["audit"]["validation_text_before_fit"] == 0 and
              all("holdout" not in row["path"] for row in reads) and
              all(row["fit_complete"] for row in reads if row["path"].endswith("validation.csv") and "b" not in row["mode"]), reads)
        check(prefix + ":timestamp_and_target_alignment_all_4727", len(rows) == len(validation_rows) == len(baseline_rows) == 4727 and
              all(all(row[column] == source[column] == baseline[column] for column in ("target_hour", "prediction_origin", "target_end")) and
                  float(row["target_energy_kwh"]) == float(source["target_energy_kwh"]) == float(baseline["target_energy_kwh"])
                  for row, source, baseline in zip(rows, validation_rows, baseline_rows, strict=True)))
        check(prefix + ":baselines_frozen_predictions", all(float(row["naive_raw_kwh"]) == float(base["naive_kwh"]) and
              float(row["seasonal_naive_24_raw_kwh"]) == float(base["seasonal_naive_24_kwh"]) for row, base in zip(rows, baseline_rows, strict=True)))
        check(prefix + ":D09_every_value_all_models", scores["official_prediction"] == "final" and scores["prediction_policy"] == POLICY and
              all(Decimal(row[f"{name}_final_kwh"]) == max(Decimal(0), Decimal(row[f"{name}_raw_kwh"])) and
                  Decimal(row[f"{name}_final_kwh"]).is_finite() for row in rows for name in ("hgb", "naive", "seasonal_naive_24")))
        independent = {}
        for name in ("hgb", "naive", "seasonal_naive_24"):
            final = oracle(rows, f"{name}_final_kwh")
            raw = oracle(rows, f"{name}_raw_kwh")
            negatives = sum(Decimal(row[f"{name}_raw_kwh"]) < 0 for row in rows)
            check(prefix + ":decimal_metrics_" + name, all(math.isclose(final[key], scores["models"][name][key], abs_tol=1e-12, rel_tol=0) for key in final) and
                  all(math.isclose(raw[key], scores["models"][name]["raw_" + key], abs_tol=1e-12, rel_tol=0) for key in raw) and
                  negatives == scores["models"][name]["negative_raw_count"], dict(final=final, raw=raw, negatives=negatives))
            independent[name] = dict(final=final, raw=raw, negatives=negatives)
        all_scores[prefix] = independent
        with threadpool_limits(limits=2):
            bundle = joblib.load(directory / "candidate.joblib")
            raw, final = predict_bundle(bundle, validation[schema])
        saved_raw = np.array([float(row["hgb_raw_kwh"]) for row in rows])
        saved_final = np.array([float(row["hgb_final_kwh"]) for row in rows])
        check(prefix + ":load_in_new_verifier_matches_saved_predictions", np.array_equal(raw, saved_raw) and np.array_equal(final, saved_final) and
              runtime["persistence"]["raw_exact"] and runtime["persistence"]["final_exact"] and runtime["persistence"]["max_raw_difference_kwh"] == 0)
        check(prefix + ":bundle_policy_and_schema", bundle["prediction_policy"] == POLICY and bundle["final_locked"] is False and
              bundle["training_split"] == "train" and list(bundle["estimator"].feature_names_in_) == schema)
        check(prefix + ":inference_ignores_labels_by_contract", expect_value_error(lambda: predict_bundle(bundle, validation)) and
              expect_value_error(lambda: predict_bundle(bundle, validation[list(reversed(schema))])))
    identical = {name: sha256(a / name) == sha256(b / name) for name in ("candidate.joblib", "predictions-validation.csv", "metrics-validation.json", "model-config.json")}
    check("same_config_reproducibility_saved_artifacts", all(identical.values()), identical)
    check("D09_synthetic_negative_zero_positive", np.array_equal(nonnegative(np.array([-0.12, 0., 0.8])), np.array([0., 0., 0.8])))
    check("D09_rejects_nan_inf_and_wrong_dimensions", all(expect_value_error(lambda values=values: nonnegative(values)) for values in ([np.nan], [np.inf], [[1.]])))
    tree = ast.parse((ROOT / "forecasting/train_hgb.py").read_text(encoding="utf-8"))
    fits = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "fit"]
    source_text = (ROOT / "forecasting/train_hgb.py").read_text(encoding="utf-8")
    check("single_fit_no_search_or_random_split", len(fits) == 1 and all(name not in source_text for name in ("GridSearchCV", "RandomizedSearchCV", "train_test_split")))
    changed_after = [path for path, expected in frozen.items() if sha256(path) != expected]
    check("preserved_after_all_training_and_QA", not changed_after, dict(count=len(frozen), changed=changed_after))
    result = dict(status="VERIFIED", passed=len(checks), total_checks=len(checks), checks=checks,
                  captured_at=datetime.now(timezone.utc).isoformat(), independent_metrics=all_scores,
                  preserved_files=len(frozen), reproducibility=identical, test_evaluated=False,
                  limitations="Feature leakage inherited from immutable Phase2A full-axis QA; Test binary hashes only; no Test scoring or final model lock")
    write_json(destination, result)
    for directory in (a, b):
        write_json(directory / "verification.json", dict(status="VERIFIED", phase="2B1", run_id=directory.name,
                   qa_path=str(destination.relative_to(ROOT)), qa_sha256=sha256(destination), passed=len(checks), total_checks=len(checks),
                   test_evaluated=False, final_locked=False))
    print(json.dumps(dict(status="VERIFIED", passed=len(checks), preserved=len(frozen), reproducibility=identical)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", action="store_true")
    args = parser.parse_args()
    capture() if args.capture else verify()

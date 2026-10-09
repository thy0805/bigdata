import argparse
import ast
import csv
import json
import math
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal, localcontext
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / ".agent/qa/phase2a-20261009"
sys.path.insert(0, str(ROOT / "forecasting"))
import prepare_baselines as product


def win_path(value):
    if len(value) > 2 and value[1] == ":":
        return Path("/mnt") / value[0].lower() / value[3:].replace("\\", "/")
    return Path(value)


def frozen_paths():
    paths = []
    for folder in (ROOT / "pipeline", ROOT / "data/processed/runs", ROOT / ".agent/qa/phase1-full-20261009", ROOT / ".agent/qa/phase1-smoke-20261009"):
        paths.extend(p for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    paths.extend(ROOT.glob("*.docx"))
    paths.extend(ROOT.glob("*.pdf"))
    inputs = json.loads((ROOT / ".agent/qa/phase1-smoke-20261009/inputs-manifest.json").read_text(encoding="utf-8"))
    paths.extend(win_path(p) for p in inputs["source_hashes_before"])
    paths.append(ROOT / "data/raw/household_power_consumption.txt")
    return sorted(set(paths))


def snapshot():
    path = QA / "preservation-before.json"
    if path.exists():
        raise FileExistsError(path)
    values = {str(p): product.sha256(p) for p in frozen_paths()}
    result = {"captured_at": datetime.now(timezone.utc).isoformat(), "files": values, "disk": {name: shutil.disk_usage(f"/mnt/{name}").free for name in ("c", "d")}, "python": platform.python_version()}
    product.write_json(path, result)
    print(json.dumps({"frozen_files": len(values), "disk": result["disk"]}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", action="store_true")
    parser.add_argument("--run-id")
    parser.add_argument("--compare-run")
    args = parser.parse_args()
    if args.snapshot:
        snapshot()
        return
    run = ROOT / "data/ml/runs" / args.run_id
    checks = []

    def check(name, passed, details=None):
        checks.append({"name": name, "passed": bool(passed), "details": details})

    frame, source = product.load_source()
    energy = frame.set_index("hour_start")["energy_kwh"]
    prepared, flags = product.build_features(energy)
    prepared = product.assign_splits(prepared)
    manifest = json.loads((run / "manifest.json").read_text())
    check("source_VERIFIED_hash_run_metadata", manifest["source"] == source, source)
    check("all_declared_output_hashes", all(product.sha256(run / p) == value for p, value in manifest["outputs_sha256"].items()))
    check("code_requirements_provenance", manifest["code_sha256"] == product.sha256(ROOT / "forecasting/prepare_baselines.py") and manifest["requirements_sha256"] == product.sha256(ROOT / "forecasting/requirements.txt"))
    check("Python312_pinned_packages", platform.python_version().startswith("3.12.") and all(line.strip().split("==")[1] == manifest["packages"][line.strip().split("==")[0]] for line in (ROOT / "forecasting/requirements.txt").read_text().splitlines() if line.strip()))
    pip_check = subprocess.run([sys.executable, "-m", "pip", "check"], text=True, capture_output=True)
    check("dependency_compatibility", pip_check.returncode == 0, pip_check.stdout.strip())
    check("source_grid_NULL_coverage", energy.isna().sum() == (~frame["is_complete"]).sum() and energy.index.equals(pd.date_range(energy.index[0], energy.index[-1], freq="h")), {"hours": len(energy), "null": int(energy.isna().sum())})
    observed_partial = frame.loc[~frame["is_complete"] & frame["observed_energy_kwh"].notna()]
    check("partial_observed_not_used_as_target", len(observed_partial) > 0 and observed_partial["energy_kwh"].isna().all(), {"partial_with_observed": len(observed_partial)})
    with (product.SOURCE_DIR / "hourly-grid.csv").open(newline="", encoding="utf-8") as stream:
        source_rows = list(csv.DictReader(stream))
    reference = {datetime.fromisoformat(r["hour_start"]): None if r["energy_kwh"] == "NULL" else Decimal(r["energy_kwh"]) for r in source_rows}
    expected_eligible = {}
    max_errors = {f"lag_{k}_kwh": Decimal(0) for k in product.LAGS}
    max_errors.update({f"rolling_mean_{w}_kwh": Decimal(0) for w in product.WINDOWS})
    errors = []
    expected_rows = {}
    n = len(reference)
    first, second = n * 70 // 100, n * 85 // 100
    hour = timedelta(hours=1)
    for pos, (stamp, target) in enumerate(reference.items()):
        expected = {f"lag_{k}_kwh": reference.get(stamp - k * hour) for k in product.LAGS}
        for w in product.WINDOWS:
            values = [reference.get(stamp - k * hour) for k in range(1, w + 1)]
            expected[f"rolling_mean_{w}_kwh"] = sum(values) / Decimal(w) if all(v is not None for v in values) else None
        expected["target_hour_of_day"] = stamp.hour
        expected["target_day_of_week"] = stamp.weekday()
        expected["target_month"] = stamp.month
        expected["target_is_weekend"] = int(stamp.weekday() >= 5)
        expected_eligible[stamp] = target is not None and all(v is not None for v in expected.values())
        expected_rows[stamp] = expected
        row = prepared.loc[stamp]
        if bool(row["eligible"]) != expected_eligible[stamp]:
            errors.append([str(stamp), "eligible"])
        if row["prediction_origin"].to_pydatetime() != stamp or row["target_end"].to_pydatetime() != stamp + hour or row["latest_observed_hour"].to_pydatetime() != stamp - hour:
            errors.append([str(stamp), "target_origin_off_by_one"])
        for field, expected_value in expected.items():
            actual = row[field]
            if expected_value is None:
                if not pd.isna(actual):
                    errors.append([str(stamp), field, "expected_NULL"])
            elif field in max_errors:
                delta = abs(Decimal(str(actual)) - expected_value)
                max_errors[field] = max(max_errors[field], delta)
                if pd.isna(actual) or delta > Decimal("2e-14"):
                    errors.append([str(stamp), field, str(delta)])
            elif actual != expected_value:
                errors.append([str(stamp), field, "calendar"])
    check("independent_full_axis_feature_target_oracle", not errors, {"hours": n, "features": len(product.FEATURES), "max_error_kwh": {k: str(v) for k, v in max_errors.items()}, "errors": errors[:10]})
    outputs = {}
    output_errors = []
    for split, filename in (("train", "train.csv"), ("validation", "validation.csv"), ("test", "holdout/test.csv")):
        with (run / filename).open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        outputs[split] = rows
        expected_keys = [stamp for pos, stamp in enumerate(reference) if expected_eligible[stamp] and ("train" if pos < first else "validation" if pos < second else "test") == split]
        if [datetime.fromisoformat(r["target_hour"]) for r in rows] != expected_keys:
            output_errors.append([split, "keys"])
        for row in rows:
            stamp = datetime.fromisoformat(row["target_hour"])
            for field in product.FEATURES + ["target_energy_kwh"]:
                expected = reference[stamp] if field == "target_energy_kwh" else expected_rows[stamp][field]
                if abs(Decimal(row[field]) - Decimal(expected)) > Decimal("2e-14"):
                    output_errors.append([split, str(stamp), field])
    check("saved_CSV_values_schema_order_and_eligibility", not output_errors, {"errors": output_errors[:10], "rows": {k: len(v) for k, v in outputs.items()}, "holdout_QA": "preparation/schema checks only; no Test predictions or metrics"})
    eligibility = pd.read_csv(run / "eligibility.csv", keep_default_na=False)
    check("eligibility_axis_preserved_no_dropped_NULLs", len(eligibility) == n and eligibility["target_hour"].tolist() == [str(s) for s in reference] and int(eligibility["eligible"].sum()) == sum(expected_eligible.values()))
    check("split_before_filter_no_overlap", prepared.iloc[first - 1]["split"] == "train" and prepared.iloc[first]["split"] == "validation" and prepared.iloc[second - 1]["split"] == "validation" and prepared.iloc[second]["split"] == "test" and sum(len(v) for v in outputs.values()) == sum(expected_eligible.values()), {"train_end": str(prepared.index[first - 1]), "validation_start": str(prepared.index[first]), "validation_end": str(prepared.index[second - 1]), "test_start": str(prepared.index[second])})
    check("train_labels_available_by_first_validation_origin", prepared.index[first - 1] + pd.Timedelta(hours=1) <= prepared.index[first])
    check("measurement_sources_strictly_before_target", all(field["latest_source_offset_hours"] is None or field["latest_source_offset_hours"] < 0 for field in product.feature_schema()["features"]))
    check("target_and_diagnostics_excluded_from_feature_columns", not set(product.FEATURES) & set(product.feature_schema()["excluded_from_features"]))
    check("dataset_start_end_boundaries", not prepared.iloc[0]["eligible"] and not prepared.iloc[-1]["eligible"] and not prepared.iloc[:168]["eligible"].any())
    missing_groups = []
    begin = None
    for stamp, value in reference.items():
        if value is None and begin is None:
            begin = stamp
        if value is not None and begin is not None:
            missing_groups.append((begin, stamp - hour, int((stamp - begin) / hour)))
            begin = None
    if begin is not None:
        missing_groups.append((begin, next(reversed(reference)), int((next(reversed(reference)) - begin) / hour) + 1))
    longest = max(missing_groups, key=lambda r: r[2])
    after_gap = pd.Timestamp(longest[1] + hour)
    check("long_missing_region_excluded_and_rolling_not_compressed", not prepared.loc[longest[0]:longest[1], "eligible"].any() and pd.isna(prepared.loc[after_gap, "lag_1_kwh"]) and pd.isna(prepared.loc[after_gap, "rolling_mean_24_kwh"]), {"hourly_gap_start": str(longest[0]), "hourly_gap_end": str(longest[1]), "incomplete_hours": longest[2], "raw_gap_7226_minutes": "Phase1 audit reference only, raw not re-audited in Phase2A"})
    synthetic_index = pd.date_range("2020-01-01", periods=240, freq="h")
    synthetic = pd.Series(np.arange(240, dtype=float), index=synthetic_index)
    synthetic.iloc[180] = np.nan
    synth_table, _ = product.build_features(synthetic)
    check("synthetic_missing_hour_not_zero_or_fake_adjacent", pd.isna(synth_table.iloc[181]["lag_1_kwh"]) and synth_table.iloc[182]["lag_1_kwh"] == 181 and pd.isna(synth_table.iloc[181]["rolling_mean_3_kwh"]) and synth_table.iloc[0]["target_energy_kwh"] == 0)
    check("synthetic_rolling_full_coverage_required", pd.isna(synth_table.iloc[204]["rolling_mean_24_kwh"]) and not pd.isna(synth_table.iloc[205]["rolling_mean_24_kwh"]))
    compressed_rejected = False
    try:
        product.build_features(synthetic.dropna())
    except ValueError:
        compressed_rejected = True
    check("compressed_time_axis_rejected", compressed_rejected)
    at = prepared.index[first + 50]
    mutated = energy.copy()
    mutated.loc[at:] = mutated.loc[at:] + 999
    mutation_table, _ = product.build_features(mutated)
    check("future_and_target_perturbation_leaves_features_unchanged", prepared.loc[:at, product.FEATURES].equals(mutation_table.loc[:at, product.FEATURES]))
    mutated_test = energy.copy()
    mutated_test.iloc[second:] = mutated_test.iloc[second:] + 1000
    mutation_test, _ = product.build_features(mutated_test)
    mutation_test = product.assign_splits(mutation_test)
    original_predictions, original_metrics = product.validation_baselines(prepared)
    changed_predictions, changed_metrics = product.validation_baselines(mutation_test)
    check("Test_perturbation_cannot_change_Validation_outputs", original_predictions.equals(changed_predictions) and original_metrics == changed_metrics)
    with (run / "predictions-validation.csv").open(newline="", encoding="utf-8") as stream:
        predictions = list(csv.DictReader(stream))
    check("baselines_common_Validation_mask", [r["target_hour"] for r in predictions] == [r["target_hour"] for r in outputs["validation"]] and all(not prepared.loc[r["target_hour"], "split"] == "test" for r in predictions))
    prediction_errors = []
    all_errors = {name: [] for name in ("naive", "seasonal_naive_24")}
    samples = []
    for pos, row in enumerate(predictions):
        stamp = datetime.fromisoformat(row["target_hour"])
        for model, lag in (("naive", 1), ("seasonal_naive_24", 24)):
            expected = reference[stamp - lag * hour]
            if abs(expected - Decimal(row[f"{model}_kwh"])) > Decimal("2e-14"):
                prediction_errors.append([str(stamp), model])
            all_errors[model].append(reference[stamp] - expected)
        if pos in (0, len(predictions) // 2, len(predictions) - 1):
            samples.append(row)
    metrics = json.loads((run / "metrics-validation.json").read_text())
    oracle_metrics = {}
    with localcontext() as ctx:
        ctx.prec = 40
        for model, values in all_errors.items():
            count = Decimal(len(values))
            oracle_metrics[model] = {"mae_kwh": str(sum(abs(v) for v in values) / count), "rmse_kwh": str((sum(v * v for v in values) / count).sqrt())}
    check("baseline_predictions_independent_timestamp_oracle", not prediction_errors, {"errors": prediction_errors[:10], "manual_samples": samples})
    check("Validation_MAE_RMSE_independent_Decimal", all(abs(Decimal(str(metrics["models"][name][field])) - Decimal(value)) < Decimal("2e-14") for name, scores in oracle_metrics.items() for field, value in scores.items()), oracle_metrics)
    check("only_Validation_metrics_no_Test_predictions", metrics["evaluation_split"] == "validation" and not metrics["test_evaluated"] and not manifest["test_evaluated"] and not manifest["model_trained"] and not any("predict" in p.name.lower() for p in (run / "holdout").iterdir()))
    tree = ast.parse((ROOT / "forecasting/prepare_baselines.py").read_text(encoding="utf-8"))
    calls = [node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)]
    check("no_fit_training_calls_in_Phase2A", not any(c in ("fit", "fit_predict", "fit_transform", "partial_fit") for c in calls))
    seal = json.loads((run / "holdout/seal.json").read_text())
    check("holdout_procedural_seal", seal["status"] == "SEALED_FOR_FINAL_EVALUATION" and seal["test_sha256"] == product.sha256(run / "holdout/test.csv") and not seal["test_evaluated"])
    original = json.loads((QA / "preservation-before.json").read_text())
    changed = [p for p, digest in original["files"].items() if not Path(p).exists() or product.sha256(p) != digest]
    new_frozen = sorted(set(str(p) for p in frozen_paths()) - set(original["files"]))
    check("Phase1_pipeline_sources_Word_PDF_all_preserved", not changed and not new_frozen, {"files": len(original["files"]), "changed": changed, "new_frozen_paths": new_frozen})
    if args.compare_run:
        other = ROOT / "data/ml/runs" / args.compare_run
        other_manifest = json.loads((other / "manifest.json").read_text())
        check("rerun_deterministic_outputs_byte_identical", manifest["outputs_sha256"] == other_manifest["outputs_sha256"] and manifest["source"] == other_manifest["source"] and manifest["packages"] == other_manifest["packages"] and manifest["code_sha256"] == other_manifest["code_sha256"], {"compared_run": args.compare_run, "artifacts": len(manifest["outputs_sha256"])})
    disk = {name: shutil.disk_usage(f"/mnt/{name}").free for name in ("c", "d")}
    check("physical_C_D_free_space_above_5GiB", min(disk.values()) > 5 * 1024 ** 3, disk)
    result = {"captured_at": datetime.now(timezone.utc).isoformat(), "run_id": args.run_id, "status": "VERIFIED" if all(c["passed"] for c in checks) else "APPLIED_UNVERIFIED", "passed": sum(c["passed"] for c in checks), "total_checks": len(checks), "checks": checks, "scope": "M01-M04; no ML fit, no Test evaluation", "independent_oracle": "Decimal + timestamp dictionary from accepted Flink hourly CSV only; all hours/features and all Validation baseline predictions/metrics", "disk": disk}
    product.write_json(run / "verification.json", result)
    product.write_json(QA / f"verification-{args.run_id}.json", result)
    print(json.dumps({"status": result["status"], "passed": result["passed"], "total": result["total_checks"], "failed": [c for c in checks if not c["passed"]]}, ensure_ascii=False))
    if result["status"] != "VERIFIED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

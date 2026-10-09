import argparse
import hashlib
import importlib.metadata
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, root_mean_squared_error


ROOT = Path(__file__).resolve().parents[1]
SOURCE_RUN = "20261009T102201900234-full"
SOURCE_DIR = ROOT / "data/processed/runs" / SOURCE_RUN
SOURCE_HASH = "8b03f1e3c82a5344c071a19f756cb7ec87fce18cc9a612cd63c4dcf4a8b5b2bc"
HOUR_COLUMNS = [
    "hour_start", "record_count", "distinct_minute_count", "valid_power_count",
    "observed_energy_kwh", "is_complete", "energy_kwh", "sub1_valid_count",
    "sub2_valid_count", "sub3_valid_count", "sub1_observed_kwh",
    "sub2_observed_kwh", "sub3_observed_kwh", "negative_residual_count",
]
LAGS = (1, 2, 3, 24, 168)
WINDOWS = (3, 24)
FEATURES = [f"lag_{k}_kwh" for k in LAGS] + [f"rolling_mean_{w}_kwh" for w in WINDOWS] + [
    "target_hour_of_day", "target_day_of_week", "target_month", "target_is_weekend",
]
PACKAGES = ("numpy", "pandas", "scikit-learn", "scipy", "joblib", "threadpoolctl", "python-dateutil", "pytz", "tzdata", "six")


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def validate_grid(frame):
    if list(frame.columns) != HOUR_COLUMNS:
        raise ValueError("Hourly schema must match the 14 accepted Flink columns")
    hours = pd.to_datetime(frame["hour_start"], format="%Y-%m-%d %H:%M:%S", errors="raise")
    index = pd.DatetimeIndex(hours)
    if index.tz is not None or index.has_duplicates or not index.is_monotonic_increasing:
        raise ValueError("Expected unique sorted naive timestamps")
    if not index.equals(pd.date_range(index[0], index[-1], freq="h")):
        raise ValueError("Source must retain the entire consecutive hourly axis")
    numeric = [c for c in HOUR_COLUMNS if c not in ("hour_start", "is_complete")]
    frame = frame.copy()
    for col in numeric:
        frame[col] = pd.to_numeric(frame[col], errors="raise")
        if np.isinf(frame[col].to_numpy(dtype=float)).any():
            raise ValueError(f"Non-finite value: {col}")
    counts = [c for c in numeric if c.endswith("count")]
    for col in counts:
        values = frame[col]
        if values.isna().any() or not ((values >= 0) & (values <= 60) & (values % 1 == 0)).all():
            raise ValueError(f"Invalid count: {col}")
    complete = frame["is_complete"].astype(str).str.lower()
    if not complete.isin(["true", "false"]).all():
        raise ValueError("Invalid is_complete")
    complete = complete.eq("true")
    expected = frame["record_count"].eq(60) & frame["distinct_minute_count"].eq(60) & frame["valid_power_count"].eq(60)
    if not complete.equals(expected) or not frame["energy_kwh"].notna().equals(complete):
        raise ValueError("Full-hour energy and coverage disagree")
    if (frame.loc[complete, "energy_kwh"] < 0).any():
        raise ValueError("Negative observed full-hour energy")
    frame["hour_start"] = index
    frame["is_complete"] = complete
    return frame


def load_source():
    source = SOURCE_DIR / "hourly-grid.csv"
    if sha256(source) != SOURCE_HASH:
        raise ValueError("Accepted source checksum mismatch")
    verification = json.loads((SOURCE_DIR / "verification.json").read_text(encoding="utf-8"))
    manifest = json.loads((SOURCE_DIR / "manifest.json").read_text(encoding="utf-8"))
    if verification.get("status") != "VERIFIED" or verification.get("run_id") != SOURCE_RUN:
        raise ValueError("Source run has not passed Phase1 verification")
    if verification["passed"] != verification["total_checks"] or not all(c["passed"] for c in verification["checks"]):
        raise ValueError("Source verification contains a failed check")
    if manifest["run_id"] != SOURCE_RUN or manifest["mode"] != "BATCH" or manifest["metrics"]["parse_error_rows"] != 0:
        raise ValueError("Unexpected Flink run metadata")
    if not manifest["jobs"] or any(job["state"] != "FINISHED" for job in manifest["jobs"]):
        raise ValueError("Source Flink job not finished")
    frame = validate_grid(pd.read_csv(source, na_values=["NULL"], keep_default_na=False))
    if len(frame) != verification["audit"]["hours"] or int(frame["is_complete"].sum()) != verification["audit"]["complete_hours"]:
        raise ValueError("Hourly source does not match accepted audit")
    return frame, {
        "run_id": SOURCE_RUN, "path": source.relative_to(ROOT).as_posix(), "sha256": SOURCE_HASH,
        "verification_sha256": sha256(SOURCE_DIR / "verification.json"),
        "manifest_sha256": sha256(SOURCE_DIR / "manifest.json"),
        "verification_status": verification["status"], "flink_job_ids": [j["jid"] for j in manifest["jobs"]],
        "mode": "BATCH", "timezone_policy": "naive source calendar; no UTC/DST inference",
    }


def build_features(energy):
    index = energy.index
    if index.tz is not None or not index.equals(pd.date_range(index[0], index[-1], freq="h")):
        raise ValueError("Features require the full hourly grid, not a compressed non-NULL series")
    table = pd.DataFrame(index=index)
    table.index.name = "target_hour"
    table["prediction_origin"] = index
    table["target_end"] = index + pd.Timedelta(hours=1)
    table["latest_observed_hour"] = index - pd.Timedelta(hours=1)
    table["target_energy_kwh"] = energy
    for lag in LAGS:
        table[f"lag_{lag}_kwh"] = energy.reindex(index - pd.Timedelta(hours=lag)).to_numpy()
    past = energy.shift(1)
    for window in WINDOWS:
        table[f"rolling_mean_{window}_kwh"] = past.rolling(window, min_periods=window).mean()
    table["target_hour_of_day"] = index.hour
    table["target_day_of_week"] = index.dayofweek
    table["target_month"] = index.month
    table["target_is_weekend"] = (index.dayofweek >= 5).astype(int)
    flags = pd.DataFrame(index=index)
    flags["missing_target"] = energy.isna()
    flags["insufficient_history"] = np.arange(len(index)) < max(LAGS)
    for lag in LAGS:
        flags[f"missing_lag_{lag}"] = table[f"lag_{lag}_kwh"].isna()
    for window in WINDOWS:
        flags[f"missing_rolling_{window}"] = table[f"rolling_mean_{window}_kwh"].isna()
    table["eligible"] = table[["target_energy_kwh"] + FEATURES].notna().all(axis=1)
    table["exclusion_primary"] = ""
    for reason in flags:
        chosen = flags[reason] & table["exclusion_primary"].eq("") & ~table["eligible"]
        table.loc[chosen, "exclusion_primary"] = reason
    table["exclusion_reasons"] = flags.apply(lambda row: ";".join(row.index[row]), axis=1)
    return table, flags


def assign_splits(table):
    n = len(table)
    first, second = n * 70 // 100, n * 85 // 100
    result = table.copy()
    result["split"] = np.where(np.arange(n) < first, "train", np.where(np.arange(n) < second, "validation", "test"))
    return result


def validation_baselines(table):
    selected = table.loc[table["split"].eq("validation") & table["eligible"]]
    if selected.empty:
        raise ValueError("No eligible Validation timestamps")
    predictions = selected[["prediction_origin", "target_end", "target_energy_kwh"]].copy()
    predictions["naive_kwh"] = selected["lag_1_kwh"]
    predictions["seasonal_naive_24_kwh"] = selected["lag_24_kwh"]
    metrics = {"evaluation_split": "validation", "unit": "kWh", "common_mask": "all ML features and target available", "n": len(selected), "test_evaluated": False, "models": {}}
    for name in ("naive", "seasonal_naive_24"):
        predicted = predictions[f"{name}_kwh"]
        metrics["models"][name] = {
            "mae_kwh": float(mean_absolute_error(predictions["target_energy_kwh"], predicted)),
            "rmse_kwh": float(root_mean_squared_error(predictions["target_energy_kwh"], predicted)),
        }
    return predictions, metrics


def split_summary(table, flags):
    summary = {}
    for name in ("train", "validation", "test"):
        subset = table.loc[table["split"].eq(name)]
        eligible = subset.loc[subset["eligible"]]
        summary[name] = {
            "axis_start": str(subset.index[0]), "axis_end": str(subset.index[-1]), "axis_hours": len(subset),
            "eligible_start": str(eligible.index[0]), "eligible_end": str(eligible.index[-1]),
            "eligible_hours": len(eligible), "excluded_hours": int((~subset["eligible"]).sum()),
            "exclusion_primary": {k: int(v) for k, v in subset.loc[~subset["eligible"], "exclusion_primary"].value_counts().sort_index().items()},
            "reason_counts_overlapping": {k: int(v) for k, v in flags.loc[subset.index].sum().items()},
        }
    return summary


def feature_schema():
    fields = []
    for lag in LAGS:
        fields.append({"name": f"lag_{lag}_kwh", "dtype": "float64", "unit": "kWh", "source": f"E(target_hour - {lag} hours)", "latest_source_offset_hours": -lag})
    for window in WINDOWS:
        fields.append({"name": f"rolling_mean_{window}_kwh", "dtype": "float64", "unit": "kWh", "source": f"mean E(target_hour - {window} hours) through E(target_hour - 1 hour); all required", "latest_source_offset_hours": -1})
    for name, definition in (("target_hour_of_day", "0..23"), ("target_day_of_week", "Monday=0..Sunday=6"), ("target_month", "1..12"), ("target_is_weekend", "Saturday/Sunday=1, other=0")):
        fields.append({"name": name, "dtype": "integer", "unit": "calendar", "source": f"target_hour known calendar: {definition}", "latest_source_offset_hours": None})
    return {
        "feature_columns": FEATURES, "features": fields, "target": "target_energy_kwh = E(target_hour), interval [target_hour,target_hour+1h)",
        "prediction_origin": "target_hour, immediately after the preceding hour is fully observed", "horizon_hours": 1,
        "latest_allowed_measurement": "hour_start <= target_hour - 1h", "missing_policy": "No imputation; complete source hours only; exact timestamp lags; full rolling windows",
        "gap_policy": "Exact lag168 may reference a real past hour across intervening missing timestamps. No compressed shifts or rolling across missing hours.",
        "excluded_from_features": ["target_energy_kwh", "prediction_origin", "target_end", "latest_observed_hour", "split", "eligible", "exclusion_primary", "exclusion_reasons"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + "-phase2a")
    args = parser.parse_args()
    if not args.run_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in args.run_id):
        raise ValueError("Unsafe run ID")
    output = ROOT / "data/ml/runs" / args.run_id
    if output.exists():
        raise FileExistsError(output)
    frame, source = load_source()
    energy = frame.set_index("hour_start")["energy_kwh"]
    table, flags = build_features(energy)
    table = assign_splits(table)
    predictions, metrics = validation_baselines(table)
    summary = split_summary(table, flags)
    output.mkdir(parents=True)
    (output / "holdout").mkdir()
    columns = ["prediction_origin", "target_end", "latest_observed_hour", "target_energy_kwh"] + FEATURES
    for split, filename in (("train", "train.csv"), ("validation", "validation.csv"), ("test", "holdout/test.csv")):
        table.loc[table["split"].eq(split) & table["eligible"], columns].to_csv(output / filename, na_rep="NULL", float_format="%.17g", lineterminator="\n")
    table[["split", "eligible", "exclusion_primary", "exclusion_reasons"]].to_csv(output / "eligibility.csv", lineterminator="\n")
    predictions.to_csv(output / "predictions-validation.csv", float_format="%.17g", lineterminator="\n")
    write_json(output / "feature-schema.json", feature_schema())
    write_json(output / "split-summary.json", summary)
    write_json(output / "metrics-validation.json", metrics)
    packages = {p: importlib.metadata.version(p) for p in PACKAGES}
    write_json(output / "holdout/seal.json", {
        "status": "SEALED_FOR_FINAL_EVALUATION", "test_evaluated": False, "model_trained": False,
        "test_sha256": sha256(output / "holdout/test.csv"), "eligible_hours": summary["test"]["eligible_hours"],
        "policy": "Prepared labels/features only; no Test predictions, metrics, selection or tuning in Phase2A. This is a procedural seal, not encryption.",
    })
    outputs = {p.relative_to(output).as_posix(): sha256(p) for p in sorted(output.rglob("*")) if p.is_file()}
    manifest = {
        "status": "APPLIED_UNVERIFIED", "run_id": args.run_id, "created_at": datetime.now(timezone.utc).isoformat(),
        "source": source, "python": platform.python_version(), "packages": packages,
        "code_sha256": sha256(Path(__file__)), "requirements_sha256": sha256(Path(__file__).with_name("requirements.txt")),
        "input_axis_hours": len(table), "input_complete_hours": int(energy.notna().sum()), "input_null_hours": int(energy.isna().sum()),
        "eligible_ml_hours": int(table["eligible"].sum()), "excluded_ml_hours": int((~table["eligible"]).sum()),
        "split_rule": "floor(0.70*N), floor(0.85*N) on complete target-hour axis before eligibility filtering",
        "evaluation_mode": "one-step rolling origin with previously observed actuals; not recursive multi-step",
        "test_evaluated": False, "model_trained": False, "outputs_sha256": outputs,
    }
    if sha256(SOURCE_DIR / "hourly-grid.csv") != SOURCE_HASH:
        raise ValueError("Source changed during processing")
    write_json(output / "manifest.json", manifest)
    print(json.dumps({"output": str(output), "eligible": manifest["eligible_ml_hours"], "splits": summary, "metrics": metrics}, ensure_ascii=False))


if __name__ == "__main__":
    main()

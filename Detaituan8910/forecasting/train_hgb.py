import argparse
import hashlib
import importlib.metadata
import json
import platform
import resource
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from threadpoolctl import threadpool_info, threadpool_limits

from predictor import POLICY, nonnegative, predict_bundle


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/ml/runs/20261009-phase2a-a"
SOURCE_VERIFICATION_HASH = "3a7ad0ad97c1dd95a2194b0742729d5285e7be07130d10aad6e30029aeebd9b8"
PARAMS = dict(loss="squared_error", learning_rate=0.05, max_iter=200,
              max_leaf_nodes=15, min_samples_leaf=30, l2_regularization=1.0,
              max_bins=255, early_stopping=False, random_state=42)
META = ["target_hour", "prediction_origin", "target_end", "latest_observed_hour", "target_energy_kwh"]


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def source_gate():
    if sha256(SOURCE / "verification.json") != SOURCE_VERIFICATION_HASH:
        raise ValueError("Accepted Phase2A verification hash changed")
    verified = read_json(SOURCE / "verification.json")
    if verified["status"] != "VERIFIED" or verified["passed"] != verified["total_checks"]:
        raise ValueError("Phase2A is not VERIFIED")
    manifest = read_json(SOURCE / "manifest.json")
    for name, expected in manifest["outputs_sha256"].items():
        if name.startswith("holdout/") or (name.endswith(".csv") and name != "train.csv"):
            continue
        if sha256(SOURCE / name) != expected:
            raise ValueError(f"Phase2A artifact changed: {name}")
    for name, expected in (("prepare_baselines.py", manifest["code_sha256"]),
                           ("requirements.txt", manifest["requirements_sha256"])):
        if sha256(ROOT / "forecasting" / name) != expected:
            raise ValueError(f"Accepted preparation code changed: {name}")
    provenance = manifest["source"]
    if sha256(ROOT / provenance["path"]) != provenance["sha256"]:
        raise ValueError("Flink hourly source changed")
    installed = {name: importlib.metadata.version(name) for name in manifest["packages"]}
    if installed != manifest["packages"] or platform.python_version() != manifest["python"]:
        raise ValueError("Runtime differs from accepted pinned environment")
    return manifest, installed, read_json(SOURCE / "feature-schema.json")["feature_columns"]


def load_split(name, features, count):
    if name not in ("train", "validation"):
        raise ValueError("Only Train and Validation are authorized")
    frame = pd.read_csv(SOURCE / f"{name}.csv", float_precision="round_trip")
    if list(frame.columns) != META + features or len(frame) != count:
        raise ValueError(f"Invalid schema/count for {name}")
    times = pd.to_datetime(frame["target_hour"], format="%Y-%m-%d %H:%M:%S")
    if not times.is_unique or not times.is_monotonic_increasing:
        raise ValueError("Timestamp ordering/uniqueness failed")
    for column, offset in (("prediction_origin", 0), ("target_end", 1), ("latest_observed_hour", -1)):
        expected = times + pd.Timedelta(hours=offset)
        if not pd.to_datetime(frame[column]).equals(expected):
            raise ValueError(f"Invalid {column}")
    if not np.isfinite(frame[features + ["target_energy_kwh"]].to_numpy()).all():
        raise ValueError("Missing/non-finite source values")
    if (frame["target_energy_kwh"] < 0).any():
        raise ValueError("Negative observed target")
    split = read_json(SOURCE / "split-summary.json")[name]
    if frame["target_hour"].iloc[0] != split["eligible_start"] or frame["target_hour"].iloc[-1] != split["eligible_end"]:
        raise ValueError("Split boundary changed")
    return frame


def fit_candidate(train, features):
    estimator = HistGradientBoostingRegressor(**PARAMS)
    estimator.fit(train[features], train["target_energy_kwh"])
    return estimator


def metrics(y, raw):
    final = nonnegative(raw)
    raw_mae = float(mean_absolute_error(y, raw))
    raw_rmse = float(root_mean_squared_error(y, raw))
    final_mae = float(mean_absolute_error(y, final))
    final_rmse = float(root_mean_squared_error(y, final))
    return dict(mae_kwh=final_mae, rmse_kwh=final_rmse,
                raw_mae_kwh=raw_mae, raw_rmse_kwh=raw_rmse,
                negative_raw_count=int(np.sum(raw < 0)), minimum_raw_kwh=float(np.min(raw)),
                changed_prediction_count=int(np.sum(final != raw)),
                d09_mae_reduction_kwh=raw_mae - final_mae,
                d09_rmse_reduction_kwh=raw_rmse - final_rmse)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if not args.run_id.startswith("20261009-phase2b1-") or Path(args.run_id).name != args.run_id:
        raise ValueError("Run identifier outside approved scope")
    output = ROOT / "models/runs" / args.run_id
    output.mkdir(parents=True, exist_ok=False)
    state = dict(active=True, fit_complete=False, dataset_opens=[], validation_text_before_fit=0)

    def audit(event, arguments):
        if not state["active"] or event != "open" or not isinstance(arguments[0], (str, bytes)):
            return
        path = Path(arguments[0].decode() if isinstance(arguments[0], bytes) else arguments[0]).absolute()
        if SOURCE not in path.parents:
            return
        if "holdout" in path.parts:
            raise PermissionError("Test access forbidden in Phase2B1 training")
        if path.suffix != ".csv":
            return
        mode = arguments[1] or ""
        if path.name != "train.csv" and not state["fit_complete"]:
            state["validation_text_before_fit"] += 1
            raise PermissionError("Validation labels unavailable before fit completes")
        state["dataset_opens"].append(dict(path=str(path.relative_to(ROOT)), mode=mode,
                                           fit_complete=state["fit_complete"]))

    sys.addaudithook(audit)
    try:
        source, installed, features = source_gate()
        if len(features) != 11:
            raise ValueError("Expected 11 approved features")
        train = load_split("train", features, 22513)
        started = time.perf_counter()
        with threadpool_limits(limits=2):
            estimator = fit_candidate(train, features)
            fit_seconds = time.perf_counter() - started
            state["fit_complete"] = True
            for name in ("validation.csv", "predictions-validation.csv"):
                if sha256(SOURCE / name) != source["outputs_sha256"][name]:
                    raise ValueError(f"Validation artifact changed: {name}")
            validation = load_split("validation", features, 4727)
            if train["target_hour"].iloc[-1] >= validation["target_hour"].iloc[0]:
                raise ValueError("Train and Validation overlap")
            bundle = dict(estimator=estimator, feature_columns=features, prediction_policy=POLICY,
                          model_version="hgb-uci-hourly-v0.1-candidate", final_locked=False,
                          training_split="train", source_run_id=source["run_id"], flink_source=source["source"])
            raw, final = predict_bundle(bundle, validation[features])
            joblib.dump(bundle, output / "candidate.joblib", compress=3, protocol=5)
            reloaded = joblib.load(output / "candidate.joblib")
            loaded_raw, loaded_final = predict_bundle(reloaded, validation[features])
            persistence = dict(raw_exact=bool(np.array_equal(raw, loaded_raw)),
                               final_exact=bool(np.array_equal(final, loaded_final)),
                               max_raw_difference_kwh=float(np.max(np.abs(raw - loaded_raw))))
            pools = threadpool_info()
        baseline = pd.read_csv(SOURCE / "predictions-validation.csv", float_precision="round_trip")
        if not baseline[META[:3] + ["target_energy_kwh"]].equals(validation[META[:3] + ["target_energy_kwh"]]):
            raise ValueError("Baseline timestamps/targets differ")
        predictions = validation[META[:3] + ["target_energy_kwh"]].copy()
        predictions["hgb_raw_kwh"] = raw
        predictions["hgb_final_kwh"] = final
        predictions["naive_raw_kwh"] = baseline["naive_kwh"]
        predictions["naive_final_kwh"] = nonnegative(baseline["naive_kwh"].to_numpy())
        predictions["seasonal_naive_24_raw_kwh"] = baseline["seasonal_naive_24_kwh"]
        predictions["seasonal_naive_24_final_kwh"] = nonnegative(baseline["seasonal_naive_24_kwh"].to_numpy())
        predictions.to_csv(output / "predictions-validation.csv", index=False, float_format="%.17g", lineterminator="\n")
        scores = {name: metrics(validation["target_energy_kwh"], predictions[f"{name}_raw_kwh"].to_numpy())
                  for name in ("hgb", "naive", "seasonal_naive_24")}
        write_json(output / "metrics-validation.json", dict(evaluation_split="validation", unit="kWh", n=4727,
                   official_prediction="final", prediction_policy=POLICY, models=scores, test_evaluated=False))
        write_json(output / "runtime-evidence.json", dict(fit_seconds=fit_seconds, peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   fitted_rows=len(train), feature_count=len(features), n_iter=int(estimator.n_iter_),
                   do_early_stopping=bool(estimator.do_early_stopping_), validation_loaded_after_fit=True,
                   fit_X_sha256=hashlib.sha256(train[features].to_numpy(dtype=np.float64).tobytes()).hexdigest(),
                   fit_y_sha256=hashlib.sha256(train["target_energy_kwh"].to_numpy(dtype=np.float64).tobytes()).hexdigest(),
                   persistence=persistence, audit=state, threadpools=pools))
        write_json(output / "model-config.json", dict(approved_parameters=PARAMS, actual_parameters=estimator.get_params(),
                   feature_columns=features, model_version=bundle["model_version"], prediction_policy=POLICY,
                   training_split="train", final_locked=False))
        names = ("candidate.joblib", "predictions-validation.csv", "metrics-validation.json", "runtime-evidence.json", "model-config.json")
        write_json(output / "manifest.json", dict(status="APPLIED_UNVERIFIED", run_id=args.run_id,
                   created_at=datetime.now(timezone.utc).isoformat(), model_version=bundle["model_version"],
                   python=platform.python_version(), packages=installed, training_split="train", evaluation_split="validation",
                   train_n=22513, validation_n=4727, test_evaluated=False, final_locked=False,
                   source_phase2a_manifest_sha256=sha256(SOURCE / "manifest.json"),
                   source_phase2a_verification_sha256=SOURCE_VERIFICATION_HASH, source_phase2a_outputs=source["outputs_sha256"],
                   flink_source=source["source"], prediction_policy=POLICY,
                   code_sha256={name: sha256(ROOT / "forecasting" / name) for name in ("train_hgb.py", "predictor.py", "requirements.txt")},
                   outputs_sha256={name: sha256(output / name) for name in names}))
        print(json.dumps(dict(run_id=args.run_id, metrics=scores, persistence=persistence, fit_seconds=fit_seconds)))
    finally:
        state["active"] = False


if __name__ == "__main__":
    main()

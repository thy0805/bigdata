import hashlib
import importlib.metadata
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "forecasting"))
from predictor import POLICY, predict_bundle

MODEL = "models/final/hgb-uci-hourly-v1.0-train-only"
ML = "data/ml/runs/20261009-phase2a-a"
RUN = "models/runs/20261009-phase2b2-a"
HOURLY = "data/processed/runs/20261009T102201900234-full"
MODEL_SHA = "f4c33c54b026a3c81312dff9c9623c7dad33a3f9df4986ecd8693b7267d8749c"
HOURLY_SHA = "8b03f1e3c82a5344c071a19f756cb7ec87fce18cc9a612cd63c4dcf4a8b5b2bc"
TEST_SHA = "f9785b91f46c43bbb22c08c98294cd32739f75e5df0218e355baa53d5fbd3574"
META = ["target_hour", "prediction_origin", "target_end", "latest_observed_hour", "target_energy_kwh"]
GROUPS = ["Khu vực bếp", "Khu vực giặt giũ", "Bình nước nóng và điều hòa"]


class ArtifactError(ValueError):
    pass


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require(passed, message):
    if not passed:
        raise ArtifactError(message)


def source_signature(root=ROOT):
    root = Path(root)
    signature = {}

    def checked(relative, expected):
        actual = sha256(root / relative)
        require(actual == expected, "Checksum không khớp: " + relative)
        signature[relative] = actual

    final = read_json(root / MODEL / "manifest.json")
    qa = read_json(root / ".agent/qa/phase2b2-20261009/verification.json")
    companion = read_json(root / RUN / "verification.json")
    require(qa["status"] == "VERIFIED" and qa["passed"] == qa["total_checks"] == 51 and
            all(item["passed"] for item in qa["checks"]), "QA Phase2B2 chưa VERIFIED")
    checked(companion["qa_path"], companion["qa_sha256"])
    require(companion["status"] == "VERIFIED", "Run Test chưa VERIFIED")
    checked(MODEL+"/manifest.json", qa["final_manifest_sha256"])
    require(final["status"] == "LOCKED" and final["model_sha256"] == MODEL_SHA and final["no_refit"] and
            final["training_split"] == "train" and final["fitted_rows"] == 22513, "Model cuối không đúng phiên bản đã khóa")
    checked(MODEL+"/model.joblib", MODEL_SHA)
    checked(ML+"/manifest.json", final["source_phase2a_manifest_sha256"])
    for name, value in final["source_phase2a_outputs"].items():
        checked(ML+"/"+name, value)
    require(final["source_phase2a_outputs"]["holdout/test.csv"] == TEST_SHA, "Test không đúng bản đã khóa")
    schema = read_json(root / ML / "feature-schema.json")
    require(schema["feature_columns"] == final["feature_columns"] and len(final["feature_columns"]) == 11 and
            final["prediction_policy"] == POLICY, "Feature schema hoặc D09 không khớp")
    checked(HOURLY+"/hourly-grid.csv", HOURLY_SHA)
    require(final["flink_source"]["sha256"] == HOURLY_SHA, "Nguồn Flink không khớp")
    checked(HOURLY+"/manifest.json", final["flink_source"]["manifest_sha256"])
    checked(HOURLY+"/verification.json", final["flink_source"]["verification_sha256"])
    require(read_json(root / HOURLY / "verification.json")["status"] == "VERIFIED", "Dữ liệu Flink chưa VERIFIED")
    manifest = read_json(root / RUN / "manifest.json")
    for name, value in manifest["outputs_sha256"].items():
        checked(RUN+"/"+name, value)
    require(read_json(root / RUN / "metrics-test.json") == final["test_metrics"] and final["test_metrics"]["n"] == 4590,
            "Metric Test không khớp bản chính thức")
    require(all(importlib.metadata.version(name) == version for name, version in final["packages"].items()),
            "Môi trường ML khác các phiên bản đã khóa")
    for relative in (RUN+"/manifest.json", RUN+"/verification.json"):
        signature[relative] = sha256(root / relative)
    return tuple(sorted(signature.items()))


@st.cache_data(show_spinner=False, max_entries=3)
def load_data(root_path, signature):
    root = Path(root_path)
    hourly = pd.read_csv(root / HOURLY / "hourly-grid.csv", na_values=["NULL"], float_precision="round_trip")
    hourly["hour_start"] = pd.to_datetime(hourly["hour_start"], format="%Y-%m-%d %H:%M:%S")
    hourly["is_complete"] = hourly["is_complete"].astype(bool)
    final = read_json(root / MODEL / "manifest.json")
    test = pd.read_csv(root / ML / "holdout/test.csv", float_precision="round_trip")
    saved = pd.read_csv(root / RUN / "predictions-test.csv", float_precision="round_trip")
    for frame in (test, saved):
        for field in META[:4]:
            frame[field] = pd.to_datetime(frame[field], format="%Y-%m-%d %H:%M:%S")
    require(list(test.columns) == META+final["feature_columns"] and len(test) == len(saved) == 4590, "Schema hoặc số dòng Test sai")
    require(test[META].equals(saved[META]) and test["target_hour"].is_unique, "Mask Test và dự báo không khớp")
    require(len(hourly) == 34589 and hourly["hour_start"].is_unique and hourly["hour_start"].is_monotonic_increasing,
            "Trục thời gian giờ không hợp lệ")
    require(hourly["hour_start"].equals(pd.Series(pd.date_range(hourly["hour_start"].iloc[0], hourly["hour_start"].iloc[-1], freq="h"))),
            "Trục giờ đã bị nén qua khoảng thiếu")
    return dict(hourly=hourly, test=test, saved=saved, final=final,
                metrics=read_json(root / RUN / "metrics-test.json"),
                flink=read_json(root / HOURLY / "manifest.json"),
                splits=read_json(root / ML / "split-summary.json"))


@st.cache_resource(show_spinner=False, max_entries=2)
def load_model(root_path, model_sha, version):
    root = Path(root_path)
    require(model_sha == MODEL_SHA and sha256(root / MODEL / "model.joblib") == model_sha, "Checksum model sai trước khi nạp")
    bundle = joblib.load(root / MODEL / "model.joblib")
    require(bundle["final_locked"] and bundle["model_version"] == version and bundle["refit"] is False and
            bundle["prediction_policy"] == POLICY, "Bundle model không đúng metadata đã khóa")
    return bundle


def select_range(hourly, start, end):
    lower, upper = pd.Timestamp(start), pd.Timestamp(end)+pd.Timedelta(days=1)
    if lower >= upper:
        return hourly.iloc[:0].copy()
    return hourly.loc[(hourly["hour_start"] >= lower) & (hourly["hour_start"] < upper)].copy()


def summarize(hourly):
    full = hourly.loc[hourly["is_complete"] & hourly["energy_kwh"].notna()]
    valid = int(hourly["valid_power_count"].sum())
    expected = len(hourly)*60
    recorded = int(hourly["record_count"].sum())
    observed = hourly["observed_energy_kwh"].sum(min_count=1)
    peak = full.loc[full["energy_kwh"].idxmax()] if len(full) else None
    return dict(observed_kwh=float(observed) if pd.notna(observed) else None,
                average_full_kwh=float(full["energy_kwh"].mean()) if len(full) else None,
                peak_kwh=float(peak["energy_kwh"]) if peak is not None else None,
                peak_hour=peak["hour_start"] if peak is not None else None,
                coverage=valid/expected if expected else None, valid_minutes=valid, expected_minutes=expected,
                missing_measurement_minutes=recorded-valid, unrecorded_boundary_minutes=expected-recorded,
                complete_hours=len(full), incomplete_hours=len(hourly)-len(full),
                negative_residual_minutes=int(hourly["negative_residual_count"].sum()),
                hours=len(hourly), recorded_minutes=recorded)


def subgroups(hourly):
    rows = []
    denominator = len(hourly)*60
    for index, name in enumerate(GROUPS, 1):
        total = hourly[f"sub{index}_observed_kwh"].sum(min_count=1)
        valid = int(hourly[f"sub{index}_valid_count"].sum())
        rows.append(dict(group=name, observed_kwh=float(total) if pd.notna(total) else None,
                         coverage=valid/denominator if denominator else None, valid_minutes=valid))
    return pd.DataFrame(rows)


def eligible_forecasts(test, start, end):
    lower, upper = pd.Timestamp(start), pd.Timestamp(end)+pd.Timedelta(days=1)
    return test.loc[(test["target_hour"] >= lower) & (test["target_hour"] < upper)].copy()


def forecast(bundle, test, stamp):
    row = test.loc[test["target_hour"] == pd.Timestamp(stamp)]
    require(len(row) == 1, "Mốc dự báo không có đủ feature hợp lệ trong Test")
    features = row[bundle["feature_columns"]].copy()
    require("target_energy_kwh" not in features.columns and len(features.columns) == 11, "Input model chứa nhãn hoặc sai feature")
    raw, final = predict_bundle(bundle, features)
    record = row.iloc[0]
    return dict(prediction_raw_kwh=float(raw[0]), prediction_final_kwh=float(final[0]),
                prediction_origin=record["prediction_origin"], target_hour=record["target_hour"], target_end=record["target_end"],
                latest_observed_hour=record["latest_observed_hour"], actual_kwh=float(record["target_energy_kwh"]),
                feature_columns=list(features.columns), model_version=bundle["model_version"])

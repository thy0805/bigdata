import ast
import csv
import json
import math
import os
import sys
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

os.environ.update(OMP_NUM_THREADS="2", OPENBLAS_NUM_THREADS="2", MKL_NUM_THREADS="2")
ROOT = Path(__file__).resolve().parents[2]
QA = ROOT / ".agent/qa/phase4-app-20261009"
sys.path.insert(0, str(ROOT / "dashboard"))
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from streamlit.testing.v1 import AppTest
import charts
import data_service as d

checks = []
witness = {"fit_calls": 0, "forbidden_io": [], "app_runs": 0}
frozen = d.read_json(QA / "preflight.json")["files"]
active_guard = False


def audit(event, args):
    if active_guard and event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
        path = str(Path(os.fsdecode(args[0])).resolve())
        mode, flags = args[1:3]
        writing = any(char in str(mode) for char in "wax+") or bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
        raw_read = not writing and ("/data/raw/" in path or path.endswith("individual+household+electric+power+consumption.zip"))
        if (path in frozen and writing) or raw_read:
            witness["forbidden_io"].append(path)
            raise RuntimeError("Forbidden artifact IO: " + path)


sys.addaudithook(audit)


def check(name, value, details=None):
    checks.append(dict(name=name, passed=bool(value), details=details))
    print(("PASS " if value else "FAIL ") + name, flush=True)


def close(actual, expected):
    return actual is None if expected is None else actual is not None and math.isclose(float(actual), float(expected), abs_tol=1e-10, rel_tol=1e-12)


def no_fit(*args, **kwargs):
    witness["fit_calls"] += 1
    raise RuntimeError("fit is forbidden in Phase4")


def app_ok(app, name):
    witness["app_runs"] += 1
    check(name, not app.exception and not app.error, [str(x.value) for x in app.exception])


for file in (ROOT / "dashboard").glob("*.py"):
    tree = ast.parse(file.read_text(encoding="utf-8"))
    check("syntax/no_fit:" + file.name, not any(isinstance(node, ast.Attribute) and node.attr in ("fit", "fit_transform", "partial_fit") for node in ast.walk(tree)))

signature = d.source_signature()
check("source_gate_21_hashes", len(signature) == 21)
d.load_data.clear()
with patch.object(pd, "read_csv", wraps=pd.read_csv) as reader:
    data = d.load_data(str(ROOT), signature)
    first_reads = reader.call_count
    again = d.load_data(str(ROOT), signature)
    check("data_cache_hit", first_reads == 3 and reader.call_count == first_reads)
    d.load_data(str(ROOT), signature + (("qa-key-version", "different"),))
    check("content_signature_cache_invalidation", reader.call_count == first_reads * 2)
with patch.object(d, "sha256", return_value="0" * 64):
    try:
        d.source_signature()
    except d.ArtifactError:
        check("wrong_hash_rejected_before_cache", True)
    else:
        check("wrong_hash_rejected_before_cache", False)

hourly, test, saved = data["hourly"], data["test"], data["saved"]
check("hourly_complete_and_missing", int(hourly.is_complete.sum()) == 34085 and int(hourly.energy_kwh.isna().sum()) == 504)
check("test_schema_and_mask", list(test.columns) == d.META + data["final"]["feature_columns"] and test[d.META].equals(saved[d.META]))
with (ROOT / d.HOURLY / "hourly-grid.csv").open(encoding="utf-8", newline="") as stream:
    original = list(csv.DictReader(stream))


def oracle(rows):
    observed = [Decimal(row["observed_energy_kwh"]) for row in rows if row["observed_energy_kwh"] != "NULL"]
    full = [row for row in rows if row["is_complete"].lower() == "true" and row["energy_kwh"] != "NULL"]
    values = [Decimal(row["energy_kwh"]) for row in full]
    valid = sum(int(row["valid_power_count"]) for row in rows)
    recorded = sum(int(row["record_count"]) for row in rows)
    peak = max(full, key=lambda row: Decimal(row["energy_kwh"])) if full else None
    return dict(observed_kwh=sum(observed) if observed else None,
                average_full_kwh=sum(values)/len(values) if values else None,
                peak_kwh=Decimal(peak["energy_kwh"]) if peak else None,
                peak_hour=pd.Timestamp(peak["hour_start"]) if peak else None,
                coverage=Decimal(valid)/(len(rows)*60) if rows else None,
                valid_minutes=valid, expected_minutes=len(rows)*60, recorded_minutes=recorded,
                missing_measurement_minutes=recorded-valid, unrecorded_boundary_minutes=len(rows)*60-recorded,
                complete_hours=len(full), incomplete_hours=len(rows)-len(full), hours=len(rows),
                negative_residual_minutes=sum(int(row["negative_residual_count"]) for row in rows))


oracle_results = {}
for name, start, end in (("whole", date(2006, 12, 16), date(2010, 11, 26)),
                         ("default", date(2010, 11, 20), date(2010, 11, 26)),
                         ("first_day", date(2006, 12, 16), date(2006, 12, 16)),
                         ("last_day", date(2010, 11, 26), date(2010, 11, 26)),
                         ("reversed", date(2010, 11, 26), date(2010, 11, 20))):
    selected = d.select_range(hourly, start, end)
    rows = [row for row in original if start <= datetime.fromisoformat(row["hour_start"]).date() <= end]
    expected, actual = oracle(rows), d.summarize(selected)
    numeric = ("observed_kwh", "average_full_kwh", "peak_kwh", "coverage")
    check("KPI_decimal_oracle:" + name, all(close(actual[key], expected[key]) for key in numeric) and
          all(actual[key] == expected[key] for key in expected if key not in numeric))
    oracle_results[name] = {key: str(value) for key, value in expected.items()}
    groups = d.subgroups(selected)
    group_checks = []
    for index in range(1, 4):
        observed = [Decimal(row[f"sub{index}_observed_kwh"]) for row in rows if row[f"sub{index}_observed_kwh"] != "NULL"]
        total = sum(observed) if observed else None
        valid = sum(int(row[f"sub{index}_valid_count"]) for row in rows)
        group_checks.append(close(groups.iloc[index-1].observed_kwh, total) and groups.iloc[index-1].valid_minutes == valid)
    check("subgroups_decimal_oracle:" + name, all(group_checks))

empty = hourly.iloc[:0]
missing = hourly.loc[hourly.valid_power_count == 0]
check("all_missing_not_zero", d.summarize(missing)["observed_kwh"] is None and d.summarize(missing)["peak_kwh"] is None)
check("boundary_minutes_81", d.summarize(hourly)["unrecorded_boundary_minutes"] == 81)
check("recorded_missing_25979", d.summarize(hourly)["missing_measurement_minutes"] == 25979)
line = charts.energy_line(hourly).data[0]
check("energy_gap_preserved", line.connectgaps is False and len(line.x) == 34589 and np.isnan(line.y).sum() == 504)
comparison = charts.comparison(saved, hourly, date(2010, 4, 24), date(2010, 11, 26), True)
check("comparison_gap_and_mask", len(comparison.data) == 4 and all(trace.connectgaps is False and np.isfinite(trace.y).sum() == 4590 for trace in comparison.data))
month_figure = charts.monthly(hourly)
check("monthly_category_axis", month_figure.layout.xaxis.type == "category")
month_oracle = {}
for row in original:
    key = row["hour_start"][:7]
    month_oracle.setdefault(key, [])
    if row["observed_energy_kwh"] != "NULL":
        month_oracle[key].append(Decimal(row["observed_energy_kwh"]))
check("monthly_decimal_oracle", all(close(value, sum(month_oracle[key]) if month_oracle[key] else None)
                                    for key, value in zip(month_figure.data[0].x, month_figure.data[0].y)))
for name, frame in (("empty", empty), ("missing", missing)):
    for figure in (charts.energy_line(frame), charts.profile(frame, "hour"), charts.profile(frame, "weekday"), charts.monthly(frame), charts.subgroup_bar(d.subgroups(frame))):
        figure.to_json()
    check("chart_empty_safe:" + name, True)

d.load_model.clear()
with patch.object(d.joblib, "load", wraps=d.joblib.load) as loader:
    bundle = d.load_model(str(ROOT), d.MODEL_SHA, data["final"]["version"])
    cached_bundle = d.load_model(str(ROOT), d.MODEL_SHA, data["final"]["version"])
    check("model_cache_hit", loader.call_count == 1 and cached_bundle is bundle)

active_guard = True
with patch.object(HistGradientBoostingRegressor, "fit", no_fit):
    for index in (0, len(test)//2, len(test)-1):
        stamp = test.target_hour.iloc[index]
        with patch.object(bundle["estimator"], "predict", wraps=bundle["estimator"].predict) as predict:
            result = d.forecast(bundle, test, stamp)
            input_frame = predict.call_args.args[0]
        check("real_model_saved_prediction:" + str(index), close(result["prediction_raw_kwh"], saved.hgb_raw_kwh.iloc[index]) and close(result["prediction_final_kwh"], saved.hgb_final_kwh.iloc[index]))
        check("no_target_input_and_order:" + str(index), list(input_frame.columns) == bundle["feature_columns"] and len(input_frame) == 1 and "target_energy_kwh" not in input_frame)
        perturbed = test.copy()
        perturbed.loc[perturbed.target_hour == stamp, "target_energy_kwh"] = -9999
        check("target_label_perturbation:" + str(index), d.forecast(bundle, perturbed, stamp)["prediction_final_kwh"] == result["prediction_final_kwh"])
    bad_stamp = hourly.loc[hourly.energy_kwh.isna(), "hour_start"].iloc[-1]
    try:
        d.forecast(bundle, test, bad_stamp)
    except d.ArtifactError:
        check("missing_features_rejected", True)
    else:
        check("missing_features_rejected", False)
    try:
        bad = test.copy()
        bad.loc[0, bundle["feature_columns"][0]] = np.nan
        d.forecast(bundle, bad, test.target_hour.iloc[0])
    except ValueError:
        check("nonfinite_features_rejected", True)
    else:
        check("nonfinite_features_rejected", False)
    app = AppTest.from_file(str(ROOT / "dashboard/app.py"), default_timeout=30).run()
    app_ok(app, "AppTest_initial")
    check("exact_three_tabs", [tab.label for tab in app.tabs] == ["Tổng quan", "Phân tích", "Dự báo"])
    check("official_metric_4590", any(metric.label == "Số mẫu Test" and metric.value == "4.590" for metric in app.metric))
    app.selectbox(key="forecast_stamp").select(test.target_hour.iloc[-1]).run()
    app.button[0].click().run()
    app_ok(app, "AppTest_real_forecast_last")
    check("button_real_final_model", close(app.session_state["forecast_result"]["prediction_final_kwh"], saved.hgb_final_kwh.iloc[-1]))
    app.checkbox(key="baselines").check().run()
    app_ok(app, "AppTest_baselines")
    for name, start, end in (("first_day_no_test", date(2006, 12, 16), date(2006, 12, 16)),
                             ("whole", date(2006, 12, 16), date(2010, 11, 26)),
                             ("first_test", date(2010, 4, 24), date(2010, 4, 24)),
                             ("last_day", date(2010, 11, 26), date(2010, 11, 26)),
                             ("reversed", date(2010, 11, 26), date(2010, 11, 20))):
        app.date_input(key="start").set_value(start)
        app.date_input(key="end").set_value(end)
        app.run()
        app_ok(app, "AppTest_filter:" + name)
        check("fixed_metric_after_filter:" + name, any(metric.label == "Số mẫu Test" and metric.value == "4.590" for metric in app.metric))
        if name in ("first_day_no_test", "reversed"):
            check("no_forecast_when_ineligible:" + name, len(app.selectbox) == 0)
        if name == "first_test":
            app.selectbox(key="forecast_stamp").select(test.target_hour.iloc[0]).run()
            app.button[0].click().run()
            app_ok(app, "AppTest_real_forecast_first")
            check("button_first_matches", close(app.session_state["forecast_result"]["prediction_final_kwh"], saved.hgb_final_kwh.iloc[0]))
    missing_days = hourly.groupby(hourly.hour_start.dt.date).valid_power_count.sum()
    missing_day = missing_days[missing_days == 0].index[0]
    app.date_input(key="start").set_value(missing_day)
    app.date_input(key="end").set_value(missing_day)
    app.run()
    app_ok(app, "AppTest_all_missing_day")
    check("missing_KPI_not_zero", next(metric.value for metric in app.metric if metric.label == "Điện năng ghi nhận (kWh)") == "—")
    with patch.object(d, "source_signature", side_effect=d.ArtifactError("QA invalid checksum")):
        broken = AppTest.from_file(str(ROOT / "dashboard/app.py"), default_timeout=30).run()
        check("bad_hash_visible_error_and_stop", len(broken.error) == 1 and "QA invalid checksum" in broken.error[0].value and not broken.exception and len(broken.tabs) == 0)

active_guard = False
check("no_fit_runtime", witness["fit_calls"] == 0)
check("no_raw_scan_or_frozen_write", not witness["forbidden_io"])
preserved = [path for path, value in frozen.items() if Path(path).is_file() and d.sha256(path) == value]
missing_frozen = [path for path in frozen if not Path(path).is_file()]
changed = [path for path in frozen if Path(path).is_file() and path not in preserved]
check("frozen_preflight_files_preserved", len(preserved) == len(frozen) and not changed and not missing_frozen, dict(preserved=len(preserved), changed=changed, missing=missing_frozen))
report = dict(status="VERIFIED" if all(item["passed"] for item in checks) else "FAIL", scope="technical; visual QA separate",
              time=datetime.now(timezone.utc).isoformat(), total_checks=len(checks), passed=sum(item["passed"] for item in checks),
              checks=checks, witness=witness, kpi_oracle=oracle_results, model_sha256=d.MODEL_SHA,
              source_signature=dict(signature), preservation=dict(total=len(frozen), matching=len(preserved), changed=changed, missing=missing_frozen))
destination = QA / "technical-verification.json"
revision = 2
while destination.exists():
    destination = QA / f"technical-verification-v{revision}.json"
    revision += 1
with destination.open("x", encoding="utf-8") as stream:
    json.dump(report, stream, ensure_ascii=False, indent=2)
print(json.dumps(dict(status=report["status"], passed=report["passed"], total=report["total_checks"])), flush=True)
sys.exit(0 if report["status"] == "VERIFIED" else 1)

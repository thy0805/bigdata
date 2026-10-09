from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
original = ROOT / '.agent/scripts/verify_phase4_app.py'
source = original.read_text(encoding='utf-8')
replacements = {
    'QA = ROOT / ".agent/qa/phase4-app-20261009"': 'QA = ROOT / ".agent/qa/phase4-data-guide-20261010"',
    'frozen = d.read_json(QA / "preflight.json")["files"]':
        'frozen = d.read_json(ROOT / ".agent/qa/phase4-app-20261009/preflight.json")["files"].copy()\nfrozen.pop(str(ROOT / "dashboard/app.py"))',
    'check("exact_three_tabs", [tab.label for tab in app.tabs] == ["Tổng quan", "Phân tích", "Dự báo"])':
        '''check("three_main_tabs_and_two_guide_tabs", [tab.label for tab in app.tabs] == ["Tổng quan", "Phân tích", "Dự báo", "Dữ liệu gốc", "Đặc trưng dự báo"])
    check("guide_title", any(e.label == "Tìm hiểu bộ dữ liệu và cách AI dự báo" for e in app.expander))
    raw_table, feature_table = [item.value for item in app.table]
    check("nine_raw_columns", list(raw_table.index) == ["Date", "Time", "Global_active_power", "Global_reactive_power", "Voltage", "Global_intensity", "Sub_metering_1", "Sub_metering_2", "Sub_metering_3"])
    check("raw_units_preserved", raw_table.loc["Global_active_power", "Đơn vị / cách đọc"] == "kW" and raw_table.loc["Global_reactive_power", "Đơn vị / cách đọc"] == "kW (theo UCI)" and all(raw_table.loc[name, "Đơn vị / cách đọc"] == "Wh (mỗi phút)" for name in ["Sub_metering_1", "Sub_metering_2", "Sub_metering_3"]))
    check("eleven_features_in_locked_order", list(feature_table.index) == data["final"]["feature_columns"] and len(feature_table) == 11)
    check("feature_translations", feature_table.iloc[:, 0].tolist() == ["Điện năng 1 giờ trước", "Điện năng 2 giờ trước", "Điện năng 3 giờ trước", "Điện năng cùng giờ hôm trước", "Điện năng cùng giờ tuần trước", "Điện năng trung bình 3 giờ trước", "Điện năng trung bình 24 giờ trước", "Giờ trong ngày cần dự báo", "Thứ trong tuần của giờ cần dự báo", "Tháng trong năm của giờ cần dự báo", "Giờ cần dự báo thuộc cuối tuần hay ngày thường"])
    check("dataset_counts_distinct", all(any(metric.label == label and metric.value == value for metric in app.metric) for label, value in [("Dòng dữ liệu gốc", "2.075.259"), ("Cột dữ liệu gốc", "9"), ("Tần suất ghi", "1 phút")]))
    visible = " ".join(str(item.value) for item in list(app.markdown) + list(app.caption))
    check("no_technical_metadata_in_ui", all(token not in visible for token in ["SHA-256", "D09", data["final"]["model_sha256"], data["final"]["version"], data["flink"]["jobs"][0]["jid"]]))
    check("clear_source_target_and_limits", all(token in visible for token in ["Sceaux", "16/12/2006", "26/11/2010", "34.589", "34.085", "504", "không phải 11 cột", "không học lại từ Test", "năm 2026", "https://archive.ics.uci.edu/dataset/235/"]))'''
}
for old, new in replacements.items():
    if source.count(old) != 1:
        raise SystemExit('Regression adapter source mismatch; no QA executed')
    source = source.replace(old, new)
old_app = __import__('subprocess').check_output(['git', '-c', 'safe.directory=' + ROOT.parent.as_posix(), '-C', str(ROOT.parent),
                                               'show', '2da758a:Detaituan8910/dashboard/app.py']).decode('utf-8')
new_app = (ROOT / 'dashboard/app.py').read_text(encoding='utf-8')
start = 'with st.expander("Nguồn dữ liệu, model và giới hạn"):'
new_start = 'with st.expander("Tìm hiểu bộ dữ liệu và cách AI dự báo", expanded=False):'
footer = 'st.markdown(\'<div class="footer-note">'
if old_app.split(start)[0] != new_app.split(new_start)[0] or old_app.split(footer)[1] != new_app.split(footer)[1]:
    raise SystemExit('Change outside authorized expander; no QA executed')
exec(compile(source, str(original), 'exec'), dict(__file__=str(__file__), __name__='__main__'))

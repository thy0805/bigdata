from datetime import timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

from charts import comparison, energy_line, monthly, profile, subgroup_bar
from data_service import ROOT, ArtifactError, eligible_forecasts, forecast, load_data, load_model, select_range, source_signature, subgroups, summarize


st.set_page_config(page_title="Điện năng hộ gia đình", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>"+Path(__file__).with_name("style.css").read_text(encoding="utf-8")+"</style>", unsafe_allow_html=True)


def number(value, decimals=2):
    if value is None or pd.isna(value):
        return "—"
    return f"{value:,.{decimals}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def time_label(value):
    return pd.Timestamp(value).strftime("%d/%m/%Y %H:%M")


def chart(figure, key):
    st.plotly_chart(figure, use_container_width=True, key=key, config=dict(displayModeBar=False, scrollZoom=False))


def forecast_card(result, detail=False):
    st.markdown('<div class="forecast-value">'+number(result["prediction_final_kwh"], 3)+'<span class="forecast-unit">kWh</span></div>', unsafe_allow_html=True)
    st.caption("Giờ mục tiêu: "+time_label(result["target_hour"])+" – "+pd.Timestamp(result["target_end"]).strftime("%H:%M"))
    st.caption("Mốc phát dự báo: "+time_label(result["prediction_origin"]))
    if detail:
        st.caption("Dữ liệu đã biết đến hết khoảng giờ bắt đầu "+time_label(result["latest_observed_hour"]))
        st.markdown("**Thực tế để đối chiếu sau dự báo:** "+number(result["actual_kwh"], 3)+" kWh")
        st.caption("Giá trị thực tế không được truyền vào model.")
    else:
        st.caption("HGB Train-only. Dự báo tại mốc lịch sử, không phải hiện tại.")


try:
    signature = source_signature()
    data = load_data(str(ROOT), signature)
    bundle = load_model(str(ROOT), data["final"]["model_sha256"], data["final"]["version"])
except (ArtifactError, OSError, ValueError, KeyError, ImportError) as error:
    st.error("Không thể dùng artifact đã khóa: "+str(error))
    st.stop()

st.markdown('<div class="brand">UCI HOUSEHOLD ENERGY</div>', unsafe_allow_html=True)
st.title("Điện năng hộ gia đình")
st.caption("Phân tích tiêu thụ và dự báo một giờ kế tiếp. Dữ liệu lịch sử của một hộ tại Pháp, 2006–2010.")

hourly, test, saved = data["hourly"], data["test"], data["saved"]
first_day, last_day = hourly["hour_start"].min().date(), hourly["hour_start"].max().date()
left, right, scope = st.columns([1, 1, 2.2])
with left:
    start = st.date_input("Từ ngày", value=last_day-timedelta(days=6), min_value=first_day, max_value=last_day, format="DD/MM/YYYY", key="start")
with right:
    end = st.date_input("Đến ngày", value=last_day, min_value=first_day, max_value=last_day, format="DD/MM/YYYY", key="end")
with scope:
    st.caption("Bộ lọc chung cho cả ba tab")
    st.caption("Ngày lịch sử; metric Test chính thức luôn giữ nguyên toàn bộ 4.590 mẫu.")

selected = select_range(hourly, start, end)
stats = summarize(selected)
groups = subgroups(selected)
eligible = eligible_forecasts(test, start, end) if start <= end else test.iloc[:0]
if start > end:
    st.warning("Ngày bắt đầu đang sau ngày kết thúc. Hãy chọn lại khoảng ngày.")
if not stats["complete_hours"]:
    st.info("Khoảng chọn không có giờ đầy đủ. Không tính trung bình/đỉnh từ các phút thiếu; dự báo chỉ có tại mốc đủ feature trong Test.")

tabs = st.tabs(["Tổng quan", "Phân tích", "Dự báo"])
with tabs[0]:
    cols = st.columns(3)
    cols[0].metric("Điện năng ghi nhận (kWh)", number(stats["observed_kwh"]))
    cols[1].metric("Trung bình giờ đầy đủ (kWh/giờ)", number(stats["average_full_kwh"], 3))
    cols[2].metric("Điện năng giờ cao nhất (kWh)", number(stats["peak_kwh"], 3))
    captions = st.columns(3)
    captions[0].caption("Độ phủ phút: "+(number(100*stats["coverage"], 2)+"%" if stats["coverage"] is not None else "—"))
    captions[1].caption(number(stats["complete_hours"], 0)+" giờ đầy đủ trong "+number(stats["hours"], 0)+" khung giờ")
    captions[2].caption(time_label(stats["peak_hour"]) if stats["peak_hour"] is not None else "Không có giờ đầy đủ")
    main, side = st.columns([2.25, 1])
    with main, st.container(border=True, key="card_overview_line"):
        st.subheader("Điện năng theo giờ")
        chart(energy_line(selected), "overview_energy")
        st.caption("Giữ khoảng trống tại giờ thiếu. Tổng ghi nhận chỉ cộng các phút có phép đo; không coi đó là tổng đầy đủ khi độ phủ dưới 100%.")
    with side, st.container(border=True, key="card_overview_forecast"):
        st.subheader("Dự báo gần nhất trong khoảng chọn")
        if len(eligible):
            result = forecast(bundle, test, eligible["target_hour"].iloc[-1])
            forecast_card(result)
        else:
            st.info("Không có mốc hợp lệ trong Test thuộc khoảng chọn. Chọn ngày từ 24/04 đến 26/11/2010 có đủ feature.")
    with st.container(border=True, key="card_overview_groups"):
        st.subheader("Ba nhóm đo phụ")
        chart(subgroup_bar(groups), "overview_groups")
        st.caption("Nhóm đo theo khu vực, không phải ba thiết bị riêng. Tổng kWh là phần ghi nhận của từng nhóm; xem độ phủ riêng trong hover.")

with tabs[1]:
    a, b = st.columns(2)
    with a, st.container(border=True, key="card_analysis_hour"):
        st.subheader("Theo giờ trong ngày")
        chart(profile(selected, "hour"), "analysis_hour")
    with b, st.container(border=True, key="card_analysis_weekday"):
        st.subheader("Theo ngày trong tuần")
        chart(profile(selected, "weekday"), "analysis_weekday")
    st.caption("Trung bình chỉ dùng giờ đầy đủ; hover hiển thị số mẫu mỗi nhóm. Nhóm không có mẫu giữ trống.")
    a, b = st.columns([1.2, 1])
    with a, st.container(border=True, key="card_analysis_month"):
        st.subheader("Xu hướng theo tháng")
        chart(monthly(selected), "analysis_month")
        st.caption("Tổng ghi nhận trong khoảng lọc, có thể là một phần tháng. Độ phủ và số giờ trong hover; không ngoại suy phần thiếu.")
    with b, st.container(border=True, key="card_analysis_groups"):
        st.subheader("So sánh nhóm đo phụ")
        chart(subgroup_bar(groups, 250), "analysis_groups")
    with st.expander("Chất lượng dữ liệu trong khoảng chọn", expanded=True):
        a, b, c, d = st.columns(4)
        a.metric("Giờ không đầy đủ", number(stats["incomplete_hours"], 0))
        b.metric("Phút thiếu phép đo", number(stats["missing_measurement_minutes"], 0))
        c.metric("Phút chưa ghi nhận ở biên", number(stats["unrecorded_boundary_minutes"], 0))
        d.metric("Phút residual âm", number(stats["negative_residual_minutes"], 0))
        st.caption("Độ phủ = phút công suất hợp lệ / (60 × số khung giờ). Phút thiếu phép đo tính trên bản ghi đã có; phút chưa ghi nhận ở biên là phần giờ đầu/cuối. Residual âm là cờ chất lượng, chưa khẳng định nguyên nhân và không ép về 0.")

with tabs[2]:
    a, b = st.columns([1.1, 1.7])
    with a, st.container(border=True, key="card_forecast_input"):
        st.subheader("Dự báo tại mốc lịch sử")
        if len(eligible):
            choices = eligible["target_hour"].tolist()
            key_range = (str(start), str(end))
            if st.session_state.get("forecast_range") != key_range:
                st.session_state["forecast_stamp"] = choices[-1]
                st.session_state["forecast_range"] = key_range
                st.session_state.pop("forecast_result", None)
            stamp = st.selectbox("Mốc phát dự báo / giờ mục tiêu", choices, format_func=time_label, key="forecast_stamp")
            if st.button("Chạy dự báo", type="primary", width="stretch"):
                st.session_state["forecast_result"] = forecast(bundle, test, stamp)
            result = st.session_state.get("forecast_result")
            if result is not None and result["target_hour"] == stamp:
                forecast_card(result, True)
            else:
                st.caption("Chọn mốc rồi nhấn Chạy dự báo. Model dùng 11 feature quá khứ và lịch đã chuẩn bị, không dùng nhãn giờ mục tiêu.")
        else:
            st.info("Không có mốc dự báo hợp lệ trong khoảng lọc. Các giờ thiếu feature không được nội suy hoặc dùng số mẫu.")
    with b, st.container(border=True, key="card_forecast_compare"):
        st.subheader("Thực tế và dự báo HGB")
        show_baselines = st.checkbox("Hiển thị hai baseline", value=False, key="baselines")
        chart(comparison(saved, hourly, start, end, show_baselines), "forecast_compare")
        st.caption("Biểu đồ trong khoảng chọn chỉ gồm mốc đủ điều kiện Test. Khoảng thiếu không nối đường. Đối chiếu sau dự báo; dự báo một bước cuốn chiếu có nhận quan sát thực tế mới.")
    st.subheader("Đánh giá chính thức trên toàn bộ Test")
    scores = data["metrics"]["models"]
    a, b, c = st.columns(3)
    a.metric("HGB MAE (kWh)", number(scores["hgb"]["mae_kwh"], 4))
    b.metric("HGB RMSE (kWh)", number(scores["hgb"]["rmse_kwh"], 4))
    c.metric("Số mẫu Test", number(data["metrics"]["n"], 0))
    st.caption("24/04/2010 17:00 – 26/11/2010 20:00; 4.590 mẫu. Metric không thay đổi theo bộ lọc. Không dùng Test để chỉnh lại model.")
    st.dataframe(pd.DataFrame([dict(Model=label, **{"MAE (kWh)":scores[name]["mae_kwh"], "RMSE (kWh)":scores[name]["rmse_kwh"]})
                              for name, label in (("hgb", "HGB"), ("naive", "Naive"), ("seasonal_naive_24", "Seasonal Naive24"))]),
                 hide_index=True, width="stretch", column_config={"MAE (kWh)":st.column_config.NumberColumn(format="%.6f"),
                                                                          "RMSE (kWh)":st.column_config.NumberColumn(format="%.6f")})

with st.expander("Nguồn dữ liệu, model và giới hạn"):
    st.write("Model: "+data["final"]["version"]+". Train-only 22.513 mẫu; D09 = max(0, prediction_raw). Không fit khi mở hoặc đổi tab.")
    st.caption("SHA-256 model: "+data["final"]["model_sha256"])
    job = data["flink"]["jobs"][0]
    st.write("Apache Flink "+data["flink"]["runtime"]["flink-version"]+" · Job "+job["jid"]+" · "+job["state"]+" · "+data["flink"]["mode"])
    st.caption("Trạng thái job từ hồ sơ đã kiểm; không biểu thị cluster đang chạy. Dashboard đọc artifact giờ Flink, không tổng hợp lại dữ liệu phút.")
    st.write("Một hộ lịch sử, timestamp theo lịch nguồn chưa xác minh timezone/DST. Không dự báo năm 2026; không dự báo nhiều tháng mà không nhận thêm quan sát; chưa mô hình hóa độ trễ đo/truyền.")
    st.caption("Feature: "+", ".join(data["final"]["feature_columns"]))
    st.markdown("[Nguồn UCI](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption)")
st.markdown('<div class="footer-note">Dữ liệu lịch sử đã xử lý bằng Apache Flink. Dự báo theo model HGB đã khóa; không kết nối công tơ trực tiếp.</div>', unsafe_allow_html=True)

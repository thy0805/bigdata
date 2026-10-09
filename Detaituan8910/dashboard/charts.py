import pandas as pd
import plotly.graph_objects as go


BLUE = "#3976db"
SLATE = "#20344e"
PALETTE = ["#3976db", "#7eaae9", "#b8cfee"]
DAYS = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ nhật"]


def style(figure, height=310, ytitle="kWh"):
    figure.update_layout(height=height, margin=dict(l=12, r=12, t=16, b=18), paper_bgcolor="white", plot_bgcolor="white",
                         font=dict(family="Geist, Segoe UI, Arial, sans-serif", size=12, color=SLATE),
                         legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), hovermode="x unified",
                         yaxis=dict(title=ytitle, gridcolor="#edf1f6", zeroline=False),
                         xaxis=dict(title=None, showgrid=False), separators=",.")
    return figure


def energy_line(hourly):
    figure = go.Figure(go.Scatter(x=hourly["hour_start"], y=hourly["energy_kwh"], mode="lines",
                                 name="Giờ đầy đủ", line=dict(color=BLUE, width=1.6), connectgaps=False,
                                 hovertemplate="%{x|%d/%m/%Y %H:%M}<br>%{y:.3f} kWh<extra></extra>"))
    return style(figure)


def subgroup_bar(groups, height=230):
    figure = go.Figure(go.Bar(x=groups["observed_kwh"], y=groups["group"], orientation="h", marker_color=PALETTE,
                             customdata=groups[["coverage"]],
                             hovertemplate="%{y}<br>%{x:.3f} kWh<br>Độ phủ %{customdata[0]:.1%}<extra></extra>"))
    figure = style(figure, height, "")
    figure.update_layout(xaxis=dict(title="Điện năng ghi nhận (kWh)"), hovermode="closest")
    return figure


def profile(hourly, field):
    full = hourly.loc[hourly["is_complete"] & hourly["energy_kwh"].notna()].copy()
    full["group"] = full["hour_start"].dt.hour if field == "hour" else full["hour_start"].dt.dayofweek
    grouped = full.groupby("group")["energy_kwh"].agg(["mean", "count"])
    axis = range(24) if field == "hour" else range(7)
    grouped = grouped.reindex(axis)
    labels = [f"{index:02d}h" for index in axis] if field == "hour" else DAYS
    figure = go.Figure(go.Bar(x=labels, y=grouped["mean"], marker_color=BLUE, customdata=grouped[["count"]],
                             hovertemplate="%{x}<br>%{y:.3f} kWh/giờ<br>%{customdata[0]:.0f} giờ đầy đủ<extra></extra>"))
    return style(figure, 260, "kWh/giờ")


def monthly(hourly):
    frame = hourly.copy()
    frame["month"] = frame["hour_start"].dt.to_period("M").astype(str)
    grouped = frame.groupby("month").agg(observed=("observed_energy_kwh", lambda s:s.sum(min_count=1)),
                                          valid=("valid_power_count", "sum"), hours=("hour_start", "size"))
    grouped["coverage"] = grouped["valid"]/(grouped["hours"]*60)
    figure = go.Figure(go.Bar(x=grouped.index, y=grouped["observed"], marker_color=BLUE, customdata=grouped[["coverage", "hours"]],
                             hovertemplate="%{x}<br>%{y:.3f} kWh ghi nhận<br>Độ phủ %{customdata[0]:.1%}<br>%{customdata[1]} khung giờ<extra></extra>"))
    figure = style(figure, 250, "kWh ghi nhận")
    figure.update_xaxes(type="category")
    return figure


def comparison(saved, hourly, start, end, baselines=False):
    lower, upper = pd.Timestamp(start), pd.Timestamp(end)+pd.Timedelta(days=1)
    grid = hourly.loc[(hourly["hour_start"] >= lower) & (hourly["hour_start"] < upper), "hour_start"]
    aligned = saved.set_index("target_hour").reindex(pd.DatetimeIndex(grid))
    figure = go.Figure()
    series = [("target_energy_kwh", "Thực tế", "#94a4ba"), ("hgb_final_kwh", "HGB", BLUE)]
    if baselines:
        series.extend([("naive_final_kwh", "Naive", "#b28f65"), ("seasonal_naive_24_final_kwh", "Seasonal Naive24", "#8f92bc")])
    for field, label, color in series:
        figure.add_trace(go.Scatter(x=aligned.index, y=aligned[field], name=label, mode="lines", connectgaps=False,
                                   line=dict(color=color, width=1.7 if label == "HGB" else 1.1),
                                   hovertemplate="%{x|%d/%m/%Y %H:%M}<br>%{y:.3f} kWh<extra>"+label+"</extra>"))
    return style(figure, 325)

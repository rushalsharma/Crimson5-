"""
Main Capstone demo: AI Investments ($B) vs US New Business Apps (M).
Growth rates (%), 2024–2025 linear-regression forecast, gap analysis, sliders.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression

from _shared import CRIMSON_PRIMARY, apply_crimson_layout, money_input, pretty_columns

DEFAULT_AI = [24, 33, 53, 79, 95, 146, 276, 189, 252]
DEFAULT_US_APPS = [2.8, 2.9, 3.2, 3.5, 3.5, 4.3, 5.4, 5.0, 5.4]
YEARS = list(range(2015, 2024))


def _growth_rates(values: list[float]) -> list[float]:
    rates = [np.nan]
    for i in range(1, len(values)):
        if values[i - 1] != 0:
            r = (values[i] - values[i - 1]) / values[i - 1] * 100
            rates.append(round(float(r), 2))
        else:
            rates.append(np.nan)
    return rates


def render(key_prefix: str = "", *, use_sidebar: bool = True) -> None:
    """Render full UI. Use unique key_prefix when embedding in integrated dashboard."""
    kp = key_prefix

    st.markdown("### AI Investments vs US New Business Apps — Growth Analysis")
    st.caption("Crimson 5 Energy · Cursor AI visualization demo · E-176 Capstone")

    ai_values: list[float] = []
    us_values: list[float] = []

    def _collect_ai(container) -> None:
        nonlocal ai_values
        ai_values = []
        for i, yr in enumerate(YEARS):
            val = float(
                money_input(
                    f"AI Investments {yr} ($B)" if use_sidebar else f"AI {yr} ($B)",
                    key=f"{kp}ai_{yr}",
                    value=float(DEFAULT_AI[i]),
                    min_value=0,
                    max_value=400,
                    step=1,
                )
            )
            ai_values.append(val)

    def _collect_us(container) -> None:
        nonlocal us_values
        us_values = []
        for i, yr in enumerate(YEARS):
            us_values.append(
                float(
                    container.slider(
                        f"US New Business Apps {yr} (M)" if use_sidebar else f"US Apps {yr}",
                        0.0,
                        10.0,
                        float(DEFAULT_US_APPS[i]),
                        0.1,
                        key=f"{kp}us_{yr}",
                    )
                )
            )

    if use_sidebar:
        st.sidebar.header("Adjust AI Investments ($ Billions)")
        _collect_ai(st.sidebar)
        st.sidebar.header("Adjust US New Business Apps (Millions)")
        _collect_us(st.sidebar)
    else:
        with st.expander("Adjust AI Investments ($ Billions), 2015–2023", expanded=True):
            _collect_ai(st)
        with st.expander("Adjust US New Business Apps (Millions), 2015–2023", expanded=False):
            _collect_us(st)

    ai_rates = _growth_rates(ai_values)
    us_rates = _growth_rates(us_values)

    df = pd.DataFrame(
        {
            "Year": YEARS,
            "AI_Investments": ai_values,
            "US_New_Business_Apps": us_values,
            "AI_Growth_Rate_%": ai_rates,
            "US_Growth_Rate_%": us_rates,
        }
    )
    df["Gap_%"] = df.apply(
        lambda r: (r["AI_Growth_Rate_%"] - r["US_Growth_Rate_%"])
        if pd.notna(r["AI_Growth_Rate_%"]) and pd.notna(r["US_Growth_Rate_%"])
        else np.nan,
        axis=1,
    )

    years_with_rates = np.array(YEARS[1:]).reshape(-1, 1)
    ai_rates_fit = [r for r in ai_rates[1:] if not np.isnan(r)]
    us_rates_fit = [r for r in us_rates[1:] if not np.isnan(r)]
    pred_years = [2024, 2025]
    pred_ai: list[float] = []
    pred_us: list[float] = []

    if len(ai_rates_fit) >= 2:
        reg_ai = LinearRegression().fit(years_with_rates[: len(ai_rates_fit)], ai_rates_fit)
        pred_ai = reg_ai.predict(np.array(pred_years).reshape(-1, 1)).tolist()
    if len(us_rates_fit) >= 2:
        reg_us = LinearRegression().fit(years_with_rates[: len(us_rates_fit)], us_rates_fit)
        pred_us = reg_us.predict(np.array(pred_years).reshape(-1, 1)).tolist()

    df_pred = pd.DataFrame(
        {
            "Year": pred_years,
            "AI_Growth_Rate_%": [round(x, 2) for x in pred_ai] if pred_ai else [np.nan, np.nan],
            "US_Growth_Rate_%": [round(x, 2) for x in pred_us] if pred_us else [np.nan, np.nan],
        }
    )
    df_pred["Gap_%"] = df_pred["AI_Growth_Rate_%"] - df_pred["US_Growth_Rate_%"]

    st.subheader("Chart 1: Growth Rates (%) by Year (X: Growth Rates, Y: Years)")
    df_plot1 = df[df["Year"] >= 2016].copy()
    df_plot1 = df_plot1.melt(
        id_vars=["Year"],
        value_vars=["AI_Growth_Rate_%", "US_Growth_Rate_%"],
        var_name="Series",
        value_name="Growth_Rate_%",
    )
    df_plot1["Series"] = df_plot1["Series"].replace(
        {"AI_Growth_Rate_%": "AI Investments ($B)", "US_Growth_Rate_%": "US New Business Apps (M)"}
    )
    fig1 = px.bar(
        df_plot1,
        x="Growth_Rate_%",
        y="Year",
        color="Series",
        orientation="h",
        barmode="group",
        title="Growth Rates (%) — X: Growth Rates, Y: Years",
        color_discrete_map={
            "AI Investments ($B)": CRIMSON_PRIMARY,
            "US New Business Apps (M)": "#1f77b4",
        },
    )
    fig1.update_layout(yaxis=dict(autorange="reversed"), height=400)
    apply_crimson_layout(fig1)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Chart 2: Trend in Growth Rates (%) — X: Years, Y: Growth Rates")
    df_line = df[df["Year"] >= 2016][["Year", "AI_Growth_Rate_%", "US_Growth_Rate_%"]].copy()
    df_line_full = pd.concat([df_line, df_pred[["Year", "AI_Growth_Rate_%", "US_Growth_Rate_%"]]], ignore_index=True)
    df_line_full = df_line_full.sort_values("Year").reset_index(drop=True)

    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=df_line_full["Year"],
            y=df_line_full["AI_Growth_Rate_%"],
            mode="lines+markers",
            name="AI Investments ($B) Growth %",
            line=dict(color=CRIMSON_PRIMARY, width=2),
        )
    )
    fig2.add_trace(
        go.Scatter(
            x=df_line_full["Year"],
            y=df_line_full["US_Growth_Rate_%"],
            mode="lines+markers",
            name="US New Business Apps (M) Growth %",
            line=dict(color="#1f77b4", width=2),
        )
    )
    for py in pred_years:
        if py in df_line_full["Year"].values:
            fig2.add_vline(x=py - 0.5, line_dash="dash", line_color="gray", opacity=0.7)
    fig2.update_layout(
        title="Growth Rate (%) Trend — X: Years, Y: Growth Rates",
        xaxis_title="Year",
        yaxis_title="Growth Rate (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    apply_crimson_layout(fig2)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Gap Analysis: AI Investments vs US New Business Apps")
    df_gap = df[df["Year"] >= 2016][["Year", "AI_Growth_Rate_%", "US_Growth_Rate_%", "Gap_%"]].copy()
    df_gap = pd.concat([df_gap, df_pred[["Year", "AI_Growth_Rate_%", "US_Growth_Rate_%", "Gap_%"]]], ignore_index=True)
    fig_gap = go.Figure()
    fig_gap.add_trace(
        go.Bar(
            x=df_gap["Year"],
            y=df_gap["Gap_%"],
            name="Gap (AI % − US %)",
            marker_color=["#2ca02c" if (g is not None and not pd.isna(g) and g > 0) else "#d62728" for g in df_gap["Gap_%"]],
        )
    )
    fig_gap.add_hline(y=0, line_dash="solid", line_color="gray")
    fig_gap.update_layout(
        title="Gap Between AI Investments Growth and US New Business Apps Growth (%)",
        xaxis_title="Year",
        yaxis_title="Gap (percentage points)",
    )
    apply_crimson_layout(fig_gap, height=350)
    st.plotly_chart(fig_gap, use_container_width=True)

    st.subheader("Data Tables")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Historical (2015–2023) & Growth Rates**")
        st.table(
            pretty_columns(df).style.format(
                {
                    "AI Investments": "{:.1f}",
                    "US New Business Apps": "{:.2f}",
                    "AI Growth Rate %": "{:.2f}",
                    "US Growth Rate %": "{:.2f}",
                    "Gap %": "{:.2f}",
                },
                na_rep="—",
            ).set_table_styles(
                [
                    {"selector": "th", "props": [("color", "#111827"), ("background-color", "#fdf2f4"), ("border", "1px solid #111827")]},
                    {"selector": "td", "props": [("color", "#111827"), ("background-color", "#ffffff"), ("border", "1px solid #111827")]},
                ]
            )
        )
    with c2:
        st.markdown("**Predicted Growth Rates (2024–2025)**")
        st.table(
            pretty_columns(df_pred).style.format(
                {
                    "AI Growth Rate %": "{:.2f}",
                    "US Growth Rate %": "{:.2f}",
                    "Gap %": "{:.2f}",
                },
                na_rep="—",
            ).set_table_styles(
                [
                    {"selector": "th", "props": [("color", "#111827"), ("background-color", "#fdf2f4"), ("border", "1px solid #111827")]},
                    {"selector": "td", "props": [("color", "#111827"), ("background-color", "#ffffff"), ("border", "1px solid #111827")]},
                ]
            )
        )

    st.caption("Sliders update charts and linear-regression forecasts automatically.")


if __name__ == "__main__":
    st.set_page_config(page_title="AI Investments & US Business Apps", layout="wide")
    st.title("Crimson 5 Energy — Main Capstone Demo")
    render(key_prefix="", use_sidebar=True)

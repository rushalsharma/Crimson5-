"""Panel 2: Tangible + intangible returns; ROI % vs year."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from _shared import CRIMSON_PRIMARY, apply_crimson_layout, chart_caption, dataframe_download, executive_insight, money_input, page_header, pretty_columns


def render(key_prefix: str = "p2_") -> None:
    kp = key_prefix
    presentation_mode = bool(st.session_state.get("presentation_mode", False))
    page_header(
        title="ROI & Value",
        subtitle="Evaluate tangible and intangible business value from the cloud transformation.",
        badge="Business Case",
    )
    with st.expander("Presenter talking points", expanded=False):
        st.markdown(
            """
            - This panel separates tangible value from intangible value.
            - Tangible value includes infrastructure savings and operational productivity.
            - Intangible value includes agility, compliance confidence, trust, decision speed, and strategic flexibility.
            - The key message is that cloud ROI often improves after benefit ramp-up, so the program should be evaluated as a staged transformation investment.
            """
        )
    with st.expander("Assumptions used", expanded=False):
        st.markdown(
            """
            - Defaults assume Year 1 investment with benefits ramping over five years.
            - Sliders control tangible value, intangible scoring, investment, and discount rate.
            - Output shows cumulative ROI progression and Year 5 ROI.
            - This simplified ROI view is directional and not a full finance model.
            """
        )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Tangible (annual $ benefit, steady state)")
        cost_reduction = money_input(
            "Infra cost reduction ($/yr)",
            key=f"{kp}td1",
            value=900_000,
            min_value=0,
            max_value=20_000_000,
            step=50_000,
        )
        productivity = money_input(
            "Ops productivity value ($/yr)",
            key=f"{kp}td2",
            value=600_000,
            min_value=0,
            max_value=20_000_000,
            step=50_000,
        )
    with c2:
        st.subheader("Intangible (0–1 scales → $ equivalent)")
        agility = st.slider("Agility / speed-to-market", 0.0, 1.0, 0.65, key=f"{kp}int1")
        trust = st.slider("Brand / trust / compliance posture", 0.0, 1.0, 0.55, key=f"{kp}int2")
        intangible_scale = money_input(
            "Max intangible $/yr at score=1",
            key=f"{kp}intscale",
            value=1_200_000,
            min_value=0,
            max_value=10_000_000,
            step=50_000,
        )

    investment_y1 = money_input(
        "Total program investment Year 1 ($)",
        key=f"{kp}inv",
        value=6_000_000,
        min_value=100_000,
        max_value=30_000_000,
        step=100_000,
    )
    discount = st.slider("Discount rate (%)", 0.0, 25.0, 10.0, 0.5, key=f"{kp}disc") / 100.0

    years = np.arange(1, 6)
    tangible_annual = cost_reduction + productivity
    intangible_annual = (0.5 * agility + 0.5 * trust) * intangible_scale
    benefits = []
    cumulative_net = 0.0
    roi_pct = []
    for y in years:
        ramp = min(1.0, 0.3 + 0.2 * (y - 1))
        b = (tangible_annual + intangible_annual) * ramp * (1.05 ** (y - 1))
        invest = investment_y1 if y == 1 else 0.0
        net = b - invest
        cumulative_net += net / ((1 + discount) ** (y - 1))
        denom = investment_y1 if investment_y1 else 1.0
        roi_pct.append(100.0 * cumulative_net / denom)

    df = pd.DataFrame({"Year": years, "ROI_%": roi_pct})

    m1, m2, m3 = st.columns(3)
    m1.metric("Tangible annual value", f"${tangible_annual:,.0f}")
    m2.metric("Intangible equivalent annual value", f"${intangible_annual:,.0f}")
    m3.metric("Year 5 ROI", f"{roi_pct[-1]:.1f}%")

    df_disp = pretty_columns(df)
    tbl = df_disp.style.format({"ROI %": "{:.1f}%"}).set_table_styles(
        [
            {"selector": "th", "props": [("color", "#111827"), ("background-color", "#fdf2f4"), ("border", "1px solid #111827")]},
            {"selector": "td", "props": [("color", "#111827"), ("background-color", "#ffffff"), ("border", "1px solid #111827")]},
        ]
    )
    if presentation_mode:
        with st.expander("View detailed table", expanded=False):
            st.table(tbl)
            dataframe_download(df_disp, "panel2_roi_timeseries.csv")
    else:
        st.table(tbl)
        dataframe_download(df_disp, "panel2_roi_timeseries.csv")
    executive_insight(
        "ROI improves after benefit ramp-up, so Crimson 5 should evaluate cloud as a staged transformation investment rather than a one-year expense."
    )

    fig = go.Figure(
        go.Scatter(
            x=df["Year"],
            y=df["ROI_%"],
            mode="lines+markers",
            line=dict(color=CRIMSON_PRIMARY, width=3),
            marker=dict(size=10),
            name="Cumulative ROI %",
        )
    )
    fig.add_hline(y=0, line_dash="dash", line_color="#64748b")
    fig.update_layout(
        title="Cumulative ROI vs time",
        xaxis_title="Year",
        yaxis_title="Cumulative ROI (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    apply_crimson_layout(fig)
    st.plotly_chart(fig, use_container_width=True)
    chart_caption("The break-even crossing is the key executive decision marker.")


if __name__ == "__main__":
    st.set_page_config(page_title="Panel 2 — ROI", layout="wide")
    st.title("Crimson 5 Energy — Panel 2")
    render()

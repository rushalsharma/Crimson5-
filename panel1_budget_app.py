"""Panel 1: 5-year OpEx / CapEx projection with cash-flow table and chart ($ vs year)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from _shared import CRIMSON_PRIMARY, apply_crimson_layout, chart_caption, dataframe_download, executive_insight, money_input, page_header, pretty_columns


def render(key_prefix: str = "p1_") -> None:
    kp = key_prefix
    presentation_mode = bool(st.session_state.get("presentation_mode", False))
    page_header(
        title="Budget Planning",
        subtitle="Estimate five-year cloud cash demand and understand how cost grows over time.",
        badge="Business Case",
    )
    with st.expander("Presenter talking points", expanded=False):
        st.markdown(
            """
            - This panel estimates five-year cloud cash demand using Year 1 OpEx, Year 1 CapEx, and annual cost growth.
            - The key decision is not only "how much will it cost," but "when do we need cost governance?"
            - Small annual changes compound over time, so cloud cost visibility should begin early.
            - Management implication: establish FinOps ownership by Year 2, track monthly variance, and trigger reviews when spend exceeds forecast.
            """
        )
    with st.expander("Assumptions used", expanded=False):
        st.markdown(
            """
            - Defaults start from Year 1 OpEx and CapEx with a shared annual growth rate.
            - Sliders control Year 1 spend levels and the yearly change percentage.
            - Output shows annual and cumulative five-year cash demand.
            - This is a planning model; it does not capture vendor contracts or one-time shocks.
            """
        )

    c1, c2, c3 = st.columns(3)
    with c1:
        y1_opex = money_input(
            "Year 1 OpEx ($)",
            key=f"{kp}y1_opex",
            value=2_400_000,
            min_value=0,
            max_value=50_000_000,
            step=50_000,
        )
    with c2:
        y1_capex = money_input(
            "Year 1 CapEx ($)",
            key=f"{kp}y1_capex",
            value=3_200_000,
            min_value=0,
            max_value=50_000_000,
            step=50_000,
        )
    with c3:
        annual_change_pct = st.slider("Annual change (both OpEx & CapEx) %", -20.0, 40.0, 8.0, 0.5, key=f"{kp}chg")

    years = np.arange(1, 6)
    g = 1.0 + annual_change_pct / 100.0
    opex = [y1_opex * (g ** (y - 1)) for y in years]
    capex = [y1_capex * (g ** (y - 1)) for y in years]
    total = [o + c for o, c in zip(opex, capex)]

    cumulative_cash = np.cumsum(total)
    df = pd.DataFrame({"Year": years, "OpEx": opex, "CapEx": capex, "Total cash": total, "Cumulative cash": cumulative_cash})

    m1, m2, m3 = st.columns(3)
    m1.metric("5-year total cash demand", f"${sum(total):,.0f}")
    m2.metric("Year 5 run-rate total", f"${total[-1]:,.0f}")
    growth_pct = ((total[-1] / total[0]) - 1.0) * 100.0 if total[0] else 0.0
    m3.metric("Year 1 to Year 5 growth", f"{growth_pct:.1f}%")

    df_disp = pretty_columns(df)
    tbl = df_disp.style.format(
        {"OpEx": "${:,.0f}", "CapEx": "${:,.0f}", "Total cash": "${:,.0f}", "Cumulative cash": "${:,.0f}"}
    ).set_table_styles(
        [
            {"selector": "th", "props": [("color", "#111827"), ("background-color", "#fdf2f4"), ("border", "1px solid #111827")]},
            {"selector": "td", "props": [("color", "#111827"), ("background-color", "#ffffff"), ("border", "1px solid #111827")]},
        ]
    )
    if presentation_mode:
        with st.expander("View detailed table", expanded=False):
            st.table(tbl)
            dataframe_download(df_disp, "panel1_budget_projection.csv")
    else:
        st.table(tbl)
        dataframe_download(df_disp, "panel1_budget_projection.csv")
    executive_insight(
        "Cloud spend should be managed as a portfolio, not as isolated infrastructure cost. Early FinOps guardrails prevent reactive optimization later."
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(y=df["Year"], x=df["OpEx"], name="OpEx", orientation="h", marker_color=CRIMSON_PRIMARY))
    fig.add_trace(go.Bar(y=df["Year"], x=df["CapEx"], name="CapEx", orientation="h", marker_color="#94a3b8"))
    fig.update_layout(
        barmode="stack",
        title="Annual cloud cash outlay",
        xaxis_title="Spend ($)",
        yaxis_title="Year",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_yaxes(tickmode="linear", dtick=1, autorange="reversed")
    apply_crimson_layout(fig, height=380)
    st.plotly_chart(fig, use_container_width=True)
    chart_caption("Small annual growth changes compound quickly across the five-year horizon.")


if __name__ == "__main__":
    st.set_page_config(page_title="Panel 1 — Budget", layout="wide")
    st.title("Crimson 5 Energy — Panel 1")
    render()

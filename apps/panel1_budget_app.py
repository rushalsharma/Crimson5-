"""Panel 1: 5-year OpEx / CapEx projection with cash-flow table and chart ($ vs year)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from _shared import CRIMSON_PRIMARY, apply_crimson_layout, money_input, pretty_columns


def render(key_prefix: str = "p1_") -> None:
    kp = key_prefix
    st.markdown("### Panel 1 — Budget Planning & Cost Estimation")
    st.caption("FinOps-style 5-year view: Year-1 OpEx/CapEx + annual change % (NIST-aligned CAPEX→OPEX shift).")

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

    df = pd.DataFrame({"Year": years, "OpEx": opex, "CapEx": capex, "Total cash": total})

    df_disp = pretty_columns(df)
    tbl = df_disp.style.format({"OpEx": "${:,.0f}", "CapEx": "${:,.0f}", "Total cash": "${:,.0f}"}).set_table_styles(
        [
            {"selector": "th", "props": [("color", "#111827"), ("background-color", "#fdf2f4"), ("border", "1px solid #111827")]},
            {"selector": "td", "props": [("color", "#111827"), ("background-color", "#ffffff"), ("border", "1px solid #111827")]},
        ]
    )
    st.table(tbl)

    fig = go.Figure()
    fig.add_trace(go.Bar(y=df["Year"], x=df["OpEx"], name="OpEx", orientation="h", marker_color=CRIMSON_PRIMARY))
    fig.add_trace(go.Bar(y=df["Year"], x=df["CapEx"], name="CapEx", orientation="h", marker_color="#94a3b8"))
    fig.update_layout(barmode="stack", title="Cash flow ($) by year (X: $, Y: Year)", xaxis_title="USD", yaxis_title="Year")
    fig.update_yaxes(tickmode="linear", dtick=1, autorange="reversed")
    apply_crimson_layout(fig, height=380)
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    st.set_page_config(page_title="Panel 1 — Budget", layout="wide")
    st.title("Crimson 5 Energy — Panel 1")
    render()

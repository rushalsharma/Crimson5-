"""Panel 6: Uptime vs cost — redundancy level and single vs multi-region."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from _shared import CRIMSON_PRIMARY, apply_crimson_layout, chart_caption, executive_insight, page_header


def render(key_prefix: str = "p6_") -> None:
    kp = key_prefix
    page_header(
        title="Resilience Design",
        subtitle="Compare availability gains against non-linear resilience cost.",
        badge="Operations",
    )
    with st.expander("Presenter talking points", expanded=False):
        st.markdown(
            """
            - This panel models the tradeoff between redundancy, multi-region architecture, uptime, and cost.
            - Availability improves with more resilience, but cost increases non-linearly.
            - The goal is not maximum resilience everywhere, but right-sized resilience for each workload tier.
            - Management implication: use SLA tiers to decide where multi-region or higher redundancy is justified.
            """
        )
    with st.expander("Assumptions used", expanded=False):
        st.markdown(
            """
            - Defaults assume redundancy level 4 with multi-region enabled.
            - Sliders control redundancy level and multi-region architecture.
            - Output compares estimated availability with monthly resilience spend.
            - This simplified resilience model is not a real SLA calculator, but helps compare cost-resilience tradeoffs.
            """
        )

    redundancy = st.slider("Redundancy level (1–5)", 1, 5, 4, key=f"{kp}red")
    multi_region = st.toggle("Multi-region active/active", value=True, key=f"{kp}mr")

    uptime = 99.5 + (redundancy - 1) * 0.09
    if multi_region:
        uptime += 0.04
    uptime = min(99.995, uptime)

    base = 18_000.0
    monthly_cost = base * (redundancy**1.85) * (1.45 if multi_region else 1.0)

    c1, c2 = st.columns(2)
    c1.metric("Modeled monthly resilience spend", f"${monthly_cost:,.0f}")
    c2.metric("Estimated availability", f"{uptime:.3f}%")

    levels = list(range(1, 6))
    costs = [base * (r**1.85) * (1.45 if multi_region else 1.0) for r in levels]
    uptimes = [min(99.995, 99.5 + (r - 1) * 0.09 + (0.04 if multi_region else 0)) for r in levels]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=costs, y=uptimes, mode="lines+markers", line=dict(color=CRIMSON_PRIMARY, width=2), name="Cost vs uptime"))
    fig.add_trace(
        go.Scatter(
            x=[monthly_cost],
            y=[uptime],
            mode="markers",
            marker=dict(size=16, color="#dc2626", symbol="star"),
            name="Current selection",
        )
    )
    fig.update_layout(
        title="Availability vs monthly resilience cost",
        xaxis_title="Monthly resilience spend ($)",
        yaxis_title="Availability (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    apply_crimson_layout(fig)
    st.plotly_chart(fig, use_container_width=True)
    chart_caption("Higher redundancy improves availability, but cost rises faster than uptime.")
    executive_insight("Resilience has a non-linear cost curve; the right design balances availability needs with financial discipline.")

if __name__ == "__main__":
    st.set_page_config(page_title="Panel 6 — Resilience", layout="wide")
    st.title("Crimson 5 Energy — Panel 6")
    render()

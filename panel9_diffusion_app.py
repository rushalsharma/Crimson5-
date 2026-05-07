"""Panel 9: Bass / Rogers-style diffusion — marketing %, network effect, B2B vs B2C."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from _shared import CRIMSON_PRIMARY, apply_crimson_layout, chart_caption, executive_insight, page_header


def render(key_prefix: str = "p9_") -> None:
    kp = key_prefix
    page_header(
        title="Market Diffusion",
        subtitle="Simulate market adoption under marketing intensity and network effects.",
        badge="Market",
    )
    with st.expander("Presenter talking points", expanded=False):
        st.markdown(
            """
            - This panel models how marketing intensity and network effects influence adoption over time.
            - Adoption often follows an S-curve: slow at first, faster as momentum builds, then eventually stabilizing.
            - Internal cloud capability can support market growth, but go-to-market execution still matters.
            - Management implication: scaling digital products requires both technical readiness and market activation.
            """
        )
    with st.expander("Assumptions used", expanded=False):
        st.markdown(
            """
            - Defaults use moderate marketing intensity and network effect strength.
            - Sliders control marketing, network effects, and market segment.
            - Output shows expected cumulative adoption over time.
            - This is a simplified diffusion model and not a sales forecast.
            """
        )

    marketing = st.slider("Marketing intensity (% of YoY GTM budget)", 0, 100, 35, key=f"{kp}mkt")
    network = st.slider("Network effect strength (0–1)", 0.0, 1.0, 0.55, 0.05, key=f"{kp}net")
    market = st.selectbox("Market segment", ["B2B (utilities)", "B2C (prosumers)"], key=f"{kp}seg")

    years = np.arange(0, 11)
    p = 0.008 + marketing / 6000
    q = 0.28 + network * 0.75
    if "B2C" in market:
        q += 0.12
    F = np.zeros(len(years))
    for i in range(1, len(years)):
        F[i] = F[i - 1] + (p + q * F[i - 1]) * (1 - F[i - 1])
    adopters = np.clip(F * 100, 0, 100)

    fig = go.Figure(
        go.Scatter(x=years, y=adopters, mode="lines", fill="tozeroy", line=dict(color=CRIMSON_PRIMARY, width=2), name="Cumulative adoption %")
    )
    fig.update_layout(
        title="Market adoption S-curve",
        xaxis_title="Year",
        yaxis_title="Market adoption (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    apply_crimson_layout(fig)
    st.plotly_chart(fig, use_container_width=True)
    chart_caption("Network effects and marketing intensity together determine how quickly adoption compounds.")
    executive_insight("Market diffusion depends on both go-to-market intensity and network effects; adoption is rarely linear.")

if __name__ == "__main__":
    st.set_page_config(page_title="Panel 9 — Diffusion", layout="wide")
    st.title("Crimson 5 Energy — Panel 9")
    render()

"""Panel 9: Bass / Rogers-style diffusion — marketing %, network effect, B2B vs B2C."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from _shared import CRIMSON_PRIMARY, apply_crimson_layout


def render(key_prefix: str = "p9_") -> None:
    kp = key_prefix
    st.markdown("### Panel 9 — Product Diffusion & Market Strategy")
    st.caption("Rogers DOI + Bass-style S-curve; network effects accelerate adoption.")

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
    fig.update_layout(title="S-curve adoption (%)", xaxis_title="Year", yaxis_title="Market adoption %")
    apply_crimson_layout(fig)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Panel 9 — Diffusion", layout="wide")
    st.title("Crimson 5 Energy — Panel 9")
    render()

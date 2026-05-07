"""Panel 8: Adoption vs training hours, leadership engagement, resistance index."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from _shared import CRIMSON_PRIMARY, apply_crimson_layout


def render(key_prefix: str = "p8_") -> None:
    kp = key_prefix
    st.markdown("### Panel 8 — Org Change & Adoption")
    st.caption("Kotter + Edmondson + Davis TAM: training and sponsorship accelerate adoption; resistance decays with leadership.")

    training_h = st.slider("Training hours / employee (0–40)", 0, 40, 28, key=f"{kp}tr")
    leadership = st.slider("Leadership engagement (%)", 0, 100, 72, key=f"{kp}ld")
    years = st.slider("Horizon (years)", 0, 10, 5, key=f"{kp}yr")

    t = np.arange(0, years + 1)
    resistance = 0.55 * np.exp(-0.12 * t) * (1.1 - leadership / 130)
    adoption = (1 - np.exp(-0.08 * training_h * (t / max(years, 1)))) * (0.35 + 0.65 * leadership / 100) * (1 - 0.35 * resistance)
    adoption = np.clip(adoption, 0, 1) * 100

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=t,
            y=adoption,
            name="Adoption %",
            mode="lines+markers",
            line=dict(color=CRIMSON_PRIMARY, width=2),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=t,
            y=resistance * 100,
            name="Resistance index",
            mode="lines",
            line=dict(color="#64748b", dash="dash"),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title="Adoption vs time (with resistance index)",
        xaxis_title="Year",
    )
    fig.update_yaxes(title_text="Adoption %", range=[0, 105], secondary_y=False)
    fig.update_yaxes(title_text="Resistance index", range=[0, 100], showgrid=False, secondary_y=True)
    apply_crimson_layout(fig)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Panel 8 — Adoption", layout="wide")
    st.title("Crimson 5 Energy — Panel 8")
    render()

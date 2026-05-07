"""Panel 7 (worksheet): AI investment vs data quality → ROI curve with under/over zones."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from _shared import CRIMSON_PRIMARY, apply_crimson_layout


def _roi_curve(ai_k: float, dq: float) -> np.ndarray:
    """Vectorized ROI % as function of AI spend (0..500k grid)."""
    x = np.linspace(0, 500_000, 120)
    # Plateauing benefit: dq scales asymptote; ai spend has diminishing returns
    asymptote = 35 + 40 * (dq / 100) ** 1.2
    roi = asymptote * (1 - np.exp(-x / 180_000)) - (x / 50_000) * 2.5
    return x, roi


def render(key_prefix: str = "p7_") -> None:
    kp = key_prefix
    st.markdown("### Panel 7 — Innovation & AI Integration (ROI Explorer)")
    st.caption("Sensitivity of ROI % to AI investment and data quality; color zones for under / balanced / over-investment.")

    ai_invest = st.slider("AI investment ($)", 0, 500_000, 220_000, 5_000, key=f"{kp}ai")
    data_quality = st.slider("Data quality (%)", 0, 100, 78, key=f"{kp}dq")

    xs, rois = _roi_curve(ai_invest, data_quality)
    current_roi = float(np.interp(ai_invest, xs, rois))

    zone = "Under-invest" if current_roi < 12 else ("Over-invest" if ai_invest > 320_000 and current_roi < rois.max() * 0.92 else "Balanced")

    st.metric("Estimated ROI % at selected investment", f"{current_roi:.1f}%", delta=zone)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=rois, mode="lines", name="ROI curve", line=dict(color=CRIMSON_PRIMARY, width=3)))
    # Zones: simple vertical bands
    fig.add_vrect(x0=0, x1=120_000, fillcolor="rgba(220,38,38,0.12)", layer="below", line_width=0, annotation_text="Under", annotation_position="top left")
    fig.add_vrect(x0=120_000, x1=320_000, fillcolor="rgba(22,163,74,0.12)", layer="below", line_width=0, annotation_text="Balanced", annotation_position="top")
    fig.add_vrect(x1=500_000, x0=320_000, fillcolor="rgba(234,179,8,0.12)", layer="below", line_width=0, annotation_text="Over", annotation_position="top right")
    fig.add_trace(
        go.Scatter(
            x=[ai_invest],
            y=[current_roi],
            mode="markers",
            marker=dict(size=14, color="#0f172a"),
            name="Selection",
        )
    )
    fig.update_layout(title="ROI % vs AI investment ($)", xaxis_title="AI investment ($)", yaxis_title="ROI %")
    apply_crimson_layout(fig)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        """
        <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:8px;">
          <span><span style="display:inline-block;width:12px;height:12px;background:rgba(220,38,38,0.35);border-radius:2px;margin-right:6px;"></span>Under-investment zone</span>
          <span><span style="display:inline-block;width:12px;height:12px;background:rgba(22,163,74,0.35);border-radius:2px;margin-right:6px;"></span>Balanced zone</span>
          <span><span style="display:inline-block;width:12px;height:12px;background:rgba(234,179,8,0.35);border-radius:2px;margin-right:6px;"></span>Over-investment zone</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    st.set_page_config(page_title="Panel 7 — AI ROI", layout="wide")
    st.title("Crimson 5 Energy — Panel 7")
    render()

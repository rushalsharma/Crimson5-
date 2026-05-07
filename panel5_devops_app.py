"""Panel 5: CI/CD efficiency — automation % and team size vs deploy frequency & failure rate."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from _shared import CRIMSON_PRIMARY, apply_crimson_layout, chart_caption, executive_insight, page_header, status_pill


def render(key_prefix: str = "p5_") -> None:
    kp = key_prefix
    page_header(
        title="DevOps Roadmap",
        subtitle="Simulate how automation and team capacity affect delivery performance.",
        badge="Operations",
    )
    with st.expander("Presenter talking points", expanded=False):
        st.markdown(
            """
            - This panel shows how automation and team capacity affect delivery performance.
            - Higher automation can improve deployment frequency, but change failure rate must remain visible.
            - Cloud transformation only creates value when teams can deliver faster and more reliably.
            - Management implication: invest in automation, but track reliability metrics alongside speed.
            """
        )
    with st.expander("Assumptions used", expanded=False):
        st.markdown(
            """
            - Defaults start from baseline deploy frequency and change failure rate.
            - Sliders control automation level and platform team size.
            - Output shows modeled deployment throughput, failure risk, and health status.
            - This is a simplified performance model, not a full DORA benchmark.
            """
        )

    automation = st.slider("Pipeline automation %", 0, 100, 72, key=f"{kp}auto")
    team_size = st.slider("Platform team size (FTE)", 1, 40, 12, key=f"{kp}team")

    base_deploy_per_week = 2.0
    base_fail_pct = 18.0

    deploy_freq = base_deploy_per_week * (1 + automation / 100.0 * 1.2) * np.sqrt(team_size / 8.0)
    fail_rate = max(2.0, base_fail_pct * (1 - automation / 100.0 * 0.55) * (1.05 if team_size < 6 else 0.92))

    deploy_delta = deploy_freq - base_deploy_per_week
    fail_delta = fail_rate - base_fail_pct
    health = "Green" if fail_rate < 10 else ("Yellow" if fail_rate <= 19 else "Red")
    status_pill("Delivery status", health)
    status_color = {"Green": "#16a34a", "Yellow": "#ca8a04", "Red": "#dc2626"}[health]
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:10px;margin:8px 0 12px 0;">
          <span style="display:inline-block;width:14px;height:14px;background:{status_color};border-radius:2px;"></span>
          <span><b>Health Status:</b> <span style="font-weight:700;color:{status_color};">{health}</span></span>
          <span>— deploys/week <b>{deploy_freq:.1f}</b> (<b>{deploy_delta:+.1f}</b> from baseline), failure rate <b>{fail_rate:.1f}%</b> (<b>{fail_delta:+.1f}%</b> from baseline)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:8px;">
          <span><span style="display:inline-block;width:12px;height:12px;background:#16a34a;border-radius:2px;margin-right:6px;"></span>Green (&lt;10% failure)</span>
          <span><span style="display:inline-block;width:12px;height:12px;background:#ca8a04;border-radius:2px;margin-right:6px;"></span>Yellow (11–19% failure)</span>
          <span><span style="display:inline-block;width:12px;height:12px;background:#dc2626;border-radius:2px;margin-right:6px;"></span>Red (&gt;20% failure)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = pd.DataFrame(
        {
            "Metric": ["Deploy frequency (/wk)", "Change failure rate (%)"],
            "Value": [deploy_freq, fail_rate],
        }
    )
    fig = go.Figure(
        go.Bar(
            x=df["Metric"],
            y=df["Value"],
            marker_color=[CRIMSON_PRIMARY, "#64748b"],
            text=[f"{deploy_freq:.1f}", f"{fail_rate:.1f}%"],
            textposition="inside",
            textfont=dict(color="#ffffff", size=14),
        )
    )
    fig.update_layout(
        title="DevOps performance snapshot",
        xaxis_title="Metric",
        yaxis_title="Value",
        yaxis=dict(range=[0, max(df["Value"]) * 1.30]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    apply_crimson_layout(fig, height=460)
    st.plotly_chart(fig, use_container_width=True)
    chart_caption("Throughput improves with automation, but change failure rate must stay visible.")
    executive_insight(
        "Automation improves deployment throughput, but reliability must remain visible through change failure rate."
    )


if __name__ == "__main__":
    st.set_page_config(page_title="Panel 5 — DevOps", layout="wide")
    st.title("Crimson 5 Energy — Panel 5")
    render()

"""Panel 4: Governance refinement — SLA matrix + decision flow (Mermaid)."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from _shared import chart_caption, executive_insight, page_header, section_card


DECISION_FLOW = """
flowchart LR
    req[Change request] --> tier{Workload tier}
    tier -->|Tier1 BES| cab[CAB + CIP evidence]
    tier -->|Tier2| std[Standard change path]
    tier -->|Tier3| auto[Automated pipeline]
    cab --> deploy[Controlled deploy]
    std --> deploy
    auto --> deploy
"""


def render(key_prefix: str = "p4_") -> None:
    _ = key_prefix
    presentation_mode = bool(st.session_state.get("presentation_mode", False))
    page_header(
        title="SLA & Decision Rights",
        subtitle="Align service levels and change controls to workload criticality.",
        badge="Governance",
    )
    with st.expander("Presenter talking points", expanded=False):
        st.markdown(
            """
            - This panel translates governance into operational service levels.
            - Different workloads require different availability, response, RTO, and RPO targets.
            - Tiered SLAs help avoid overengineering low-risk systems while protecting mission-critical workloads.
            - Management implication: resilience spending should be aligned to workload criticality.
            """
        )
    with st.expander("Assumptions used", expanded=False):
        st.markdown(
            """
            - Defaults use three workload tiers with different SLA and recovery targets.
            - There are no sliders; this panel shows policy structure and change routing.
            - Output represents how controls scale by workload criticality.
            - This is not a legal SLA document; use it as an operating baseline.
            """
        )
    section_card("Operating intent", "Align controls to workload criticality so decision rights and evidence scale with risk.")

    sla_md = """
| Tier | Availability target | Incident P1 response | RTO | RPO |
|------|---------------------|------------------------|-----|-----|
| **Tier 1 — BES-critical** | 99.95% | 15 min | 4 h | 1 h |
| **Tier 2 — Customer / market** | 99.9% | 30 min | 8 h | 4 h |
| **Tier 3 — Dev / analytics** | 99.5% | 4 h | 24 h | 24 h |
"""
    if presentation_mode:
        with st.expander("View detailed table", expanded=False):
            st.markdown(sla_md)
    else:
        st.markdown(sla_md)

    st.subheader("Decision structure (Mermaid)")
    components.html(
        f"""
        <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
        </script>
        <pre class="mermaid">{DECISION_FLOW}</pre>
        """,
        height=320,
    )
    chart_caption("Tiering routes changes into the right controls (CAB/CIP evidence vs standard vs automated).")
    executive_insight("Tiered SLAs prevent overengineering while preserving resilience for mission-critical utility workloads.")


if __name__ == "__main__":
    st.set_page_config(page_title="Panel 4 — SLA", layout="wide")
    st.title("Crimson 5 Energy — Panel 4")
    render()

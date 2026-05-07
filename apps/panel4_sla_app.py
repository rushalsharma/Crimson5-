"""Panel 4: Governance refinement — SLA matrix + decision flow (Mermaid)."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components


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
    st.markdown("### Panel 4 — Governance Model Refinement & SLA")
    st.caption("Tiered SLAs: availability, incident response, RTO/RPO — Class 10 SLA template structure.")

    st.markdown(
        """
| Tier | Availability target | Incident P1 response | RTO | RPO |
|------|---------------------|------------------------|-----|-----|
| **Tier 1 — BES-critical** | 99.95% | 15 min | 4 h | 1 h |
| **Tier 2 — Customer / market** | 99.9% | 30 min | 8 h | 4 h |
| **Tier 3 — Dev / analytics** | 99.5% | 4 h | 24 h | 24 h |
"""
    )

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


if __name__ == "__main__":
    st.set_page_config(page_title="Panel 4 — SLA", layout="wide")
    st.title("Crimson 5 Energy — Panel 4")
    render()

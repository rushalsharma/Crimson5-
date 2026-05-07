"""Panel 3: Governance & compliance — org chart (Mermaid) + RACI summary."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from _shared import chart_caption, executive_insight, page_header, section_card


MERMAID = """
flowchart TB
    subgraph exec [Executive]
        CEO[CIO / CTO Steering]
        CRO[Chief Risk & Compliance]
    end
    subgraph boards [Governance Boards]
        CSC[Cloud Steering Committee]
        ARC[Architecture Review Board]
        SEC[Security & CIP Council]
    end
    subgraph delivery [Execution]
        COE[Cloud Center of Excellence]
        PLAT[Platform Engineering]
        APP[App Teams / Grid Ops]
    end
    CEO --> CSC
    CRO --> SEC
    CSC --> ARC
    CSC --> COE
    ARC --> PLAT
    SEC --> PLAT
    COE --> PLAT
    PLAT --> APP
"""


def render(key_prefix: str = "p3_") -> None:
    _ = key_prefix
    presentation_mode = bool(st.session_state.get("presentation_mode", False))
    page_header(
        title="Governance & Compliance",
        subtitle="Define decision rights, accountability, and compliance evidence pathways.",
        badge="Governance",
    )
    with st.expander("Presenter talking points", expanded=False):
        st.markdown(
            """
            - This panel defines who owns cloud decisions, architecture, security, compliance, and FinOps.
            - The RACI model clarifies accountability across executive leadership, CISO, enterprise architecture, Cloud COE, and platform engineering.
            - Governance is not just control; it prevents fragmented decision-making as cloud adoption scales.
            - Management implication: evidence collection and compliance ownership should be continuous, not audit-driven at the end.
            """
        )
    with st.expander("Assumptions used", expanded=False):
        st.markdown(
            """
            - Defaults use a standard utility governance structure and common compliance frameworks.
            - There are no sliders; this panel is a decision-rights reference model.
            - Output highlights accountability mapping and organizational flow.
            - This is a template view and should be tailored to your actual org chart.
            """
        )

    section_card("RACI summary", "A=Accountable, R=Responsible, C=Consulted, I=Informed")
    raci_md = """
| Role | Cloud strategy | Security/CIP | Architecture | FinOps |
|------|------------------|--------------|--------------|--------|
| **CIO / Steering** | A | C | C | A |
| **CISO** | C | A | C | I |
| **EA Lead** | C | C | A | C |
| **Cloud COE** | R | C | R | R |
| **Platform Eng** | R | R | R | R |
"""
    if presentation_mode:
        with st.expander("View detailed table", expanded=False):
            st.markdown(raci_md)
    else:
        st.markdown(raci_md)

    st.subheader("Organizational chart (Mermaid)")
    components.html(
        f"""
        <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
        </script>
        <pre class="mermaid">{MERMAID}</pre>
        """,
        height=620,
        scrolling=False,
    )
    chart_caption("Decision-rights structure connects steering, risk, and execution teams with clear escalation paths.")
    executive_insight("Clear accountability and evidence pathways reduce compliance friction during scale-up.")


if __name__ == "__main__":
    st.set_page_config(page_title="Panel 3 — Governance", layout="wide")
    st.title("Crimson 5 Energy — Panel 3")
    render()

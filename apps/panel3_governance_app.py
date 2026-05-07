"""Panel 3: Governance & compliance — org chart (Mermaid) + RACI summary."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components


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
    st.markdown("### Panel 3 — Governance & Compliance")
    st.caption("Weill & Ross decision rights + SOC 2 / ISO 27001 / GDPR / NERC CIP alignment.")

    st.markdown(
        """
| Role | Cloud strategy | Security/CIP | Architecture | FinOps |
|------|------------------|--------------|--------------|--------|
| **CIO / Steering** | A | C | C | A |
| **CISO** | C | A | C | I |
| **EA Lead** | C | C | A | C |
| **Cloud COE** | R | C | R | R |
| **Platform Eng** | R | R | R | R |

*A=Accountable, R=Responsible, C=Consulted, I=Informed*
"""
    )

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


if __name__ == "__main__":
    st.set_page_config(page_title="Panel 3 — Governance", layout="wide")
    st.title("Crimson 5 Energy — Panel 3")
    render()

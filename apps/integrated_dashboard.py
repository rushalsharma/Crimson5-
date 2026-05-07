"""
Crimson 5 Energy — Integrated Cloud Simulation Portfolio (Section 12).
Run from repo root:  streamlit run apps/integrated_dashboard.py
"""

from __future__ import annotations

import streamlit as st

# Script directory must be import root for panel modules
import main_capstone_app
import panel1_budget_app
import panel2_roi_app
import panel3_governance_app
import panel4_sla_app
import panel5_devops_app
import panel6_resilience_app
import panel7_ai_roi_app
import panel8_adoption_app
import panel9_diffusion_app
import cloud_cost_panel_app

from _shared import apply_streamlit_theme, kpi_row


def render(key_prefix: str = "", *, use_sidebar: bool = True) -> None:
    """Render the integrated dashboard from the root app.

    The root app passes a key prefix and sidebar flag for consistency with other panel apps.
    """
    # The integrated dashboard currently always uses the sidebar menu layout.
    main()


def main() -> None:
    st.set_page_config(page_title="Crimson 5 Energy — Integrated Dashboard", layout="wide")
    apply_streamlit_theme()

    menu = st.sidebar.radio(
        "Menu",
        [
            "Main page",
            "Panel 1 Budget",
            "Panel 2 ROI",
            "Panel 3 Governance",
            "Panel 4 SLA",
            "Panel 5 DevOps",
            "Panel 6 Resilience",
            "Panel 7 AI ROI",
            "Panel 8 Adoption",
            "Panel 9 Diffusion",
            "Cloud Cost Management Panel",
            "FinOps Insights Panel",
            "Main demo",
        ],
        index=0,
    )

    if menu == "Main page":
        st.title("Crimson 5 Energy — Integrated Dashboard")
        st.markdown("**Integrated Cloud Simulation Portfolio** · E-176 Capstone · Panels 1–9 + main demo")
        st.markdown("##### Summary metrics (illustrative defaults from each panel model)")
        kpi_row(
            [
                ("Panel 2 — ROI (Y5, model)", "~35–45%", "vs Y1 invest"),
                ("Panel 6 — Uptime (default sliders)", "~99.9%", "tiered design"),
                ("Panel 8 — Adoption @ 12 mo", "~70–85%", "training + sponsors"),
            ]
        )
        st.info("Use the left menu to open each panel.")
    elif menu == "Panel 1 Budget":
        st.title("Panel 1 — Budget Planning & Cost Estimation")
        panel1_budget_app.render(key_prefix="int_p1_")
    elif menu == "Panel 2 ROI":
        st.title("Panel 2 — ROI & Value Analysis")
        panel2_roi_app.render(key_prefix="int_p2_")
    elif menu == "Panel 3 Governance":
        st.title("Panel 3 — Governance & Compliance")
        panel3_governance_app.render(key_prefix="int_p3_")
    elif menu == "Panel 4 SLA":
        st.title("Panel 4 — Governance Model & SLA")
        panel4_sla_app.render(key_prefix="int_p4_")
    elif menu == "Panel 5 DevOps":
        st.title("Panel 5 — Implementation Roadmap & DevOps")
        panel5_devops_app.render(key_prefix="int_p5_")
    elif menu == "Panel 6 Resilience":
        st.title("Panel 6 — Performance & Resilience Design")
        panel6_resilience_app.render(key_prefix="int_p6_")
    elif menu == "Panel 7 AI ROI":
        st.title("Panel 7 — Innovation & AI Integration")
        panel7_ai_roi_app.render(key_prefix="int_p7_")
    elif menu == "Panel 8 Adoption":
        st.title("Panel 8 — Organizational Change & Adoption")
        panel8_adoption_app.render(key_prefix="int_p8_")
    elif menu == "Panel 9 Diffusion":
        st.title("Panel 9 — Product Diffusion & Market Strategy")
        panel9_diffusion_app.render(key_prefix="int_p9_")
    elif menu == "Cloud Cost Management Panel":
        st.title("Cloud Cost Management Panel")
        cloud_cost_panel_app.render(key_prefix="int_cc_")
    elif menu == "FinOps Insights Panel":
        st.title("FinOps Insights Panel")
        cloud_cost_panel_app.render_finops(key_prefix="int_fi_")
    elif menu == "Main demo":
        st.title("Main Demo — AI Investments vs US New Business Apps")
        main_capstone_app.render(key_prefix="int_mc_", use_sidebar=False)


if __name__ == "__main__":
    main()

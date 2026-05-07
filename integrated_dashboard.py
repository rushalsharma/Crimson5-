"""
Crimson 5 Energy — Integrated Cloud Simulation Portfolio (Section 12).
Run from repo root:  streamlit run apps/integrated_dashboard.py
"""

from __future__ import annotations

import pandas as pd
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

from _shared import apply_streamlit_theme, executive_insight, kpi_row, section_card


def main() -> None:
    st.set_page_config(page_title="Crimson 5 Energy — Integrated Dashboard", layout="wide", initial_sidebar_state="expanded")
    apply_streamlit_theme()

    st.sidebar.markdown("### Crimson 5 Energy")
    st.sidebar.caption("Crimson 5 Energy · E-176 Capstone")
    st.sidebar.markdown(
        "Use this dashboard as a portfolio simulation: adjust assumptions, review risk/value tradeoffs, and interpret executive insights."
    )
    if st.sidebar.button("Reset demo defaults", use_container_width=True):
        # Reset integrated dashboard widget state (all panel prefixes use int_* keys).
        for key in list(st.session_state.keys()):
            if key.startswith("int_"):
                del st.session_state[key]
        st.session_state["c5_nav"] = "Home"
        st.session_state["presentation_mode"] = False
        st.rerun()
    st.sidebar.toggle("Presentation mode", key="presentation_mode", value=st.session_state.get("presentation_mode", False))
    nav_items = [
        "Home",
        "1. Budget Planning",
        "2. ROI & Value",
        "3. Governance & Compliance",
        "4. SLA & Decision Rights",
        "5. DevOps Roadmap",
        "6. Resilience Design",
        "7. AI ROI Explorer",
        "8. Adoption & Change",
        "9. Market Diffusion",
        "Cloud Cost Explorer",
        "FinOps Insights",
        "AI Investment Demo",
        "Executive Summary",
    ]
    menu = st.sidebar.radio(
        "Navigate",
        nav_items,
        index=0,
        key="c5_nav",
    )

    if menu == "Home":
        with st.expander("Presenter talking points", expanded=False):
            st.markdown(
                """
                - This dashboard presents Crimson 5 Energy’s cloud transformation as an integrated executive portfolio.
                - It connects financial planning, ROI, governance, operations, AI value, adoption, market growth, and FinOps.
                - The goal is not to create a production-grade calculator, but to support better executive decision-making through scenario-based simulation.
                - Use the sidebar flow to move from business case -> operating model -> innovation scale -> cost governance.
                """
            )
        st.markdown(
            """
            <div style="
              padding:18px 20px;
              border:1px solid var(--c5-border);
              border-radius:14px;
              background: linear-gradient(135deg, #fffafa 0%, #fff4f6 100%);
              margin: 6px 0 14px 0;
            ">
              <div style="font-size:31px;font-weight:900;line-height:1.15;color:var(--c5-text);">
                Crimson 5 Energy Cloud Management Simulator
              </div>
              <div style="margin-top:8px;font-size:16px;line-height:1.45;color:var(--c5-muted);max-width:1100px;">
                An integrated executive dashboard for cloud budget, ROI, governance, resilience, AI value, adoption, and market diffusion.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### How to use this dashboard")
        section_card(
            "Suggested flow",
            "Start with Budget and ROI to understand investment impact; then review Governance, SLA, DevOps, and Resilience to assess operational readiness. "
            "Use AI ROI, Adoption, and Diffusion panels to evaluate innovation and market scaling, and Cloud Cost / FinOps panels for spend visibility and optimization.",
        )
        st.markdown("##### Recommended presentation flow")
        st.markdown(
            """
            <div style="border-left:3px solid var(--c5-accent);padding-left:14px;margin-top:2px;">
              <div style="margin:8px 0;"><b>1. Budget Planning</b> — What will it cost?</div>
              <div style="margin:8px 0;"><b>2. ROI &amp; Value</b> — What value does it create?</div>
              <div style="margin:8px 0;"><b>3. Governance</b> — Who owns decisions and evidence?</div>
              <div style="margin:8px 0;"><b>4. SLA / DevOps / Resilience</b> — Can it operate safely?</div>
              <div style="margin:8px 0;"><b>5. AI ROI / Adoption / Diffusion</b> — Can it scale into innovation value?</div>
              <div style="margin:8px 0;"><b>6. Cloud Cost / FinOps</b> — How do we control and optimize spend?</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### Portfolio journey map")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                """
                <div style="padding:12px;border:1px solid var(--c5-border);border-radius:12px;background:#fff;">
                  <div style="font-weight:800;margin-bottom:6px;">Business Case</div>
                  <div style="color:var(--c5-muted);">Panels 1–2</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <div style="padding:12px;border:1px solid var(--c5-border);border-radius:12px;background:#fff;margin-top:10px;">
                  <div style="font-weight:800;margin-bottom:6px;">Growth & Adoption</div>
                  <div style="color:var(--c5-muted);">Panels 7–9</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                """
                <div style="padding:12px;border:1px solid var(--c5-border);border-radius:12px;background:#fff;">
                  <div style="font-weight:800;margin-bottom:6px;">Operating Model</div>
                  <div style="color:var(--c5-muted);">Panels 3–6</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <div style="padding:12px;border:1px solid var(--c5-border);border-radius:12px;background:#fff;margin-top:10px;">
                  <div style="font-weight:800;margin-bottom:6px;">Cost Governance</div>
                  <div style="color:var(--c5-muted);">Cloud Cost + FinOps</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div style="
              border:1px solid #f3d5db;
              background:#fdf2f4;
              border-radius:12px;
              padding:12px 14px;
              margin:8px 0;
              box-shadow:0 3px 10px rgba(17, 24, 39, 0.04);
            ">
              <div style="font-weight:800;color:#7a1123;margin-bottom:6px;">How to interpret this dashboard</div>
              <div style="color:#1f2937;line-height:1.4;">
                This dashboard uses simplified simulation models for cloud budget, ROI, governance, DevOps, resilience, AI ROI, adoption, and diffusion.
                The goal is to support executive decision-making, not replace detailed financial modeling, real AWS Cost Explorer analysis, compliance audits, or production SLA engineering.
                The models are assumption-driven and should be interpreted directionally.
                It is most useful as a portfolio view that connects financial, technical, governance, innovation, and adoption dimensions in one place.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        executive_insight(
            "The dashboard demonstrates how Crimson 5 Energy can evaluate cloud transformation as a managed portfolio: balancing financial discipline, governance, technical resilience, AI innovation, user adoption, and market growth."
        )
    elif menu == "Executive Summary":
        with st.expander("Presenter talking points", expanded=False):
            st.markdown(
                """
                - The dashboard shows cloud transformation as a managed portfolio rather than a standalone IT project.
                - Financial value depends on cost visibility, ROI discipline, governance, resilience, AI readiness, adoption, and FinOps.
                - Crimson 5 should proceed in stages, starting with governance and cost visibility before scaling advanced capabilities.
                - Final recommendation: proceed with cloud transformation, but pair it with early FinOps, clear accountability, tiered resilience, and adoption management.
                """
            )
        st.markdown("## Executive Summary")
        st.caption("One-page synthesis of financial, operational, and growth signals across the full dashboard.")
        st.markdown("##### Executive KPI snapshot")
        kpi_row(
            [
                ("5-year cloud cash demand", "~$34M", "Budget trajectory"),
                ("Year 5 ROI", "~40%", "Discounted model"),
                ("Modeled uptime", "~99.9%", "Resilience design"),
                ("Adoption maturity", "~75%", "People readiness"),
                ("AI ROI potential", "~20–30%", "Balanced investment zone"),
            ]
        )
        st.markdown("")

        # Default-model rollups (aligned to panel defaults).
        years = [1, 2, 3, 4, 5]
        annual_change_pct = 8.0
        g = 1.0 + annual_change_pct / 100.0
        y1_opex, y1_capex = 2_400_000, 3_200_000
        total_cash = [y1_opex * (g ** (y - 1)) + y1_capex * (g ** (y - 1)) for y in years]
        cash_demand_5y = sum(total_cash)

        # Panel 2 defaults.
        cost_reduction, productivity = 900_000, 600_000
        agility, trust, intangible_scale = 0.65, 0.55, 1_200_000
        investment_y1, discount = 6_000_000, 0.10
        tangible_annual = cost_reduction + productivity
        intangible_annual = (0.5 * agility + 0.5 * trust) * intangible_scale
        cumulative_net = 0.0
        roi_pct = []
        for y in years:
            ramp = min(1.0, 0.3 + 0.2 * (y - 1))
            benefit = (tangible_annual + intangible_annual) * ramp * (1.05 ** (y - 1))
            invest = investment_y1 if y == 1 else 0.0
            net = benefit - invest
            cumulative_net += net / ((1 + discount) ** (y - 1))
            roi_pct.append(100.0 * cumulative_net / investment_y1)

        # Panel 6 defaults.
        redundancy, multi_region = 4, True
        availability = min(99.995, 99.5 + (redundancy - 1) * 0.09 + (0.04 if multi_region else 0.0))

        # Panel 7 defaults.
        ai_invest_default, dq_default = 220_000, 78
        ai_asymptote = 35 + 40 * (dq_default / 100) ** 1.2
        ai_roi = ai_asymptote * (1 - (2.718281828 ** (-ai_invest_default / 180_000))) - (ai_invest_default / 50_000) * 2.5

        # Panel 8 defaults (horizon=5 years).
        import numpy as np

        training_h, leadership, horizon = 28, 72, 5
        t = np.arange(0, horizon + 1)
        resistance = 0.55 * np.exp(-0.12 * t) * (1.1 - leadership / 130)
        adoption = (1 - np.exp(-0.08 * training_h * (t / max(horizon, 1)))) * (0.35 + 0.65 * leadership / 100) * (1 - 0.35 * resistance)
        adoption_pct = float(np.clip(adoption, 0, 1)[-1] * 100)

        kpi_row(
            [
                ("Total 5-year cash demand", f"${cash_demand_5y:,.0f}", "Panel 1 defaults"),
                ("Year 5 ROI", f"{roi_pct[-1]:.1f}%", "Panel 2 defaults"),
                ("Default resilience availability", f"{availability:.3f}%", "Panel 6 defaults"),
                ("AI ROI at default investment", f"{ai_roi:.1f}%", "Panel 7 defaults"),
                ("Adoption at default horizon", f"{adoption_pct:.1f}%", "Panel 8 defaults"),
            ]
        )

        summary_df = pd.DataFrame(
            [
                {
                    "Dimension": "Financial case",
                    "Panel": "Panels 1–2",
                    "Current signal": "Cash demand rises while ROI becomes positive by later years",
                    "Management implication": "Phase investments and enforce early FinOps controls",
                },
                {
                    "Dimension": "Governance readiness",
                    "Panel": "Panels 3–4",
                    "Current signal": "Clear RACI and SLA tiering structure defined",
                    "Management implication": "Institutionalize decision rights before scale-up",
                },
                {
                    "Dimension": "Delivery readiness",
                    "Panel": "Panel 5",
                    "Current signal": "Automation can improve throughput with failure-rate risk",
                    "Management implication": "Track velocity and reliability together",
                },
                {
                    "Dimension": "Resilience posture",
                    "Panel": "Panel 6",
                    "Current signal": "Availability improves but cost grows non-linearly",
                    "Management implication": "Choose resilience tier by business criticality",
                },
                {
                    "Dimension": "Innovation value",
                    "Panel": "Panel 7",
                    "Current signal": "AI ROI sensitive to spend and data quality",
                    "Management implication": "Tie AI funding to data readiness milestones",
                },
                {
                    "Dimension": "Change adoption",
                    "Panel": "Panel 8",
                    "Current signal": "Leadership support materially accelerates adoption",
                    "Management implication": "Use sponsor-led change, not training-only plans",
                },
                {
                    "Dimension": "Market scaling",
                    "Panel": "Panel 9",
                    "Current signal": "Adoption accelerates with stronger network effects",
                    "Management implication": "Coordinate GTM intensity with ecosystem strategy",
                },
                {
                    "Dimension": "Cost accountability",
                    "Panel": "Cloud Cost / FinOps",
                    "Current signal": "Spend concentration and policy savings are visible",
                    "Management implication": "Prioritize top drivers and enforce shared ownership",
                },
            ]
        )
        st.table(summary_df)

        executive_insight(
            "Crimson 5 should proceed as a staged cloud transformation, with early FinOps governance, tiered resilience design, AI investment tied to data quality, and adoption management led by executive sponsors.",
            title="Final recommendation",
        )

    elif menu == "1. Budget Planning":
        panel1_budget_app.render(key_prefix="int_p1_")
    elif menu == "2. ROI & Value":
        panel2_roi_app.render(key_prefix="int_p2_")
    elif menu == "3. Governance & Compliance":
        panel3_governance_app.render(key_prefix="int_p3_")
    elif menu == "4. SLA & Decision Rights":
        panel4_sla_app.render(key_prefix="int_p4_")
    elif menu == "5. DevOps Roadmap":
        panel5_devops_app.render(key_prefix="int_p5_")
    elif menu == "6. Resilience Design":
        panel6_resilience_app.render(key_prefix="int_p6_")
    elif menu == "7. AI ROI Explorer":
        panel7_ai_roi_app.render(key_prefix="int_p7_")
    elif menu == "8. Adoption & Change":
        panel8_adoption_app.render(key_prefix="int_p8_")
    elif menu == "9. Market Diffusion":
        panel9_diffusion_app.render(key_prefix="int_p9_")
    elif menu == "Cloud Cost Explorer":
        cloud_cost_panel_app.render(key_prefix="int_cc_")
    elif menu == "FinOps Insights":
        cloud_cost_panel_app.render_finops(key_prefix="int_fi_")
    elif menu == "AI Investment Demo":
        main_capstone_app.render(key_prefix="int_mc_", use_sidebar=False)


if __name__ == "__main__":
    main()

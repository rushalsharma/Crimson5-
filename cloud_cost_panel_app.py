"""Cloud Cost Management and FinOps Insights panels (separate implementations)."""

from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from _shared import apply_crimson_layout, chart_caption, dataframe_download, executive_insight, page_header, pretty_columns, status_pill


def _demo_df(start: date, end: date, granularity: str, metric: str, group_by: str) -> pd.DataFrame:
    idx = (
        pd.date_range(start.replace(day=1), end, freq="MS")
        if granularity == "Monthly"
        else pd.date_range(start, end, freq="D")
    )
    rng = np.random.default_rng(42)
    base = 1300 + np.linspace(0, 550, len(idx))
    bump = 220 if metric == "AmortizedCost" else 0
    values = [
        np.clip(base + rng.normal(0, 90, len(idx)) + bump, 100, None),
        np.clip(base * 0.35 + rng.normal(0, 40, len(idx)), 40, None),
        np.clip(base * 0.22 + rng.normal(0, 30, len(idx)), 30, None),
    ]
    groups = {
        "Service": ["AmazonEC2", "AmazonS3", "AmazonRDS"],
        "Region": ["us-east-1", "us-west-2", "eu-west-1"],
        "Linked Account": ["Prod-001", "Shared-002", "Data-003"],
    }[group_by]
    rows = []
    for i, d in enumerate(idx):
        for g, arr in zip(groups, values):
            rows.append({"Date": d.date(), "Group": g, "Amount": float(arr[i])})
    return pd.DataFrame(rows)


def _cred_form(prefix: str) -> tuple[str, str, str, str]:
    with st.expander("AWS Credentials (optional)", expanded=False):
        with st.form(f"{prefix}cred_form"):
            ak = st.text_input("AWS Access Key ID", value=st.session_state.get(f"{prefix}ak", ""))
            sk = st.text_input("AWS Secret Access Key", value=st.session_state.get(f"{prefix}sk", ""), type="password")
            tk = st.text_input("AWS Session Token (optional)", value=st.session_state.get(f"{prefix}tk", ""))
            rg = st.text_input("AWS Region", value=st.session_state.get(f"{prefix}rg", "us-east-1"))
            saved = st.form_submit_button("Save credentials")
            if saved:
                st.session_state[f"{prefix}ak"] = ak
                st.session_state[f"{prefix}sk"] = sk
                st.session_state[f"{prefix}tk"] = tk
                st.session_state[f"{prefix}rg"] = rg
                st.success("Credentials saved for this session.")
    return (
        st.session_state.get(f"{prefix}ak", ""),
        st.session_state.get(f"{prefix}sk", ""),
        st.session_state.get(f"{prefix}tk", ""),
        st.session_state.get(f"{prefix}rg", "us-east-1"),
    )


def _ce_data(
    *,
    start: date,
    end: date,
    granularity: str,
    metric: str,
    group_by: str,
    creds_prefix: str,
) -> tuple[pd.DataFrame, bool]:
    ak, sk, tk, rg = _cred_form(creds_prefix)
    if not ak or not sk:
        return _demo_df(start, end, granularity, metric, group_by), True
    try:
        import boto3

        session = boto3.session.Session(
            aws_access_key_id=ak,
            aws_secret_access_key=sk,
            aws_session_token=tk or None,
            region_name=rg or "us-east-1",
        )
        ce = session.client("ce")
        key = {"Service": "SERVICE", "Region": "REGION", "Linked Account": "LINKED_ACCOUNT"}[group_by]
        resp = ce.get_cost_and_usage(
            TimePeriod={"Start": start.isoformat(), "End": (end + timedelta(days=1)).isoformat()},
            Granularity=granularity.upper(),
            Metrics=[metric],
            GroupBy=[{"Type": "DIMENSION", "Key": key}],
        )
        rows = []
        for t in resp.get("ResultsByTime", []):
            d = pd.to_datetime(t["TimePeriod"]["Start"]).date()
            for g in t.get("Groups", []):
                rows.append({"Date": d, "Group": g["Keys"][0], "Amount": float(g["Metrics"][metric]["Amount"])})
        df = pd.DataFrame(rows)
        if df.empty:
            raise RuntimeError("No CE data returned.")
        return df, False
    except Exception as e:  # noqa: BLE001
        st.warning(f"Demo Mode enabled: {e}")
        return _demo_df(start, end, granularity, metric, group_by), True


def render(key_prefix: str = "cc_") -> None:
    """Cloud Cost Management panel ONLY."""
    kp = key_prefix
    presentation_mode = bool(st.session_state.get("presentation_mode", False))
    page_header(
        title="Cloud Cost Management",
        subtitle="Explore AWS-style spend by service, region, or linked account.",
        badge="Operations",
    )
    with st.expander("Presenter talking points", expanded=False):
        st.markdown(
            """
            - This panel shows how cloud spend can be viewed by service, region, or linked account.
            - For the classroom demo, demo mode is recommended rather than entering real AWS credentials.
            - The value is showing how spend visibility supports accountability and forecasting.
            - Management implication: cloud cost should be transparent to engineering, finance, and business stakeholders.
            """
        )
    st.info("Demo mode is recommended for classroom presentation. Do not enter real AWS credentials while screen sharing.")
    with st.expander("Assumptions used", expanded=False):
        st.markdown(
            """
            - Defaults use recent dates, top-3 groups, and demo data when credentials are absent.
            - Controls adjust date range, granularity, metric, grouping, and Top-N focus.
            - Output shows spend trends and top cost drivers.
            - Demo mode is synthetic and directional, not billing-authoritative.
            """
        )

    c1, c2, c3 = st.columns(3)
    with c1:
        start = st.date_input("Date range start", date.today() - timedelta(days=90), key=f"{kp}start")
        end = st.date_input("Date range end", date.today(), key=f"{kp}end")
    with c2:
        granularity = st.selectbox("Granularity", ["Daily", "Monthly"], key=f"{kp}gran")
        metric = st.selectbox("Metric", ["UnblendedCost", "AmortizedCost"], key=f"{kp}metric")
    with c3:
        group_by = st.selectbox("Group by", ["Service", "Region", "Linked Account"], key=f"{kp}gb")
        top_n = st.slider("Top-N services/groups", 1, 10, 3, key=f"{kp}topn")

    df, demo = _ce_data(start=start, end=end, granularity=granularity, metric=metric, group_by=group_by, creds_prefix=f"{kp}cred_")
    status_pill("Mode", "Demo Mode" if demo else "Production Mode")

    grouped = df.groupby(["Date", "Group"], as_index=False)["Amount"].sum()
    ranked = grouped.groupby("Group", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)
    keep = ranked.head(top_n)["Group"].tolist()
    grouped = grouped[grouped["Group"].isin(keep)]

    fig = px.line(grouped, x="Date", y="Amount", color="Group", title=f"Cloud spend by {group_by}")
    apply_crimson_layout(fig)
    fig.update_layout(
        title=f"Cloud spend by {group_by.lower()}",
        xaxis_title="Date",
        yaxis_title="Spend ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)
    chart_caption("A small set of services or regions usually drives most cloud spend.")
    table_df = pretty_columns(ranked.rename(columns={"Group": group_by, "Amount": "TotalCost"}))
    with st.expander("View detailed table", expanded=not presentation_mode):
        st.table(
            table_df.style.format({"TotalCost": "${:,.2f}"}).set_table_styles(
                [
                    {"selector": "th", "props": [("color", "#111827"), ("background-color", "#ffffff"), ("border-bottom", "2px solid #ecd0d7")]},
                    {"selector": "td", "props": [("color", "#111827"), ("background-color", "#ffffff"), ("border-bottom", "1px solid #eceff3")]},
                ]
            )
        )
        dataframe_download(table_df, "cloud_cost_ranked_groups.csv")
    executive_insight("Cloud cost visibility is the foundation for accountability, forecasting, and optimization.")


def render_finops(key_prefix: str = "fi_") -> None:
    """FinOps Insights panel ONLY."""
    kp = key_prefix
    presentation_mode = bool(st.session_state.get("presentation_mode", False))
    page_header(
        title="FinOps Insights",
        subtitle="Translate cloud spend into actionable cost governance signals.",
        badge="Governance",
    )
    with st.expander("Presenter talking points", expanded=False):
        st.markdown(
            """
            - This panel converts cloud spend data into management signals.
            - It highlights month-over-month change, top service concentration, anomalies, and potential savings.
            - FinOps is not just about cutting cost; it is about maximizing value from technology spend.
            - Management implication: cost decisions should be shared across engineering, finance, and business teams.
            """
        )
    st.info("Demo mode is recommended for classroom presentation. Do not enter real AWS credentials while screen sharing.")
    with st.expander("Assumptions used", expanded=False):
        st.markdown(
            """
            - Defaults use monthly service-level spend with a policy savings slider.
            - Controls adjust date range, metric, and projected policy reduction.
            - Output highlights trend, concentration, anomalies, and projected savings.
            - Signals are simplified and intended for prioritization, not final budgeting.
            """
        )

    c1, c2 = st.columns(2)
    with c1:
        start = st.date_input("Date range start", date.today() - timedelta(days=180), key=f"{kp}start")
        end = st.date_input("Date range end", date.today(), key=f"{kp}end")
    with c2:
        metric = st.selectbox("Metric", ["UnblendedCost", "AmortizedCost"], key=f"{kp}metric")
        policy = st.slider("Cost-reduction policy (%)", 0, 30, 10, key=f"{kp}policy")

    # For FinOps insights, fix grouping to Service and monthly cadence.
    df, demo = _ce_data(start=start, end=end, granularity="Monthly", metric=metric, group_by="Service", creds_prefix=f"{kp}cred_")
    status_pill("Mode", "Demo Mode" if demo else "Production Mode")

    by_service = df.groupby(["Date", "Group"], as_index=False)["Amount"].sum()
    totals = by_service.groupby("Date", as_index=False)["Amount"].sum().sort_values("Date")
    totals["ProjectedAmount"] = totals["Amount"] * (1 - policy / 100.0)

    fig = px.line(by_service, x="Date", y="Amount", color="Group", title="Spend by service with projected savings")
    fig.add_scatter(
        x=totals["Date"],
        y=totals["ProjectedAmount"],
        mode="lines",
        name=f"Projected ({policy}% policy)",
        line=dict(color="#16a34a", dash="dash"),
    )
    apply_crimson_layout(fig)
    fig.update_layout(
        title="Service spend with policy projection",
        xaxis_title="Date",
        yaxis_title="Spend ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)
    chart_caption("The dashed projection shows potential savings if policy changes are sustained.")

    prev = totals["Amount"].iloc[-2] if len(totals) > 1 else np.nan
    cur = totals["Amount"].iloc[-1] if len(totals) > 0 else np.nan
    mom = ((cur - prev) / prev * 100.0) if pd.notna(prev) and prev != 0 else np.nan
    svc_totals = by_service.groupby("Group", as_index=False)["Amount"].sum().sort_values("Amount", ascending=False)
    top3 = (svc_totals.head(3)["Amount"].sum() / svc_totals["Amount"].sum() * 100.0) if not svc_totals.empty else np.nan
    z = (totals["Amount"] - totals["Amount"].mean()) / (totals["Amount"].std() if totals["Amount"].std() > 0 else 1)
    anomalies = int((z.abs() > 2.0).sum())

    m1, m2, m3 = st.columns(3)
    m1.metric("Month-over-month % change", f"{mom:.2f}%" if pd.notna(mom) else "N/A")
    m2.metric("Top-3 service concentration", f"{top3:.2f}%" if pd.notna(top3) else "N/A")
    m3.metric("Simple anomaly count", str(anomalies))
    with st.expander("View detailed table", expanded=not presentation_mode):
        detailed = pretty_columns(totals.rename(columns={"Amount": "CurrentSpend", "ProjectedAmount": "ProjectedSpend"}))
        st.table(detailed.style.format({"CurrentSpend": "${:,.2f}", "ProjectedSpend": "${:,.2f}"}))
        dataframe_download(detailed, "finops_monthly_totals.csv")
    executive_insight("FinOps turns cloud cost data into shared decisions across engineering, finance, and business teams.")


if __name__ == "__main__":
    st.set_page_config(page_title="Cloud Cost & FinOps", layout="wide")
    st.title("Crimson 5 Energy — Cloud Cost Management")
    render()

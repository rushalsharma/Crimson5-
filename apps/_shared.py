"""Shared Plotly theme and KPI helpers for Crimson 5 Energy apps."""

from __future__ import annotations

import plotly.graph_objects as go

CRIMSON_PRIMARY = "#A51C30"
CRIMSON_DARK = "#5C0E1A"
CRIMSON_ACCENT = "#F0C2C8"


def apply_streamlit_theme() -> None:
    """Apply Crimson 5 Energy light-only CSS theme."""
    import streamlit as st

    st.markdown(
        """
        <style>
          :root {
            --c5-bg: #fffdfd;
            --c5-surface: #ffffff;
            --c5-surface-soft: #fdf2f4;
            --c5-border: #f3d5db;
            --c5-accent: #a51c30;
            --c5-accent-dark: #7a1123;
            --c5-text: #111827;
            --c5-muted: #374151;
          }
          .stApp {
            background: linear-gradient(180deg, var(--c5-bg) 0%, #fff8f8 100%);
            color: var(--c5-text);
          }
          h1,h2,h3,h4,h5,h6,p,li,label,div,span {
            color: var(--c5-text) !important;
            font-size: 16px;
          }
          h1 { font-size: 2.2rem !important; }
          h2 { font-size: 1.6rem !important; }
          h3 { font-size: 1.35rem !important; }
          label, [data-testid="stWidgetLabel"] p { font-size: 15px !important; }
          input, textarea, [data-baseweb="select"] * { font-size: 15px !important; }
          [data-testid="stSidebar"] {
            background: var(--c5-surface-soft) !important;
            border-right: 1px solid var(--c5-border);
          }
          [data-testid="stSidebar"] * {
            color: var(--c5-text) !important;
          }
          [data-testid="stHeader"] { background: #ffffff !important; }
          [data-testid="stToolbar"] { background: #ffffff !important; display: none !important; }
          [data-testid="stDecoration"] { display: none !important; }
          #MainMenu { visibility: hidden; }
          [data-testid="stMetric"] {
            background: var(--c5-surface);
            border: 1px solid var(--c5-border);
            border-radius: 10px;
            padding: 8px 10px;
          }
          [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
            color: var(--c5-text) !important;
          }
          .stRadio > div, .stSelectbox > div, .stTextInput > div, .stNumberInput > div,
          .stDateInput > div, .stMultiSelect > div {
            background: var(--c5-surface) !important;
            color: var(--c5-text) !important;
          }
          .stSelectbox [data-baseweb="select"],
          .stMultiSelect [data-baseweb="select"],
          .stTextInput input, .stNumberInput input {
            background: var(--c5-surface) !important;
            color: var(--c5-text) !important;
            border: 1px solid var(--c5-border) !important;
          }
          [data-baseweb="select"] *,
          [data-baseweb="select"] input,
          [data-baseweb="select"] span,
          [data-baseweb="select"] div {
            background: #ffffff !important;
            color: #111827 !important;
          }
          [data-baseweb="select"] [class*="singleValue"],
          [data-baseweb="select"] [class*="valueContainer"],
          [data-baseweb="select"] [class*="control"],
          [data-baseweb="select"] [class*="container"] {
            background: #ffffff !important;
            color: #111827 !important;
          }
          [data-baseweb="slider"] div {
            background-color: transparent !important;
          }
          [data-baseweb="slider"] [role="slider"] {
            background-color: var(--c5-accent) !important;
            border-color: var(--c5-accent-dark) !important;
          }
          [data-baseweb="slider"] > div > div > div {
            background: #f0d3d9 !important;
          }
          [data-testid="stDataFrame"], .stTable {
            background: var(--c5-surface) !important;
            border: 1px solid var(--c5-border) !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 6px 18px rgba(122, 17, 35, 0.08) !important;
          }
          [data-testid="stDataFrame"] [role="gridcell"],
          [data-testid="stDataFrame"] [role="columnheader"],
          [data-testid="stDataFrame"] [data-testid="stDataFrameResizable"],
          [data-testid="stDataFrame"] canvas,
          .stDataFrame div, .stDataFrame span, .stDataFrame p,
          .stTable td, .stTable th {
            color: #111827 !important;
            background: #ffffff !important;
            font-size: 15px !important;
            font-weight: 500 !important;
            border-bottom: 1px solid #eceff3 !important;
          }
          .stTable table, [data-testid="stDataFrame"] table {
            border-collapse: collapse !important;
            width: 100% !important;
          }
          .stTable th, [data-testid="stDataFrame"] thead th, [data-testid="stDataFrame"] [role="columnheader"] {
            background: #ffffff !important;
            color: #111827 !important;
            font-weight: 700 !important;
            border-bottom: 2px solid #ecd0d7 !important;
          }
          .stTable tbody tr:nth-child(even) td,
          [data-testid="stDataFrame"] tbody tr:nth-child(even) td {
            background: #fafbfc !important;
          }
          .stTable tbody tr:hover td,
          [data-testid="stDataFrame"] tbody tr:hover td {
            background: #fff1f4 !important;
          }
          [data-testid="stDataFrame"] * {
            color: var(--c5-text) !important;
            background: var(--c5-surface) !important;
          }
          [data-testid="stMarkdownContainer"] table {
            background: var(--c5-surface) !important;
            color: var(--c5-text) !important;
            border-color: var(--c5-border) !important;
          }
          [data-testid="stMarkdownContainer"] table th {
            background: #ffffff !important;
            color: #111827 !important;
            border-bottom: 2px solid #ecd0d7 !important;
            border-top: none !important;
            border-left: none !important;
            border-right: none !important;
            font-weight: 700 !important;
          }
          [data-testid="stMarkdownContainer"] table td {
            background: #ffffff !important;
            color: #111827 !important;
            border-top: none !important;
            border-left: none !important;
            border-right: none !important;
            border-bottom: 1px solid #eceff3 !important;
          }
          [data-testid="stAlert"] {
            background: #fff7f8 !important;
            border: 1px solid var(--c5-border) !important;
            color: var(--c5-text) !important;
          }
          [data-testid="stCaptionContainer"], .stCaption, [data-testid="stCaptionContainer"] p {
            color: #1f2937 !important;
            font-size: 14px !important;
          }
          .stExpander {
            background: var(--c5-surface) !important;
            border: 1px solid var(--c5-border) !important;
            border-radius: 10px !important;
          }
          [data-testid="stExpander"] details summary,
          [data-testid="stExpander"] details summary * {
            background: #fff7f8 !important;
            color: #111827 !important;
          }
          [data-testid="stExpander"] details[open] summary,
          [data-testid="stExpander"] details[open] summary * {
            background: #fff1f4 !important;
            color: #111827 !important;
          }
          .stButton > button, .stDownloadButton > button {
            background: var(--c5-accent) !important;
            color: #ffffff !important;
            border: 1px solid var(--c5-accent-dark) !important;
            border-radius: 10px !important;
            font-size: 22px !important;
            font-weight: 700 !important;
            line-height: 1 !important;
            min-height: 44px !important;
            box-shadow: 0 2px 8px rgba(122, 17, 35, 0.25) !important;
            text-align: center !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
          }
          .stButton > button p, .stDownloadButton > button p {
            margin: 0 !important;
            color: #ffffff !important;
            font-size: 22px !important;
            font-weight: 800 !important;
            line-height: 1 !important;
          }
          .stForm button, .stFormSubmitButton button {
            background: var(--c5-accent) !important;
            color: #ffffff !important;
          }
          .stForm button *, .stFormSubmitButton button * {
            color: #ffffff !important;
          }
          .stButton > button:hover, .stDownloadButton > button:hover {
            background: var(--c5-accent-dark) !important;
          }
          div[role="listbox"], div[role="option"], ul[role="listbox"], li[role="option"] {
            background: #ffffff !important;
            color: #111827 !important;
          }
          [data-baseweb="popover"] * {
            background: #ffffff !important;
            color: #111827 !important;
          }
          hr {
            border-color: var(--c5-border) !important;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_crimson_layout(fig: go.Figure, height: int | None = 400) -> go.Figure:
    fg = "#111827"
    grid = "#d1d5db"
    plot_bg = "#ffffff"
    paper_bg = "#ffffff"

    fig.update_layout(
        font=dict(family="Arial, sans-serif", color=fg, size=14),
        plot_bgcolor=plot_bg,
        paper_bgcolor=paper_bg,
        title_font_color=fg,
        legend=dict(font=dict(color=fg, size=13), title=dict(font=dict(color=fg))),
        height=height,
        margin=dict(l=48, r=24, t=56, b=48),
    )
    fig.update_xaxes(
        tickfont=dict(color=fg, size=12),
        title_font=dict(color=fg, size=14),
        showgrid=True,
        gridcolor=grid,
        zerolinecolor=grid,
    )
    fig.update_yaxes(
        tickfont=dict(color=fg, size=12),
        title_font=dict(color=fg, size=14),
        showgrid=True,
        gridcolor=grid,
        zerolinecolor=grid,
    )
    return fig


def kpi_row(metrics: list[tuple[str, str, str | None]]) -> None:
    """Render a row of Streamlit metrics. Each item: (label, value, delta)."""
    import streamlit as st

    cols = st.columns(len(metrics))
    for col, (label, value, delta) in zip(cols, metrics):
        with col:
            st.metric(label, value, delta=delta)


def pretty_columns(df):
    """Return dataframe with underscore-free title-cased column headers."""
    import pandas as pd

    if not isinstance(df, pd.DataFrame):
        return df
    out = df.copy()
    out.columns = [str(c).replace("_", " ").strip() for c in out.columns]
    return out


def money_input(
    label: str,
    *,
    key: str,
    value: int,
    min_value: int = 0,
    max_value: int = 1_000_000_000,
    step: int = 1_000,
) -> int:
    """Money input with +/- buttons and comma-formatted text field."""
    import streamlit as st

    num_key = f"{key}__num"
    txt_key = f"{key}__txt"
    fmt_key = f"{key}__format_pending"
    minus_key = f"{key}__minus"
    plus_key = f"{key}__plus"

    if num_key not in st.session_state:
        st.session_state[num_key] = int(value)
    if txt_key not in st.session_state:
        st.session_state[txt_key] = f"{int(st.session_state[num_key]):,}"
    if fmt_key not in st.session_state:
        st.session_state[fmt_key] = False

    # Important: update widget value before text_input is instantiated.
    if st.session_state.get(fmt_key, False):
        st.session_state[txt_key] = f"{int(st.session_state[num_key]):,}"
        st.session_state[fmt_key] = False

    def _sync_from_text() -> None:
        raw = str(st.session_state.get(txt_key, "")).replace(",", "").strip()
        if raw in {"", "-", "+"}:
            return
        try:
            parsed = int(float(raw))
        except ValueError:
            return
        parsed = max(min_value, min(max_value, parsed))
        st.session_state[num_key] = parsed
        st.session_state[fmt_key] = True

    st.markdown(f"**{label}**")
    c1, c2, c3 = st.columns([1, 5, 1])
    with c1:
        if st.button("−", key=minus_key, use_container_width=True):
            st.session_state[num_key] = max(min_value, st.session_state[num_key] - step)
            st.session_state[fmt_key] = True
    with c2:
        st.text_input(
            label,
            key=txt_key,
            label_visibility="collapsed",
            on_change=_sync_from_text,
        )
    with c3:
        if st.button("＋", key=plus_key, use_container_width=True):
            st.session_state[num_key] = min(max_value, st.session_state[num_key] + step)
            st.session_state[fmt_key] = True

    return int(st.session_state[num_key])

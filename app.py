"""
Root entry: AI Investments vs US New Business Apps (delegates to apps.main_capstone_app).
Run: streamlit run app.py
"""

from pathlib import Path
import sys

import streamlit as st

# Ensure `apps/` is on path when launched from repo root
root_path = Path(__file__).resolve().parent
if str(root_path / "apps") not in sys.path:
    sys.path.insert(0, str(root_path / "apps"))

import integrated_dashboard  # type: ignore  # dynamic path: apps/ added above

st.set_page_config(page_title="AI Investments & US Business Apps", layout="wide")
st.title("Crimson 5 — Main Capstone Demo")
integrated_dashboard.render(key_prefix="rootapp_", use_sidebar=True)

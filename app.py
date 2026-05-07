"""
Root entry: AI Investments vs US New Business Apps (delegates to apps.main_capstone_app).
Run: streamlit run app.py
"""

from pathlib import Path
import sys

# Ensure `apps/` is on path when launched from repo root
_APPS = Path(__file__).resolve().parent / "apps"
if str(_APPS) not in sys.path:
    sys.path.insert(0, str(_APPS))

import streamlit as st

import main_capstone_app  # type: ignore  # dynamic path: apps/ added above

st.set_page_config(page_title="AI Investments & US Business Apps", layout="wide")
st.title("Crimson 5 — Main Capstone Demo")
main_capstone_app.render(key_prefix="rootapp_", use_sidebar=True)

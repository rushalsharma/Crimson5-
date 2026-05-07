@echo off
cd /d "%~dp0"
echo Starting Streamlit app...
python -m streamlit run app.py
if errorlevel 1 (
    py -m streamlit run app.py
)
if errorlevel 1 (
    streamlit run app.py
)
pause

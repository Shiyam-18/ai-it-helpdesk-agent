@echo off
setlocal
if not exist .venv\Scripts\python.exe (
    echo Virtual environment not found.
    echo Run: python -m venv .venv
    echo Then: .venv\Scripts\pip install -r requirements.txt
    exit /b 1
)
call .venv\Scripts\activate
streamlit run app.py

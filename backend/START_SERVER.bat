@echo off
echo.
echo ============================================================
echo         TruthLens - Deepfake Detection System
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Run the server
echo.
echo Starting TruthLens Backend Server...
echo.
python main.py

pause

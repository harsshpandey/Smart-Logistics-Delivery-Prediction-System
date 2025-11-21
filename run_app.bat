@echo off
REM Smart Logistics Delivery Prediction - Startup Script
REM This script activates the virtual environment and launches the Streamlit app

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Smart Logistics Delivery Prediction
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

REM Activate virtual environment
echo [1/3] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

REM Check if dependencies are installed
echo.
echo [2/3] Checking dependencies...
pip list | findstr streamlit > nul
if errorlevel 1 (
    echo [WARNING] Dependencies may not be installed
    echo Installing requirements...
    pip install -r requirements.txt
)
echo [OK] Dependencies ready

REM Launch Streamlit app
echo.
echo [3/3] Launching application...
echo.
echo ========================================
echo App is running at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo ========================================
echo.

streamlit run app/streamlit_app.py

pause

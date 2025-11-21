# Smart Logistics Delivery Prediction - PowerShell Startup Script
# Usage: ./run_app.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Smart Logistics Delivery Prediction" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
  Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
  Write-Host "Please run: python -m venv .venv" -ForegroundColor Yellow
  Read-Host "Press Enter to exit"
  exit 1
}

# Activate virtual environment
Write-Host "[1/3] Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "[OK] Virtual environment activated" -ForegroundColor Green

# Check if dependencies are installed
Write-Host ""
Write-Host "[2/3] Checking dependencies..." -ForegroundColor Yellow
$streamlitInstalled = pip list | Select-String streamlit
if (-not $streamlitInstalled) {
  Write-Host "[WARNING] Dependencies may not be installed" -ForegroundColor Yellow
  Write-Host "Installing requirements..." -ForegroundColor Yellow
  pip install -r requirements.txt
}
Write-Host "[OK] Dependencies ready" -ForegroundColor Green

# Launch Streamlit app
Write-Host ""
Write-Host "[3/3] Launching application..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "App is running at: http://localhost:8501" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

streamlit run app/streamlit_app.py

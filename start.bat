@echo off
REM PhishLab - Quick Start Script for Windows
REM This script automates the setup and launch of PhishLab

echo ============================================================
echo PhishLab - Educational Phishing Simulation Framework
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Check if we're in the correct directory
if not exist "app.py" (
    echo [ERROR] app.py not found. Please run this script from the phishlab directory
    pause
    exit /b 1
)

echo [OK] Found app.py
echo.

REM Check if dependencies are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [INSTALLING] Dependencies not found. Installing now...
    echo This may take a minute...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencies installed successfully
) else (
    echo [OK] Dependencies already installed
)

echo.
echo ============================================================
echo Starting PhishLab...
echo ============================================================
echo.
echo ETHICAL DISCLAIMER:
echo This is an EDUCATIONAL tool for cybersecurity awareness.
echo No real phishing attacks are performed.
echo All simulations are safe and offline.
echo.
echo ============================================================
echo.
echo [INFO] Server will start at http://localhost:5000
echo [INFO] Press CTRL+C to stop the server
echo.
echo Opening browser in 5 seconds...
echo.

REM Wait 5 seconds then open browser
timeout /t 5 /nobreak >nul
start http://localhost:5000

REM Start the Flask application
python app.py

echo.
echo ============================================================
echo PhishLab has been stopped
echo ============================================================
pause

#!/bin/bash
# PhishLab - Quick Start Script for Linux/Mac
# This script automates the setup and launch of PhishLab

echo "============================================================"
echo "PhishLab - Educational Phishing Simulation Framework"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

echo "[OK] Python is installed"
echo ""

# Check if we're in the correct directory
if [ ! -f "app.py" ]; then
    echo "[ERROR] app.py not found. Please run this script from the phishlab directory"
    exit 1
fi

echo "[OK] Found app.py"
echo ""

# Check if dependencies are installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[INSTALLING] Dependencies not found. Installing now..."
    echo "This may take a minute..."
    echo ""
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
    echo ""
    echo "[OK] Dependencies installed successfully"
else
    echo "[OK] Dependencies already installed"
fi

echo ""
echo "============================================================"
echo "Starting PhishLab..."
echo "============================================================"
echo ""
echo "ETHICAL DISCLAIMER:"
echo "This is an EDUCATIONAL tool for cybersecurity awareness."
echo "No real phishing attacks are performed."
echo "All simulations are safe and offline."
echo ""
echo "============================================================"
echo ""
echo "[INFO] Server will start at http://localhost:5000"
echo "[INFO] Press CTRL+C to stop the server"
echo ""
echo "Opening browser in 5 seconds..."
echo ""

# Wait 5 seconds
sleep 5

# Open browser based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost:5000
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open http://localhost:5000 2>/dev/null || echo "Please open http://localhost:5000 in your browser"
fi

# Start the Flask application
python3 app.py

echo ""
echo "============================================================"
echo "PhishLab has been stopped"
echo "============================================================"

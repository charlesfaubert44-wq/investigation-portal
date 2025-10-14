#!/bin/bash

echo "======================================"
echo "Yellowknife Grocery Price Tracker"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Check if dependencies are installed
echo "Checking dependencies..."
if ! python3 -c "import flask" &> /dev/null
then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "Starting application..."
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
python3 app.py

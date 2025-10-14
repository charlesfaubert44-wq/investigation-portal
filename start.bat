@echo off
echo ======================================
echo Yellowknife Grocery Price Tracker
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed.
    echo Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting application...
echo Press Ctrl+C to stop the server
echo.

REM Run the application
python app.py
pause

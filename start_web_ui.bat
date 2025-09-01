@echo off
echo Starting Gumtree Auto Lister Web UI...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not available
    echo Please install pip and try again
    pause
    exit /b 1
)

REM Install requirements if needed
echo Installing/updating requirements...
pip install -r requirements.txt

REM Start the Flask application
echo.
echo Starting Flask web server...
echo The web UI will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause

@echo off
echo.
echo 🚀 Starting Universal Data Analyzer...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Create directories
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs

echo.
echo ✅ Setup complete!
echo.
echo 🌐 Starting Flask server...
echo    Backend: http://localhost:5000
echo.
echo 📖 To use the app:
echo    1. Open index.html in your browser
echo    2. Or the browser will open automatically
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start Flask server and open browser
start http://localhost:5000
start index.html
python app.py

pause

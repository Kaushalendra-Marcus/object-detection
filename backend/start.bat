@echo off
REM YOLO Detection API - Startup Script for Windows

cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║    🎯 YOLO Object Detection API - Startup        ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Activate virtual environment
echo [1/3] Activating virtual environment...
call myenv\Scripts\activate.bat

REM Install/upgrade dependencies
echo [2/3] Checking dependencies...
pip install -q fastapi uvicorn python-multipart websockets aiofiles

REM Start API
echo [3/3] Starting API server...
echo.
echo ✓ API Server starting on http://localhost:8000
echo ✓ Swagger UI available at http://localhost:8000/docs
echo ✓ Web Dashboard at http://localhost:3000 (when running frontend)
echo.
echo Press Ctrl+C to stop the server
echo.

python api.py

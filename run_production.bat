@echo off
title VoiceForm AI - Production Launcher (Unified Port 8000)
cd /d "%~dp0"

echo ========================================================
echo        VoiceForm AI - Production Server Launcher
echo       Serving Unified Web UI & Whisper Backend
echo                   http://localhost:8000
echo ========================================================
echo.

if not exist "frontend\dist\index.html" (
    echo Building frontend production assets...
    cd frontend
    call npm run build
    cd ..
    echo Frontend build complete.
    echo.
)

echo Starting Unified Production Server on port 8000...
echo.
start http://localhost:8000

cd /d "%~dp0backend"
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
pause

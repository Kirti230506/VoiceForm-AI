@echo off
title VoiceForm AI - Launcher
cd /d "%~dp0"
echo ========================================================
echo             VoiceForm AI Full-Stack Launcher
echo ========================================================
echo.
echo Launching Backend Server on http://127.0.0.1:8000 ...
start "VoiceForm AI Backend" cmd /k "run_backend.bat"

timeout /t 3 /nobreak >nul

echo Launching React Frontend on http://localhost:5173 ...
start "VoiceForm AI Frontend" cmd /k "run_frontend.bat"

echo.
echo System launched!
echo - Frontend: http://localhost:5173
echo - Backend API Docs: http://127.0.0.1:8000/docs
echo.
pause

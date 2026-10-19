@echo off
title VoiceForm AI - Backend Server
cd /d "%~dp0backend"
echo ========================================================
echo        Starting VoiceForm AI FastAPI Backend
echo   Whisper Speech-to-Text + NLP/NER + Scheme Engine
echo ========================================================
echo.
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause

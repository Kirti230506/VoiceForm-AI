@echo off
title VoiceForm AI - Instant Public Share Link
cd /d "%~dp0"

echo ========================================================
echo        VoiceForm AI - Instant Public Share Link
echo ========================================================
echo.
echo STEP 1: Make sure your server is running on port 8000!
echo         (Run "run_production.bat" first).
echo.
echo STEP 2: Connecting to secure HTTPS public tunnel...
echo         A public web link will appear below in 3 seconds.
echo.
echo You can copy that HTTPS link and send it to ANYONE:
echo - Opens on any mobile phone, tablet, or PC
echo - Microphone works securely over HTTPS
echo - When you want to stop sharing, just close this window!
echo ========================================================
echo.

ssh -p 443 -o StrictHostKeyChecking=no -R0:localhost:8000 a.pinggy.io
pause

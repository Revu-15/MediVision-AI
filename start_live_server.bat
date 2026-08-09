@echo off
title MediVision AI - Live Server Launcher
echo ========================================================
echo        🏥 MediVision AI - Live Server Launcher
echo ========================================================
echo.
echo [1/2] Starting Flask Backend Server (Port 5000)...
start /min "MediVision Flask" cmd /c ".\venv\Scripts\python app.py"

echo [2/2] Connecting ngrok Public Live Tunnel...
start /min "MediVision ngrok" cmd /c ".\venv\Scripts\ngrok.exe http 5000"

echo.
echo ========================================================
echo  🎉 MediVision AI is now LIVE on the internet!
echo.
echo  🌐 Live URL: https://devoutly-walnut-cartridge.ngrok-free.dev
echo  💻 Local URL: http://127.0.0.1:5000
echo ========================================================
echo.
echo Keep this window open to maintain your live link.
echo Press any key to stop the live server.
pause > nul

echo Stopping MediVision AI live server...
taskkill /FI "WINDOWTITLE eq MediVision Flask*" /F > nul 2>&1
taskkill /FI "WINDOWTITLE eq MediVision ngrok*" /F > nul 2>&1
echo Done.

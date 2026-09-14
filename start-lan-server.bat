@echo off
setlocal enabledelayedexpansion
title Math-Mastery LAN Server
cd /d "%~dp0"

rem ===== Config =====
set PORT=8000
rem ==================

echo ============================================================
echo   Math-Mastery LAN Web Server
echo   Listening port: %PORT%
echo   Press Ctrl+C to stop
echo ============================================================
echo.

rem Try to open firewall port (requires admin)
netsh advfirewall firewall add rule name="Math-Mastery HTTP %PORT%" dir=in action=allow protocol=TCP localport=%PORT% >nul 2>&1

echo Local access:
echo   http://localhost:%PORT%
echo.
echo Access from other devices on LAN (use any of these):
echo.

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set ip=%%a
    set ip=!ip: =!
    if not "!ip!"=="" echo   http://!ip!:%PORT%
)

echo.
echo If no IP shown above, run "ipconfig" to check your LAN IPv4 address.
echo Other devices must be on the same network and able to ping this IP.
echo.
echo Starting server (Ctrl+C to stop)...
echo.

python -m http.server %PORT% --bind 0.0.0.0
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start server. Check that Python 3 is installed and port %PORT% is free.
    pause
)
endlocal

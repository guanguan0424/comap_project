@echo off
cd /d "%~dp0.."

REM Check if port 8080 is available
netstat -ano | findstr ":8080" >nul
if not errorlevel 1 (
    echo Port 8080 is busy, using port 8081
    set PORT=8081
) else (
    set PORT=8080
)

echo Starting Allure Report Server...
echo Report URL: http://localhost:%PORT%
echo Server starting...

REM Wait a moment and open browser
ping -n 2 127.0.0.1 >nul
start http://localhost:%PORT%

echo.
echo Server started at http://localhost:%PORT%
echo Press Ctrl+C to stop the server
echo.
python -m http.server %PORT%

echo.
echo Server stopped
pause
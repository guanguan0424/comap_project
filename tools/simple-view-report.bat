@echo off

REM Change to project root directory
cd /d "%~dp0.."

REM Check if allure-report exists
if not exist "allure-report" (
    echo Error: allure-report directory not found
    echo Please generate test report first:
    echo pytest --alluredir=allure-results
    echo allure generate allure-results -o allure-report --clean
    pause
    exit /b 1
)

echo Starting Allure Report Server...

REM Check if port 8080 is available
netstat -ano | findstr ":8080" >nul
if not errorlevel 1 (
    echo Port 8080 is busy, using port 8081
    set PORT=8081
) else (
    set PORT=8080
)

echo Report URL: http://localhost:%PORT%

echo Starting server...

REM Start server in the background and open browser
cd "allure-report"
start http://localhost:%PORT%
python -m http.server %PORT%
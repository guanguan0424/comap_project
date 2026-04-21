@echo off
chcp 65001 >nul
echo ========================================
echo           测试报告查看工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查报告目录是否存在
if not exist "allure-report" (
    echo ❌ 未找到allure-report目录
    echo 💡 请先生成测试报告：
    echo    pytest --alluredir=allure-results
    echo    allure generate allure-results -o allure-report --clean
    pause
    exit /b 1
)

REM 切换到报告目录
cd /d "%~dp0allure-report"

REM 检查端口是否被占用
netstat -ano | findstr ":8080" >nul
if not errorlevel 1 (
    echo ⚠️  端口8080已被占用，尝试使用8081端口
    set PORT=8081
) else (
    set PORT=8080
)

echo 🚀 启动Allure报告服务器...
echo 📊 报告地址: http://localhost:%PORT%
echo ⏳ 服务器启动中...

REM 延迟1秒后自动打开浏览器
ping -n 2 127.0.0.1 >nul
start http://localhost:%PORT%

REM 启动HTTP服务器
echo.
echo ✅ 服务器已启动在 http://localhost:%PORT%
echo 📋 按 Ctrl+C 停止服务器
echo.
python -m http.server %PORT%

echo.
echo 🔚 服务器已停止
pause
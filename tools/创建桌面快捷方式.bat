@echo off
chcp 65001 >nul

echo ========================================
echo         创建桌面快捷方式工具
echo ========================================
echo.

set "DESKTOP=%USERPROFILE%\Desktop"
set "BATCH_FILE=%~dp0一键查看报告.bat"
set "SHORTCUT=%DESKTOP%\查看测试报告.lnk"

REM 检查批处理文件是否存在
if not exist "%BATCH_FILE%" (
    echo ❌ 未找到一键查看报告.bat文件
    pause
    exit /b 1
)

echo 📁 批处理文件位置: %BATCH_FILE%
echo 📋 桌面快捷方式: %SHORTCUT%
echo.

REM 使用PowerShell创建快捷方式
powershell -Command "
$WshShell = New-Object -comObject WScript.Shell;
$Shortcut = $WshShell.CreateShortcut('%SHORTCUT%');
$Shortcut.TargetPath = '%BATCH_FILE%';
$Shortcut.WorkingDirectory = '%~dp0';
$Shortcut.IconLocation = '%%SystemRoot%%\system32\SHELL32.dll,21';
$Shortcut.Description = '一键查看Allure测试报告';
$Shortcut.Save();
"

if errorlevel 1 (
    echo ❌ 创建快捷方式失败
    echo 💡 请手动创建快捷方式：
    echo   1. 右键桌面 -> 新建 -> 快捷方式
    echo   2. 输入: cmd /k \"cd /d d:\comap_project && 一键查看报告.bat\"
    echo   3. 命名为: 查看测试报告
    pause
    exit /b 1
)

echo ✅ 桌面快捷方式创建成功！
echo 📋 现在你可以在桌面双击 \"查看测试报告\" 来打开报告了
echo.
pause
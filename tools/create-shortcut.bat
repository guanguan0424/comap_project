@echo off
set "DESKTOP=%USERPROFILE%\Desktop"
set "LINK=%DESKTOP%\View Test Report.lnk"
set "BATCH=d:\comap_project\tools\view-report.bat"

echo Creating desktop shortcut...
echo Shortcut: %LINK%
echo Target: %BATCH%

REM Create shortcut command
echo Set oWS = WScript.CreateObject("WScript.Shell") > %TEMP%\create_shortcut.vbs
echo sLinkFile = "%LINK%" >> %TEMP%\create_shortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %TEMP%\create_shortcut.vbs
echo oLink.TargetPath = "%BATCH%" >> %TEMP%\create_shortcut.vbs
echo oLink.WorkingDirectory = "d:\comap_project\tools" >> %TEMP%\create_shortcut.vbs
echo oLink.Description = "View Test Report" >> %TEMP%\create_shortcut.vbs
echo oLink.Save >> %TEMP%\create_shortcut.vbs
echo WScript.Echo "Shortcut created successfully!" >> %TEMP%\create_shortcut.vbs

cscript //nologo %TEMP%\create_shortcut.vbs
del %TEMP%\create_shortcut.vbs

echo.
echo Desktop shortcut created!
echo You can now double-click "View Test Report" on your desktop
pause
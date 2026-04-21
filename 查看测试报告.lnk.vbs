Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.ExpandEnvironmentStrings("%USERPROFILE%") & "\Desktop\查看测试报告.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
    oLink.TargetPath = "d:\comap_project\一键查看报告.bat"
    oLink.WorkingDirectory = "d:\comap_project"
    oLink.Description = "一键查看Allure测试报告"
    oLink.Save
WScript.Echo "桌面快捷方式创建成功！"
# PowerShell脚本 - 使用Allure运行测试并生成报告

# 清理之前的测试结果
Write-Host "=== 清理之前的测试结果 ===" -ForegroundColor Yellow

if (Test-Path "allure-results") {
    Remove-Item -Recurse -Force "allure-results"
}
if (Test-Path "allure-report") {
    Remove-Item -Recurse -Force "allure-report"
}

# 清理旧截图（保留最近3天的）
Write-Host "=== 清理旧的截图文件 ===" -ForegroundColor Yellow
python manage_screenshots.py cleanup --days 3 --verbose

# 创建测试结果目录
New-Item -ItemType Directory -Force -Path "allure-results"

# 运行UI测试并生成Allure数据
Write-Host "=== 运行UI登录测试 ===" -ForegroundColor Green
pytest tests/ui/test_complete_login.py -v --alluredir=allure-results

# 检查是否有Allure命令行工具
$allurePath = "allure"

# 生成Allure报告
Write-Host "=== 生成Allure测试报告 ===" -ForegroundColor Green
try {
    allure generate allure-results --clean -o allure-report
    Write-Host "Allure报告生成成功!" -ForegroundColor Green
} catch {
    Write-Host "未找到Allure命令行工具，可执行以下步骤手动安装:" -ForegroundColor Yellow
    Write-Host "1. 下载Allure命令行工具: https://github.com/allure-framework/allure2/releases" -ForegroundColor Cyan
    Write-Host "2. 解压并添加到系统PATH环境变量" -ForegroundColor Cyan
    Write-Host "3. 或者使用以下命令查看原始测试数据: tree allure-results" -ForegroundColor Cyan
}

# 打开报告（如果可能）
if (Test-Path "allure-report\index.html") {
    $reportPath = "$PWD\allure-report\index.html"
    Write-Host "=== 测试报告路径 ===" -ForegroundColor Cyan
    Write-Host "文件路径: $reportPath" -ForegroundColor White
    
    # 尝试用浏览器打开
    try {
        Start-Process "$reportPath"
        Write-Host "已尝试在浏览器中打开报告" -ForegroundColor Green
    } catch {
        Write-Host "请手动打开报告文件: $reportPath" -ForegroundColor Yellow
    }
} else {
    Write-Host "=== 测试结果文件 ===" -ForegroundColor Cyan
    Get-ChildItem "allure-results" | Format-Table Name, Length, LastWriteTime
}
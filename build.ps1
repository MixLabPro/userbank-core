# Personal Profile MCP 打包脚本 (PowerShell)

Write-Host "========================================" -ForegroundColor Green
Write-Host "Personal Profile MCP 打包脚本" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host ""
Write-Host "检查 PyInstaller 是否已安装..." -ForegroundColor Yellow

try {
    $null = pip show pyinstaller 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "PyInstaller 未安装，正在安装..." -ForegroundColor Yellow
        pip install pyinstaller
        if ($LASTEXITCODE -ne 0) {
            Write-Host "PyInstaller 安装失败！" -ForegroundColor Red
            Read-Host "按任意键退出"
            exit 1
        }
    } else {
        Write-Host "PyInstaller 已安装" -ForegroundColor Green
    }
} catch {
    Write-Host "检查 PyInstaller 时出错: $_" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

Write-Host ""
Write-Host "清理之前的构建文件..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "开始打包 main.py (UserBank_Stdio_Core.exe)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

pyinstaller build_main.spec --clean --noconfirm
if ($LASTEXITCODE -ne 0) {
    Write-Host "main.py 打包失败！" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "开始打包 main_sse.py (UserBank_SSE_Core.exe)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

pyinstaller build_main_sse.spec --clean --noconfirm
if ($LASTEXITCODE -ne 0) {
    Write-Host "main_sse.py 打包失败！" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "打包完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "生成的文件位置：" -ForegroundColor Cyan
Write-Host "- UserBank_Stdio_Core.exe: dist\UserBank_Stdio_Core.exe" -ForegroundColor White
Write-Host "- UserBank_SSE_Core.exe: dist\UserBank_SSE_Core.exe" -ForegroundColor White
Write-Host ""
Write-Host "您可以将这些 exe 文件复制到任何 Windows 机器上运行。" -ForegroundColor Green
Write-Host ""

Read-Host "按任意键退出" 
@echo off
echo ========================================
echo Personal Profile MCP 打包脚本
echo ========================================

echo.
echo 检查 PyInstaller 是否已安装...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller 未安装，正在安装...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo PyInstaller 安装失败！
        pause
        exit /b 1
    )
) else (
    echo PyInstaller 已安装
)

echo.
echo 清理之前的构建文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo.
echo ========================================
echo 开始打包 main.py (UserBank_Stdio_Core.exe)
echo ========================================
pyinstaller build_main.spec --clean --noconfirm
if %errorlevel% neq 0 (
    echo main.py 打包失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo 开始打包 main_sse.py (UserBank_SSE_Core.exe)
echo ========================================
pyinstaller build_main_sse.spec --clean --noconfirm
if %errorlevel% neq 0 (
    echo main_sse.py 打包失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 生成的文件位置：
echo - UserBank_Stdio_Core.exe: dist\UserBank_Stdio_Core.exe
echo - UserBank_SSE_Core.exe: dist\UserBank_SSE_Core.exe
echo.
echo 您可以将这些 exe 文件复制到任何 Windows 机器上运行。
echo.

pause 
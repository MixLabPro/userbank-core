@echo off
REM 个人画像数据结构分类系统 MCP 服务器启动脚本
REM Personal Profile Data Structure Classification System MCP Server Startup Script

echo ========================================
echo 🧠 个人画像数据结构分类系统
echo Personal Profile Data Structure Classification System
echo ========================================
echo.

REM 切换到项目目录
cd /d "F:\Github\Profile"

echo 📍 当前目录: %CD%
echo.

REM 检查 uv 是否可用
echo 🔍 检查 uv 环境...
uv --version
if %ERRORLEVEL% neq 0 (
    echo ❌ uv 未安装或不可用
    echo 请先安装 uv: https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)

echo ✅ uv 环境正常
echo.

REM 同步依赖
echo 📦 同步项目依赖...
uv sync
if %ERRORLEVEL% neq 0 (
    echo ❌ 依赖同步失败
    pause
    exit /b 1
)

echo ✅ 依赖同步完成
echo.

REM 启动 MCP 服务器
echo 🚀 启动 MCP 服务器...
echo 📡 等待客户端连接...
echo.
echo 提示: 按 Ctrl+C 停止服务器
echo.

uv run python main.py

echo.
echo 👋 服务器已停止
pause 
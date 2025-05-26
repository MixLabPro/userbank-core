# 个人画像数据结构分类系统 MCP 服务器启动脚本
# Personal Profile Data Structure Classification System MCP Server Startup Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🧠 个人画像数据结构分类系统" -ForegroundColor Green
Write-Host "Personal Profile Data Structure Classification System" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 切换到项目目录
$ProjectPath = "F:\Github\Profile"
Set-Location $ProjectPath

Write-Host "📍 当前目录: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

# 检查 uv 是否可用
Write-Host "🔍 检查 uv 环境..." -ForegroundColor Blue
try {
    $uvVersion = uv --version
    Write-Host "✅ uv 环境正常: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ uv 未安装或不可用" -ForegroundColor Red
    Write-Host "请先安装 uv: https://docs.astral.sh/uv/getting-started/installation/" -ForegroundColor Yellow
    Read-Host "按任意键退出"
    exit 1
}

Write-Host ""

# 同步依赖
Write-Host "📦 同步项目依赖..." -ForegroundColor Blue
try {
    uv sync
    Write-Host "✅ 依赖同步完成" -ForegroundColor Green
} catch {
    Write-Host "❌ 依赖同步失败" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

Write-Host ""

# 启动 MCP 服务器
Write-Host "🚀 启动 MCP 服务器..." -ForegroundColor Magenta
Write-Host "📡 等待客户端连接..." -ForegroundColor Magenta
Write-Host ""
Write-Host "提示: 按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host ""

try {
    uv run python main.py
} catch {
    Write-Host "❌ 服务器启动失败: $_" -ForegroundColor Red
} finally {
    Write-Host ""
    Write-Host "👋 服务器已停止" -ForegroundColor Yellow
    Read-Host "按任意键退出"
} 
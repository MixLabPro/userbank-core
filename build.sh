#!/bin/bash

echo "========================================"
echo "Personal Profile MCP 打包脚本"
echo "========================================"

# 检查 Python3 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查 venv 模块是否可用
if ! python3 -c "import venv" &> /dev/null; then
    echo "错误：Python3 venv 模块不可用，请安装 python3-venv"
    exit 1
fi

# 创建虚拟环境
echo ""
echo "检查虚拟环境..."
if [ -d "venv" ]; then
    echo "虚拟环境已存在，直接使用..."
else
    echo "创建新的虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "创建虚拟环境失败！"
        exit 1
    fi
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "激活虚拟环境失败！"
    exit 1
fi

# 升级 pip
echo "升级 pip..."
python -m pip install --upgrade pip

# 安装依赖
echo ""
echo "安装项目依赖..."
if [ -f "requirements.txt" ]; then
    # 检查是否已经安装了所有依赖
    if ! pip freeze | grep -q -f requirements.txt; then
        echo "安装/更新依赖..."
        pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "安装依赖失败！"
            exit 1
        fi
    else
        echo "依赖已安装，跳过安装步骤"
    fi
else
    echo "警告：未找到 requirements.txt 文件"
fi

# 安装 PyInstaller
echo ""
echo "检查 PyInstaller 是否已安装..."
if ! pip show pyinstaller >/dev/null 2>&1; then
    echo "PyInstaller 未安装，正在安装..."
    pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo "PyInstaller 安装失败！"
        exit 1
    fi
else
    echo "PyInstaller 已安装"
fi

echo ""
echo "清理之前的构建文件..."
rm -rf dist
rm -rf build

echo ""
echo "========================================"
echo "开始打包 main.py (UserBank_Stdio_Core)"
echo "========================================"
pyinstaller build_main.spec --clean --noconfirm
if [ $? -ne 0 ]; then
    echo "main.py 打包失败！"
    exit 1
fi

echo ""
echo "========================================"
echo "开始打包 main_sse.py (UserBank_SSE_Core)"
echo "========================================"
pyinstaller build_main_sse.spec --clean --noconfirm
if [ $? -ne 0 ]; then
    echo "main_sse.py 打包失败！"
    exit 1
fi

# 代码签名部分
echo ""
echo "========================================"
echo "开始代码签名"
echo "========================================"

# 检查是否有开发者证书
if security find-identity -v -p codesigning | grep -q "Developer ID Application"; then
    # 获取开发者证书
    CERTIFICATE=$(security find-identity -v -p codesigning | grep "Developer ID Application" | head -n 1 | awk -F'"' '{print $2}')
    
    echo "使用证书: $CERTIFICATE"
    
    # 签名 UserBank_Stdio_Core
    echo "签名 UserBank_Stdio_Core..."
    codesign --force --deep --sign "$CERTIFICATE" "dist/UserBank_Stdio_Core"
    if [ $? -ne 0 ]; then
        echo "UserBank_Stdio_Core 签名失败！"
        exit 1
    fi
    
    # 签名 UserBank_SSE_Core
    echo "签名 UserBank_SSE_Core..."
    codesign --force --deep --sign "$CERTIFICATE" "dist/UserBank_SSE_Core"
    if [ $? -ne 0 ]; then
        echo "UserBank_SSE_Core 签名失败！"
        exit 1
    fi
    
    # 验证签名
    echo "验证签名..."
    codesign --verify --deep --strict "dist/UserBank_Stdio_Core"
    codesign --verify --deep --strict "dist/UserBank_SSE_Core"
    
    echo "代码签名完成！"
else
    echo "警告：未找到开发者证书，跳过签名步骤"
    echo "如需签名，请先安装开发者证书"
fi

echo ""
echo "========================================"
echo "打包完成！"
echo "========================================"
echo ""
echo "生成的文件位置："
echo "- UserBank_Stdio_Core: dist/UserBank_Stdio_Core"
echo "- UserBank_SSE_Core: dist/UserBank_SSE_Core"
echo ""
echo "您可以将这些可执行文件复制到任何 macOS 机器上运行。"
echo "注意：如果未签名，首次运行时可能需要执行 chmod +x 命令赋予执行权限。"
echo ""

# 自动赋予执行权限
chmod +x dist/UserBank_Stdio_Core
chmod +x dist/UserBank_SSE_Core

echo "已自动赋予执行权限。"

# 退出虚拟环境
deactivate

echo "按回车键退出..."
read 
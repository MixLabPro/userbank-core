#!/usr/bin/env python3
"""
快速启动脚本
Quick Start Script

提供多种启动选项和系统检查功能
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """检查依赖项"""
    print("🔍 检查系统依赖...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
        print("❌ Python版本过低，需要Python 3.10+")
        return False
    else:
        print(f"✅ Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查FastMCP
    try:
        import fastmcp
        print("✅ FastMCP已安装")
    except ImportError:
        print("❌ FastMCP未安装，请运行: pip install fastmcp")
        return False
    
    # 检查项目文件
    required_files = [
        "src/database.py",
        "src/mcp_tools.py", 
        "src/__init__.py",
        "main.py"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ 缺少文件: {file_path}")
            return False
    
    return True

def show_menu():
    """显示启动菜单"""
    print("\n🧠 个人画像数据管理系统 - 快速启动")
    print("=" * 50)
    print("请选择启动选项:")
    print("1. 🧪 运行系统测试")
    print("2. 📖 查看使用示例")
    print("3. 🚀 启动MCP服务器")
    print("4. 📊 查看数据库状态")
    print("5. 🔧 系统诊断")
    print("6. ❌ 退出")
    print("=" * 50)

def run_tests():
    """运行系统测试"""
    print("\n🧪 运行系统测试...")
    try:
        result = subprocess.run([sys.executable, "test_system.py"], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("✅ 系统测试通过")
        else:
            print("❌ 系统测试失败")
            print(result.stderr)
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")

def run_examples():
    """运行使用示例"""
    print("\n📖 运行使用示例...")
    try:
        result = subprocess.run([sys.executable, "example_usage.py"], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("✅ 示例运行完成")
        else:
            print("❌ 示例运行失败")
            print(result.stderr)
    except Exception as e:
        print(f"❌ 运行示例时出错: {e}")

def start_server():
    """启动MCP服务器"""
    print("\n🚀 启动MCP服务器...")
    print("💡 提示：使用Ctrl+C停止服务器")
    print("📡 服务器将在标准输入/输出上监听MCP连接")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动服务器时出错: {e}")

def check_database():
    """检查数据库状态"""
    print("\n📊 检查数据库状态...")
    
    # 添加src目录到Python路径
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    
    try:
        from src.database import get_database
        from src.mcp_tools import get_table_stats
        
        # 获取数据库实例
        db = get_database()
        
        # 获取统计信息
        result = get_table_stats()
        
        if result.get('success'):
            print("✅ 数据库连接正常")
            print("\n📋 表统计信息:")
            for table, stats in result['all_stats'].items():
                print(f"  • {stats['table_description']}: {stats['total_records']} 条记录")
                if stats['latest_record']:
                    print(f"    最新记录: {stats['latest_record']}")
        else:
            print(f"❌ 获取数据库状态失败: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ 检查数据库时出错: {e}")

def system_diagnosis():
    """系统诊断"""
    print("\n🔧 系统诊断...")
    
    # 检查文件权限
    print("📁 检查文件权限...")
    current_dir = Path(".")
    if os.access(current_dir, os.R_OK | os.W_OK):
        print("✅ 当前目录可读写")
    else:
        print("❌ 当前目录权限不足")
    
    # 检查数据库文件
    db_file = Path("profile_data.db")
    if db_file.exists():
        print(f"✅ 数据库文件存在: {db_file.stat().st_size} 字节")
    else:
        print("ℹ️ 数据库文件不存在（首次运行时会自动创建）")
    
    # 检查日志文件
    log_file = Path("profile_system.log")
    if log_file.exists():
        print(f"✅ 日志文件存在: {log_file.stat().st_size} 字节")
    else:
        print("ℹ️ 日志文件不存在（运行时会自动创建）")
    
    # 检查环境变量
    print("\n🌍 环境信息:")
    print(f"  • Python路径: {sys.executable}")
    print(f"  • 工作目录: {os.getcwd()}")
    print(f"  • 平台: {sys.platform}")

def main():
    """主函数"""
    print("🧠 个人画像数据管理系统 - 快速启动工具")
    
    # 检查依赖项
    if not check_dependencies():
        print("\n❌ 依赖检查失败")
        return
    
    print("\n✅ 系统检查通过！")
    print("📖 请查看 README.md 了解详细使用说明")
    print("🧪 运行 'python test_system.py' 进行系统测试")
    print("📖 运行 'python example_usage.py' 查看使用示例")
    print("🚀 运行 'python main.py' 启动MCP服务器")

if __name__ == "__main__":
    main()
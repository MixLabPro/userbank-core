#!/usr/bin/env python3
"""
简化的MCP服务器启动脚本
Simplified MCP Server Startup Script
"""

import sys
import logging
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """启动MCP服务器"""
    try:
        print("🧠 个人画像数据结构分类系统")
        print("=" * 50)
        
        # 测试数据库连接
        print("📊 测试数据库连接...")
        from src.database import get_database
        db = get_database()
        print("✅ 数据库连接成功")
        
        # 测试MCP工具
        print("🔧 加载MCP工具...")
        from src.mcp_tools import mcp
        print("✅ MCP工具加载成功")
        
        # 显示可用工具
        print("\n📋 可用的MCP工具:")
        tools = [
            "add_belief", "add_insight", "add_focus", 
            "add_long_term_goal", "add_short_term_goal", 
            "add_preference", "add_decision", "add_methodology",
            "get_record", "search_records", "get_all_records",
            "update_record", "delete_record", 
            "get_table_stats", "get_available_tables"
        ]
        
        for i, tool in enumerate(tools, 1):
            print(f"  {i:2d}. {tool}")
        
        print("\n🚀 启动MCP服务器...")
        print("📡 等待客户端连接...")
        print("💡 提示：使用Ctrl+C停止服务器")
        print("=" * 50)
        
        # 启动MCP服务器
        mcp.run()
        
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
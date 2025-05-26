#!/usr/bin/env python3
"""
个人画像数据结构分类系统主程序
Personal Profile Data Structure Classification System Main Program

基于FastMCP框架的个人画像数据管理工具
"""

import logging
import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.mcp_tools import mcp
from src.database import get_database

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('profile_system.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """主程序入口"""
    try:
        logger.info("🧠 个人画像数据结构分类系统启动中...")
        
        # 初始化数据库
        logger.info("📊 初始化数据库...")
        db = get_database()
        logger.info("✅ 数据库初始化完成")
        
        # 打印系统信息
        print("=" * 60)
        print("🧠 个人画像数据结构分类系统")
        print("Personal Profile Data Structure Classification System")
        print("=" * 60)
        print("📋 可用的数据表:")
        print("  • belief (信念)")
        print("  • insight (洞察)")
        print("  • focus (关注点)")
        print("  • long_term_goal (长期目标)")
        print("  • short_term_goal (短期目标)")
        print("  • preference (偏好)")
        print("  • decision (决策)")
        print("  • methodology (方法论)")
        print("=" * 60)
        print("🔧 可用的MCP工具:")
        print("  • 添加工具: add_belief, add_insight, add_focus, etc.")
        print("  • 查询工具: get_record, search_records, get_all_records")
        print("  • 更新工具: update_record")
        print("  • 删除工具: delete_record")
        print("  • 统计工具: get_table_stats, get_available_tables")
        print("=" * 60)
        
        # 启动MCP服务器
        logger.info("🚀 启动MCP服务器...")
        print("🚀 MCP服务器正在启动...")
        print("📡 等待客户端连接...")
        
        # 运行MCP服务器
        mcp.run()
        
    except KeyboardInterrupt:
        logger.info("👋 用户中断，系统正在关闭...")
        print("\n👋 系统正在关闭...")
    except Exception as e:
        logger.error(f"❌ 系统启动失败: {e}")
        print(f"❌ 系统启动失败: {e}")
        sys.exit(1)
    finally:
        # 清理资源
        try:
            db = get_database()
            db.close()
            logger.info("🔒 数据库连接已关闭")
        except:
            pass

if __name__ == "__main__":
    main()

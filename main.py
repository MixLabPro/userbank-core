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

# 配置日志 - 只输出到文件，不输出到控制台
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('profile_system.log', encoding='utf-8')
        # 移除 StreamHandler() 以避免控制台输出干扰 MCP 通信
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
        
        # 记录系统信息到日志文件
        logger.info("=" * 60)
        logger.info("🧠 个人画像数据结构分类系统")
        logger.info("Personal Profile Data Structure Classification System")
        logger.info("=" * 60)
        logger.info("📋 可用的数据表:")
        logger.info("  • belief (信念)")
        logger.info("  • insight (洞察)")
        logger.info("  • focus (关注点)")
        logger.info("  • long_term_goal (长期目标)")
        logger.info("  • short_term_goal (短期目标)")
        logger.info("  • preference (偏好)")
        logger.info("  • decision (决策)")
        logger.info("  • methodology (方法论)")
        logger.info("=" * 60)
        logger.info("🔧 可用的MCP工具:")
        logger.info("  • 添加工具: add_belief, add_insight, add_focus, etc.")
        logger.info("  • 查询工具: get_record, search_records, get_all_records")
        logger.info("  • 更新工具: update_record")
        logger.info("  • 删除工具: delete_record")
        logger.info("  • 统计工具: get_table_stats, get_available_tables")
        logger.info("  • 批量工具: get_all_table_contents, get_table_names_with_details")
        logger.info("  • 导出工具: export_table_data")
        logger.info("=" * 60)
        
        # 启动MCP服务器
        logger.info("🚀 启动MCP服务器...")
        logger.info("📡 等待客户端连接...")
        
        # 运行MCP服务器 - 这里不应该有任何 print 输出
        mcp.run()
        
    except KeyboardInterrupt:
        logger.info("👋 用户中断，系统正在关闭...")
    except Exception as e:
        logger.error(f"❌ 系统启动失败: {e}")
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

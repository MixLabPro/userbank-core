#!/usr/bin/env python3
"""
个人画像数据库MCP服务器启动脚本
"""

import sys
import os
import logging
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from server import main
    from config import get_log_level, is_development_mode, get_config_summary
    
    # 配置日志
    log_level = getattr(logging, get_log_level().upper())
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    def print_startup_info():
        """打印启动信息"""
        print("=" * 60)
        print("个人画像数据库MCP服务器")
        print("=" * 60)
        
        config_summary = get_config_summary()
        
        print(f"服务器名称: {config_summary['server_name']}")
        print(f"服务器版本: {config_summary['server_version']}")
        print(f"数据库路径: {config_summary['database_path']}")
        print(f"日志级别: {config_summary['log_level']}")
        print(f"开发模式: {'是' if config_summary['development_mode'] else '否'}")
        print(f"支持的表: {', '.join(config_summary['supported_tables'])}")
        print(f"支持的分析类型: {', '.join(config_summary['supported_analysis_types'])}")
        
        print("\n可用的MCP工具:")
        tools = [
            "add_record - 添加新记录",
            "get_records - 获取记录列表", 
            "search_records - 搜索记录",
            "update_record - 更新记录",
            "delete_record - 删除记录",
            "get_statistics - 获取统计信息",
            "get_recent_records - 获取最近记录",
            "analyze_patterns - 分析数据模式"
        ]
        
        for tool in tools:
            print(f"  • {tool}")
        
        print("\n" + "=" * 60)
        print("服务器正在启动...")
        print("=" * 60)
    
    if __name__ == "__main__":
        try:
            print_startup_info()
            
            # 启动MCP服务器
            import asyncio
            asyncio.run(main())
            
        except KeyboardInterrupt:
            logger.info("服务器被用户中断")
            print("\n服务器已停止")
        except Exception as e:
            logger.error(f"服务器启动失败: {e}")
            print(f"\n错误: {e}")
            sys.exit(1)
            
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装所有依赖包:")
    print("pip install -r requirements.txt")
    sys.exit(1) 
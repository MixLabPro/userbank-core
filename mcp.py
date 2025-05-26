#!/usr/bin/env python3
"""
个人画像数据库MCP服务器入口文件
为MCP开发工具提供标准的服务器对象访问
"""

import sys
import os
import logging
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    # 导入配置和服务器
    from config import get_log_level, is_development_mode
    from server import mcp, main  # 导入全局mcp对象和main函数
    
    # 配置日志
    log_level = getattr(logging, get_log_level().upper())
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    # mcp对象已经在server模块中定义，直接使用即可
    
    # 如果直接运行此文件，启动服务器
    if __name__ == "__main__":
        try:
            logger.info("启动个人画像数据库MCP服务器...")
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
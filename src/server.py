#!/usr/bin/env python3
"""
MCP服务器启动脚本
个人画像数据管理系统的MCP服务器入口点
"""

import asyncio
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_tools import main

if __name__ == "__main__":
    """启动MCP服务器"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("服务器已停止")
    except Exception as e:
        print(f"服务器启动失败: {e}")
        sys.exit(1) 
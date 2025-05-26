#!/usr/bin/env python3
"""
个人画像数据结构分类系统主程序
Personal Profile Data Structure Classification System Main Program

基于MCP官方SDK的个人画像数据管理工具
"""

import sys
import asyncio
import traceback
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """主程序入口"""
    try:
        # 导入MCP工具模块的main函数
        from mcp_tools import main as mcp_main
        
        # 运行MCP服务器
        asyncio.run(mcp_main())
        
    except KeyboardInterrupt:
        print("服务器已停止", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"服务器启动失败: {str(e)}", file=sys.stderr)
        print("详细错误信息:", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
FastMCP 测试脚本
用于验证 FastMCP 模块是否正常工作
"""

import sys
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_fastmcp_import():
    """测试 FastMCP 导入"""
    try:
        logger.info("🔍 正在测试 FastMCP 导入...")
        from fastmcp import FastMCP
        logger.info("✅ FastMCP 导入成功！")
        return True
    except ImportError as e:
        logger.error(f"❌ FastMCP 导入失败: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ 未知错误: {e}")
        return False

def test_fastmcp_basic():
    """测试 FastMCP 基本功能"""
    try:
        logger.info("🔍 正在测试 FastMCP 基本功能...")
        from fastmcp import FastMCP
        
        # 创建 FastMCP 实例
        mcp = FastMCP("测试服务器 🧪")
        
        # 定义一个简单的工具
        @mcp.tool()
        def add_numbers(a: int, b: int) -> int:
            """添加两个数字"""
            return a + b
        
        logger.info("✅ FastMCP 基本功能测试成功！")
        logger.info(f"📊 服务器名称: {mcp.name}")
        return True
        
    except Exception as e:
        logger.error(f"❌ FastMCP 基本功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("🧪 FastMCP 测试程序")
    print("=" * 50)
    
    # 测试导入
    if not test_fastmcp_import():
        print("❌ FastMCP 导入测试失败")
        sys.exit(1)
    
    # 测试基本功能
    if not test_fastmcp_basic():
        print("❌ FastMCP 基本功能测试失败")
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 所有测试通过！FastMCP 工作正常")
    print("=" * 50)

if __name__ == "__main__":
    main() 
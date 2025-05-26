# test.py
print("测试Python环境")

try:
    from mcp.server.fastmcp import FastMCP
    print("MCP导入成功")
    
    mcp = FastMCP("test-server")
    print("FastMCP实例创建成功")
    
except ImportError as e:
    print(f"导入错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
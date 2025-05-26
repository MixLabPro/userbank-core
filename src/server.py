# src/server.py
from mcp.server.fastmcp import FastMCP

# 创建 FastMCP 服务器实例
mcp = FastMCP("my-mcp-server")

@mcp.tool()
def hello(name: str) -> str:
    """一个简单的问候工具
    
    Args:
        name: 要问候的名字
    
    Returns:
        问候消息
    """
    return f"你好，{name}！"

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """加法计算器
    
    Args:
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        两个数字的和
    """
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """获取个性化问候语
    
    Args:
        name: 用户名字
    
    Returns:
        个性化的问候消息
    """
    return f"欢迎，{name}！这是一个动态资源示例。"

if __name__ == "__main__":
    # 运行服务器，使用stdio传输
    mcp.run()
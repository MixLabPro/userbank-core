# 个人画像数据管理系统 - FastMCP SSE模式

基于 FastMCP 2.0+ 的个人画像数据管理系统，使用 SSE (Server-Sent Events) 传输模式提供高效的实时通信。

## 🚀 特性

- **FastMCP 2.0+ 支持**: 使用最新的 FastMCP 框架
- **SSE 传输**: 高效的服务器推送事件通信
- **完整的个人画像管理**: 支持记忆、观点、洞察、目标等多维度数据
- **实时日志记录**: 详细的操作日志和错误处理
- **健康检查**: 内置的服务器状态监控
- **CORS 支持**: 支持跨域客户端连接

## 📋 系统要求

- Python 3.8+
- FastMCP 2.0+
- SQLite3 数据库

## 🛠️ 安装和设置

### 1. 安装依赖

```bash
# 安装SSE模式依赖
pip install -r requirements_sse.txt

# 或者手动安装主要依赖
pip install fastmcp>=2.0.0 uvicorn>=0.24.0 starlette>=0.27.0
```

### 2. 数据库初始化

确保 `profile_data.db` 数据库文件存在，或者系统会自动创建。

### 3. 启动服务器

```bash
# 启动SSE服务器
python main_sse.py
```

服务器将在以下地址启动：
- **主服务器**: http://localhost:8000
- **SSE端点**: http://localhost:8000/sse
- **健康检查**: http://localhost:8000/health

## 🔧 客户端连接

### 使用 FastMCP 客户端

```python
import asyncio
from fastmcp import Client

async def connect_to_server():
    # 方式1: 自动推断SSE传输（推荐）
    client = Client("http://localhost:8000/sse")
    
    # 方式2: 显式指定SSE传输
    from fastmcp.client.transports import SSETransport
    transport = SSETransport(url="http://localhost:8000/sse")
    client = Client(transport)
    
    async with client:
        # 健康检查
        result = await client.call_tool("ping")
        print(f"服务器状态: {result}")
        
        # 获取用户画像
        persona = await client.call_tool("get_persona")
        print(f"用户画像: {persona}")

# 运行客户端
asyncio.run(connect_to_server())
```

### 测试客户端

运行提供的测试客户端：

```bash
python test_sse_client.py
```

## 🛠️ 可用工具

### 核心工具

| 工具名称 | 描述 | 用途 |
|---------|------|------|
| `ping` | 健康检查 | 测试服务器连接状态 |
| `get_server_info` | 服务器信息 | 获取服务器统计和配置信息 |
| `get_persona` | 获取用户画像 | 获取当前用户的核心信息 |
| `save_persona` | 保存用户画像 | 更新用户的基本信息 |

### 数据管理工具

| 工具名称 | 描述 | 支持操作 |
|---------|------|----------|
| `manage_memories` | 记忆管理 | query, save |
| `manage_viewpoints` | 观点管理 | query, save |
| `manage_insights` | 洞察管理 | query, save |
| `manage_goals` | 目标管理 | query, save |
| `manage_preferences` | 偏好管理 | query, save |
| `manage_methodologies` | 方法论管理 | query, save |
| `manage_focuses` | 关注点管理 | query, save |
| `manage_predictions` | 预测管理 | query, save |

### 数据库工具

| 工具名称 | 描述 | 用途 |
|---------|------|------|
| `execute_custom_sql` | 执行SQL | 自定义数据库查询 |
| `get_table_schema` | 表结构信息 | 获取数据库表结构 |

## 📝 使用示例

### 1. 基本健康检查

```python
async with client:
    # 测试连接
    ping_result = await client.call_tool("ping")
    print(ping_result)
    # 输出: {"status": "healthy", "timestamp": "...", "server": "个人画像数据管理系统"}
```

### 2. 管理记忆数据

```python
async with client:
    # 查询记忆
    memories = await client.call_tool("manage_memories", {
        "action": "query",
        "limit": 10,
        "filter": {"memory_type": "学习"}
    })
    
    # 保存新记忆
    result = await client.call_tool("manage_memories", {
        "action": "save",
        "content": "学习了FastMCP的SSE传输模式",
        "memory_type": "学习",
        "importance": 8,
        "keywords": ["FastMCP", "SSE", "学习"]
    })
```

### 3. 获取服务器统计信息

```python
async with client:
    info = await client.call_tool("get_server_info")
    print(f"记忆数量: {info['statistics']['memories_count']}")
    print(f"目标数量: {info['statistics']['goals_count']}")
```

## 🔍 SSE 传输特性

### 优势

1. **实时通信**: 支持服务器主动推送数据
2. **高效连接**: 基于HTTP的长连接，减少握手开销
3. **自动重连**: 客户端自动处理连接断开和重连
4. **跨域支持**: 内置CORS支持，便于Web客户端连接

### 连接管理

```python
# 保持连接活跃（默认行为）
client = Client("http://localhost:8000/sse")  # keep_alive=True

# 每次使用新连接
from fastmcp.client.transports import SSETransport
transport = SSETransport(url="http://localhost:8000/sse")
client = Client(transport, keep_alive=False)
```

### 认证支持

```python
# 带认证头的连接
transport = SSETransport(
    url="http://localhost:8000/sse",
    headers={"Authorization": "Bearer your-token"}
)
client = Client(transport)
```

## 🐛 故障排除

### 常见问题

1. **连接失败**
   ```
   错误: 无法连接到服务器
   解决: 确保服务器已启动，检查端口8000是否被占用
   ```

2. **工具调用失败**
   ```
   错误: 工具执行失败
   解决: 检查服务器日志，确认参数格式正确
   ```

3. **数据库错误**
   ```
   错误: 数据库操作失败
   解决: 检查数据库文件权限，确认表结构完整
   ```

### 调试模式

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 服务器日志

服务器会输出详细的操作日志：

```
2024-01-01 12:00:00 - main_sse - INFO - 正在启动个人画像数据管理系统 - FastMCP SSE模式
2024-01-01 12:00:01 - main_sse - INFO - 成功初始化所有工具实例
2024-01-01 12:00:02 - main_sse - INFO - 记忆管理操作: query
```

## 🔄 与其他传输模式的比较

| 特性 | SSE | Streamable HTTP | Stdio |
|------|-----|-----------------|-------|
| 实时推送 | ✅ | ✅ | ❌ |
| 网络部署 | ✅ | ✅ | ❌ |
| 本地开发 | ✅ | ✅ | ✅ |
| 跨域支持 | ✅ | ✅ | ❌ |
| 连接开销 | 低 | 低 | 最低 |

## 📚 相关文档

- [FastMCP 官方文档](https://gofastmcp.com/)
- [SSE 传输文档](https://gofastmcp.com/clients/transports#sse-server-sent-events)
- [客户端使用指南](https://gofastmcp.com/clients/)

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

本项目采用 MIT 许可证。 
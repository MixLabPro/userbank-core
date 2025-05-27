# 个人画像数据管理系统 - SSE模式

这是个人画像数据管理系统的Server-Sent Events (SSE) 传输模式实现，基于Model Context Protocol (MCP)。

## 功能特性

- 支持SSE传输协议，适用于需要服务器到客户端流式传输的场景
- 完整的个人画像数据管理功能（信念、洞察、关注点、目标、偏好、决策、方法论）
- 安全的本地连接（防止DNS重绑定攻击）
- 健康检查端点
- CORS支持（仅限本地连接）

## 安装依赖

```bash
pip install -r requirements_sse.txt
```

## 启动服务器

### 方法1：使用启动脚本
```bash
python start_sse.py
```

### 方法2：直接运行
```bash
python main_sse.py
```

### 方法3：使用uvicorn
```bash
uvicorn main_sse:app --host 127.0.0.1 --port 8000
```

## 服务端点

启动后，服务器将在以下端点提供服务：

- **SSE连接**: `http://127.0.0.1:8000/sse`
- **消息端点**: `http://127.0.0.1:8000/messages` (POST)
- **健康检查**: `http://127.0.0.1:8000/health` (GET)

## 客户端连接示例

### Python客户端示例

```python
import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def main():
    async with sse_client("http://127.0.0.1:8000/sse") as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            # 初始化会话
            await session.initialize()
            
            # 调用工具
            result = await session.call_tool("add_belief", {
                "content": "持续学习是成长的关键",
                "related": ["学习", "成长"]
            })
            print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript客户端示例

```javascript
// 建立SSE连接
const eventSource = new EventSource('http://127.0.0.1:8000/sse');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('收到消息:', data);
};

// 发送消息到服务器
async function sendMessage(message) {
    const response = await fetch('http://127.0.0.1:8000/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(message)
    });
    return response.json();
}

// 调用工具示例
sendMessage({
    jsonrpc: "2.0",
    id: 1,
    method: "tools/call",
    params: {
        name: "add_belief",
        arguments: {
            content: "持续学习是成长的关键",
            related: ["学习", "成长"]
        }
    }
});
```

## 可用工具

系统提供以下工具函数：

### 数据添加
- `add_belief(content, related)` - 添加信念记录
- `add_insight(content, related)` - 添加洞察记录
- `add_focus(content, related)` - 添加关注点记录
- `add_long_term_goal(content, related)` - 添加长期目标记录
- `add_short_term_goal(content, related)` - 添加短期目标记录
- `add_preference(content, related)` - 添加偏好记录
- `add_decision(content, related)` - 添加决策记录
- `add_methodology(content, related)` - 添加方法论记录

### 数据管理
- `update_record(table_name, record_id, content, related)` - 更新记录
- `delete_record(table_name, record_id)` - 删除记录
- `get_record(table_name, record_id)` - 获取单条记录

### 数据查询
- `search_records(table_name, keyword, related_topic, limit, offset)` - 搜索记录
- `get_all_records(table_name, limit, offset)` - 获取表中所有记录
- `get_table_stats(table_name)` - 获取表统计信息
- `get_available_tables()` - 获取所有可用表
- `get_all_table_contents(include_empty, limit_per_table)` - 获取所有表内容
- `get_table_names_with_details()` - 获取表详细信息

### 数据导出
- `export_table_data(table_name, format)` - 导出表数据（支持JSON和CSV格式）

## 安全特性

1. **DNS重绑定攻击防护**: 验证Origin头，只允许本地连接
2. **本地绑定**: 服务器只绑定到127.0.0.1，不接受外部连接
3. **CORS限制**: 只允许本地域名的跨域请求
4. **错误处理**: 完善的错误处理和日志记录

## 与stdio模式的区别

| 特性 | stdio模式 | SSE模式 |
|------|-----------|---------|
| 传输方式 | 标准输入输出 | HTTP + Server-Sent Events |
| 适用场景 | 命令行工具、本地集成 | Web应用、远程访问 |
| 网络支持 | 否 | 是 |
| 流式传输 | 双向 | 服务器到客户端 |
| 安全性 | 进程隔离 | HTTP安全措施 |

## 故障排除

### 常见问题

1. **端口被占用**
   ```
   解决方案：修改main_sse.py中的端口号，或停止占用8000端口的进程
   ```

2. **CORS错误**
   ```
   解决方案：确保客户端从localhost或127.0.0.1访问服务器
   ```

3. **连接被拒绝**
   ```
   解决方案：检查Origin头是否为本地地址，确保服务器正在运行
   ```

### 调试模式

启动时添加调试参数：

```bash
python main_sse.py --log-level debug
```

或在代码中修改日志级别：

```python
logging.basicConfig(level=logging.DEBUG)
```

## 性能优化

1. **连接池**: 对于高并发场景，考虑使用连接池
2. **缓存**: 对频繁查询的数据添加缓存层
3. **分页**: 大量数据查询时使用分页参数
4. **索引**: 在数据库中为常用查询字段添加索引

## 扩展开发

要添加新的工具函数：

1. 在`main_sse.py`中定义新函数
2. 使用`@server.call_tool()`装饰器
3. 添加适当的错误处理
4. 更新文档

示例：

```python
@server.call_tool()
async def my_new_tool(param1: str, param2: int = 10) -> Dict[str, Any]:
    """我的新工具"""
    try:
        # 工具逻辑
        result = do_something(param1, param2)
        return {
            "success": True,
            "message": "操作成功",
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"操作失败: {str(e)}"
        }
``` 
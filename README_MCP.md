# 个人画像数据管理系统 MCP 服务器

基于标准 MCP (Model Context Protocol) Python SDK 的个人画像数据管理工具集。

## 功能特性

本MCP服务器提供以下功能：

### 数据管理工具
- **信念管理** (`add_belief`) - 添加个人信念记录
- **洞察管理** (`add_insight`) - 添加个人洞察记录  
- **关注点管理** (`add_focus`) - 添加关注点记录
- **目标管理** (`add_long_term_goal`, `add_short_term_goal`) - 管理长期和短期目标
- **偏好管理** (`add_preference`) - 添加个人偏好记录
- **决策管理** (`add_decision`) - 记录重要决策
- **方法论管理** (`add_methodology`) - 管理个人方法论

### 数据操作工具
- **记录更新** (`update_record`) - 更新现有记录
- **记录删除** (`delete_record`) - 删除指定记录
- **记录查询** (`get_record`) - 获取单条记录详情
- **记录搜索** (`search_records`) - 按关键词或主题搜索记录
- **批量查询** (`get_all_records`) - 获取表中所有记录

### 统计分析工具
- **表统计** (`get_table_stats`) - 获取表的统计信息
- **表信息** (`get_available_tables`) - 获取所有可用表的信息
- **完整内容** (`get_all_table_contents`) - 获取所有表的完整内容
- **详细信息** (`get_table_names_with_details`) - 获取表的详细信息

### 数据导出工具
- **数据导出** (`export_table_data`) - 导出表数据为JSON或CSV格式

## 安装和配置

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动服务器
```bash
python src/server.py
```

### 3. 在MCP客户端中配置

#### Claude Desktop 配置
在 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "profile-manager": {
      "command": "python",
      "args": ["path/to/your/project/src/server.py"]
    }
  }
}
```

#### Cursor 配置
在 Cursor 的 MCP 设置中添加服务器配置。

## 使用示例

### 添加信念记录
```json
{
  "tool": "add_belief",
  "arguments": {
    "content": "持续学习是个人成长的关键",
    "related": ["学习", "成长", "自我提升"]
  }
}
```

### 搜索记录
```json
{
  "tool": "search_records",
  "arguments": {
    "table_name": "belief",
    "keyword": "学习",
    "limit": 10
  }
}
```

### 获取统计信息
```json
{
  "tool": "get_table_stats",
  "arguments": {
    "table_name": "belief"
  }
}
```

## 数据表结构

系统包含以下8个数据表：

| 表名 | 中文名称 | 描述 |
|------|----------|------|
| `belief` | 信念 | 个人核心信念和价值观 |
| `insight` | 洞察 | 个人洞察和思考 |
| `focus` | 关注点 | 当前关注的重点领域 |
| `long_term_goal` | 长期目标 | 长期规划和目标 |
| `short_term_goal` | 短期目标 | 短期任务和目标 |
| `preference` | 偏好 | 个人喜好和偏好 |
| `decision` | 决策 | 重要决策记录 |
| `methodology` | 方法论 | 个人工作和生活方法论 |

## 技术架构

- **协议**: Model Context Protocol (MCP)
- **SDK**: 标准 MCP Python SDK
- **数据库**: SQLite (通过 database.py 模块)
- **传输**: STDIO 传输协议

## 开发说明

### 项目结构
```
src/
├── mcp_tools.py      # MCP工具定义和服务器实现
├── server.py         # 服务器启动脚本
├── database.py       # 数据库操作模块
└── ...
```

### 扩展功能
要添加新的工具，需要：

1. 在 `mcp_tools.py` 中添加实现函数
2. 在 `handle_list_tools()` 中注册工具定义
3. 在 `handle_call_tool()` 中添加工具调用逻辑

## 故障排除

### 常见问题

1. **导入错误**: 确保已安装正确版本的 `mcp` 包
2. **数据库错误**: 检查数据库文件权限和路径
3. **连接问题**: 确认MCP客户端配置正确

### 调试模式
可以直接运行 `python src/server.py` 来测试服务器启动。

## 许可证

本项目遵循相应的开源许可证。 
# 个人画像数据结构分类系统

🧠 **Personal Profile Data Structure Classification System**

基于FastMCP框架的个人画像数据管理工具，用于分类和管理个人思维模式和行为特征数据。

## 📋 项目概述

本项目实现了一个完整的个人画像数据分类系统，按照认知层、动机层和行为层的三层八类框架进行数据管理：

### 🏗️ 数据结构框架

#### 认知层 (Cognition Layer)
- **信念 (Belief)**: 对事物的本质、价值、关系或未来状态的判断性陈述
- **洞察 (Insight)**: 通过经历或深度思考获得的深层认识
- **关注点 (Focus)**: 注意力主动投放的领域、问题或主题

#### 动机层 (Motivation Layer)
- **长期目标 (Long-term Goal)**: 期望在较长时间周期内实现的抽象期望状态
- **短期目标 (Short-term Goal)**: 期望在近期实现的具体、可衡量的期望结果
- **偏好 (Preference)**: 个人在选择时的稳定倾向性

#### 行为层 (Action Layer)
- **决策 (Decision)**: 在特定场景下做出的具体选择
- **方法论 (Methodology)**: 实现目标的系统性路径或框架

## 🚀 功能特性

- ✅ **完整的数据库管理**: SQLite数据库，包含8个分类表
- ✅ **高性能索引**: 为内容、时间和主题字段创建索引
- ✅ **MCP工具集成**: 基于FastMCP的完整增删改查工具
- ✅ **详细日志记录**: 完整的操作日志和错误处理
- ✅ **类型安全**: 完整的类型注解和参数验证
- ✅ **异常处理**: 全面的try-catch错误处理机制

## 📦 安装和设置

### 前置要求
- Python 3.10+
- uv (推荐) 或 pip

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd profile
```

2. **安装依赖**
```bash
# 使用uv (推荐)
uv sync

# 或使用pip
pip install -r requirements.txt
```

3. **运行系统**
```bash
python main.py
```

## 🔧 MCP工具使用指南

### 添加数据工具

```python
# 添加信念记录
add_belief(content="AI的最大价值在于提升人类创造力", related=["技术", "未来", "创新"])

# 添加洞察记录
add_insight(content="经过三个月的实践，我发现正确的提示工程比模型选择更关键", related=["技术", "经验"])

# 添加长期目标
add_long_term_goal(content="希望成为AI领域的知识分享者", related=["职业", "技术"])
```

### 查询数据工具

```python
# 获取单条记录
get_record(table_name="belief", record_id=1)

# 搜索记录
search_records(table_name="belief", keyword="AI", limit=10)

# 获取所有记录
get_all_records(table_name="belief", limit=50)

# 获取统计信息
get_table_stats(table_name="belief")
```

### 更新和删除工具

```python
# 更新记录
update_record(table_name="belief", record_id=1, content="新的信念内容", related=["新主题"])

# 删除记录
delete_record(table_name="belief", record_id=1)
```

### 系统管理工具

```python
# 获取所有可用表
get_available_tables()

# 获取所有表的统计信息
get_table_stats()
```

## 📊 数据库结构

每个表都包含以下字段：

| 字段名 | 类型 | 描述 | 索引 |
|--------|------|------|------|
| id | INTEGER | 主键，自动递增 | PRIMARY KEY |
| content | TEXT | 记录内容 | ✅ |
| related | TEXT | 相关主题（JSON格式） | ✅ |
| created_time | TIMESTAMP | 创建时间 | ✅ |
| updated_time | TIMESTAMP | 更新时间 | - |

### 表列表

1. `belief` - 信念表
2. `insight` - 洞察表
3. `focus` - 关注点表
4. `long_term_goal` - 长期目标表
5. `short_term_goal` - 短期目标表
6. `preference` - 偏好表
7. `decision` - 决策表
8. `methodology` - 方法论表

## 🔍 使用示例

### 启动系统
```bash
python main.py
```

系统启动后会显示：
```
============================================================
🧠 个人画像数据结构分类系统
Personal Profile Data Structure Classification System
============================================================
📋 可用的数据表:
  • belief (信念)
  • insight (洞察)
  • focus (关注点)
  • long_term_goal (长期目标)
  • short_term_goal (短期目标)
  • preference (偏好)
  • decision (决策)
  • methodology (方法论)
============================================================
🔧 可用的MCP工具:
  • 添加工具: add_belief, add_insight, add_focus, etc.
  • 查询工具: get_record, search_records, get_all_records
  • 更新工具: update_record
  • 删除工具: delete_record
  • 统计工具: get_table_stats, get_available_tables
============================================================
🚀 MCP服务器正在启动...
📡 等待客户端连接...
```

### 通过MCP客户端使用

连接到MCP服务器后，可以使用所有提供的工具进行数据管理。

## 📁 项目结构

```
profile/
├── src/
│   ├── __init__.py          # 包初始化文件
│   ├── database.py          # 数据库管理模块
│   └── mcp_tools.py         # MCP工具模块
├── main.py                  # 主程序入口
├── pyproject.toml          # 项目配置文件
├── README.md               # 项目说明文档
├── profile_data.db         # SQLite数据库文件（运行时生成）
└── profile_system.log      # 系统日志文件（运行时生成）
```

## 🛠️ 开发和扩展

### 添加新的分类类型

1. 在 `database.py` 的 `tables` 列表中添加新表名
2. 在 `mcp_tools.py` 的 `TABLE_DESCRIPTIONS` 中添加描述
3. 创建对应的 `add_<table_name>` 工具函数

### 自定义数据库路径

```python
from src.database import ProfileDatabase

# 使用自定义数据库路径
db = ProfileDatabase("custom_path/my_profile.db")
```

## 🔧 故障排除

### 常见问题

#### 1. ModuleNotFoundError: No module named 'fastmcp'

**问题**: 启动时出现 `ModuleNotFoundError: No module named 'fastmcp'` 错误

**解决方案**:
```bash
# 确保使用 uv 运行项目
uv sync
uv run python main.py

# 或者使用提供的启动脚本
# Windows 批处理文件
start_mcp_server.bat

# PowerShell 脚本
.\start_mcp_server.ps1
```

#### 2. MCP 配置问题

**问题**: MCP 服务器无法连接

**解决方案**: 确保 `mcp_config.json` 使用正确的配置：
```json
{
  "mcpServers": {
    "profile-system": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "F:\\Github\\Profile",
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

#### 3. 虚拟环境问题

**问题**: Python 环境不正确

**解决方案**:
```bash
# 检查 uv 版本
uv --version

# 重新同步依赖
uv sync

# 验证 FastMCP 安装
uv run python -c "import fastmcp; print('FastMCP 版本:', fastmcp.__version__)"
```

#### 4. 权限问题

**问题**: 数据库文件无法创建或访问

**解决方案**:
- 确保项目目录有写入权限
- 检查防病毒软件是否阻止文件创建
- 尝试以管理员身份运行

### 启动脚本

项目提供了两个启动脚本：

1. **Windows 批处理文件** (`start_mcp_server.bat`)
   - 双击运行
   - 自动检查环境和依赖
   - 提供详细的状态信息

2. **PowerShell 脚本** (`start_mcp_server.ps1`)
   - 在 PowerShell 中运行: `.\start_mcp_server.ps1`
   - 彩色输出和更好的错误处理
   - 适合开发环境使用

### 测试工具

使用 `test_fastmcp.py` 验证 FastMCP 安装：
```bash
uv run python test_fastmcp.py
```

## 📝 日志和监控

系统会自动生成详细的日志文件 `profile_system.log`，包含：
- 系统启动和关闭信息
- 数据库操作记录
- 错误和异常信息
- MCP工具调用记录

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [FastMCP](https://gofastmcp.com/) - 提供了优秀的MCP框架
- [SQLite](https://sqlite.org/) - 轻量级数据库解决方案

---

**🧠 让数据管理变得智能而简单！**

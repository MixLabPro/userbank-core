# 个人画像数据库 MCP 服务器

## 📖 项目简介

这是一个基于 **Model Context Protocol (MCP)** 的个人画像数据库管理系统。该项目实现了一个功能完整的MCP服务器，专门用于管理和分析个人的思维模式、行为特征和认知数据。

### 🧠 核心理念

基于认知科学的**三层八类框架**，将个人数据按照认知层次进行分类管理：

**认知层 (Cognition Layer)**
- 🧭 **信念 (Beliefs)**: 对事物的判断性陈述和未来预测
- 💡 **洞察 (Insights)**: 通过经历获得的深层认识  
- 🎯 **关注点 (Focuses)**: 注意力投放的领域和主题

**动机层 (Motivation Layer)**
- 🚀 **长期目标 (Long-term Goals)**: 1年以上的抽象期望状态
- ⚡ **短期目标 (Short-term Goals)**: 1年内的具体可衡量目标
- ❤️ **偏好 (Preferences)**: 个人选择时的稳定倾向性

**行为层 (Action Layer)**
- 🤔 **决策 (Decisions)**: 特定场景下的具体选择
- 🛠️ **方法论 (Methodologies)**: 实现目标的系统性路径

## ✨ 主要功能

### 🔧 MCP工具集成
- `add_record`: 添加新记录到指定数据表
- `get_records`: 获取记录列表，支持分页和排序
- `search_records`: 智能搜索，支持跨表和关键词匹配
- `update_record`: 更新现有记录的内容和属性
- `delete_record`: 删除指定记录
- `get_statistics`: 获取详细的数据库统计信息
- `get_recent_records`: 获取最近时间段的记录
- `analyze_patterns`: 数据模式分析（情绪分布、主题频率、时间趋势等）

### 📊 数据分析功能
- **情绪分布分析**: 统计不同情绪标签的分布情况
- **主题频率分析**: 识别最常出现的主题和关键词
- **时间趋势分析**: 分析记录创建的时间模式
- **目标进度分析**: 跟踪长短期目标的完成状态

### 🗄️ 数据管理特性
- **完整的CRUD操作**: 支持增删改查所有操作
- **智能搜索**: 内容和标签的全文搜索
- **数据验证**: 输入数据的格式和类型验证
- **性能优化**: SQLite数据库索引优化
- **详细日志**: 完整的操作日志和错误处理

## 🛠️ 技术栈

- **Python 3.8+**: 主要编程语言
- **MCP 1.9.1+**: Model Context Protocol 核心库
- **FastMCP**: 快速MCP服务器框架
- **SQLite**: 轻量级数据库存储
- **Pydantic**: 数据验证和序列化
- **Uvicorn**: ASGI服务器支持

## 📦 安装说明

### 1. 克隆项目

```bash
git clone <your-repository-url>
cd <project-directory>
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv mcp-env

# 激活虚拟环境
# Windows
mcp-env\Scripts\activate
# macOS/Linux
source mcp-env/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 🚀 使用方法

### 方式一：启动MCP服务器

```bash
# 使用启动脚本（推荐）
python run_server.py

# 或直接运行服务器
python src/server.py
```

启动后会看到详细的服务器信息：
```
============================================================
个人画像数据库MCP服务器
============================================================
服务器名称: personal-profile-db
服务器版本: 1.0.0
数据库路径: personal_profile.db
日志级别: INFO
开发模式: 否
支持的表: beliefs, insights, focuses, long_term_goals, short_term_goals, preferences, decisions, methodologies
支持的分析类型: emotion_distribution, topic_frequency, time_trends, goal_progress

可用的MCP工具:
  • add_record - 添加新记录
  • get_records - 获取记录列表
  • search_records - 搜索记录
  • update_record - 更新记录
  • delete_record - 删除记录
  • get_statistics - 获取统计信息
  • get_recent_records - 获取最近记录
  • analyze_patterns - 分析数据模式
============================================================
```

### 方式二：直接使用Python API

```python
from src.database import PersonalProfileDatabase

# 初始化数据库
db = PersonalProfileDatabase()

# 添加信念记录
belief_data = {
    "content": "持续学习是成功的关键",
    "related": ["学习", "成长", "成功"],
    "emotion": "积极"
}
record_id = db.insert_record("beliefs", belief_data)
print(f"添加记录成功，ID: {record_id}")

# 搜索相关记录
results = db.search_records("all", "学习")
print(f"找到 {len(results)} 条相关记录")
```

### 方式三：运行测试验证

```bash
# 运行完整测试套件
python run_tests.py

# 运行简单环境测试
python test.py
```

## 📋 MCP工具详细说明

### 1. add_record - 添加记录
```json
{
  "tool": "add_record",
  "arguments": {
    "table_name": "belief",
    "content": "AI将改变未来的工作方式",
    "related": ["AI", "未来", "工作"],
    "emotion": "积极",
    "extra_fields": {
      "confidence": 8
    }
  }
}
```

### 2. search_records - 搜索记录
```json
{
  "tool": "search_records",
  "arguments": {
    "keyword": "学习",
    "table_name": "all",
    "limit": 20
  }
}
```

### 3. get_statistics - 获取统计信息
```json
{
  "tool": "get_statistics",
  "arguments": {}
}
```

### 4. analyze_patterns - 数据分析
```json
{
  "tool": "analyze_patterns",
  "arguments": {
    "analysis_type": "emotion_distribution",
    "time_range": 30
  }
}
```

支持的分析类型：
- `emotion_distribution`: 情绪分布分析
- `topic_frequency`: 主题频率分析
- `time_trends`: 时间趋势分析
- `goal_progress`: 目标进度分析

## 📁 项目结构

```
.
├── README.md                           # 项目说明文档
├── QUICK_START.md                      # 快速开始指南
├── README_DATABASE.md                  # 数据库详细文档
├── requirements.txt                    # Python依赖包列表
├── run_server.py                       # MCP服务器启动脚本
├── run_tests.py                        # 测试运行脚本
├── test.py                            # 简单环境测试
├── personal_profile.db                 # SQLite数据库文件
├── sample_personal_profile_export.json # 示例数据导出
├── src/                               # 源代码目录
│   ├── server.py                      # MCP服务器主文件
│   ├── database.py                    # 数据库操作类
│   ├── config.py                      # 配置文件
│   └── test_database.py               # 数据库测试
└── mcp-env/                           # Python虚拟环境
```

## 🗃️ 数据表结构

| 表名 | 中文名 | 用途 | 特殊字段 |
|------|--------|------|----------|
| beliefs | 信念 | 存储对事物的判断和预测 | - |
| insights | 洞察 | 存储通过经历获得的认识 | - |
| focuses | 关注点 | 存储关注的领域和主题 | - |
| long_term_goals | 长期目标 | 存储1年以上的目标 | status |
| short_term_goals | 短期目标 | 存储1年内的目标 | status, deadline |
| preferences | 偏好 | 存储个人选择倾向 | strength (1-10) |
| decisions | 决策 | 存储具体的选择 | context, outcome |
| methodologies | 方法论 | 存储系统性的方法 | category, effectiveness (1-10) |

### 通用字段说明
- `id`: 主键，自动递增
- `content`: 记录内容（必填）
- `related`: 相关主题标签（JSON数组格式）
- `emotion`: 情绪标签（积极/消极/中性/非常积极/非常消极）
- `create_time`: 创建时间（自动生成）
- `update_time`: 更新时间（自动更新）

## 🔧 开发指南

### 添加新的MCP工具

```python
@mcp.tool()
def your_new_tool(param1: str, param2: int) -> str:
    """
    工具描述
    
    Args:
        param1: 参数1描述
        param2: 参数2描述
    
    Returns:
        返回值描述
    """
    try:
        # 工具逻辑实现
        result = f"处理结果: {param1} - {param2}"
        logger.info(f"工具执行成功: {result}")  # 日志输出
        return json.dumps({
            "success": True,
            "result": result
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"工具执行错误: {e}")  # 错误日志
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)
```

### 扩展数据库表

1. 在 `src/database.py` 的 `init_database()` 方法中添加新表
2. 在 `src/server.py` 的 `TABLE_MAPPING` 中添加表名映射
3. 在 `src/config.py` 中更新配置信息

### 自定义配置

编辑 `src/config.py` 文件来修改：
- 数据库路径
- 查询限制
- 验证规则
- 分析参数

## 🐛 故障排除

### 常见问题

1. **导入错误**: 确保已激活虚拟环境并安装所有依赖
   ```bash
   pip install -r requirements.txt
   ```

2. **数据库锁定**: 确保没有其他程序占用数据库文件
   ```bash
   # 检查数据库文件权限
   ls -la personal_profile.db
   ```

3. **MCP连接问题**: 检查MCP客户端配置和服务器启动状态

4. **权限问题**: 确保对项目目录有读写权限

### 调试模式

启用详细日志输出：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

或设置环境变量：
```bash
export LOG_LEVEL=DEBUG
python run_server.py
```

### 重置数据库

```bash
# 备份现有数据（可选）
cp personal_profile.db personal_profile_backup.db

# 删除数据库文件
rm personal_profile.db

# 重新启动服务器会自动创建新数据库
python run_server.py
```

## 📊 使用示例

### 完整的工作流程示例

```python
from src.database import PersonalProfileDatabase

# 1. 初始化数据库
db = PersonalProfileDatabase()

# 2. 添加不同类型的记录
# 添加信念
belief = {
    "content": "技术应该服务于人类的福祉",
    "related": ["技术", "人文", "价值观"],
    "emotion": "积极"
}
db.insert_record("beliefs", belief)

# 添加短期目标
goal = {
    "content": "本季度学习完成Python高级编程",
    "related": ["学习", "Python", "编程"],
    "emotion": "积极",
    "status": "active",
    "deadline": "2024-06-30"
}
db.insert_record("short_term_goals", goal)

# 添加方法论
method = {
    "content": "使用费曼学习法深度理解概念",
    "related": ["学习方法", "理解", "教学"],
    "emotion": "积极",
    "category": "学习方法",
    "effectiveness": 9
}
db.insert_record("methodologies", method)

# 3. 搜索和分析
# 搜索学习相关的记录
learning_records = db.search_records("all", "学习")
print(f"学习相关记录: {len(learning_records)} 条")

# 获取统计信息
stats = db.get_statistics()
print("数据库统计:", stats)

# 4. 数据分析（通过MCP工具）
# 这需要通过MCP客户端调用analyze_patterns工具
```

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范
- 使用中文注释和文档字符串
- 遵循PEP 8代码风格
- 添加适当的错误处理和日志记录
- 为新功能编写测试用例

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 🐛 Issues: [GitHub Issues](https://github.com/your-username/your-repo/issues)
- 📧 Email: your-email@example.com

## 🙏 致谢

感谢以下开源项目的支持：

- [Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk) - MCP协议实现
- [FastMCP](https://github.com/jlowin/fastmcp) - 快速MCP服务器框架
- [Pydantic](https://github.com/pydantic/pydantic) - 数据验证库
- [SQLite](https://www.sqlite.org/) - 轻量级数据库引擎

## 📚 相关文档

- 📖 [快速开始指南](QUICK_START.md) - 5分钟快速上手
- 🗄️ [数据库详细文档](README_DATABASE.md) - 完整的数据库说明
- 🧪 [测试文档](run_tests.py) - 测试用例和验证
- ⚙️ [配置说明](src/config.py) - 详细的配置选项

---

⭐ 如果这个项目对您有帮助，请给它一个星标！

🚀 **开始使用**: `python run_server.py`

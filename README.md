# UserBank Core

<div align="center">
  
**个人数据银行的核心实现**

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-1.9+-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*从"数据寄存在各个平台" 到 "拥有自己的数据银行"*

[快速开始](#-快速开始) • [核心功能](#-核心功能) • [使用指南](#-使用指南) • [API参考](#-api参考) • [开发指南](#-开发指南)

</div>

---

## 🎯 什么是UserBank Core？

UserBank 全称是**Unified Smart Experience Records Bank**，基于**MCP（Model Context Protocol）** 构建的个人数据管理系统。作为UserBank的核心实现，UserBank Core让你能够统一管理与AI交互产生的所有智能经验记录。通过标准化的MCP接口，任何支持MCP的AI应用都可以安全、一致地访问你的个人数据。

### 解决的问题

当你与不同AI助手（Claude、ChatGPT等）交互时，数据分散存储：

```
现状：数据分散 ❌
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Claude    │  │   ChatGPT   │  │   其他AI    │
│ 你的记忆A   │  │ 你的记忆B   │  │ 你的记忆C   │
│ 你的偏好A   │  │ 你的偏好B   │  │ 你的偏好C   │
└─────────────┘  └─────────────┘  └─────────────┘
```

### UserBank Core解决方案

```
UserBank Core：统一智能体验记录引擎 ✅
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Claude    │     │   ChatGPT   │     │   其他AI    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │      MCP协议      │      MCP协议      │
       │      标准接口     │      标准接口     │
       └───────────────────┼───────────────────┘
                          │
                  ┌───────▼────────┐
                  │   UserBank     │
                  │     Core       │
                  │ ┌─────────────┐ │
                  │ │ 统一的记忆  │ │
                  │ │ 完整的偏好  │ │
                  │ │ 所有观点    │ │
                  │ │ 目标计划    │ │
                  │ │ 方法论等    │ │
                  │ └─────────────┘ │
                  └────────────────┘
```

## ✨ 核心功能

### 🏗️ 核心引擎特性
- **MCP原生支持**：深度集成Model Context Protocol，提供标准化数据访问
- **轻量级部署**：最小化依赖，快速启动智能体验记录银行

### 🔐 真正的数据主权
- **你的数据存储在你控制的地方**，不是平台的"寄存品"
- **完整导出**：一键导出所有数据，包含元数据
- **标准化访问**：通过MCP协议实现安全、一致的数据访问

### 🗃️ 9种数据类型管理
- **👤 Persona**: 个人基本信息和身份档案
- **🧠 Memory**: AI交互记忆，支持6种类型分类
- **💭 Viewpoint**: 个人观点和立场记录
- **💡 Insight**: 深度洞察和感悟
- **🎯 Goal**: 目标管理，支持长短期规划
- **❤️ Preference**: 个人偏好设置
- **🛠️ Methodology**: 个人方法论和最佳实践
- **🔍 Focus**: 当前关注点和优先级管理
- **🔮 Prediction**: 预测记录和验证追踪

### 🔐 隐私控制
- **简化权限模型**: `public` / `private` 两级权限
- **数据完全自控**: 所有数据存储在你的本地SQLite数据库
- **选择性共享**: 可以精确控制哪些数据对AI可见

### 🔄 MCP标准化接口
- **统一访问方式**: 所有AI应用通过相同的MCP工具访问数据
- **实时数据同步**: 支持多个AI应用同时访问最新数据
- **标准化操作**: 查询、保存、更新等操作完全标准化

## 🚀 快速开始

### 环境要求

- Python 3.13+
- 支持MCP的AI应用（如Claude Desktop等）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/MixLabPro/userbank-core.git
cd userbank-core
```

2. **安装依赖**
```bash
# 使用uv（推荐）
uv sync

# 或使用pip
pip install -r requirements.txt
```

3. **配置数据库路径**
编辑 `config.json` 文件：
```json
{
  "database": {
    "path": "你的数据库存储路径",
    "filename": "profile_data.db"
  },
  "server": {
    "port": 2333,
    "host": "0.0.0.0"
  }
}
```

4. **启动MCP服务器**
```bash
# 标准模式
python main.py

# 或SSE模式（支持服务器推送事件）
python main_sse.py
```

5. **配置AI应用连接**
在支持MCP的AI应用中添加服务器配置：
```json
{
    "mcpServers": {
      "userbank": {
        "command": "uv",
        "args": [
          "run",
          "--with",
          "mcp",
          "mcp",
          "run",
          "F:/Github/userbank/main.py"
        ]
      }
    }
  }
```

### 初始化个人档案

首次使用时，建议先设置基本的个人信息：

```python
# 通过MCP工具调用
save_persona(
    name="你的姓名",
    personality="你的性格描述",
    bio="个人简介"
)
```

## 📊 数据模型详解

### 👤 Persona - 个人档案
```typescript
interface Persona {
  id: 1;                     // 固定为1（系统只维护一个档案）
  name: string;              // 姓名
  gender?: string;           // 性别
  personality?: string;      // 性格描述
  avatar_url?: string;       // 头像链接
  bio?: string;              // 个人简介
  privacy_level: 'public' | 'private';
}
```

### 🧠 Memory - 记忆管理
```typescript
interface Memory {
  content: string;           // 记忆内容
  memory_type: 'experience' | 'event' | 'learning' | 'interaction' | 'achievement' | 'mistake';
  importance: number;        // 1-10重要程度评级
  related_people?: string;   // 相关人员
  location?: string;         // 发生地点
  memory_date?: string;      // 具体日期
  keywords: string[];        // 关键词标签
  source_app: string;        // 数据来源应用
  reference_urls?: string[]; // 相关链接
  privacy_level: 'public' | 'private';
}
```

### 💭 Viewpoint - 观点立场
```typescript
interface Viewpoint {
  content: string;           // 观点内容
  source_people?: string;    // 观点来源人员
  related_event?: string;    // 相关事件
  keywords: string[];        // 关键词
  reference_urls?: string[]; // 参考链接
  privacy_level: 'public' | 'private';
}
```

### 🎯 Goal - 目标管理
```typescript
interface Goal {
  content: string;           // 目标内容
  type: 'long_term' | 'short_term' | 'plan' | 'todo';
  deadline?: string;         // 截止日期
  status: 'planning' | 'in_progress' | 'completed' | 'abandoned';
  keywords: string[];        // 关键词
  privacy_level: 'public' | 'private';
}
```

## 🛠️ 使用指南

### 基本操作示例

#### 1. 添加记忆
```python
# 通过MCP工具
manage_memories(
    action="save",
    content="今天学习了Rust的所有权概念，理解了借用检查器的工作原理",
    memory_type="learning",
    importance=8,
    keywords=["Rust", "所有权", "借用检查器", "编程语言"],
    related_people="技术导师张老师"
)
```

#### 2. 查询记忆
```python
# 查询学习相关的重要记忆
manage_memories(
    action="query",
    filter={
        "memory_type": ["learning"],
        "importance": {"gte": 7}
    },
    limit=10
)
```

#### 3. 设置目标
```python
manage_goals(
    action="save",
    content="3个月内完成Rust项目重构",
    type="short_term",
    deadline="2024-06-01",
    status="planning",
    keywords=["Rust", "重构", "项目管理"]
)
```

#### 4. 记录观点
```python
manage_viewpoints(
    action="save",
    content="我认为代码可读性比性能优化更重要，除非性能成为明显瓶颈",
    keywords=["编程哲学", "代码质量", "性能优化"],
    related_event="团队代码评审讨论"
)
```

### 高级查询功能

#### 复杂条件查询
```python
# 查询最近一周的重要学习记忆
manage_memories(
    action="query",
    filter={
        "and": [
            {"memory_type": ["learning", "experience"]},
            {"importance": {"gte": 7}},
            {"created_time": {"gte": "2024-03-01"}},
            {"keywords": {"contains": "编程"}}
        ]
    },
    sort_by="importance",
    sort_order="desc",
    limit=20
)
```

#### 关联数据查询
```python
# 查询与特定目标相关的所有数据
execute_custom_sql(
    sql="""
    SELECT m.content, m.memory_type, m.importance 
    FROM memory m 
    WHERE m.keywords LIKE '%Rust%' 
    ORDER BY m.importance DESC
    """,
    fetch_results=True
)
```

## 🔧 API参考

### MCP工具列表

| 工具名称 | 功能描述 | 主要参数 |
|---------|---------|---------|
| **基础信息** |
| `get_persona()` | 获取个人档案信息 | - |
| `save_persona()` | 更新个人档案 | name, gender, personality, bio |
| **数据管理** |
| `manage_memories()` | 记忆数据管理 | action, content, memory_type, importance |
| `manage_viewpoints()` | 观点数据管理 | action, content, keywords |
| `manage_goals()` | 目标数据管理 | action, content, type, deadline, status |
| `manage_preferences()` | 偏好数据管理 | action, content, context |
| `manage_insights()` | 洞察数据管理 | action, content, keywords |
| `manage_methodologies()` | 方法论管理 | action, content, type, effectiveness |
| `manage_focuses()` | 关注点管理 | action, content, priority, status |
| `manage_predictions()` | 预测记录管理 | action, content, timeframe, basis |
| **数据库操作** |
| `execute_custom_sql()` | 执行自定义SQL | sql, params, fetch_results |
| `get_table_schema()` | 获取表结构信息 | table_name |

### 查询过滤器语法

```python
# 基本过滤器
filter = {
    "memory_type": ["learning", "experience"],  # 包含匹配
    "importance": {"gte": 7},                   # 大于等于
    "created_time": {"gte": "2024-01-01"}      # 日期范围
}

# 复合条件
filter = {
    "and": [
        {"importance": {"gte": 8}},
        {"keywords": {"contains": "编程"}},
        {"privacy_level": {"ne": "private"}}
    ]
}

# 支持的操作符
# eq: 等于, ne: 不等于, gt: 大于, gte: 大于等于
# lt: 小于, lte: 小于等于, contains: 包含, in: 在列表中
```

## 🎭 使用场景

### 场景1：跨平台对话延续

**问题**: 昨天在ChatGPT讨论项目架构，今天想在Claude继续

**解决方案**:
```python
# Claude通过MCP自动检索相关上下文
memories = manage_memories(
    action="query",
    filter={
        "keywords": {"contains": "架构"},
        "memory_date": {"gte": "yesterday"},
        "memory_type": ["interaction", "learning"]
    }
)
# Claude现在可以无缝继续昨天的讨论
```

### 场景2：个性化学习辅导

**问题**: 希望AI了解我的学习进度和偏好

**解决方案**:
```python
# AI获取学习背景
persona = get_persona()
learning_history = manage_memories(
    action="query",
    filter={
        "memory_type": ["learning"],
        "keywords": {"contains": "Rust"}
    }
)
# AI基于你的背景定制教学内容
```

### 场景3：目标追踪和复盘

**问题**: 想要系统地管理和追踪个人目标

**解决方案**:
```python
# 设置目标
manage_goals(
    action="save",
    content="掌握Rust异步编程",
    type="short_term",
    deadline="2024-05-01"
)

# 记录学习进展
manage_memories(
    action="save",
    content="完成了tokio基础教程，理解了async/await概念",
    memory_type="learning",
    importance=7,
    keywords=["Rust", "异步编程", "tokio"]
)

# 定期复盘
goals = manage_goals(
    action="query",
    filter={"status": ["in_progress"]}
)
```

## 🔒 隐私和安全

### 数据控制
- **本地存储**: 所有数据存储在你控制的SQLite数据库中
- **完全导出**: 支持完整的数据导出和备份
- **选择性访问**: 可以精确控制哪些数据对AI应用可见


## 🏗️ 开发指南

### 项目结构
```
userbank-core/
├── main.py              # MCP服务器主入口
├── main_sse.py          # SSE模式服务器
├── config.json          # 配置文件
├── config_manager.py    # 配置管理器
├── requirements.txt     # 依赖列表
├── Database/
│   ├── database.py      # 数据库操作类
│   └── __init__.py
├── tools/               # MCP工具模块
│   ├── base.py          # 基础工具类
│   ├── persona_tools.py # 个人档案工具
│   ├── memory_tools.py  # 记忆管理工具
│   ├── viewpoint_tools.py # 观点管理工具
│   ├── goal_tools.py    # 目标管理工具
│   └── ...              # 其他工具模块
└── README.md
```

## 🤝 贡献指南

作为UserBank生态系统的核心组件，我们欢迎各种形式的贡献：

1. **核心功能改进**: 提交新功能或改进现有核心功能
2. **Bug修复**: 报告和修复发现的问题
3. **文档完善**: 改进文档和使用指南
4. **测试用例**: 添加测试用例提高代码质量（见roadmap v0.2.0）
5. **性能优化**: 优化数据库查询和系统性能
6. **生态集成**: 帮助构建UserBank生态系统的其他组件

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/MixLabPro/userbank-core.git
cd userbank-core

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装开发依赖
pip install -r requirements.txt
pip install -e .

# 启动开发服务器
python main.py
```

## 📚 相关资源

- **MCP协议文档**: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Claude Desktop MCP配置**: [Claude MCP Guide](https://docs.anthropic.com/claude/docs/mcp)
- **SQLite文档**: [https://sqlite.org/docs.html](https://sqlite.org/docs.html)
- **FastMCP框架**: [https://github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp)

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">
  
**让AI真正了解你，从拥有自己的数据开始**

*UserBank Core - 存储一次，AI处处可用*

[GitHub](https://github.com/your-username/userbank-core) • [Issues](https://github.com/your-username/userbank-core/issues) • [Discussions](https://github.com/your-username/userbank-core/discussions)

</div>
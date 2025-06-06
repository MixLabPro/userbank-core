# UserBank Core

<div align="center">
  
**Core Implementation of Personal Data Bank**

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-1.9+-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

*From "Data Hosted on Various Platforms" to "Owning Your Own Data Bank"*

[Quick Start](#-quick-start) • [Core Features](#-core-features) • [Usage Guide](#-usage-guide) • [API Reference](#-api-reference) • [Development Guide](#-development-guide)• [中文版](./README-zh.md)

</div>

---

## 🎯 What is UserBank Core?

UserBank stands for **Unified Smart Experience Records Bank**, a personal data management system built on **MCP (Model Context Protocol)**. As the core implementation of UserBank, UserBank Core enables you to uniformly manage all intelligent experience records generated from AI interactions. Through standardized MCP interfaces, any AI application that supports MCP can securely and consistently access your personal data.

### Problems Solved

When you interact with different AI assistants (Claude, ChatGPT, etc.), data is scattered across platforms:

```
Current State: Scattered Data ❌
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Claude    │  │   ChatGPT   │  │  Other AI   │
│ Your Memory A│  │ Your Memory B│  │ Your Memory C│
│ Your Pref A  │  │ Your Pref B  │  │ Your Pref C  │
└─────────────┘  └─────────────┘  └─────────────┘
```

### UserBank Core Solution

```
UserBank Core: Unified Intelligent Experience Record Engine ✅
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Claude    │     │   ChatGPT   │     │  Other AI   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │   MCP Protocol    │   MCP Protocol    │
       │ Standard Interface│ Standard Interface│
       └───────────────────┼───────────────────┘
                          │
                  ┌───────▼────────┐
                  │   UserBank     │
                  │     Core       │
                  │ ┌─────────────┐ │
                  │ │ Unified     │ │
                  │ │ Memories    │ │
                  │ │ Complete    │ │
                  │ │ Preferences │ │
                  │ │ All Views   │ │
                  │ │ Goals Plans │ │
                  │ │ Methods etc │ │
                  │ └─────────────┘ │
                  └────────────────┘
```

## ✨ Core Features

### 🏗️ Core Engine Features
- **Native MCP Support**: Deep integration with Model Context Protocol, providing standardized data access
- **Lightweight Deployment**: Minimal dependencies, quick startup for intelligent experience record bank

### 🔐 True Data Sovereignty
- **Your data is stored where you control it**, not as "deposits" on platforms
- **Complete Export**: One-click export of all data, including metadata
- **Standardized Access**: Secure, consistent data access through MCP protocol

### 🗃️ 9 Data Type Management
- **👤 Persona**: Personal basic information and identity profile
- **🧠 Memory**: AI interaction memories, supporting 6 type classifications
- **💭 Viewpoint**: Personal opinions and stance records
- **💡 Insight**: Deep insights and realizations
- **🎯 Goal**: Goal management, supporting long and short-term planning
- **❤️ Preference**: Personal preference settings
- **🛠️ Methodology**: Personal methodologies and best practices
- **🔍 Focus**: Current focus points and priority management
- **🔮 Prediction**: Prediction records and verification tracking

### 🔐 Privacy Control
- **Simplified Permission Model**: `public` / `private` two-level permissions
- **Complete Data Self-Control**: All data stored in your local SQLite database
- **Selective Sharing**: Precise control over which data is visible to AI

### 🔄 MCP Standardized Interface
- **Unified Access Method**: All AI applications access data through the same MCP tools
- **Real-time Data Sync**: Support for multiple AI applications accessing latest data simultaneously
- **Standardized Operations**: Query, save, update operations are completely standardized

## 🚀 Quick Start

### Requirements

- Python 3.13+
- AI applications that support MCP (such as Claude Desktop, etc.)

### Installation Steps

1. **Clone the Project**
```bash
git clone https://github.com/MixLabPro/userbank-core.git
cd userbank-core
```

2. **Install Dependencies**
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

3. **Configure Database Path**
Edit the `config.json` file:
```json
{
  "database": {
    "path": "your_database_storage_path",
    "filename": "profile_data.db"
  },
  "server": {
    "port": 8088,
    "host": "0.0.0.0"
  }
}
```

4. **Start MCP Server**
```bash
# Standard mode
python main.py

# Or SSE mode (supports Server-Sent Events)
python main_sse.py
```

5. **Configure AI Application Connection**
Add server configuration in MCP-supporting AI applications:
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

### Initialize Personal Profile

For first-time use, it's recommended to set basic personal information:

```python
# Through MCP tool call
save_persona(
    name="Your Name",
    personality="Your personality description",
    bio="Personal bio"
)
```

## 📊 Data Model Details

### 👤 Persona - Personal Profile
```typescript
interface Persona {
  id: 1;                     // Fixed as 1 (system maintains only one profile)
  name: string;              // Name
  gender?: string;           // Gender
  personality?: string;      // Personality description
  avatar_url?: string;       // Avatar URL
  bio?: string;              // Personal bio
  privacy_level: 'public' | 'private';
}
```

### 🧠 Memory - Memory Management
```typescript
interface Memory {
  content: string;           // Memory content
  memory_type: 'experience' | 'event' | 'learning' | 'interaction' | 'achievement' | 'mistake';
  importance: number;        // 1-10 importance rating
  related_people?: string;   // Related people
  location?: string;         // Location
  memory_date?: string;      // Specific date
  keywords: string[];        // Keyword tags
  source_app: string;        // Source application
  reference_urls?: string[]; // Related links
  privacy_level: 'public' | 'private';
}
```

### 💭 Viewpoint - Opinions and Stances
```typescript
interface Viewpoint {
  content: string;           // Viewpoint content
  source_people?: string;    // Source person
  related_event?: string;    // Related event
  keywords: string[];        // Keywords
  reference_urls?: string[]; // Reference links
  privacy_level: 'public' | 'private';
}
```

### 🎯 Goal - Goal Management
```typescript
interface Goal {
  content: string;           // Goal content
  type: 'long_term' | 'short_term' | 'plan' | 'todo';
  deadline?: string;         // Deadline
  status: 'planning' | 'in_progress' | 'completed' | 'abandoned';
  keywords: string[];        // Keywords
  privacy_level: 'public' | 'private';
}
```

## 🛠️ Usage Guide

### Basic Operation Examples

#### 1. Adding Memory
```python
# Through MCP tool
manage_memories(
    action="save",
    content="Today I learned Rust's ownership concept and understood how the borrow checker works",
    memory_type="learning",
    importance=8,
    keywords=["Rust", "ownership", "borrow checker", "programming language"],
    related_people="Technical mentor Teacher Zhang"
)
```

#### 2. Querying Memory
```python
# Query important learning-related memories
manage_memories(
    action="query",
    filter={
        "memory_type": ["learning"],
        "importance": {"gte": 7}
    },
    limit=10
)
```

#### 3. Setting Goals
```python
manage_goals(
    action="save",
    content="Complete Rust project refactoring within 3 months",
    type="short_term",
    deadline="2024-06-01",
    status="planning",
    keywords=["Rust", "refactoring", "project management"]
)
```

#### 4. Recording Viewpoints
```python
manage_viewpoints(
    action="save",
    content="I believe code readability is more important than performance optimization, unless performance becomes an obvious bottleneck",
    keywords=["programming philosophy", "code quality", "performance optimization"],
    related_event="Team code review discussion"
)
```

### Advanced Query Features

#### Complex Conditional Queries
```python
# Query important learning memories from the past week
manage_memories(
    action="query",
    filter={
        "and": [
            {"memory_type": ["learning", "experience"]},
            {"importance": {"gte": 7}},
            {"created_time": {"gte": "2024-03-01"}},
            {"keywords": {"contains": "programming"}}
        ]
    },
    sort_by="importance",
    sort_order="desc",
    limit=20
)
```

#### Related Data Queries
```python
# Query all data related to specific goals
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

## 🔧 API Reference

### MCP Tool List

| Tool Name | Function Description | Main Parameters |
|-----------|---------------------|-----------------|
| **Basic Information** |
| `get_persona()` | Get personal profile information | - |
| `save_persona()` | Update personal profile | name, gender, personality, bio |
| **Data Management** |
| `manage_memories()` | Memory data management | action, content, memory_type, importance |
| `manage_viewpoints()` | Viewpoint data management | action, content, keywords |
| `manage_goals()` | Goal data management | action, content, type, deadline, status |
| `manage_preferences()` | Preference data management | action, content, context |
| `manage_insights()` | Insight data management | action, content, keywords |
| `manage_methodologies()` | Methodology management | action, content, type, effectiveness |
| `manage_focuses()` | Focus management | action, content, priority, status |
| `manage_predictions()` | Prediction record management | action, content, timeframe, basis |
| **Database Operations** |
| `execute_custom_sql()` | Execute custom SQL | sql, params, fetch_results |
| `get_table_schema()` | Get table structure information | table_name |

### Query Filter Syntax

```python
# Basic filters
filter = {
    "memory_type": ["learning", "experience"],  # Include matching
    "importance": {"gte": 7},                   # Greater than or equal
    "created_time": {"gte": "2024-01-01"}      # Date range
}

# Compound conditions
filter = {
    "and": [
        {"importance": {"gte": 8}},
        {"keywords": {"contains": "programming"}},
        {"privacy_level": {"ne": "private"}}
    ]
}

# Supported operators
# eq: equals, ne: not equals, gt: greater than, gte: greater than or equal
# lt: less than, lte: less than or equal, contains: contains, in: in list
```

## 🎭 Use Cases

### Scenario 1: Cross-Platform Conversation Continuation

**Problem**: Discussed project architecture in ChatGPT yesterday, want to continue in Claude today

**Solution**:
```python
# Claude automatically retrieves relevant context through MCP
memories = manage_memories(
    action="query",
    filter={
        "keywords": {"contains": "architecture"},
        "memory_date": {"gte": "yesterday"},
        "memory_type": ["interaction", "learning"]
    }
)
# Claude can now seamlessly continue yesterday's discussion
```

### Scenario 2: Personalized Learning Assistance

**Problem**: Want AI to understand my learning progress and preferences

**Solution**:
```python
# AI gets learning background
persona = get_persona()
learning_history = manage_memories(
    action="query",
    filter={
        "memory_type": ["learning"],
        "keywords": {"contains": "Rust"}
    }
)
# AI customizes teaching content based on your background
```

### Scenario 3: Goal Tracking and Review

**Problem**: Want to systematically manage and track personal goals

**Solution**:
```python
# Set goals
manage_goals(
    action="save",
    content="Master Rust async programming",
    type="short_term",
    deadline="2024-05-01"
)

# Record learning progress
manage_memories(
    action="save",
    content="Completed tokio basics tutorial, understood async/await concepts",
    memory_type="learning",
    importance=7,
    keywords=["Rust", "async programming", "tokio"]
)

# Regular review
goals = manage_goals(
    action="query",
    filter={"status": ["in_progress"]}
)
```

## 🔒 Privacy and Security

### Data Control
- **Local Storage**: All data stored in SQLite database under your control
- **Complete Export**: Support for complete data export and backup
- **Selective Access**: Precise control over which data is visible to AI applications

## 🏗️ Development Guide

### Project Structure
```
userbank-core/
├── main.py              # MCP server main entry
├── main_sse.py          # SSE mode server
├── config.json          # Configuration file
├── config_manager.py    # Configuration manager
├── requirements.txt     # Dependencies list
├── Database/
│   ├── database.py      # Database operation class
│   └── __init__.py
├── tools/               # MCP tool modules
│   ├── base.py          # Base tool class
│   ├── persona_tools.py # Personal profile tools
│   ├── memory_tools.py  # Memory management tools
│   ├── viewpoint_tools.py # Viewpoint management tools
│   ├── goal_tools.py    # Goal management tools
│   └── ...              # Other tool modules
└── README.md
```

## 🤝 Contributing Guide

As a core component of the UserBank ecosystem, we welcome all forms of contributions:

1. **Core Feature Improvements**: Submit new features or improve existing core functionality
2. **Bug Fixes**: Report and fix discovered issues
3. **Documentation Enhancement**: Improve documentation and usage guides
4. **Test Cases**: Add test cases to improve code quality (see roadmap v0.2.0)
5. **Performance Optimization**: Optimize database queries and system performance
6. **Ecosystem Integration**: Help build other components of the UserBank ecosystem

### Development Environment Setup

```bash
# Clone project
git clone https://github.com/MixLabPro/userbank-core.git
cd userbank-core

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Start development server
python main.py
```

## 📚 Related Resources

- **MCP Protocol Documentation**: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Claude Desktop MCP Configuration**: [Claude MCP Guide](https://docs.anthropic.com/claude/docs/mcp)
- **SQLite Documentation**: [https://sqlite.org/docs.html](https://sqlite.org/docs.html)
- **FastMCP Framework**: [https://github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp)

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details

---

<div align="center">
  
**Let AI truly understand you, starting with owning your own data**

*UserBank Core - Store once, use everywhere with AI*

[GitHub](https://github.com/your-username/userbank-core) • [Issues](https://github.com/your-username/userbank-core/issues) • [Discussions](https://github.com/your-username/userbank-core/discussions)

</div>
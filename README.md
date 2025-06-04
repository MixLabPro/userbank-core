# Profile Access Protocol (PAP)

<div align="center">
  
**让用户真正拥有自己的AI交互数据**

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://profile.dev/pap)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Draft-orange.svg)](https://github.com/profile/pap)

*从"数据寄存在各个平台" 到 "拥有自己的数据银行"*

[快速开始](#-快速开始) • [核心亮点](#-核心亮点) • [使用场景](#-使用场景) • [API参考](#-api参考) • [实现指南](#-实现指南)

</div>

---

## 🎯 什么是PAP？

Profile Access Protocol (PAP) 是一个开放协议，让每个用户都能拥有自己的**Personal Data Store (PDS)**——一个完全由自己控制的个人数据仓库。通过**MCP（Model Context Protocol）**，AI应用可以安全、标准化地访问用户的个人数据。

### 现状问题

当你与不同AI助手（Claude、ChatGPT、Perplexity等）交互时：

```
你的数据分散在各处 ❌
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Claude    │  │   ChatGPT   │  │ Perplexity  │
│ 你的记忆A   │  │ 你的记忆B   │  │ 你的记忆C   │
│ 你的偏好A   │  │ 你的偏好B   │  │ 你的偏好C   │
└─────────────┘  └─────────────┘  └─────────────┘
```

### PAP + MCP 解决方案

```
你拥有统一的个人数据仓库 ✅
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Claude    │     │   ChatGPT   │     │ Perplexity  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │      MCP over     │      MCP over     │
       │      PAP API      │      PAP API      │
       └───────────────────┼───────────────────┘
                          │
                  ┌───────▼────────┐
                  │  你的Personal  │
                  │  Data Store    │
                  │ ┌─────────────┐ │
                  │ │ 完整的记忆  │ │
                  │ │ 统一的偏好  │ │
                  │ │ 所有观点    │ │
                  │ │ 历史决策    │ │
                  │ └─────────────┘ │
                  └────────────────┘
```

## ✨ 核心亮点

### 🔐 真正的数据主权
- **你的数据存储在你控制的地方**，不是平台的"寄存品"
- **完整导出**：一键导出所有数据，包含元数据
- **标准化访问**：通过MCP协议实现安全、一致的数据访问



### 🛡️ 简化隐私模型
```typescript
enum PrivacyLevel {
  PUBLIC = "public",        // 完全公开
  PRIVATE = "private"       // 仅自己可见
}
```

### 🔄 MCP协议集成
- **标准化接口**：通过MCP Server提供一致的数据访问方式
- **安全授权**：基于MCP的权限控制机制
- **实时同步**：支持AI应用实时获取最新的个人数据

## 🚀 快速开始

### 对于用户：拥有你的PDS

```bash
# 方式1：一键部署（推荐新手）
docker run -d -p 8080:8080 profile/pds:latest

# 方式2：本地应用
brew install pap-desktop  # 基于SQLite

# 方式3：云托管
# 选择可信的PDS提供商（类似选择邮箱服务商）
```

### 初始化你的Profile

```bash
curl -X POST http://localhost:8080/pap/v1/profile/init \
  -H "Content-Type: application/json" \
  -d '{
    "persona": {
      "name": "张三",
      "personality": "理性、好奇、注重隐私",
      "gender": "male",
      "bio": "技术专家，喜欢深度思考"
    }
  }'
```

### 通过MCP连接AI应用到你的PDS

```javascript
// AI应用通过MCP Server连接到PAP
const mcp = new MCPClient({
  server: 'pap://your-pds.example.com:8080',
  capabilities: ['read_memories', 'read_preferences', 'write_memories']
});

// 通过MCP协议访问记忆
const memories = await mcp.callTool('get_memories', {
  filter: { 
    memory_type: ['learning', 'experience'],
    importance: { min: 7 },
    privacy_level: 'public'
  },
  limit: 20
});

// 通过MCP协议添加新记忆
await mcp.callTool('add_memory', {
  content: "今天学习了Rust的所有权概念，终于理解了借用检查器的工作原理",
  memory_type: "learning",
  importance: 8,
  keywords: ["Rust", "所有权", "借用检查器", "编程语言"],
  related_people: "技术讲师李老师"
});
```

## 📊 个人档案数据模型

PAP定义了9种核心资源类型，构建你的完整数字身份：

| 资源类型 | 说明 | 关键字段 | 示例 |
|---------|------|---------|------|
| **persona** 👤 | 基本身份信息 | name, gender, personality, bio | 姓名：张三，性格：理性思考型 |
| **memory** 🧠 | AI交互记忆 | content, memory_type, importance, related_people | "学习Rust所有权概念的深度体验" |
| **viewpoint** 💭 | 个人观点立场 | content, source_people, related_event | "我认为代码可读性比性能更重要" |
| **insight** 💡 | 深度洞察感悟 | content, source_people | "技术选择往往反映团队的组织结构" |
| **goal** 🎯 | 目标计划 | content, type, deadline, status | 短期目标："3个月内完成系统重构" |
| **preference** ❤️ | 个人偏好 | content, context | "喜欢在安静环境中深度思考，适用于学习时" |
| **methodology** 🛠️ | 方法论 | content, type, effectiveness, use_cases | "使用TDD进行开发，已验证有效" |
| **focus** 🔍 | 当前关注 | content, priority, status, deadline | "正在深入学习Rust，优先级8" |
| **prediction** 🔮 | 预测记录 | content, timeframe, basis, verification_status | "AI将根本改变软件开发方式，基于当前趋势分析" |

### 核心特性

#### 👤 Persona基本身份
```typescript
interface Persona {
  id: 1;                     // 固定为1（系统只维护一个人物档案）
  name: string;              // 用户姓名
  gender?: string;           // 性别，影响语言风格
  personality?: string;      // 性格描述
  avatar_url?: string;       // 头像链接
  bio?: string;              // 个人简介
  privacy_level: PrivacyLevel;
}
```

#### 🧠 Memory类型分类
```typescript
interface Memory {
  content: string;           // 记忆内容
  memory_type: "experience" | "event" | "learning" | "interaction" | "achievement" | "mistake";
  importance: number;        // 1-10，重要程度评级
  related_people?: string;   // 相关人员
  location?: string;         // 发生地点
  memory_date?: Date;        // 具体日期
  keywords: string[];        // 关键词数组（JSON格式）
  source_app: string;        // 数据来源应用
  category_id?: number;      // 分类ID
  reference_urls?: string[]; // 相关链接
  privacy_level: PrivacyLevel;
}
```

#### 💭 Viewpoint观点立场
```typescript
interface Viewpoint {
  content: string;           // 观点内容
  source_people?: string;    // 观点来源人员
  related_event?: string;    // 相关事件
  reference_urls?: string[]; // 参考链接数组
  keywords: string[];
  source_app: string;        // 数据来源应用
  privacy_level: PrivacyLevel;
}
```

#### 💡 Insight深度洞察
```typescript
interface Insight {
  content: string;           // 洞察内容
  source_people?: string;    // 洞察来源人员
  reference_urls?: string[]; // 参考链接
  keywords: string[];
  privacy_level: PrivacyLevel;
}
```

#### 🎯 Goal层次化管理
```typescript
interface Goal {
  content: string;
  type: "long_term" | "short_term" | "plan" | "todo";  // 四层目标体系
  deadline?: Date;
  status: "planning" | "in_progress" | "completed" | "abandoned";
  keywords: string[];
  privacy_level: PrivacyLevel;
}
```

#### ❤️ Preference个人偏好
```typescript
interface Preference {
  content: string;           // 偏好内容
  context?: string;          // 适用场景，如"学习时"、"工作中"
  keywords: string[];
  privacy_level: PrivacyLevel;
}
```

#### 🛠️ Methodology方法论
```typescript
interface Methodology {
  content: string;           // 方法论内容
  type?: string;             // 类型，如"问题解决"、"决策制定"
  effectiveness: "proven" | "experimental" | "theoretical";  // 有效性
  use_cases?: string;        // 适用场景
  reference_urls?: string[]; // 参考链接
  keywords: string[];
  privacy_level: PrivacyLevel;
}
```

#### 🔍 Focus优先级管理
```typescript
interface Focus {
  content: string;
  priority: number;          // 1-10，优先级评分
  status: "active" | "paused" | "completed";
  context?: string;          // 上下文场景
  deadline?: Date;
  keywords: string[];
  privacy_level: PrivacyLevel;
}
```

#### 🔮 Prediction验证追踪
```typescript
interface Prediction {
  content: string;
  timeframe?: string;        // 时间范围
  basis?: string;            // 预测依据
  verification_status: "pending" | "correct" | "incorrect" | "partial";
  reference_urls?: string[]; // 参考链接
  keywords: string[];
  privacy_level: PrivacyLevel;
}
```

### 数据关联网络

所有资源类型之间可以建立丰富的语义关联：

```typescript
// 示例：构建知识图谱
viewpoint("代码可读性重要") 
  → supports → 
    methodology("Code Review流程")
  → implements → 
    goal("选择更详细的命名规范")
  → inspired_by →
    memory("上次重构项目的经验教训")
```

### 统一的元数据

每个资源都包含以下标准字段：

- **keywords**: JSON数组格式的关键词标签，支持语义搜索
- **source_app**: 数据来源应用，支持多应用数据集成和MCP追踪
- **privacy_level**: 隐私级别控制（public/private）
- **created_time**: 创建时间戳
- **updated_time**: 更新时间戳
- **category_id**: 关联到分类体系，支持层次化组织

## 🎭 使用场景

### 场景1：跨平台对话延续（通过MCP）

**问题**：昨天在ChatGPT讨论项目架构，今天想在Claude继续

```typescript
// Claude通过MCP检测到上下文需求
const context = {
  trigger: "用户说：继续昨天关于微服务的讨论",
  keywords: ["微服务", "架构设计", "API Gateway"]
};

// 通过MCP请求相关记忆（用户授权）
const memories = await mcp.callTool('query_memories', {
  filter: {
    keywords: { overlap: context.keywords },
    memory_date: { gte: "yesterday" },
    memory_type: ["interaction", "learning"]
  }
});

// Claude现在可以无缝继续
// "基于昨天的讨论，你们确定了使用API Gateway模式..."
```

### 场景2：个性化学习辅导（通过MCP）

**问题**：在多平台学习，希望AI了解学习进度和偏好

```typescript
// 通过MCP渐进式数据访问
const basicInfo = await mcp.callTool('get_persona');
// → { expertise: { rust: 'beginner', python: 'expert' } }

// AI发现需要更多上下文来个性化教学
const learningHistory = await mcp.callTool('query_memories', {
  filter: {
    memory_type: ["learning"],
    keywords: { contains: ["Rust", "编程"] }
  }
});

// 基于你的背景定制解释
// "让我用你熟悉的Python概念来类比Rust的所有权..."
```

### 场景3：MCP实时数据同步

**问题**：在多个AI应用间保持数据一致性

```typescript
// AI应用A添加新记忆
await mcp.callTool('add_memory', {
  content: "发现了新的代码重构技巧",
  memory_type: "learning",
  importance: 7,
  keywords: ["重构", "代码质量"]
});

// AI应用B立即可以访问
const recentLearning = await mcp.callTool('query_memories', {
  filter: {
    memory_type: ["learning"],
    created_time: { gte: "today" }
  }
});
```

## 🔒 隐私控制规范

### 简化权限控制

```typescript
// 基于MCP的访问控制
interface MCPPermissions {
  read_memories: boolean;
  write_memories: boolean;
  read_preferences: boolean;
  read_viewpoints: boolean;
  // 更细粒度的权限控制在v2.0实现
}

// 隐私级别过滤
{
  "memories": {
    "default": "public",
    "sensitive_keywords": ["salary", "personal"] // 自动标记为private
  }
}
```

## 📡 API参考

### MCP工具集成

| MCP工具 | 说明 | 参数 |
|---------|------|------|
| **数据查询** |
| `get_persona` | 获取基本身份信息 | - |
| `query_memories` | 查询记忆数据 | filter, limit, sort |
| `query_viewpoints` | 查询观点数据 | filter, limit |
| `get_preferences` | 获取偏好设置 | context? |
| **数据操作** |
| `add_memory` | 添加新记忆 | content, memory_type, importance, keywords |
| `update_memory` | 更新记忆 | id, updates |
| `add_viewpoint` | 添加观点 | content, source_people?, keywords |
| **关系查询** |
| `find_related` | 查找相关资源 | resource_type, resource_id, relation_type? |

### RESTful API端点

| 方法 | 端点 | 说明 |
|------|------|------|
| **Profile管理** |
| GET | `/profile` | 获取完整档案信息 |
| PATCH | `/profile/persona` | 更新身份信息 |
| **数据操作** |
| GET | `/profile/{collection}` | 获取数据集合 |
| POST | `/profile/{collection}` | 创建新资源 |
| PUT | `/profile/{collection}/{id}` | 更新资源 |
| DELETE | `/profile/{collection}/{id}` | 删除资源 |
| **MCP集成** |
| GET | `/mcp/capabilities` | 获取MCP服务能力 |
| POST | `/mcp/tools/{tool_name}` | 调用MCP工具 |
| **数据管理** |
| POST | `/export` | 导出数据 |
| POST | `/import` | 导入数据 |

### 查询语言示例

```typescript
// 通过MCP查询示例
await mcp.callTool('query_memories', {
  filter: {
    and: [
      { importance: { gte: 8 } },
      { keywords: { contains: "机器学习" } },
      { memory_date: { gte: "2024-01-01" } },
      { privacy_level: { ne: "private" } }
    ]
  },
  sort: { memory_date: "desc" },
  limit: 50
});
```

## 🏗️ 实现指南

### MCP Server实现

```python
from mcp import Server, Tool
from typing import Dict, List, Any

class PAPMCPServer(Server):
    def __init__(self, pap_storage):
        super().__init__("pap-server", "1.0.0")
        self.storage = pap_storage
        self._register_tools()
    
    def _register_tools(self):
        @self.tool("query_memories")
        async def query_memories(filter: Dict[str, Any], limit: int = 20) -> List[Dict]:
            """查询记忆数据"""
            memories = await self.storage.query_memories(filter, limit)
            return [self._sanitize_memory(m) for m in memories]
        
        @self.tool("add_memory")
        async def add_memory(
            content: str,
            memory_type: str,
            importance: int,
            keywords: List[str],
            related_people: str = None
        ) -> Dict:
            """添加新记忆"""
            memory = {
                'content': content,
                'memory_type': memory_type,
                'importance': importance,
                'keywords': keywords,
                'related_people': related_people,
                'source_app': self.get_client_app(),
                'privacy_level': 'public'
            }
            return await self.storage.create_memory(memory)
    
    def _sanitize_memory(self, memory: Dict) -> Dict:
        """根据隐私设置过滤记忆内容"""
        if memory['privacy_level'] == 'private' and not self.has_owner_access():
            return {'id': memory['id'], 'summary': '私有记忆'}
        return memory
```

### 最小可行实现

```python
# 1. 基础数据结构
class PAPProfile:
    def __init__(self):
        self.persona = {}
        self.collections = {
            'memories': [],
            'viewpoints': [],
            'goals': []
        }
    
    def add_memory(self, content, memory_type, importance=5, keywords=None):
        memory = {
            'id': self.generate_id(),
            'content': content,
            'memory_type': memory_type,
            'importance': importance,
            'keywords': keywords or [],
            'source_app': 'manual',
            'privacy_level': 'public',
            'created_time': datetime.now()
        }
        self.collections['memories'].append(memory)
        return memory

# 2. MCP集成
class MCPIntegration:
    def __init__(self, profile):
        self.profile = profile
        self.server = PAPMCPServer(profile)
    
    async def start_server(self):
        await self.server.run(port=8080)
```

## 🌟 技术亮点

### 1. MCP协议标准化

与传统的"各自为政"的API不同，PAP通过MCP协议实现：

- **统一接口**：所有AI应用通过相同的MCP工具访问数据
- **安全控制**：基于MCP的标准化权限管理
- **实时同步**：多应用间的数据一致性保障
- **可扩展性**：易于添加新的数据类型和功能

### 2. Memory为核心的设计

基于database设计的记忆系统：

- **6种记忆类型**：experience, event, learning, interaction, achievement, mistake
- **重要性评级**：1-10级别的智能重要性评估
- **时空关联**：包含具体日期、地点和相关人员信息
- **来源追踪**：记录数据来源应用，支持多平台集成
- **关键词索引**：JSON格式的灵活标签系统

### 3. 真正的数据可移植性

```bash
# 完整导出（包含数据库结构）
pap export --format=complete --include-schema

# 生成标准.pap文件
profile_backup_20240320.pap
├── manifest.json
├── persona.json
├── collections/
│   ├── memories.jsonl
│   ├── viewpoints.jsonl
│   └── relations.jsonl
└── schema/
    └── database.sql

# 一键迁移到新PDS
pap import --from=profile_backup_20240320.pap --to=new-pds.example.com
```

### 4. 面向未来的扩展性

```typescript
// 通过MCP支持自定义资源类型
interface CustomHabit extends Resource {
  "@type": "com.example.habit";
  name: string;
  frequency: "daily" | "weekly";
  streak: number;
  triggers: string[];
}

// MCP插件系统
class PAPMCPPlugin {
  install(server: MCPServer): void;
  uninstall(server: MCPServer): void;
  registerTools(server: MCPServer): void;
}
```

## 🤝 参与贡献

PAP是开放协议，我们欢迎：

1. **协议改进**：通过[RFC流程](https://github.com/profile/pap-rfcs)提交提案
2. **MCP集成**：贡献不同AI平台的MCP适配器
3. **参考实现**：贡献不同语言和框架的实现
4. **兼容性测试**：完善测试套件
5. **文档完善**：使用指南、最佳实践
6. **生态建设**：客户端库、工具、插件

### 开发路线图

- **v1.0** ✅ 核心协议规范 + 基础隐私控制
- **v1.1** 🔄 MCP协议深度集成 + 多应用同步
- **v1.2** 📅 语义搜索和AI增强 + 智能记忆管理
- **v2.0** 🎯 高级功能实现：
  - 多样化认证（OAuth2、WebAuthn、DID去中心化身份）
  - 端到端加密支持
  - 选择性共享机制（SELECTIVE隐私级别）
  - 完全加密存储（ENCRYPTED隐私级别）
  - 联邦化支持和跨PDS数据共享

## 📚 相关资源

- **协议规范**：[https://profile.dev/pap/spec](https://profile.dev/pap/spec)
- **MCP集成指南**：[https://github.com/profile/pap-mcp](https://github.com/profile/pap-mcp)
- **参考实现**：[https://github.com/profile/pap-reference](https://github.com/profile/pap-reference)
- **开发者工具**：[https://github.com/profile/pap-tools](https://github.com/profile/pap-tools)
- **社区论坛**：[https://forum.profile.dev](https://forum.profile.dev)

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">
  
**从数据的"房客"变成真正的"房东"**

*Profile Access Protocol - 让每个人都拥有自己的数字主权*

[官网](https://profile.dev) • [文档](https://docs.profile.dev) • [GitHub](https://github.com/profile/pap) • [RFC](https://github.com/profile/pap-rfcs)

</div>
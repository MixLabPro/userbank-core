"""
个人画像数据管理系统 - SSE模式 (修正版)
基于MCP官方文档的标准SSE实现
基于database 0.3.md和tools3.md的完整实现
"""

from mcp.server.sse import SseServerTransport
from mcp.server import Server
from mcp import types
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from typing import List, Dict, Any, Optional, Union
import json
from datetime import datetime


from Database.database import get_database

# 获取数据库实例
db = get_database()

# 定义所有表名和中文描述的映射（基于database 0.3.md）
TABLE_DESCRIPTIONS = {
    # 核心表
    'persona': '人物档案',
    'category': '分类体系',
    'relations': '通用关联',
    
    # 主要数据表
    'viewpoint': '观点',
    'insight': '洞察',
    'focus': '关注点',
    'goal': '目标',
    'preference': '偏好',
    'methodology': '方法论',
    'prediction': '预测',
    'memory': '记忆'
}

# 工具模板生成函数
def generate_prompt_content(template: str, data: Any) -> str:
    """生成基于模板的提示内容"""
    if isinstance(data, list):
        if not data:
            return template.replace("{{#each raw_data}}", "").replace("{{/each}}", "").replace("{{#if (eq raw_data.length 0)}}", "").replace("{{/if}}", "未找到符合条件的记录。")
        
        content_parts = []
        for item in data:
            item_content = template
            # 简单的模板替换
            for key, value in item.items():
                if value is not None:
                    item_content = item_content.replace(f"{{{{this.{key}}}}}", str(value))
                else:
                    item_content = item_content.replace(f"{{{{this.{key}}}}}", "")
            content_parts.append(item_content)
        
        # 替换循环标记
        result = template.replace("{{#each raw_data}}", "").replace("{{/each}}", "\n".join(content_parts))
        result = result.replace("{{#if (eq raw_data.length 0)}}", "").replace("{{/if}}", "")
        result = result.replace("{{total_count}}", str(len(data)))
        result = result.replace("{{raw_data.length}}", str(len(data)))
        
        return result
    elif isinstance(data, dict):
        result = template
        for key, value in data.items():
            if value is not None:
                result = result.replace(f"{{{{{key}}}}}", str(value))
            else:
                result = result.replace(f"{{{{{key}}}}}", "")
        return result
    else:
        return template

# 创建MCP服务器实例
app = Server("个人画像数据管理系统")

# 创建SSE传输实例
sse = SseServerTransport("/messages")

# 工具列表函数
@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """列出所有可用的工具"""
    return [
        # ============ I. Persona Tools (2 Tools) ============
        types.Tool(
            name="get_persona",
            description="获取当前用户的核心画像信息。该信息用于AI进行个性化交互。系统中只有一个用户画像，ID固定为1。",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="save_persona",
            description="保存（更新）当前用户的核心画像信息。由于ID固定为1，此操作主要用于更新现有画像。只需提供需要修改的字段。",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "用户姓名"},
                    "gender": {"type": "string", "description": "性别"},
                    "personality": {"type": "string", "description": "性格描述"},
                    "avatar_url": {"type": "string", "description": "头像链接"},
                    "bio": {"type": "string", "description": "个人简介"},
                    "privacy_level": {"type": "string", "description": "隐私级别"}
                },
                "required": []
            }
        ),
        
        # ============ II. Memory Tools (2 Tools) ============
        types.Tool(
            name="query_memories",
            description="查询符合指定条件的记忆数据。记忆是关于用户经历、学习、事件、互动等方面的记录。",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "object", "description": "筛选条件"},
                    "sort_by": {"type": "string", "description": "排序字段", "default": "created_time"},
                    "sort_order": {"type": "string", "description": "排序顺序", "default": "desc"},
                    "limit": {"type": "integer", "description": "返回记录数限制", "default": 20},
                    "offset": {"type": "integer", "description": "偏移量", "default": 0}
                },
                "required": []
            }
        ),
        types.Tool(
            name="save_memory",
            description="保存（添加或更新）一条记忆记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "记录ID（更新时提供）"},
                    "content": {"type": "string", "description": "记忆内容"},
                    "memory_type": {"type": "string", "description": "记忆类型"},
                    "importance": {"type": "integer", "description": "重要程度(1-10)"},
                    "related_people": {"type": "string", "description": "相关人员"},
                    "location": {"type": "string", "description": "发生地点"},
                    "memory_date": {"type": "string", "description": "记忆日期"},
                    "keywords": {"type": "array", "items": {"type": "string"}, "description": "关键词"},
                    "source_app": {"type": "string", "description": "数据来源应用", "default": "unknown"},
                    "reference_urls": {"type": "array", "items": {"type": "string"}, "description": "参考链接"},
                    "privacy_level": {"type": "string", "description": "隐私级别", "default": "public"}
                },
                "required": []
            }
        ),
        
        # ============ III. Viewpoint Tools (2 Tools) ============
        types.Tool(
            name="query_viewpoints",
            description="查询符合指定条件的观点数据。观点代表用户对特定事物的看法或立场。",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "object", "description": "筛选条件"},
                    "sort_by": {"type": "string", "description": "排序字段", "default": "created_time"},
                    "sort_order": {"type": "string", "description": "排序顺序", "default": "desc"},
                    "limit": {"type": "integer", "description": "返回记录数限制", "default": 20},
                    "offset": {"type": "integer", "description": "偏移量", "default": 0}
                },
                "required": []
            }
        ),
        types.Tool(
            name="save_viewpoint",
            description="保存（添加或更新）一条观点记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "记录ID（更新时提供）"},
                    "content": {"type": "string", "description": "观点内容"},
                    "source_people": {"type": "string", "description": "观点来源人"},
                    "keywords": {"type": "array", "items": {"type": "string"}, "description": "关键词"},
                    "source_app": {"type": "string", "description": "数据来源应用", "default": "unknown"},
                    "related_event": {"type": "string", "description": "相关事件"},
                    "reference_urls": {"type": "array", "items": {"type": "string"}, "description": "参考链接"},
                    "privacy_level": {"type": "string", "description": "隐私级别", "default": "public"}
                },
                "required": []
            }
        ),
        
        # ============ IV. Insight Tools (2 Tools) ============
        types.Tool(
            name="query_insights",
            description="查询符合指定条件的洞察数据。洞察是用户经过深度思考和分析后得出的见解或感悟。",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "object", "description": "筛选条件"},
                    "sort_by": {"type": "string", "description": "排序字段", "default": "created_time"},
                    "sort_order": {"type": "string", "description": "排序顺序", "default": "desc"},
                    "limit": {"type": "integer", "description": "返回记录数限制", "default": 20},
                    "offset": {"type": "integer", "description": "偏移量", "default": 0}
                },
                "required": []
            }
        ),
        types.Tool(
            name="save_insight",
            description="保存（添加或更新）一条洞察记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "记录ID（更新时提供）"},
                    "content": {"type": "string", "description": "洞察内容"},
                    "source_people": {"type": "string", "description": "洞察来源人"},
                    "keywords": {"type": "array", "items": {"type": "string"}, "description": "关键词"},
                    "source_app": {"type": "string", "description": "数据来源应用", "default": "unknown"},
                    "reference_urls": {"type": "array", "items": {"type": "string"}, "description": "参考链接"},
                    "privacy_level": {"type": "string", "description": "隐私级别", "default": "public"}
                },
                "required": []
            }
        ),
        
        # ============ V. Goal Tools (2 Tools) ============
        types.Tool(
            name="query_goals",
            description="查询符合指定条件的目标数据。目标包括长期规划、短期计划以及具体的待办事项。",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "object", "description": "筛选条件"},
                    "sort_by": {"type": "string", "description": "排序字段", "default": "deadline"},
                    "sort_order": {"type": "string", "description": "排序顺序", "default": "asc"},
                    "limit": {"type": "integer", "description": "返回记录数限制", "default": 20},
                    "offset": {"type": "integer", "description": "偏移量", "default": 0}
                },
                "required": []
            }
        ),
        types.Tool(
            name="save_goal",
            description="保存（添加或更新）一条目标、计划或待办事项。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "记录ID（更新时提供）"},
                    "content": {"type": "string", "description": "目标内容"},
                    "type": {"type": "string", "description": "目标类型"},
                    "deadline": {"type": "string", "description": "截止日期"},
                    "status": {"type": "string", "description": "状态", "default": "planning"},
                    "keywords": {"type": "array", "items": {"type": "string"}, "description": "关键词"},
                    "source_app": {"type": "string", "description": "数据来源应用", "default": "unknown"},
                    "privacy_level": {"type": "string", "description": "隐私级别", "default": "public"}
                },
                "required": []
            }
        ),
        
        # ============ VI. Preference Tools (2 Tools) ============
        types.Tool(
            name="query_preferences",
            description="查询符合指定条件的偏好数据。偏好描述了用户在特定情境下的喜好和习惯。",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "object", "description": "筛选条件"},
                    "sort_by": {"type": "string", "description": "排序字段", "default": "created_time"},
                    "sort_order": {"type": "string", "description": "排序顺序", "default": "desc"},
                    "limit": {"type": "integer", "description": "返回记录数限制", "default": 20},
                    "offset": {"type": "integer", "description": "偏移量", "default": 0}
                },
                "required": []
            }
        ),
        types.Tool(
            name="save_preference",
            description="保存（添加或更新）一条偏好记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "记录ID（更新时提供）"},
                    "content": {"type": "string", "description": "偏好内容"},
                    "context": {"type": "string", "description": "适用场景"},
                    "keywords": {"type": "array", "items": {"type": "string"}, "description": "关键词"},
                    "source_app": {"type": "string", "description": "数据来源应用", "default": "unknown"},
                    "privacy_level": {"type": "string", "description": "隐私级别", "default": "public"}
                },
                "required": []
            }
        ),
        
        # ============ VII. Methodology Tools (2 Tools) ============
        types.Tool(
            name="query_methodologies",
            description="查询符合指定条件的方法论数据。方法论是用户解决问题或进行决策时使用的框架或原则。",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "object", "description": "筛选条件"},
                    "sort_by": {"type": "string", "description": "排序字段", "default": "created_time"},
                    "sort_order": {"type": "string", "description": "排序顺序", "default": "desc"},
                    "limit": {"type": "integer", "description": "返回记录数限制", "default": 20},
                    "offset": {"type": "integer", "description": "偏移量", "default": 0}
                },
                "required": []
            }
        ),
        types.Tool(
            name="save_methodology",
            description="保存（添加或更新）一条方法论记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "记录ID（更新时提供）"},
                    "content": {"type": "string", "description": "方法论内容"},
                    "type": {"type": "string", "description": "类型"},
                    "effectiveness": {"type": "string", "description": "有效性", "default": "experimental"},
                    "use_cases": {"type": "string", "description": "适用场景"},
                    "keywords": {"type": "array", "items": {"type": "string"}, "description": "关键词"},
                    "source_app": {"type": "string", "description": "数据来源应用", "default": "unknown"},
                    "reference_urls": {"type": "array", "items": {"type": "string"}, "description": "参考链接"},
                    "privacy_level": {"type": "string", "description": "隐私级别", "default": "public"}
                },
                "required": []
            }
        ),
        
        # ============ VIII. Focus Tools (2 Tools) ============
        types.Tool(
            name="query_focuses",
            description="查询符合指定条件的当前关注点数据。关注点是用户当前集中精力处理或学习的事项。",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "object", "description": "筛选条件"},
                    "sort_by": {"type": "string", "description": "排序字段", "default": "priority"},
                    "sort_order": {"type": "string", "description": "排序顺序", "default": "desc"},
                    "limit": {"type": "integer", "description": "返回记录数限制", "default": 20},
                    "offset": {"type": "integer", "description": "偏移量", "default": 0}
                },
                "required": []
            }
        ),
        types.Tool(
            name="save_focus",
            description="保存（添加或更新）一条关注点记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "记录ID（更新时提供）"},
                    "content": {"type": "string", "description": "关注内容"},
                    "priority": {"type": "integer", "description": "优先级(1-10)"},
                    "status": {"type": "string", "description": "状态", "default": "active"},
                    "context": {"type": "string", "description": "上下文"},
                    "keywords": {"type": "array", "items": {"type": "string"}, "description": "关键词"},
                    "source_app": {"type": "string", "description": "数据来源应用", "default": "unknown"},
                    "deadline": {"type": "string", "description": "截止日期"},
                    "privacy_level": {"type": "string", "description": "隐私级别", "default": "public"}
                },
                "required": []
            }
        ),
        
        # ============ IX. Prediction Tools (2 Tools) ============
        types.Tool(
            name="query_predictions",
            description="查询符合指定条件的预测数据。预测是用户对未来事件、趋势的判断记录。",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "object", "description": "筛选条件"},
                    "sort_by": {"type": "string", "description": "排序字段", "default": "created_time"},
                    "sort_order": {"type": "string", "description": "排序顺序", "default": "desc"},
                    "limit": {"type": "integer", "description": "返回记录数限制", "default": 20},
                    "offset": {"type": "integer", "description": "偏移量", "default": 0}
                },
                "required": []
            }
        ),
        types.Tool(
            name="save_prediction",
            description="保存（添加或更新）一条预测记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "记录ID（更新时提供）"},
                    "content": {"type": "string", "description": "预测内容"},
                    "timeframe": {"type": "string", "description": "时间范围"},
                    "basis": {"type": "string", "description": "预测依据"},
                    "verification_status": {"type": "string", "description": "验证状态", "default": "pending"},
                    "keywords": {"type": "array", "items": {"type": "string"}, "description": "关键词"},
                    "source_app": {"type": "string", "description": "数据来源应用", "default": "unknown"},
                    "reference_urls": {"type": "array", "items": {"type": "string"}, "description": "参考链接"},
                    "privacy_level": {"type": "string", "description": "隐私级别", "default": "public"}
                },
                "required": []
            }
        ),
        
        # ============ 保留的工具方法 ============
        types.Tool(
            name="execute_custom_sql",
            description="执行自定义SQL语句",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string", "description": "要执行的SQL语句"},
                    "params": {"type": "array", "items": {"type": "string"}, "description": "SQL参数列表（可选）"},
                    "fetch_results": {"type": "boolean", "description": "是否获取查询结果（对于SELECT语句）", "default": True}
                },
                "required": ["sql"]
            }
        ),
        types.Tool(
            name="get_table_schema",
            description="获取表结构信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名（可选，不提供则获取所有表结构）", "enum": list(TABLE_DESCRIPTIONS.keys())}
                },
                "required": []
            }
        )
    ] 

# 统一工具调用处理函数
@app.call_tool()
async def call_tool(
    name: str,
    arguments: dict
) -> List[types.TextContent]:
    """统一处理所有工具调用"""
    try:
        # ============ I. Persona Tools (2 Tools) ============
        if name == "get_persona":
            try:
                persona = db.get_persona()
                if not persona:
                    content = "未找到用户画像信息。"
                    raw_data = None
                else:
                    # 生成提示内容
                    template = """# 用户画像核心信息

以下是当前用户的个人画像数据。请在与用户互动时参考这些信息，以便提供更个性化和相关的回应。

## 基本信息
- **用户姓名 (name)**: {name}
- **性别 (gender)**: {gender} (这可能会影响语言风格和称呼)
- **性格特点 (personality)**: {personality} (例如：{personality}，请据此调整沟通方式)
- **个人简介 (bio)**: {bio}
- **头像链接 (avatar_url)**: {avatar_url}

## 系统信息
- **隐私级别 (privacy_level)**: {privacy_level}
- **档案创建时间 (created_time)**: {created_time}
- **档案最后更新时间 (updated_time)**: {updated_time}

**如何使用这些信息：**
- **个性化称呼与语气**: 根据姓名和性别使用合适的称呼。
- **理解用户偏好**: 性格和简介能揭示用户的沟通偏好和可能的兴趣点。
- **内容相关性**: 结合用户画像信息，使AI的回答和建议更贴近用户需求。"""
                    
                    content = generate_prompt_content(template, persona)
                    raw_data = persona
                
                result = {
                    "content": content,
                    "raw_data": raw_data
                }
                
            except Exception as e:
                result = {
                    "content": f"获取用户画像失败: {str(e)}",
                    "raw_data": None
                }
            
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "save_persona":
            try:
                update_data = {}
                for field in ['name', 'gender', 'personality', 'avatar_url', 'bio', 'privacy_level']:
                    if field in arguments and arguments[field] is not None:
                        update_data[field] = arguments[field]
                
                if not update_data:
                    result = {
                        "id": 1,
                        "operation": "no_change",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    success = db.update_persona(**update_data)
                    if success:
                        result = {
                            "id": 1,
                            "operation": "updated",
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        result = {
                            "id": 1,
                            "operation": "failed",
                            "timestamp": datetime.now().isoformat()
                        }
                        
            except Exception as e:
                result = {
                    "id": 1,
                    "operation": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e)
                }
            
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 通用查询处理函数 ============
        elif name.startswith("query_"):
            table_name = name.replace("query_", "").rstrip("s")  # 去掉复数形式
            if table_name == "memorie":
                table_name = "memory"
            elif table_name == "methodologie":
                table_name = "methodology"
            elif table_name == "focuse":
                table_name = "focus"
            
            try:
                filter_conditions = {}
                filter_arg = arguments.get("filter", {})
                
                if filter_arg:
                    for key, value in filter_arg.items():
                        if value is not None:
                            filter_conditions[key] = value
                
                sort_by = arguments.get("sort_by", "created_time")
                sort_order = arguments.get("sort_order", "desc")
                limit = arguments.get("limit", 20)
                offset = arguments.get("offset", 0)
                
                records, total_count = db.query_records(table_name, filter_conditions, sort_by, sort_order, limit, offset)
                
                # 生成对应的模板内容
                templates = {
                    "memory": """# 用户记忆数据

以下是根据您的查询条件检索到的用户记忆记录：

{{#each raw_data}}
## 记忆记录 (ID: {{this.id}})
- **核心内容 (content)**: {{this.content}}
- **记忆类型 (memory_type)**: {{this.memory_type}}
- **重要程度 (importance)**: {{this.importance}}
- **相关人员 (related_people)**: {{this.related_people}}
- **发生地点 (location)**: {{this.location}}
- **记忆日期 (memory_date)**: {{this.memory_date}}
- **关键词 (keywords)**: {{this.keywords}}
- **数据来源应用 (source_app)**: {{this.source_app}}
- **参考链接 (reference_urls)**: {{this.reference_urls}}
- **隐私级别 (privacy_level)**: {{this.privacy_level}}
- **记录创建时间 (created_time)**: {{this.created_time}}
- **记录更新时间 (updated_time)**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
未找到符合条件的记忆记录。
{{/if}}

**查询摘要:**
- 总共找到 {{total_count}} 条相关记录。
- 当前显示 {{raw_data.length}} 条记录。""",
                    
                    "viewpoint": """# 用户观点数据

以下是根据您的查询条件检索到的用户观点记录：

{{#each raw_data}}
## 观点记录 (ID: {{this.id}})
- **核心观点 (content)**: {{this.content}}
- **观点来源人 (source_people)**: {{this.source_people}}
- **相关事件 (related_event)**: {{this.related_event}}
- **关键词 (keywords)**: {{this.keywords}}
- **数据来源应用 (source_app)**: {{this.source_app}}
- **参考链接 (reference_urls)**: {{this.reference_urls}}
- **隐私级别 (privacy_level)**: {{this.privacy_level}}
- **记录创建时间 (created_time)**: {{this.created_time}}
- **记录更新时间 (updated_time)**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
未找到符合条件的观点记录。
{{/if}}

**查询摘要:**
- 总共找到 {{total_count}} 条相关记录。
- 当前显示 {{raw_data.length}} 条记录。""",
                    
                    "insight": """# 用户洞察数据

以下是根据您的查询条件检索到的用户洞察记录：

{{#each raw_data}}
## 洞察记录 (ID: {{this.id}})
- **核心洞察 (content)**: {{this.content}}
- **洞察来源人 (source_people)**: {{this.source_people}}
- **关键词 (keywords)**: {{this.keywords}}
- **数据来源应用 (source_app)**: {{this.source_app}}
- **参考链接 (reference_urls)**: {{this.reference_urls}}
- **隐私级别 (privacy_level)**: {{this.privacy_level}}
- **记录创建时间 (created_time)**: {{this.created_time}}
- **记录更新时间 (updated_time)**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
未找到符合条件的洞察记录。
{{/if}}

**查询摘要:**
- 总共找到 {{total_count}} 条相关记录。
- 当前显示 {{raw_data.length}} 条记录。""",
                    
                    "goal": """# 用户目标数据

以下是根据您的查询条件检索到的用户目标记录：

{{#each raw_data}}
## 目标记录 (ID: {{this.id}})
- **目标内容 (content)**: {{this.content}}
- **目标类型 (type)**: {{this.type}}
- **截止日期 (deadline)**: {{this.deadline}}
- **当前状态 (status)**: {{this.status}}
- **关键词 (keywords)**: {{this.keywords}}
- **数据来源应用 (source_app)**: {{this.source_app}}
- **隐私级别 (privacy_level)**: {{this.privacy_level}}
- **记录创建时间 (created_time)**: {{this.created_time}}
- **记录更新时间 (updated_time)**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
未找到符合条件的目标记录。
{{/if}}

**查询摘要:**
- 总共找到 {{total_count}} 条相关记录。
- 当前显示 {{raw_data.length}} 条记录。""",
                    
                    "preference": """# 用户偏好数据

以下是根据您的查询条件检索到的用户偏好记录：

{{#each raw_data}}
## 偏好记录 (ID: {{this.id}})
- **偏好内容 (content)**: {{this.content}}
- **适用场景 (context)**: {{this.context}}
- **关键词 (keywords)**: {{this.keywords}}
- **数据来源应用 (source_app)**: {{this.source_app}}
- **隐私级别 (privacy_level)**: {{this.privacy_level}}
- **记录创建时间 (created_time)**: {{this.created_time}}
- **记录更新时间 (updated_time)**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
未找到符合条件的偏好记录。
{{/if}}

**查询摘要:**
- 总共找到 {{total_count}} 条相关记录。
- 当前显示 {{raw_data.length}} 条记录。""",
                    
                    "methodology": """# 用户方法论数据

以下是根据您的查询条件检索到的用户方法论记录：

{{#each raw_data}}
## 方法论记录 (ID: {{this.id}})
- **方法论内容 (content)**: {{this.content}}
- **类型 (type)**: {{this.type}}
- **有效性 (effectiveness)**: {{this.effectiveness}}
- **适用场景 (use_cases)**: {{this.use_cases}}
- **关键词 (keywords)**: {{this.keywords}}
- **数据来源应用 (source_app)**: {{this.source_app}}
- **参考链接 (reference_urls)**: {{this.reference_urls}}
- **隐私级别 (privacy_level)**: {{this.privacy_level}}
- **记录创建时间 (created_time)**: {{this.created_time}}
- **记录更新时间 (updated_time)**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
未找到符合条件的方法论记录。
{{/if}}

**查询摘要:**
- 总共找到 {{total_count}} 条相关记录。
- 当前显示 {{raw_data.length}} 条记录。""",
                    
                    "focus": """# 用户关注点数据

以下是根据您的查询条件检索到的用户当前关注点记录：

{{#each raw_data}}
## 关注点记录 (ID: {{this.id}})
- **关注内容 (content)**: {{this.content}}
- **优先级 (priority)**: {{this.priority}}
- **状态 (status)**: {{this.status}}
- **上下文 (context)**: {{this.context}}
- **关键词 (keywords)**: {{this.keywords}}
- **数据来源应用 (source_app)**: {{this.source_app}}
- **截止日期 (deadline)**: {{this.deadline}}
- **隐私级别 (privacy_level)**: {{this.privacy_level}}
- **记录创建时间 (created_time)**: {{this.created_time}}
- **记录更新时间 (updated_time)**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
未找到符合条件的关注点记录。
{{/if}}

**查询摘要:**
- 总共找到 {{total_count}} 条相关记录。
- 当前显示 {{raw_data.length}} 条记录。""",
                    
                    "prediction": """# 用户预测数据

以下是根据您的查询条件检索到的用户预测记录：

{{#each raw_data}}
## 预测记录 (ID: {{this.id}})
- **预测内容 (content)**: {{this.content}}
- **时间范围 (timeframe)**: {{this.timeframe}}
- **预测依据 (basis)**: {{this.basis}}
- **验证状态 (verification_status)**: {{this.verification_status}}
- **关键词 (keywords)**: {{this.keywords}}
- **数据来源应用 (source_app)**: {{this.source_app}}
- **参考链接 (reference_urls)**: {{this.reference_urls}}
- **隐私级别 (privacy_level)**: {{this.privacy_level}}
- **记录创建时间 (created_time)**: {{this.created_time}}
- **记录更新时间 (updated_time)**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
未找到符合条件的预测记录。
{{/if}}

**查询摘要:**
- 总共找到 {{total_count}} 条相关记录。
- 当前显示 {{raw_data.length}} 条记录。"""
                }
                
                template = templates.get(table_name, f"# {TABLE_DESCRIPTIONS.get(table_name, table_name)}数据\n\n查询到 {{{{total_count}}}} 条记录。")
                content = generate_prompt_content(template, records)
                content = content.replace("{{total_count}}", str(total_count))
                
                result = {
                    "content": content,
                    "raw_data": records,
                    "total_count": total_count
                }
                
            except Exception as e:
                result = {
                    "content": f"查询{TABLE_DESCRIPTIONS.get(table_name, table_name)}失败: {str(e)}",
                    "raw_data": [],
                    "total_count": 0
                }
            
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 通用保存处理函数 ============
        elif name.startswith("save_"):
            table_name = name.replace("save_", "")
            if table_name == "memory":
                table_name = "memory"
            elif table_name == "methodology":
                table_name = "methodology"
            elif table_name == "focus":
                table_name = "focus"
            
            try:
                record_id = arguments.get("id")
                
                if record_id is None:
                    # 创建新记录
                    record_data = {}
                    for key, value in arguments.items():
                        if key != "id" and value is not None:
                            record_data[key] = value
                    
                    # 设置默认值
                    if "source_app" not in record_data:
                        record_data["source_app"] = "unknown"
                    if "privacy_level" not in record_data:
                        record_data["privacy_level"] = "public"
                    
                    new_id = db.insert_record(table_name, **record_data)
                    result = {
                        "id": new_id,
                        "operation": "created",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    # 更新现有记录
                    update_data = {}
                    for key, value in arguments.items():
                        if key != "id" and value is not None:
                            update_data[key] = value
                    
                    if not update_data:
                        result = {
                            "id": record_id,
                            "operation": "no_change",
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        success = db.update_record(table_name, record_id, **update_data)
                        if success:
                            result = {
                                "id": record_id,
                                "operation": "updated",
                                "timestamp": datetime.now().isoformat()
                            }
                        else:
                            result = {
                                "id": record_id,
                                "operation": "failed",
                                "timestamp": datetime.now().isoformat()
                            }
                            
            except Exception as e:
                result = {
                    "id": arguments.get("id"),
                    "operation": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e)
                }
            
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 保留的工具方法 ============
        elif name == "execute_custom_sql":
            try:
                sql = arguments["sql"]
                params = arguments.get("params", [])
                fetch_results = arguments.get("fetch_results", True)
                
                result = db.execute_custom_sql(sql, params, fetch_results)
                
            except Exception as e:
                result = {
                    "success": False,
                    "message": f"执行自定义SQL失败: {str(e)}"
                }
            
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "get_table_schema":
            try:
                table_name = arguments.get("table_name")
                
                if table_name:
                    if table_name not in TABLE_DESCRIPTIONS:
                        result = {
                            "success": False,
                            "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                        }
                    else:
                        result = db.get_table_schema(table_name)
                else:
                    # 获取所有表的结构信息
                    result = db.get_table_schema()
                    
            except Exception as e:
                result = {
                    "success": False,
                    "message": f"获取表结构失败: {str(e)}"
                }
            
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        else:
            result = {
                "success": False,
                "message": f"未知的工具: {name}"
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    except Exception as e:
        result = {
            "success": False,
            "message": f"工具调用失败: {str(e)}"
        }
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))] 

# 创建SSE处理函数
async def handle_sse(request):
    async with sse.connect_sse(
        request.scope,
        request.receive,
        request._send,
    ) as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )

# 创建Starlette应用
starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ]
)

# 添加CORS中间件
starlette_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查端点
@starlette_app.route("/health")
async def health_check(request):
    return JSONResponse({"status": "healthy"})

# 主函数
async def main():
    """启动SSE服务器"""
    config = uvicorn.Config(
        app=starlette_app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    print("启动个人画像数据管理系统 - SSE模式")
    print("服务器地址: http://localhost:8000")
    print("SSE端点: http://localhost:8000/sse/messages")
    print("健康检查: http://localhost:8000/health")
    asyncio.run(main()) 
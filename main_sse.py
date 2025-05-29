"""
个人画像数据管理系统 - SSE模式 (修正版)
基于MCP官方文档的标准SSE实现
基于database.md文档的完整实现
"""

from mcp.server.sse import SseServerTransport
from mcp.server import Server
from mcp import types
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from typing import List, Dict, Any, Optional
import json

from Database.database import get_database

# 获取数据库实例
db = get_database()

# 定义所有表名和中文描述的映射
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
    'decision': '决策',
    'methodology': '方法论',
    'experience': '经验',
    'prediction': '预测'
}

# 创建MCP服务器实例
app = Server("个人画像数据管理系统")

# 创建SSE传输实例
sse = SseServerTransport("/messages")

# 工具列表函数
@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """列出所有可用的工具"""
    return [
        # ============ 人物档案相关操作 ============
        types.Tool(
            name="get_persona",
            description="获取用户画像信息",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="update_persona",
            description="更新用户画像信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "用户姓名"},
                    "gender": {"type": "string", "description": "性别", "enum": ["male", "female", "other"]},
                    "personality": {"type": "string", "description": "性格描述"},
                    "avatar_url": {"type": "string", "description": "头像链接"},
                    "bio": {"type": "string", "description": "个人简介"}
                },
                "required": []
            }
        ),
        
        # ============ 分类管理 ============
        types.Tool(
            name="get_categories",
            description="获取分类列表",
            inputSchema={
                "type": "object",
                "properties": {
                    "first_level": {"type": "string", "description": "一级分类过滤"}
                },
                "required": []
            }
        ),
        types.Tool(
            name="add_category",
            description="添加新分类",
            inputSchema={
                "type": "object",
                "properties": {
                    "first_level": {"type": "string", "description": "一级分类"},
                    "second_level": {"type": "string", "description": "二级分类"},
                    "description": {"type": "string", "description": "分类描述"}
                },
                "required": ["first_level"]
            }
        ),
        
        # ============ 观点管理 ============
        types.Tool(
            name="add_viewpoint",
            description="添加观点记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "观点内容"},
                    "subject": {"type": "string", "description": "观点主题"},
                    "stance": {"type": "integer", "description": "观点立场(-5到5)", "minimum": -5, "maximum": 5},
                    "source": {"type": "string", "description": "观点来源"},
                    "time_period": {"type": "string", "description": "时间段"},
                    "reference_urls": {"type": "array", "items": {"type": "string"}, "description": "参考链接"},
                    "category_id": {"type": "integer", "description": "分类ID"}
                },
                "required": ["content", "subject"]
            }
        ),
        
        # ============ 洞察管理 ============
        types.Tool(
            name="add_insight",
            description="添加洞察记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "洞察内容"},
                    "trigger_event": {"type": "string", "description": "触发事件"},
                    "impact_level": {"type": "string", "description": "影响程度", "enum": ["high", "medium", "low"]},
                    "reference_urls": {"type": "array", "items": {"type": "string"}, "description": "参考链接"},
                    "category_id": {"type": "integer", "description": "分类ID"}
                },
                "required": ["content"]
            }
        ),
        
        # ============ 关注点管理 ============
        types.Tool(
            name="add_focus",
            description="添加关注点记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "关注点内容"},
                    "priority": {"type": "integer", "description": "优先级(1-10)", "minimum": 1, "maximum": 10},
                    "status": {"type": "string", "description": "状态", "enum": ["active", "paused", "completed"]},
                    "context": {"type": "string", "description": "上下文"},
                    "deadline": {"type": "string", "description": "截止日期"},
                    "category_id": {"type": "integer", "description": "分类ID"}
                },
                "required": ["content"]
            }
        ),
        
        # ============ 目标管理 ============
        types.Tool(
            name="add_goal",
            description="添加目标记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "目标内容"},
                    "type": {"type": "string", "description": "目标类型", "enum": ["long_term", "short_term"]},
                    "deadline": {"type": "string", "description": "截止日期"},
                    "progress": {"type": "integer", "description": "进度(0-100)", "minimum": 0, "maximum": 100},
                    "status": {"type": "string", "description": "状态", "enum": ["planning", "in_progress", "completed", "abandoned"]},
                    "category_id": {"type": "integer", "description": "分类ID"}
                },
                "required": ["content", "type"]
            }
        ),
        
        # ============ 偏好管理 ============
        types.Tool(
            name="add_preference",
            description="添加偏好记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "偏好内容"},
                    "strength": {"type": "string", "description": "偏好强度", "enum": ["strong", "moderate", "flexible"]},
                    "context": {"type": "string", "description": "适用场景"},
                    "category_id": {"type": "integer", "description": "分类ID"}
                },
                "required": ["content"]
            }
        ),
        
        # ============ 决策管理 ============
        types.Tool(
            name="add_decision",
            description="添加决策记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "决策内容"},
                    "reasoning": {"type": "string", "description": "决策理由"},
                    "outcome": {"type": "string", "description": "决策结果"},
                    "domain": {"type": "string", "description": "决策领域"},
                    "category_id": {"type": "integer", "description": "分类ID"}
                },
                "required": ["content"]
            }
        ),
        
        # ============ 方法论管理 ============
        types.Tool(
            name="add_methodology",
            description="添加方法论记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "方法论内容"},
                    "type": {"type": "string", "description": "方法论类型"},
                    "effectiveness": {"type": "string", "description": "有效性", "enum": ["proven", "experimental", "theoretical"]},
                    "use_cases": {"type": "string", "description": "适用场景"},
                    "reference_urls": {"type": "array", "items": {"type": "string"}, "description": "参考链接"},
                    "category_id": {"type": "integer", "description": "分类ID"}
                },
                "required": ["content"]
            }
        ),
        
        # ============ 经验管理 ============
        types.Tool(
            name="add_experience",
            description="添加经验记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "经验内容"},
                    "field": {"type": "string", "description": "领域"},
                    "expertise_level": {"type": "string", "description": "专业程度", "enum": ["expert", "proficient", "intermediate", "beginner"]},
                    "years": {"type": "integer", "description": "经验年数"},
                    "key_learnings": {"type": "string", "description": "关键学习"},
                    "reference_urls": {"type": "array", "items": {"type": "string"}, "description": "参考链接"},
                    "category_id": {"type": "integer", "description": "分类ID"}
                },
                "required": ["content", "field"]
            }
        ),
        
        # ============ 预测管理 ============
        types.Tool(
            name="add_prediction",
            description="添加预测记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "预测内容"},
                    "timeframe": {"type": "string", "description": "时间范围"},
                    "basis": {"type": "string", "description": "预测依据"},
                    "verification_status": {"type": "string", "description": "验证状态", "enum": ["correct", "incorrect", "pending", "partially_correct"]},
                    "reference_urls": {"type": "array", "items": {"type": "string"}, "description": "参考链接"},
                    "category_id": {"type": "integer", "description": "分类ID"}
                },
                "required": ["content"]
            }
        ),
        
        # ============ 关联关系管理 ============
        types.Tool(
            name="add_relation",
            description="添加关联关系",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_table": {"type": "string", "description": "源表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "source_id": {"type": "integer", "description": "源记录ID"},
                    "target_table": {"type": "string", "description": "目标表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "target_id": {"type": "integer", "description": "目标记录ID"},
                    "relation_type": {"type": "string", "description": "关联类型", "enum": ["inspired_by", "conflicts_with", "supports", "leads_to", "based_on", "similar_to", "opposite_to", "caused_by"]},
                    "strength": {"type": "string", "description": "关联强度", "enum": ["strong", "medium", "weak"]},
                    "note": {"type": "string", "description": "关联说明"}
                },
                "required": ["source_table", "source_id", "target_table", "target_id", "relation_type"]
            }
        ),
        types.Tool(
            name="get_relations",
            description="获取记录的关联关系",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "record_id": {"type": "integer", "description": "记录ID"},
                    "relation_type": {"type": "string", "description": "关联类型过滤"}
                },
                "required": ["table_name", "record_id"]
            }
        ),
        
        # ============ 通用CRUD操作 ============
        types.Tool(
            name="update_record",
            description="更新记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "record_id": {"type": "integer", "description": "记录ID"}
                },
                "required": ["table_name", "record_id"]
            }
        ),
        types.Tool(
            name="delete_record",
            description="删除记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "record_id": {"type": "integer", "description": "记录ID"}
                },
                "required": ["table_name", "record_id"]
            }
        ),
        types.Tool(
            name="get_record",
            description="获取单条记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "record_id": {"type": "integer", "description": "记录ID"}
                },
                "required": ["table_name", "record_id"]
            }
        ),
        types.Tool(
            name="search_records",
            description="搜索记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "keyword": {"type": "string", "description": "搜索关键词"},
                    "category_id": {"type": "integer", "description": "分类ID"},
                    "status": {"type": "string", "description": "状态"},
                    "type": {"type": "string", "description": "类型"},
                    "limit": {"type": "integer", "description": "返回记录数限制", "default": 20},
                    "offset": {"type": "integer", "description": "偏移量", "default": 0},
                    "order_by": {"type": "string", "description": "排序字段", "default": "created_time"},
                    "order_desc": {"type": "boolean", "description": "是否降序", "default": True}
                },
                "required": ["table_name"]
            }
        ),
        types.Tool(
            name="get_all_records",
            description="获取表中所有记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "limit": {"type": "integer", "description": "返回记录数限制", "default": 50},
                    "offset": {"type": "integer", "description": "偏移量", "default": 0}
                },
                "required": ["table_name"]
            }
        ),
        
        # ============ 统计和信息查询 ============
        types.Tool(
            name="get_table_stats",
            description="获取表统计信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名（可选，不提供则获取所有表统计）", "enum": list(TABLE_DESCRIPTIONS.keys())}
                },
                "required": []
            }
        ),
        types.Tool(
            name="get_available_tables",
            description="获取所有可用的表名和描述",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="get_all_table_contents",
            description="获取所有表的完整内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_empty": {"type": "boolean", "description": "是否包含空表", "default": True},
                    "limit_per_table": {"type": "integer", "description": "每个表的记录数限制", "default": 100}
                },
                "required": []
            }
        ),
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
        ),
        
        # ============ 高级查询方法 ============
        types.Tool(
            name="get_viewpoints_by_subject",
            description="根据主题获取观点",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject": {"type": "string", "description": "观点主题"},
                    "time_period": {"type": "string", "description": "时间段过滤"}
                },
                "required": ["subject"]
            }
        ),
        types.Tool(
            name="get_active_focuses",
            description="获取活跃的关注点",
            inputSchema={
                "type": "object",
                "properties": {
                    "priority_threshold": {"type": "integer", "description": "优先级阈值"}
                },
                "required": []
            }
        ),
        types.Tool(
            name="get_goals_by_status",
            description="根据状态获取目标",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "目标状态"},
                    "type": {"type": "string", "description": "目标类型过滤"}
                },
                "required": ["status"]
            }
        ),
        types.Tool(
            name="get_high_impact_insights",
            description="获取高影响力的洞察",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "返回记录数限制", "default": 10}
                },
                "required": []
            }
        ),
        types.Tool(
            name="get_expertise_areas",
            description="获取专业领域分析",
            inputSchema={
                "type": "object",
                "properties": {},
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
        # ============ 人物档案相关操作 ============
        if name == "get_persona":
            persona = db.get_persona()
            if persona:
                result = {
                    "success": True,
                    "message": "成功获取用户画像",
                    "persona": persona
                }
            else:
                result = {
                    "success": False,
                    "message": "未找到用户画像信息"
                }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "update_persona":
            update_data = {}
            for field in ['name', 'gender', 'personality', 'avatar_url', 'bio']:
                if field in arguments and arguments[field] is not None:
                    update_data[field] = arguments[field]
            
            if not update_data:
                result = {
                    "success": False,
                    "message": "没有提供要更新的字段"
                }
            else:
                success = db.update_persona(**update_data)
                if success:
                    result = {
                        "success": True,
                        "message": "成功更新用户画像",
                        "updated_fields": list(update_data.keys())
                    }
                else:
                    result = {
                        "success": False,
                        "message": "更新用户画像失败"
                    }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 分类管理 ============
        elif name == "get_categories":
            first_level = arguments.get("first_level")
            categories = db.get_categories(first_level)
            result = {
                "success": True,
                "message": f"成功获取 {len(categories)} 个分类",
                "categories": categories
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "add_category":
            first_level = arguments["first_level"]
            second_level = arguments.get("second_level")
            description = arguments.get("description")
            
            category_id = db.insert_record('category',
                                         first_level=first_level,
                                         second_level=second_level,
                                         description=description,
                                         is_active=1)
            result = {
                "success": True,
                "message": "成功添加分类",
                "category_id": category_id,
                "first_level": first_level,
                "second_level": second_level
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 观点管理 ============
        elif name == "add_viewpoint":
            content = arguments["content"]
            subject = arguments["subject"]
            stance = arguments.get("stance")
            source = arguments.get("source")
            time_period = arguments.get("time_period")
            reference_urls = arguments.get("reference_urls", [])
            category_id = arguments.get("category_id")
            
            record_id = db.insert_record('viewpoint',
                                       content=content,
                                       subject=subject,
                                       stance=stance,
                                       source=source,
                                       time_period=time_period,
                                       reference_urls=reference_urls,
                                       category_id=category_id)
            result = {
                "success": True,
                "message": "成功添加观点记录",
                "record_id": record_id,
                "content": content,
                "subject": subject
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 洞察管理 ============
        elif name == "add_insight":
            content = arguments["content"]
            trigger_event = arguments.get("trigger_event")
            impact_level = arguments.get("impact_level", "medium")
            reference_urls = arguments.get("reference_urls", [])
            category_id = arguments.get("category_id")
            
            record_id = db.insert_record('insight',
                                       content=content,
                                       trigger_event=trigger_event,
                                       impact_level=impact_level,
                                       reference_urls=reference_urls,
                                       category_id=category_id)
            result = {
                "success": True,
                "message": "成功添加洞察记录",
                "record_id": record_id,
                "content": content,
                "impact_level": impact_level
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 关注点管理 ============
        elif name == "add_focus":
            content = arguments["content"]
            priority = arguments.get("priority")
            status = arguments.get("status", "active")
            context = arguments.get("context")
            deadline = arguments.get("deadline")
            category_id = arguments.get("category_id")
            
            record_id = db.insert_record('focus',
                                       content=content,
                                       priority=priority,
                                       status=status,
                                       context=context,
                                       deadline=deadline,
                                       category_id=category_id)
            result = {
                "success": True,
                "message": "成功添加关注点记录",
                "record_id": record_id,
                "content": content,
                "priority": priority,
                "status": status
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 目标管理 ============
        elif name == "add_goal":
            content = arguments["content"]
            goal_type = arguments["type"]
            deadline = arguments.get("deadline")
            progress = arguments.get("progress", 0)
            status = arguments.get("status", "planning")
            category_id = arguments.get("category_id")
            
            record_id = db.insert_record('goal',
                                       content=content,
                                       type=goal_type,
                                       deadline=deadline,
                                       progress=progress,
                                       status=status,
                                       category_id=category_id)
            result = {
                "success": True,
                "message": f"成功添加{goal_type}目标记录",
                "record_id": record_id,
                "content": content,
                "type": goal_type,
                "status": status
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 偏好管理 ============
        elif name == "add_preference":
            content = arguments["content"]
            strength = arguments.get("strength", "moderate")
            context = arguments.get("context")
            category_id = arguments.get("category_id")
            
            record_id = db.insert_record('preference',
                                       content=content,
                                       strength=strength,
                                       context=context,
                                       category_id=category_id)
            result = {
                "success": True,
                "message": "成功添加偏好记录",
                "record_id": record_id,
                "content": content,
                "strength": strength
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 决策管理 ============
        elif name == "add_decision":
            content = arguments["content"]
            reasoning = arguments.get("reasoning")
            outcome = arguments.get("outcome")
            domain = arguments.get("domain")
            category_id = arguments.get("category_id")
            
            record_id = db.insert_record('decision',
                                       content=content,
                                       reasoning=reasoning,
                                       outcome=outcome,
                                       domain=domain,
                                       category_id=category_id)
            result = {
                "success": True,
                "message": "成功添加决策记录",
                "record_id": record_id,
                "content": content,
                "domain": domain
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 方法论管理 ============
        elif name == "add_methodology":
            content = arguments["content"]
            method_type = arguments.get("type")
            effectiveness = arguments.get("effectiveness", "experimental")
            use_cases = arguments.get("use_cases")
            reference_urls = arguments.get("reference_urls", [])
            category_id = arguments.get("category_id")
            
            record_id = db.insert_record('methodology',
                                       content=content,
                                       type=method_type,
                                       effectiveness=effectiveness,
                                       use_cases=use_cases,
                                       reference_urls=reference_urls,
                                       category_id=category_id)
            result = {
                "success": True,
                "message": "成功添加方法论记录",
                "record_id": record_id,
                "content": content,
                "effectiveness": effectiveness
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 经验管理 ============
        elif name == "add_experience":
            content = arguments["content"]
            field = arguments["field"]
            expertise_level = arguments.get("expertise_level", "beginner")
            years = arguments.get("years", 0)
            key_learnings = arguments.get("key_learnings")
            reference_urls = arguments.get("reference_urls", [])
            category_id = arguments.get("category_id")
            
            record_id = db.insert_record('experience',
                                       content=content,
                                       field=field,
                                       expertise_level=expertise_level,
                                       years=years,
                                       key_learnings=key_learnings,
                                       reference_urls=reference_urls,
                                       category_id=category_id)
            result = {
                "success": True,
                "message": "成功添加经验记录",
                "record_id": record_id,
                "content": content,
                "field": field,
                "expertise_level": expertise_level
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 预测管理 ============
        elif name == "add_prediction":
            content = arguments["content"]
            timeframe = arguments.get("timeframe")
            basis = arguments.get("basis")
            verification_status = arguments.get("verification_status", "pending")
            reference_urls = arguments.get("reference_urls", [])
            category_id = arguments.get("category_id")
            
            record_id = db.insert_record('prediction',
                                       content=content,
                                       timeframe=timeframe,
                                       basis=basis,
                                       verification_status=verification_status,
                                       reference_urls=reference_urls,
                                       category_id=category_id)
            result = {
                "success": True,
                "message": "成功添加预测记录",
                "record_id": record_id,
                "content": content,
                "timeframe": timeframe
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 关联关系管理 ============
        elif name == "add_relation":
            source_table = arguments["source_table"]
            source_id = arguments["source_id"]
            target_table = arguments["target_table"]
            target_id = arguments["target_id"]
            relation_type = arguments["relation_type"]
            strength = arguments.get("strength", "medium")
            note = arguments.get("note")
            
            relation_id = db.add_relation(source_table, source_id, target_table, target_id,
                                        relation_type, strength, note)
            result = {
                "success": True,
                "message": "成功添加关联关系",
                "relation_id": relation_id,
                "source": f"{source_table}#{source_id}",
                "target": f"{target_table}#{target_id}",
                "relation_type": relation_type
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "get_relations":
            table_name = arguments["table_name"]
            record_id = arguments["record_id"]
            relation_type = arguments.get("relation_type")
            
            if table_name not in TABLE_DESCRIPTIONS:
                result = {
                    "success": False,
                    "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                }
            else:
                relations = db.get_relations(table_name, record_id, relation_type)
                result = {
                    "success": True,
                    "message": f"成功获取 {len(relations)} 个关联关系",
                    "relations": relations
                }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 通用CRUD操作 ============
        elif name == "update_record":
            table_name = arguments["table_name"]
            record_id = arguments["record_id"]
            
            if table_name not in TABLE_DESCRIPTIONS:
                result = {
                    "success": False,
                    "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                }
            else:
                # 提取除table_name和record_id之外的所有参数作为更新字段
                update_data = {k: v for k, v in arguments.items() if k not in ['table_name', 'record_id']}
                
                success = db.update_record(table_name, record_id, **update_data)
                if success:
                    result = {
                        "success": True,
                        "message": f"成功更新{TABLE_DESCRIPTIONS[table_name]}记录",
                        "record_id": record_id,
                        "table_name": table_name,
                        "updated_fields": list(update_data.keys())
                    }
                else:
                    result = {
                        "success": False,
                        "message": f"未找到ID为 {record_id} 的{TABLE_DESCRIPTIONS[table_name]}记录"
                    }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "delete_record":
            table_name = arguments["table_name"]
            record_id = arguments["record_id"]
            
            if table_name not in TABLE_DESCRIPTIONS:
                result = {
                    "success": False,
                    "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                }
            else:
                success = db.delete_record(table_name, record_id)
                if success:
                    result = {
                        "success": True,
                        "message": f"成功删除{TABLE_DESCRIPTIONS[table_name]}记录",
                        "record_id": record_id,
                        "table_name": table_name
                    }
                else:
                    result = {
                        "success": False,
                        "message": f"未找到ID为 {record_id} 的{TABLE_DESCRIPTIONS[table_name]}记录"
                    }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "get_record":
            table_name = arguments["table_name"]
            record_id = arguments["record_id"]
            
            if table_name not in TABLE_DESCRIPTIONS:
                result = {
                    "success": False,
                    "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                }
            else:
                record = db.get_record(table_name, record_id)
                if record:
                    result = {
                        "success": True,
                        "message": f"成功获取{TABLE_DESCRIPTIONS[table_name]}记录",
                        "record": record
                    }
                else:
                    result = {
                        "success": False,
                        "message": f"未找到ID为 {record_id} 的{TABLE_DESCRIPTIONS[table_name]}记录"
                    }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "search_records":
            table_name = arguments["table_name"]
            
            if table_name not in TABLE_DESCRIPTIONS:
                result = {
                    "success": False,
                    "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                }
            else:
                search_params = {
                    'keyword': arguments.get('keyword'),
                    'category_id': arguments.get('category_id'),
                    'status': arguments.get('status'),
                    'type': arguments.get('type'),
                    'limit': arguments.get('limit', 20),
                    'offset': arguments.get('offset', 0),
                    'order_by': arguments.get('order_by', 'created_time'),
                    'order_desc': arguments.get('order_desc', True)
                }
                
                # 移除None值
                search_params = {k: v for k, v in search_params.items() if v is not None}
                
                records = db.search_records(table_name, **search_params)
                result = {
                    "success": True,
                    "message": f"在{TABLE_DESCRIPTIONS[table_name]}表中搜索到 {len(records)} 条记录",
                    "table_name": table_name,
                    "records": records,
                    "search_params": search_params
                }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "get_all_records":
            table_name = arguments["table_name"]
            limit = arguments.get("limit", 50)
            offset = arguments.get("offset", 0)
            
            if table_name not in TABLE_DESCRIPTIONS:
                result = {
                    "success": False,
                    "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                }
            else:
                records = db.get_all_records(table_name, limit, offset)
                result = {
                    "success": True,
                    "message": f"获取{TABLE_DESCRIPTIONS[table_name]}表中 {len(records)} 条记录",
                    "table_name": table_name,
                    "records": records,
                    "params": {
                        "limit": limit,
                        "offset": offset
                    }
                }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 统计和信息查询 ============
        elif name == "get_table_stats":
            table_name = arguments.get("table_name")
            
            if table_name:
                if table_name not in TABLE_DESCRIPTIONS:
                    result = {
                        "success": False,
                        "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                    }
                else:
                    stats = db.get_table_stats(table_name)
                    stats['table_description'] = TABLE_DESCRIPTIONS[table_name]
                    result = {
                        "success": True,
                        "message": f"获取{TABLE_DESCRIPTIONS[table_name]}表统计信息",
                        "stats": stats
                    }
            else:
                # 获取所有表的统计信息
                all_stats = db.get_table_stats()
                for table, stats in all_stats.items():
                    stats['table_description'] = TABLE_DESCRIPTIONS[table]
                result = {
                    "success": True,
                    "message": "获取所有表的统计信息",
                    "all_stats": all_stats
                }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "get_available_tables":
            result = {
                "success": True,
                "message": "获取所有可用表信息",
                "tables": TABLE_DESCRIPTIONS,
                "table_count": len(TABLE_DESCRIPTIONS)
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "get_all_table_contents":
            include_empty = arguments.get("include_empty", True)
            limit_per_table = arguments.get("limit_per_table", 100)
            
            try:
                all_contents = {}
                total_records = 0
                
                for table_name, description in TABLE_DESCRIPTIONS.items():
                    try:
                        # 获取表的统计信息
                        stats = db.get_table_stats(table_name)
                        
                        # 如果不包含空表且表为空，则跳过
                        if not include_empty and stats['total_records'] == 0:
                            continue
                        
                        # 获取表的所有记录
                        records = db.get_all_records(table_name, limit_per_table, 0)
                        
                        all_contents[table_name] = {
                            "description": description,
                            "stats": stats,
                            "records": records,
                            "record_count": len(records)
                        }
                        
                        total_records += len(records)
                        
                    except Exception as e:
                        all_contents[table_name] = {
                            "description": description,
                            "error": str(e),
                            "records": [],
                            "record_count": 0
                        }
                
                result = {
                    "success": True,
                    "message": f"成功获取所有表内容，总计 {total_records} 条记录",
                    "total_records": total_records,
                    "table_count": len(all_contents),
                    "contents": all_contents,
                    "params": {
                        "include_empty": include_empty,
                        "limit_per_table": limit_per_table
                    }
                }
            except Exception as e:
                result = {
                    "success": False,
                    "message": f"获取所有表内容失败: {str(e)}"
                }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "execute_custom_sql":
            sql = arguments["sql"]
            params = arguments.get("params", [])
            fetch_results = arguments.get("fetch_results", True)
            
            result = db.execute_custom_sql(sql, params, fetch_results)
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "get_table_schema":
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
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        # ============ 高级查询方法 ============
        elif name == "get_viewpoints_by_subject":
            subject = arguments["subject"]
            time_period = arguments.get("time_period")
            
            search_params = {'keyword': subject}
            if time_period:
                search_params['time_period'] = time_period
            
            records = db.search_records('viewpoint', **search_params)
            result = {
                "success": True,
                "message": f"找到 {len(records)} 个关于'{subject}'的观点",
                "subject": subject,
                "time_period": time_period,
                "viewpoints": records
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "get_active_focuses":
            priority_threshold = arguments.get("priority_threshold")
            
            if priority_threshold:
                # 使用自定义SQL来实现优先级过滤
                sql = "SELECT * FROM focus WHERE status = 'active' AND priority >= ? ORDER BY priority DESC"
                result = db.execute_custom_sql(sql, [priority_threshold])
                if result['success']:
                    records = result['results']
                    result = {
                        "success": True,
                        "message": f"找到 {len(records)} 个活跃的关注点",
                        "focuses": records
                    }
                else:
                    return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            else:
                records = db.search_records('focus', status='active')
                result = {
                    "success": True,
                    "message": f"找到 {len(records)} 个活跃的关注点",
                    "focuses": records
                }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "get_goals_by_status":
            status = arguments["status"]
            goal_type = arguments.get("type")
            
            search_params = {'status': status}
            if goal_type:
                search_params['type'] = goal_type
            
            records = db.search_records('goal', **search_params)
            result = {
                "success": True,
                "message": f"找到 {len(records)} 个状态为'{status}'的目标",
                "status": status,
                "type": goal_type,
                "goals": records
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "get_high_impact_insights":
            limit = arguments.get("limit", 10)
            
            records = db.search_records('insight', impact_level='high', limit=limit)
            result = {
                "success": True,
                "message": f"找到 {len(records)} 个高影响力的洞察",
                "insights": records
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "get_expertise_areas":
            # 使用自定义SQL查询专业领域统计
            sql = """
            SELECT field, expertise_level, COUNT(*) as count, AVG(years) as avg_years
            FROM experience 
            GROUP BY field, expertise_level
            ORDER BY field, 
                     CASE expertise_level 
                         WHEN 'expert' THEN 4 
                         WHEN 'proficient' THEN 3 
                         WHEN 'intermediate' THEN 2 
                         WHEN 'beginner' THEN 1 
                     END DESC
            """
            
            result = db.execute_custom_sql(sql)
            if result['success']:
                result = {
                    "success": True,
                    "message": f"成功分析专业领域，共 {len(result['results'])} 个领域级别组合",
                    "expertise_analysis": result['results']
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



# ASGI应用包装器类
class ASGIApp:
    def __init__(self, handler):
        self.handler = handler
    
    async def __call__(self, scope, receive, send):
        await self.handler(scope, receive, send)

# SSE端点处理函数 - 按照MCP官方文档标准实现
async def handle_sse(scope, receive, send):
    """处理SSE连接"""
    print(f"SSE连接请求: {scope['method']} {scope['path']}")
    
    # 允许所有来源访问（已移除Origin验证）
    
    try:
        async with sse.connect_sse(scope, receive, send) as streams:
            await app.run(streams[0], streams[1], app.create_initialization_options())
    except Exception as e:
        print(f"SSE连接错误: {e}")
        from starlette.responses import Response
        response = Response("Internal Server Error", status_code=500)
        await response(scope, receive, send)

# POST消息处理函数 - 按照MCP官方文档标准实现
async def handle_messages(scope, receive, send):
    """处理POST消息"""
    print(f"POST消息请求: {scope['method']} {scope['path']}")
    
    # 允许所有来源访问（已移除Origin验证）
    
    try:
        await sse.handle_post_message(scope, receive, send)
    except Exception as e:
        print(f"POST消息处理错误: {e}")
        from starlette.responses import Response
        response = Response("Internal Server Error", status_code=500)
        await response(scope, receive, send)

# 健康检查端点
async def health_check(request):
    """健康检查端点"""
    return JSONResponse({
        "status": "healthy",
        "service": "个人画像数据管理系统",
        "transport": "SSE",
        "tables": list(TABLE_DESCRIPTIONS.keys()),
        "endpoints": {
            "sse": "/sse",
            "messages": "/messages",
            "health": "/health",
            "info": "/info"
        }
    })

# 服务器信息端点
async def server_info(request):
    """提供MCP服务器信息"""
    return JSONResponse({
        "name": "个人画像数据管理系统",
        "version": "1.0.0",
        "transport": "SSE",
        "endpoints": {
            "sse": "/sse",
            "messages": "/messages",
            "health": "/health",
            "info": "/info"
        },
        "capabilities": {
            "tools": True,
            "resources": False,
            "prompts": False,
            "sampling": False
        },
        "tables": TABLE_DESCRIPTIONS
    })

# 创建Starlette应用 - 按照MCP官方文档标准实现
starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=ASGIApp(handle_sse), methods=["GET"]),
        Route("/messages", endpoint=ASGIApp(handle_messages), methods=["POST"]),
        Route("/health", endpoint=health_check, methods=["GET"]),
        Route("/info", endpoint=server_info, methods=["GET"]),
    ]
)

# 添加CORS中间件（允许所有访问）
starlette_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # 当使用 "*" 时必须设为 False
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# 主函数
async def main():
    """启动SSE服务器"""
    
    print("正在启动个人画像数据管理系统 MCP SSE 服务器...")
    print(f"服务器地址: http://0.0.0.0:8000 (可通过任何IP访问)")
    print(f"本地访问: http://127.0.0.1:8000")
    print(f"SSE端点: http://0.0.0.0:8000/sse")
    print(f"消息端点: http://0.0.0.0:8000/messages")
    print(f"健康检查: http://0.0.0.0:8000/health")
    print(f"服务器信息: http://0.0.0.0:8000/info")
    print("按 Ctrl+C 停止服务器")
    
    # 启动服务器，绑定到所有接口以允许外部访问
    config = uvicorn.Config(
        starlette_app, 
        host="0.0.0.0",  # 绑定到所有接口，允许外部访问
        port=8000,  # 使用8000端口避免冲突
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
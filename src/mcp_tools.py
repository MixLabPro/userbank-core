"""
MCP工具模块
MCP Tools Module

基于标准MCP Python SDK的个人画像数据管理工具集
"""

import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Sequence

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

from database import get_database, ProfileDatabase

# 创建MCP服务器实例
server = Server("个人画像数据管理系统")

# 获取数据库实例
db = get_database()

# 定义所有表名和中文描述的映射
TABLE_DESCRIPTIONS = {
    'belief': '信念',
    'insight': '洞察', 
    'focus': '关注点',
    'long_term_goal': '长期目标',
    'short_term_goal': '短期目标',
    'preference': '偏好',
    'decision': '决策',
    'methodology': '方法论'
}

# 工具函数定义
def add_belief_impl(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加信念记录的实现"""
    try:
        record_id = db.insert_record('belief', content, related)
        return {
            "success": True,
            "message": f"成功添加信念记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加信念记录失败: {str(e)}"
        }

def add_insight_impl(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加洞察记录的实现"""
    try:
        record_id = db.insert_record('insight', content, related)
        return {
            "success": True,
            "message": f"成功添加洞察记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加洞察记录失败: {str(e)}"
        }

def add_focus_impl(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加关注点记录的实现"""
    try:
        record_id = db.insert_record('focus', content, related)
        return {
            "success": True,
            "message": f"成功添加关注点记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加关注点记录失败: {str(e)}"
        }

def add_long_term_goal_impl(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加长期目标记录的实现"""
    try:
        record_id = db.insert_record('long_term_goal', content, related)
        return {
            "success": True,
            "message": f"成功添加长期目标记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加长期目标记录失败: {str(e)}"
        }

def add_short_term_goal_impl(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加短期目标记录的实现"""
    try:
        record_id = db.insert_record('short_term_goal', content, related)
        return {
            "success": True,
            "message": f"成功添加短期目标记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加短期目标记录失败: {str(e)}"
        }

def add_preference_impl(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加偏好记录的实现"""
    try:
        record_id = db.insert_record('preference', content, related)
        return {
            "success": True,
            "message": f"成功添加偏好记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加偏好记录失败: {str(e)}"
        }

def add_decision_impl(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加决策记录的实现"""
    try:
        record_id = db.insert_record('decision', content, related)
        return {
            "success": True,
            "message": f"成功添加决策记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加决策记录失败: {str(e)}"
        }

def add_methodology_impl(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加方法论记录的实现"""
    try:
        record_id = db.insert_record('methodology', content, related)
        return {
            "success": True,
            "message": f"成功添加方法论记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加方法论记录失败: {str(e)}"
        }

def update_record_impl(table_name: str, record_id: int, content: str = None, related: List[str] = None) -> Dict[str, Any]:
    """更新记录的实现"""
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        success = db.update_record(table_name, record_id, content, related)
        
        if success:
            return {
                "success": True,
                "message": f"成功更新{TABLE_DESCRIPTIONS[table_name]}记录",
                "record_id": record_id,
                "table_name": table_name
            }
        else:
            return {
                "success": False,
                "message": f"未找到ID为 {record_id} 的{TABLE_DESCRIPTIONS[table_name]}记录"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"更新记录失败: {str(e)}"
        }

def delete_record_impl(table_name: str, record_id: int) -> Dict[str, Any]:
    """删除记录的实现"""
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        success = db.delete_record(table_name, record_id)
        
        if success:
            return {
                "success": True,
                "message": f"成功删除{TABLE_DESCRIPTIONS[table_name]}记录",
                "record_id": record_id,
                "table_name": table_name
            }
        else:
            return {
                "success": False,
                "message": f"未找到ID为 {record_id} 的{TABLE_DESCRIPTIONS[table_name]}记录"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"删除记录失败: {str(e)}"
        }

def get_record_impl(table_name: str, record_id: int) -> Dict[str, Any]:
    """获取单条记录的实现"""
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        record = db.get_record(table_name, record_id)
        
        if record:
            return {
                "success": True,
                "message": f"成功获取{TABLE_DESCRIPTIONS[table_name]}记录",
                "record": record
            }
        else:
            return {
                "success": False,
                "message": f"未找到ID为 {record_id} 的{TABLE_DESCRIPTIONS[table_name]}记录"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": f"获取记录失败: {str(e)}"
        }

def search_records_impl(table_name: str, keyword: str = None, related_topic: str = None, 
                       limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """搜索记录的实现"""
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        records = db.search_records(table_name, keyword, related_topic, limit, offset)
        
        return {
            "success": True,
            "message": f"在{TABLE_DESCRIPTIONS[table_name]}表中搜索到 {len(records)} 条记录",
            "table_name": table_name,
            "records": records,
            "search_params": {
                "keyword": keyword,
                "related_topic": related_topic,
                "limit": limit,
                "offset": offset
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"搜索记录失败: {str(e)}"
        }

def get_all_records_impl(table_name: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    """获取表中所有记录的实现"""
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        records = db.get_all_records(table_name, limit, offset)
        
        return {
            "success": True,
            "message": f"获取{TABLE_DESCRIPTIONS[table_name]}表中 {len(records)} 条记录",
            "table_name": table_name,
            "records": records,
            "params": {
                "limit": limit,
                "offset": offset
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"获取记录失败: {str(e)}"
        }

def get_table_stats_impl(table_name: str = None) -> Dict[str, Any]:
    """获取表统计信息的实现"""
    try:
        if table_name:
            if table_name not in TABLE_DESCRIPTIONS:
                return {
                    "success": False,
                    "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                }
            
            stats = db.get_table_stats(table_name)
            stats['table_description'] = TABLE_DESCRIPTIONS[table_name]
            
            return {
                "success": True,
                "message": f"获取{TABLE_DESCRIPTIONS[table_name]}表统计信息",
                "stats": stats
            }
        else:
            # 获取所有表的统计信息
            all_stats = {}
            for table in TABLE_DESCRIPTIONS.keys():
                stats = db.get_table_stats(table)
                stats['table_description'] = TABLE_DESCRIPTIONS[table]
                all_stats[table] = stats
            
            return {
                "success": True,
                "message": "获取所有表的统计信息",
                "all_stats": all_stats
            }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"获取统计信息失败: {str(e)}"
        }

def get_available_tables_impl() -> Dict[str, Any]:
    """获取所有可用的表名和描述的实现"""
    try:
        return {
            "success": True,
            "message": "获取所有可用表信息",
            "tables": TABLE_DESCRIPTIONS,
            "table_count": len(TABLE_DESCRIPTIONS)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"获取表信息失败: {str(e)}"
        }

def get_all_table_contents_impl(include_empty: bool = True, limit_per_table: int = 100) -> Dict[str, Any]:
    """获取所有表的完整内容的实现"""
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
        
        return {
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
        return {
            "success": False,
            "message": f"获取所有表内容失败: {str(e)}"
        }

def get_table_names_with_details_impl() -> Dict[str, Any]:
    """获取所有表名及其详细信息的实现"""
    try:
        table_details = {}
        
        for table_name, description in TABLE_DESCRIPTIONS.items():
            try:
                # 获取表的统计信息
                stats = db.get_table_stats(table_name)
                
                table_details[table_name] = {
                    "chinese_name": description,
                    "english_name": table_name,
                    "total_records": stats['total_records'],
                    "latest_record_time": stats.get('latest_record_time'),
                    "earliest_record_time": stats.get('earliest_record_time')
                }
                
            except Exception as e:
                table_details[table_name] = {
                    "chinese_name": description,
                    "english_name": table_name,
                    "error": str(e),
                    "total_records": 0
                }
        
        total_tables = len(table_details)
        total_records = sum(details.get('total_records', 0) for details in table_details.values())
        
        return {
            "success": True,
            "message": f"成功获取 {total_tables} 个表的详细信息",
            "total_tables": total_tables,
            "total_records": total_records,
            "table_details": table_details
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"获取表名详细信息失败: {str(e)}"
        }

def export_table_data_impl(table_name: str, format: str = "json") -> Dict[str, Any]:
    """导出指定表的所有数据的实现"""
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        if format not in ["json", "csv"]:
            return {
                "success": False,
                "message": f"无效的格式: {format}。支持的格式: json, csv"
            }
        
        # 获取所有记录（不限制数量）
        records = db.get_all_records(table_name, limit=10000, offset=0)
        
        if format == "json":
            export_data = {
                "table_name": table_name,
                "table_description": TABLE_DESCRIPTIONS[table_name],
                "export_time": datetime.now().isoformat(),
                "record_count": len(records),
                "records": records
            }
            
            return {
                "success": True,
                "message": f"成功导出{TABLE_DESCRIPTIONS[table_name]}表的 {len(records)} 条记录",
                "format": "json",
                "data": export_data
            }
        
        elif format == "csv":
            # 转换为CSV格式的字符串
            if not records:
                csv_data = "id,content,related,created_time,updated_time\n"
            else:
                csv_lines = ["id,content,related,created_time,updated_time"]
                for record in records:
                    # 处理CSV中的特殊字符
                    content = str(record.get('content', '')).replace('"', '""')
                    related = str(record.get('related', '')).replace('"', '""')
                    csv_line = f'{record.get("id", "")},"{content}","{related}",{record.get("created_time", "")},{record.get("updated_time", "")}'
                    csv_lines.append(csv_line)
                csv_data = "\n".join(csv_lines)
            
            return {
                "success": True,
                "message": f"成功导出{TABLE_DESCRIPTIONS[table_name]}表的 {len(records)} 条记录",
                "format": "csv",
                "data": csv_data
            }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"导出表数据失败: {str(e)}"
        }

# 注册工具列表处理器
@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """返回可用工具列表"""
    tools = [
        Tool(
            name="add_belief",
            description="添加信念记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "信念内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表（可选）"}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="add_insight",
            description="添加洞察记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "洞察内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表（可选）"}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="add_focus",
            description="添加关注点记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "关注点内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表（可选）"}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="add_long_term_goal",
            description="添加长期目标记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "长期目标内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表（可选）"}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="add_short_term_goal",
            description="添加短期目标记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "短期目标内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表（可选）"}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="add_preference",
            description="添加偏好记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "偏好内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表（可选）"}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="add_decision",
            description="添加决策记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "决策内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表（可选）"}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="add_methodology",
            description="添加方法论记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "方法论内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表（可选）"}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="update_record",
            description="更新记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "record_id": {"type": "integer", "description": "记录ID"},
                    "content": {"type": "string", "description": "新内容（可选）"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "新相关主题列表（可选）"}
                },
                "required": ["table_name", "record_id"]
            }
        ),
        Tool(
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
        Tool(
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
        Tool(
            name="search_records",
            description="搜索记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "keyword": {"type": "string", "description": "内容关键词（可选）"},
                    "related_topic": {"type": "string", "description": "相关主题（可选）"},
                    "limit": {"type": "integer", "description": "返回记录数限制（默认20）", "default": 20},
                    "offset": {"type": "integer", "description": "偏移量（默认0）", "default": 0}
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="get_all_records",
            description="获取表中所有记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "limit": {"type": "integer", "description": "返回记录数限制（默认50）", "default": 50},
                    "offset": {"type": "integer", "description": "偏移量（默认0）", "default": 0}
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="get_table_stats",
            description="获取表统计信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名（可选，如果不提供则返回所有表的统计信息）", "enum": list(TABLE_DESCRIPTIONS.keys())}
                },
                "required": []
            }
        ),
        Tool(
            name="get_available_tables",
            description="获取所有可用的表名和描述",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_all_table_contents",
            description="获取所有表的完整内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_empty": {"type": "boolean", "description": "是否包含空表（默认True）", "default": True},
                    "limit_per_table": {"type": "integer", "description": "每个表的记录数限制（默认100）", "default": 100}
                },
                "required": []
            }
        ),
        Tool(
            name="get_table_names_with_details",
            description="获取所有表名及其详细信息（包括中文描述和统计信息）",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="export_table_data",
            description="导出指定表的所有数据",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "format": {"type": "string", "description": "导出格式", "enum": ["json", "csv"], "default": "json"}
                },
                "required": ["table_name"]
            }
        )
    ]
    
    return ListToolsResult(tools=tools)

# 注册工具调用处理器
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> CallToolResult:
    """处理工具调用"""
    try:
        # 根据工具名称调用相应的实现函数
        if name == "add_belief":
            result = add_belief_impl(
                content=arguments["content"],
                related=arguments.get("related")
            )
        elif name == "add_insight":
            result = add_insight_impl(
                content=arguments["content"],
                related=arguments.get("related")
            )
        elif name == "add_focus":
            result = add_focus_impl(
                content=arguments["content"],
                related=arguments.get("related")
            )
        elif name == "add_long_term_goal":
            result = add_long_term_goal_impl(
                content=arguments["content"],
                related=arguments.get("related")
            )
        elif name == "add_short_term_goal":
            result = add_short_term_goal_impl(
                content=arguments["content"],
                related=arguments.get("related")
            )
        elif name == "add_preference":
            result = add_preference_impl(
                content=arguments["content"],
                related=arguments.get("related")
            )
        elif name == "add_decision":
            result = add_decision_impl(
                content=arguments["content"],
                related=arguments.get("related")
            )
        elif name == "add_methodology":
            result = add_methodology_impl(
                content=arguments["content"],
                related=arguments.get("related")
            )
        elif name == "update_record":
            result = update_record_impl(
                table_name=arguments["table_name"],
                record_id=arguments["record_id"],
                content=arguments.get("content"),
                related=arguments.get("related")
            )
        elif name == "delete_record":
            result = delete_record_impl(
                table_name=arguments["table_name"],
                record_id=arguments["record_id"]
            )
        elif name == "get_record":
            result = get_record_impl(
                table_name=arguments["table_name"],
                record_id=arguments["record_id"]
            )
        elif name == "search_records":
            result = search_records_impl(
                table_name=arguments["table_name"],
                keyword=arguments.get("keyword"),
                related_topic=arguments.get("related_topic"),
                limit=arguments.get("limit", 20),
                offset=arguments.get("offset", 0)
            )
        elif name == "get_all_records":
            result = get_all_records_impl(
                table_name=arguments["table_name"],
                limit=arguments.get("limit", 50),
                offset=arguments.get("offset", 0)
            )
        elif name == "get_table_stats":
            result = get_table_stats_impl(
                table_name=arguments.get("table_name")
            )
        elif name == "get_available_tables":
            result = get_available_tables_impl()
        elif name == "get_all_table_contents":
            result = get_all_table_contents_impl(
                include_empty=arguments.get("include_empty", True),
                limit_per_table=arguments.get("limit_per_table", 100)
            )
        elif name == "get_table_names_with_details":
            result = get_table_names_with_details_impl()
        elif name == "export_table_data":
            result = export_table_data_impl(
                table_name=arguments["table_name"],
                format=arguments.get("format", "json")
            )
        else:
            result = {
                "success": False,
                "message": f"未知的工具: {name}"
            }
        
        # 将结果转换为JSON字符串
        result_text = json.dumps(result, ensure_ascii=False, indent=2)
        
        return CallToolResult(
            content=[TextContent(type="text", text=result_text)]
        )
        
    except Exception as e:
        error_result = {
            "success": False,
            "message": f"工具调用失败: {str(e)}"
        }
        error_text = json.dumps(error_result, ensure_ascii=False, indent=2)
        
        return CallToolResult(
            content=[TextContent(type="text", text=error_text)]
        )

# 主函数
async def main():
    """启动MCP服务器"""
    from mcp.server.lowlevel import NotificationOptions
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="个人画像数据管理系统",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            ),
        )

# 如果直接运行此文件，启动服务器
if __name__ == "__main__":
    asyncio.run(main())

# 导出服务器实例
__all__ = ['server', 'main']
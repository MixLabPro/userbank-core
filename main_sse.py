"""
个人画像数据管理系统 - SSE模式 (修正版)
基于MCP官方文档的标准SSE实现
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

from src.database import get_database

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

# 创建MCP服务器实例
app = Server("个人画像数据管理系统")

# 创建SSE传输实例
sse = SseServerTransport("/messages")

# 工具列表函数
@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """列出所有可用的工具"""
    return [
        types.Tool(
            name="add_belief",
            description="添加信念记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "信念内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表"}
                },
                "required": ["content"]
            }
        ),
        types.Tool(
            name="add_insight",
            description="添加洞察记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "洞察内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表"}
                },
                "required": ["content"]
            }
        ),
        types.Tool(
            name="add_focus",
            description="添加关注点记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "关注点内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表"}
                },
                "required": ["content"]
            }
        ),
        types.Tool(
            name="add_long_term_goal",
            description="添加长期目标记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "长期目标内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表"}
                },
                "required": ["content"]
            }
        ),
        types.Tool(
            name="add_short_term_goal",
            description="添加短期目标记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "短期目标内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表"}
                },
                "required": ["content"]
            }
        ),
        types.Tool(
            name="add_preference",
            description="添加偏好记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "偏好内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表"}
                },
                "required": ["content"]
            }
        ),
        types.Tool(
            name="add_decision",
            description="添加决策记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "决策内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表"}
                },
                "required": ["content"]
            }
        ),
        types.Tool(
            name="add_methodology",
            description="添加方法论记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "方法论内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表"}
                },
                "required": ["content"]
            }
        ),
        types.Tool(
            name="update_record",
            description="更新记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "表名", "enum": list(TABLE_DESCRIPTIONS.keys())},
                    "record_id": {"type": "integer", "description": "记录ID"},
                    "content": {"type": "string", "description": "新内容"},
                    "related": {"type": "array", "items": {"type": "string"}, "description": "相关主题列表"}
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
                    "related_topic": {"type": "string", "description": "相关主题"},
                    "limit": {"type": "integer", "description": "返回记录数限制", "default": 20},
                    "offset": {"type": "integer", "description": "偏移量", "default": 0}
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
        if name == "add_belief":
            content = arguments["content"]
            related = arguments.get("related")
            record_id = db.insert_record('belief', content, related)
            result = {
                "success": True,
                "message": f"成功添加信念记录",
                "record_id": record_id,
                "content": content,
                "related": related or []
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "add_insight":
            content = arguments["content"]
            related = arguments.get("related")
            record_id = db.insert_record('insight', content, related)
            result = {
                "success": True,
                "message": f"成功添加洞察记录",
                "record_id": record_id,
                "content": content,
                "related": related or []
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "add_focus":
            content = arguments["content"]
            related = arguments.get("related")
            record_id = db.insert_record('focus', content, related)
            result = {
                "success": True,
                "message": f"成功添加关注点记录",
                "record_id": record_id,
                "content": content,
                "related": related or []
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "add_long_term_goal":
            content = arguments["content"]
            related = arguments.get("related")
            record_id = db.insert_record('long_term_goal', content, related)
            result = {
                "success": True,
                "message": f"成功添加长期目标记录",
                "record_id": record_id,
                "content": content,
                "related": related or []
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "add_short_term_goal":
            content = arguments["content"]
            related = arguments.get("related")
            record_id = db.insert_record('short_term_goal', content, related)
            result = {
                "success": True,
                "message": f"成功添加短期目标记录",
                "record_id": record_id,
                "content": content,
                "related": related or []
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "add_preference":
            content = arguments["content"]
            related = arguments.get("related")
            record_id = db.insert_record('preference', content, related)
            result = {
                "success": True,
                "message": f"成功添加偏好记录",
                "record_id": record_id,
                "content": content,
                "related": related or []
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "add_decision":
            content = arguments["content"]
            related = arguments.get("related")
            record_id = db.insert_record('decision', content, related)
            result = {
                "success": True,
                "message": f"成功添加决策记录",
                "record_id": record_id,
                "content": content,
                "related": related or []
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "add_methodology":
            content = arguments["content"]
            related = arguments.get("related")
            record_id = db.insert_record('methodology', content, related)
            result = {
                "success": True,
                "message": f"成功添加方法论记录",
                "record_id": record_id,
                "content": content,
                "related": related or []
            }
            return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
        elif name == "update_record":
            table_name = arguments["table_name"]
            record_id = arguments["record_id"]
            content = arguments.get("content")
            related = arguments.get("related")
            
            if table_name not in TABLE_DESCRIPTIONS:
                result = {
                    "success": False,
                    "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                }
            else:
                success = db.update_record(table_name, record_id, content, related)
                if success:
                    result = {
                        "success": True,
                        "message": f"成功更新{TABLE_DESCRIPTIONS[table_name]}记录",
                        "record_id": record_id,
                        "table_name": table_name
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
            keyword = arguments.get("keyword")
            related_topic = arguments.get("related_topic")
            limit = arguments.get("limit", 20)
            offset = arguments.get("offset", 0)
            
            if table_name not in TABLE_DESCRIPTIONS:
                result = {
                    "success": False,
                    "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                }
            else:
                records = db.search_records(table_name, keyword, related_topic, limit, offset)
                result = {
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
                all_stats = {}
                for table in TABLE_DESCRIPTIONS.keys():
                    stats = db.get_table_stats(table)
                    stats['table_description'] = TABLE_DESCRIPTIONS[table]
                    all_stats[table] = stats
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
                    schema = db.get_table_schema(table_name)
                    result = {
                        "success": True,
                        "message": f"获取{TABLE_DESCRIPTIONS[table_name]}表结构信息",
                        "schema": schema
                    }
            else:
                # 获取所有表的结构信息
                all_schemas = {}
                for table in TABLE_DESCRIPTIONS.keys():
                    schema = db.get_table_schema(table)
                    all_schemas[table] = schema
                result = {
                    "success": True,
                    "message": "获取所有表的结构信息",
                    "all_schemas": all_schemas
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
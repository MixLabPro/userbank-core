"""
个人画像数据管理系统 - 重构版本
使用模块化的工具结构
"""

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional, Union
import json
import os
from pathlib import Path
from datetime import datetime

# 导入工具模块
from tools import (
    PersonaTools, MemoryTools, ViewpointTools, InsightTools,
    GoalTools, PreferenceTools, MethodologyTools, FocusTools,
    PredictionTools, DatabaseTools
)

# 创建FastMCP服务器实例
mcp = FastMCP("个人画像数据管理系统")

# 初始化工具实例
persona_tools = PersonaTools()
memory_tools = MemoryTools()
viewpoint_tools = ViewpointTools()
insight_tools = InsightTools()
goal_tools = GoalTools()
preference_tools = PreferenceTools()
methodology_tools = MethodologyTools()
focus_tools = FocusTools()
prediction_tools = PredictionTools()
database_tools = DatabaseTools()

# ============ 人物档案相关操作 ============

@mcp.tool()
def get_persona() -> Dict[str, Any]:
    """获取当前用户的核心画像信息。该信息用于AI进行个性化交互。系统中只有一个用户画像，ID固定为1。"""
    return persona_tools.get_persona()

@mcp.tool()
def save_persona(name: str = None, gender: str = None, personality: str = None, 
                avatar_url: str = None, bio: str = None, privacy_level: str = None) -> Dict[str, Any]:
    """保存（更新）当前用户的核心画像信息。由于ID固定为1，此操作主要用于更新现有画像。只需提供需要修改的字段。"""
    return persona_tools.save_persona(name, gender, personality, avatar_url, bio, privacy_level)

# ============ 记忆工具 ============

@mcp.tool()
def manage_memories(action: str, id: int = None, content: str = None, memory_type: str = None,
                   importance: int = None, related_people: str = None, location: str = None,
                   memory_date: str = None, keywords: List[str] = None, source_app: str = 'unknown',
                   reference_urls: List[str] = None, privacy_level: str = 'public',
                   filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                   sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """记忆数据管理工具。支持查询和保存操作。
    
    参数说明：
    - action: 操作类型，'query'(查询) 或 'save'(保存)
    
    查询操作 (action='query') 使用参数：
    - filter: 查询条件字典
    - sort_by, sort_order, limit, offset: 排序和分页参数
    
    保存操作 (action='save') 使用参数：
    - id: 记录ID，None表示创建新记录，有值表示更新现有记录
    - content, memory_type, importance 等: 记忆数据字段
    """
    if action == "query":
        return memory_tools.query_memories(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return memory_tools.save_memory(id, content, memory_type, importance, related_people, 
                                       location, memory_date, keywords, source_app, 
                                       reference_urls, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"无效的操作类型: {action}，支持的操作: 'query', 'save'"
        }

# ============ 观点工具 ============

@mcp.tool()
def manage_viewpoints(action: str, id: int = None, content: str = None, source_people: str = None,
                     keywords: List[str] = None, source_app: str = 'unknown',
                     related_event: str = None, reference_urls: List[str] = None,
                     privacy_level: str = 'public', filter: Dict[str, Any] = None, 
                     sort_by: str = 'created_time', sort_order: str = 'desc', 
                     limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """观点数据管理工具。支持查询和保存操作。"""
    if action == "query":
        return viewpoint_tools.query_viewpoints(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return viewpoint_tools.save_viewpoint(id, content, source_people, keywords, 
                                             source_app, related_event, reference_urls, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"无效的操作类型: {action}，支持的操作: 'query', 'save'"
        }

# ============ 洞察工具 ============

@mcp.tool()
def manage_insights(action: str, id: int = None, content: str = None, source_people: str = None,
                   keywords: List[str] = None, source_app: str = 'unknown',
                   reference_urls: List[str] = None, privacy_level: str = 'public',
                   filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                   sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """洞察数据管理工具。支持查询和保存操作。"""
    if action == "query":
        return insight_tools.query_insights(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return insight_tools.save_insight(id, content, source_people, keywords, 
                                         source_app, reference_urls, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"无效的操作类型: {action}，支持的操作: 'query', 'save'"
        }

# ============ 目标工具 ============

@mcp.tool()
def manage_goals(action: str, id: int = None, content: str = None, type: str = None, 
                deadline: str = None, status: str = 'planning', keywords: List[str] = None, 
                source_app: str = 'unknown', privacy_level: str = 'public',
                filter: Dict[str, Any] = None, sort_by: str = 'deadline', 
                sort_order: str = 'asc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """目标数据管理工具。支持查询和保存操作。"""
    if action == "query":
        return goal_tools.query_goals(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return goal_tools.save_goal(id, content, type, deadline, status, keywords, 
                                   source_app, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"无效的操作类型: {action}，支持的操作: 'query', 'save'"
        }

# ============ 偏好工具 ============

@mcp.tool()
def manage_preferences(action: str, id: int = None, content: str = None, context: str = None,
                      keywords: List[str] = None, source_app: str = 'unknown',
                      privacy_level: str = 'public', filter: Dict[str, Any] = None, 
                      sort_by: str = 'created_time', sort_order: str = 'desc', 
                      limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """偏好数据管理工具。支持查询和保存操作。"""
    if action == "query":
        return preference_tools.query_preferences(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return preference_tools.save_preference(id, content, context, keywords, 
                                               source_app, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"无效的操作类型: {action}，支持的操作: 'query', 'save'"
        }

# ============ 方法论工具 ============

@mcp.tool()
def manage_methodologies(action: str, id: int = None, content: str = None, type: str = None,
                        effectiveness: str = 'experimental', use_cases: str = None,
                        keywords: List[str] = None, source_app: str = 'unknown',
                        reference_urls: List[str] = None, privacy_level: str = 'public',
                        filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                        sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """方法论数据管理工具。支持查询和保存操作。"""
    if action == "query":
        return methodology_tools.query_methodologies(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return methodology_tools.save_methodology(id, content, type, effectiveness, use_cases, 
                                                 keywords, source_app, reference_urls, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"无效的操作类型: {action}，支持的操作: 'query', 'save'"
        }

# ============ 关注点工具 ============

@mcp.tool()
def manage_focuses(action: str, id: int = None, content: str = None, priority: int = None, 
                  status: str = 'active', context: str = None, keywords: List[str] = None, 
                  source_app: str = 'unknown', deadline: str = None, privacy_level: str = 'public',
                  filter: Dict[str, Any] = None, sort_by: str = 'priority', 
                  sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """关注点数据管理工具。支持查询和保存操作。"""
    if action == "query":
        return focus_tools.query_focuses(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return focus_tools.save_focus(id, content, priority, status, context, keywords, 
                                     source_app, deadline, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"无效的操作类型: {action}，支持的操作: 'query', 'save'"
        }

# ============ 预测工具 ============

@mcp.tool()
def manage_predictions(action: str, id: int = None, content: str = None, timeframe: str = None, 
                      basis: str = None, verification_status: str = 'pending', 
                      keywords: List[str] = None, source_app: str = 'unknown', 
                      reference_urls: List[str] = None, privacy_level: str = 'public',
                      filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                      sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """预测数据管理工具。支持查询和保存操作。"""
    if action == "query":
        return prediction_tools.query_predictions(filter, sort_by, sort_order, limit, offset)
    elif action == "save":
        return prediction_tools.save_prediction(id, content, timeframe, basis, verification_status, 
                                               keywords, source_app, reference_urls, privacy_level)
    else:
        return {
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": f"无效的操作类型: {action}，支持的操作: 'query', 'save'"
        }

# ============ 数据库工具 ============

@mcp.tool()
def execute_custom_sql(sql: str, params: List[str] = None, fetch_results: bool = True) -> Dict[str, Any]:
    """执行自定义SQL语句"""
    return database_tools.execute_custom_sql(sql, params, fetch_results)

@mcp.tool()
def get_table_schema(table_name: str = None) -> Dict[str, Any]:
    """获取表结构信息"""
    return database_tools.get_table_schema(table_name)

# ============ 启动服务器 ============

if __name__ == "__main__":
    mcp.run()
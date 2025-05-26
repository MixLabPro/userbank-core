"""
MCP工具模块
MCP Tools Module

基于FastMCP框架的个人画像数据管理工具集
"""

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import json
import logging
from .database import get_database, ProfileDatabase

# 配置日志
logger = logging.getLogger(__name__)

# 创建FastMCP实例
mcp = FastMCP("个人画像数据管理系统 🧠")

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

@mcp.tool()
def add_belief(content: str, related: List[str] = None) -> Dict[str, Any]:
    """
    添加信念记录
    
    Args:
        content: 信念内容
        related: 相关主题列表（可选）
        
    Returns:
        操作结果
    """
    try:
        record_id = db.insert_record('belief', content, related)
        logger.info(f"成功添加信念记录，ID: {record_id}")
        return {
            "success": True,
            "message": f"成功添加信念记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        logger.error(f"添加信念记录失败: {e}")
        return {
            "success": False,
            "message": f"添加信念记录失败: {str(e)}"
        }

@mcp.tool()
def add_insight(content: str, related: List[str] = None) -> Dict[str, Any]:
    """
    添加洞察记录
    
    Args:
        content: 洞察内容
        related: 相关主题列表（可选）
        
    Returns:
        操作结果
    """
    try:
        record_id = db.insert_record('insight', content, related)
        logger.info(f"成功添加洞察记录，ID: {record_id}")
        return {
            "success": True,
            "message": f"成功添加洞察记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        logger.error(f"添加洞察记录失败: {e}")
        return {
            "success": False,
            "message": f"添加洞察记录失败: {str(e)}"
        }

@mcp.tool()
def add_focus(content: str, related: List[str] = None) -> Dict[str, Any]:
    """
    添加关注点记录
    
    Args:
        content: 关注点内容
        related: 相关主题列表（可选）
        
    Returns:
        操作结果
    """
    try:
        record_id = db.insert_record('focus', content, related)
        logger.info(f"成功添加关注点记录，ID: {record_id}")
        return {
            "success": True,
            "message": f"成功添加关注点记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        logger.error(f"添加关注点记录失败: {e}")
        return {
            "success": False,
            "message": f"添加关注点记录失败: {str(e)}"
        }

@mcp.tool()
def add_long_term_goal(content: str, related: List[str] = None) -> Dict[str, Any]:
    """
    添加长期目标记录
    
    Args:
        content: 长期目标内容
        related: 相关主题列表（可选）
        
    Returns:
        操作结果
    """
    try:
        record_id = db.insert_record('long_term_goal', content, related)
        logger.info(f"成功添加长期目标记录，ID: {record_id}")
        return {
            "success": True,
            "message": f"成功添加长期目标记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        logger.error(f"添加长期目标记录失败: {e}")
        return {
            "success": False,
            "message": f"添加长期目标记录失败: {str(e)}"
        }

@mcp.tool()
def add_short_term_goal(content: str, related: List[str] = None) -> Dict[str, Any]:
    """
    添加短期目标记录
    
    Args:
        content: 短期目标内容
        related: 相关主题列表（可选）
        
    Returns:
        操作结果
    """
    try:
        record_id = db.insert_record('short_term_goal', content, related)
        logger.info(f"成功添加短期目标记录，ID: {record_id}")
        return {
            "success": True,
            "message": f"成功添加短期目标记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        logger.error(f"添加短期目标记录失败: {e}")
        return {
            "success": False,
            "message": f"添加短期目标记录失败: {str(e)}"
        }

@mcp.tool()
def add_preference(content: str, related: List[str] = None) -> Dict[str, Any]:
    """
    添加偏好记录
    
    Args:
        content: 偏好内容
        related: 相关主题列表（可选）
        
    Returns:
        操作结果
    """
    try:
        record_id = db.insert_record('preference', content, related)
        logger.info(f"成功添加偏好记录，ID: {record_id}")
        return {
            "success": True,
            "message": f"成功添加偏好记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        logger.error(f"添加偏好记录失败: {e}")
        return {
            "success": False,
            "message": f"添加偏好记录失败: {str(e)}"
        }

@mcp.tool()
def add_decision(content: str, related: List[str] = None) -> Dict[str, Any]:
    """
    添加决策记录
    
    Args:
        content: 决策内容
        related: 相关主题列表（可选）
        
    Returns:
        操作结果
    """
    try:
        record_id = db.insert_record('decision', content, related)
        logger.info(f"成功添加决策记录，ID: {record_id}")
        return {
            "success": True,
            "message": f"成功添加决策记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        logger.error(f"添加决策记录失败: {e}")
        return {
            "success": False,
            "message": f"添加决策记录失败: {str(e)}"
        }

@mcp.tool()
def add_methodology(content: str, related: List[str] = None) -> Dict[str, Any]:
    """
    添加方法论记录
    
    Args:
        content: 方法论内容
        related: 相关主题列表（可选）
        
    Returns:
        操作结果
    """
    try:
        record_id = db.insert_record('methodology', content, related)
        logger.info(f"成功添加方法论记录，ID: {record_id}")
        return {
            "success": True,
            "message": f"成功添加方法论记录",
            "record_id": record_id,
            "content": content,
            "related": related or []
        }
    except Exception as e:
        logger.error(f"添加方法论记录失败: {e}")
        return {
            "success": False,
            "message": f"添加方法论记录失败: {str(e)}"
        }

@mcp.tool()
def update_record(table_name: str, record_id: int, content: str = None, related: List[str] = None) -> Dict[str, Any]:
    """
    更新记录
    
    Args:
        table_name: 表名 (belief/insight/focus/long_term_goal/short_term_goal/preference/decision/methodology)
        record_id: 记录ID
        content: 新内容（可选）
        related: 新相关主题列表（可选）
        
    Returns:
        操作结果
    """
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        success = db.update_record(table_name, record_id, content, related)
        
        if success:
            logger.info(f"成功更新{TABLE_DESCRIPTIONS[table_name]}记录，ID: {record_id}")
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
        logger.error(f"更新记录失败: {e}")
        return {
            "success": False,
            "message": f"更新记录失败: {str(e)}"
        }

@mcp.tool()
def delete_record(table_name: str, record_id: int) -> Dict[str, Any]:
    """
    删除记录
    
    Args:
        table_name: 表名 (belief/insight/focus/long_term_goal/short_term_goal/preference/decision/methodology)
        record_id: 记录ID
        
    Returns:
        操作结果
    """
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        success = db.delete_record(table_name, record_id)
        
        if success:
            logger.info(f"成功删除{TABLE_DESCRIPTIONS[table_name]}记录，ID: {record_id}")
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
        logger.error(f"删除记录失败: {e}")
        return {
            "success": False,
            "message": f"删除记录失败: {str(e)}"
        }

@mcp.tool()
def get_record(table_name: str, record_id: int) -> Dict[str, Any]:
    """
    获取单条记录
    
    Args:
        table_name: 表名 (belief/insight/focus/long_term_goal/short_term_goal/preference/decision/methodology)
        record_id: 记录ID
        
    Returns:
        记录详情或错误信息
    """
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        record = db.get_record(table_name, record_id)
        
        if record:
            logger.info(f"成功获取{TABLE_DESCRIPTIONS[table_name]}记录，ID: {record_id}")
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
        logger.error(f"获取记录失败: {e}")
        return {
            "success": False,
            "message": f"获取记录失败: {str(e)}"
        }

@mcp.tool()
def search_records(table_name: str, keyword: str = None, related_topic: str = None, 
                  limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """
    搜索记录
    
    Args:
        table_name: 表名 (belief/insight/focus/long_term_goal/short_term_goal/preference/decision/methodology)
        keyword: 内容关键词（可选）
        related_topic: 相关主题（可选）
        limit: 返回记录数限制（默认20）
        offset: 偏移量（默认0）
        
    Returns:
        搜索结果
    """
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        records = db.search_records(table_name, keyword, related_topic, limit, offset)
        
        logger.info(f"在{TABLE_DESCRIPTIONS[table_name]}表中搜索到 {len(records)} 条记录")
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
        logger.error(f"搜索记录失败: {e}")
        return {
            "success": False,
            "message": f"搜索记录失败: {str(e)}"
        }

@mcp.tool()
def get_all_records(table_name: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    """
    获取表中所有记录
    
    Args:
        table_name: 表名 (belief/insight/focus/long_term_goal/short_term_goal/preference/decision/methodology)
        limit: 返回记录数限制（默认50）
        offset: 偏移量（默认0）
        
    Returns:
        所有记录
    """
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        records = db.get_all_records(table_name, limit, offset)
        
        logger.info(f"获取{TABLE_DESCRIPTIONS[table_name]}表中 {len(records)} 条记录")
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
        logger.error(f"获取记录失败: {e}")
        return {
            "success": False,
            "message": f"获取记录失败: {str(e)}"
        }

@mcp.tool()
def get_table_stats(table_name: str = None) -> Dict[str, Any]:
    """
    获取表统计信息
    
    Args:
        table_name: 表名（可选，如果不提供则返回所有表的统计信息）
        
    Returns:
        统计信息
    """
    try:
        if table_name:
            if table_name not in TABLE_DESCRIPTIONS:
                return {
                    "success": False,
                    "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                }
            
            stats = db.get_table_stats(table_name)
            stats['table_description'] = TABLE_DESCRIPTIONS[table_name]
            
            logger.info(f"获取{TABLE_DESCRIPTIONS[table_name]}表统计信息")
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
            
            logger.info("获取所有表的统计信息")
            return {
                "success": True,
                "message": "获取所有表的统计信息",
                "all_stats": all_stats
            }
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return {
            "success": False,
            "message": f"获取统计信息失败: {str(e)}"
        }

@mcp.tool()
def get_available_tables() -> Dict[str, Any]:
    """
    获取所有可用的表名和描述
    
    Returns:
        表名和描述的映射
    """
    try:
        logger.info("获取所有可用表信息")
        return {
            "success": True,
            "message": "获取所有可用表信息",
            "tables": TABLE_DESCRIPTIONS,
            "table_count": len(TABLE_DESCRIPTIONS)
        }
    except Exception as e:
        logger.error(f"获取表信息失败: {e}")
        return {
            "success": False,
            "message": f"获取表信息失败: {str(e)}"
        }

# 导出MCP实例
__all__ = ['mcp']
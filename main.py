"""
FastMCP版本的个人画像数据管理系统
"""

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import json

from src.database import get_database

# 创建FastMCP服务器实例
mcp = FastMCP("个人画像数据管理系统")

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

# 添加信念记录
@mcp.tool()
def add_belief(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加信念记录"""
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

# 添加洞察记录
@mcp.tool()
def add_insight(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加洞察记录"""
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

# 添加关注点记录
@mcp.tool()
def add_focus(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加关注点记录"""
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

# 添加长期目标记录
@mcp.tool()
def add_long_term_goal(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加长期目标记录"""
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

# 添加短期目标记录
@mcp.tool()
def add_short_term_goal(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加短期目标记录"""
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

# 添加偏好记录
@mcp.tool()
def add_preference(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加偏好记录"""
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

# 添加决策记录
@mcp.tool()
def add_decision(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加决策记录"""
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

# 添加方法论记录
@mcp.tool()
def add_methodology(content: str, related: List[str] = None) -> Dict[str, Any]:
    """添加方法论记录"""
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

# 更新记录
@mcp.tool()
def update_record(table_name: str, record_id: int, content: str = None, related: List[str] = None) -> Dict[str, Any]:
    """更新记录"""
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

# 删除记录
@mcp.tool()
def delete_record(table_name: str, record_id: int) -> Dict[str, Any]:
    """删除记录"""
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

# 获取单条记录
@mcp.tool()
def get_record(table_name: str, record_id: int) -> Dict[str, Any]:
    """获取单条记录"""
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

# 搜索记录
@mcp.tool()
def search_records(table_name: str, keyword: str = None, related_topic: str = None, 
                  limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """搜索记录"""
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

# 获取表中所有记录
@mcp.tool()
def get_all_records(table_name: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    """获取表中所有记录"""
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

# 获取表统计信息
@mcp.tool()
def get_table_stats(table_name: str = None) -> Dict[str, Any]:
    """获取表统计信息"""
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

# 获取所有可用的表名和描述
@mcp.tool()
def get_available_tables() -> Dict[str, Any]:
    """获取所有可用的表名和描述"""
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

# 获取所有表的完整内容
@mcp.tool()
def get_all_table_contents(include_empty: bool = True, limit_per_table: int = 100) -> Dict[str, Any]:
    """获取所有表的完整内容"""
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

# 获取所有表名及其详细信息
@mcp.tool()
def get_table_names_with_details() -> Dict[str, Any]:
    """获取所有表名及其详细信息（包括中文描述和统计信息）"""
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

# 导出指定表的所有数据
@mcp.tool()
def export_table_data(table_name: str, format: str = "json") -> Dict[str, Any]:
    """导出指定表的所有数据"""
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
            from datetime import datetime
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

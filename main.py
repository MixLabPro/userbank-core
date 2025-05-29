"""
FastMCP版本的个人画像数据管理系统
基于database.md文档的完整实现
"""

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional, Union
import json
import os
from pathlib import Path

from Database.database import get_database

# 创建FastMCP服务器实例
mcp = FastMCP("个人画像数据管理系统")

# 获取数据库实例（现在会自动使用main.py同级目录的路径）
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

# ============ 人物档案相关操作 ============

@mcp.tool()
def get_persona() -> Dict[str, Any]:
    """获取用户画像信息"""
    try:
        persona = db.get_persona()
        if persona:
            return {
                "success": True,
                "message": "成功获取用户画像",
                "persona": persona
            }
        else:
            return {
                "success": False,
                "message": "未找到用户画像信息"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"获取用户画像失败: {str(e)}"
        }

@mcp.tool()
def update_persona(name: str = None, gender: str = None, personality: str = None, 
                  avatar_url: str = None, bio: str = None) -> Dict[str, Any]:
    """更新用户画像信息"""
    try:
        update_data = {}
        if name is not None:
            update_data['name'] = name
        if gender is not None:
            update_data['gender'] = gender
        if personality is not None:
            update_data['personality'] = personality
        if avatar_url is not None:
            update_data['avatar_url'] = avatar_url
        if bio is not None:
            update_data['bio'] = bio
        
        if not update_data:
            return {
                "success": False,
                "message": "没有提供要更新的字段"
            }
        
        success = db.update_persona(**update_data)
        if success:
            return {
                "success": True,
                "message": "成功更新用户画像",
                "updated_fields": list(update_data.keys())
            }
        else:
            return {
                "success": False,
                "message": "更新用户画像失败"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"更新用户画像失败: {str(e)}"
        }

# ============ 分类管理 ============

@mcp.tool()
def get_categories(first_level: str = None) -> Dict[str, Any]:
    """获取分类列表"""
    try:
        categories = db.get_categories(first_level)
        return {
            "success": True,
            "message": f"成功获取 {len(categories)} 个分类",
            "categories": categories
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"获取分类失败: {str(e)}"
        }

@mcp.tool()
def add_category(first_level: str, second_level: str = None, description: str = None) -> Dict[str, Any]:
    """添加新分类"""
    try:
        category_id = db.insert_record('category',
                                     first_level=first_level,
                                     second_level=second_level,
                                     description=description,
                                     is_active=1)
        return {
            "success": True,
            "message": "成功添加分类",
            "category_id": category_id,
            "first_level": first_level,
            "second_level": second_level
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加分类失败: {str(e)}"
        }

# ============ 观点管理 ============

@mcp.tool()
def add_viewpoint(content: str, subject: str, stance: int = None, source: str = None,
                 time_period: str = None, reference_urls: List[str] = None, 
                 category_id: int = None) -> Dict[str, Any]:
    """添加观点记录"""
    try:
        record_id = db.insert_record('viewpoint',
                                   content=content,
                                   subject=subject,
                                   stance=stance,
                                   source=source,
                                   time_period=time_period,
                                   reference_urls=reference_urls or [],
                                   category_id=category_id)
        return {
            "success": True,
            "message": "成功添加观点记录",
            "record_id": record_id,
            "content": content,
            "subject": subject
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加观点记录失败: {str(e)}"
        }

# ============ 洞察管理 ============

@mcp.tool()
def add_insight(content: str, trigger_event: str = None, impact_level: str = 'medium',
               reference_urls: List[str] = None, category_id: int = None) -> Dict[str, Any]:
    """添加洞察记录"""
    try:
        record_id = db.insert_record('insight',
                                   content=content,
                                   trigger_event=trigger_event,
                                   impact_level=impact_level,
                                   reference_urls=reference_urls or [],
                                   category_id=category_id)
        return {
            "success": True,
            "message": "成功添加洞察记录",
            "record_id": record_id,
            "content": content,
            "impact_level": impact_level
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加洞察记录失败: {str(e)}"
        }

# ============ 关注点管理 ============

@mcp.tool()
def add_focus(content: str, priority: int = None, status: str = 'active',
             context: str = None, deadline: str = None, category_id: int = None) -> Dict[str, Any]:
    """添加关注点记录"""
    try:
        record_id = db.insert_record('focus',
                                   content=content,
                                   priority=priority,
                                   status=status,
                                   context=context,
                                   deadline=deadline,
                                   category_id=category_id)
        return {
            "success": True,
            "message": "成功添加关注点记录",
            "record_id": record_id,
            "content": content,
            "priority": priority,
            "status": status
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加关注点记录失败: {str(e)}"
        }

# ============ 目标管理 ============

@mcp.tool()
def add_goal(content: str, type: str, deadline: str = None, progress: int = 0,
            status: str = 'planning', category_id: int = None) -> Dict[str, Any]:
    """添加目标记录"""
    try:
        record_id = db.insert_record('goal',
                                   content=content,
                                   type=type,
                                   deadline=deadline,
                                   progress=progress,
                                   status=status,
                                   category_id=category_id)
        return {
            "success": True,
            "message": f"成功添加{type}目标记录",
            "record_id": record_id,
            "content": content,
            "type": type,
            "status": status
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加目标记录失败: {str(e)}"
        }

# ============ 偏好管理 ============

@mcp.tool()
def add_preference(content: str, strength: str = 'moderate', context: str = None,
                  category_id: int = None) -> Dict[str, Any]:
    """添加偏好记录"""
    try:
        record_id = db.insert_record('preference',
                                   content=content,
                                   strength=strength,
                                   context=context,
                                   category_id=category_id)
        return {
            "success": True,
            "message": "成功添加偏好记录",
            "record_id": record_id,
            "content": content,
            "strength": strength
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加偏好记录失败: {str(e)}"
        }

# ============ 决策管理 ============

@mcp.tool()
def add_decision(content: str, reasoning: str = None, outcome: str = None,
                domain: str = None, category_id: int = None) -> Dict[str, Any]:
    """添加决策记录"""
    try:
        record_id = db.insert_record('decision',
                                   content=content,
                                   reasoning=reasoning,
                                   outcome=outcome,
                                   domain=domain,
                                   category_id=category_id)
        return {
            "success": True,
            "message": "成功添加决策记录",
            "record_id": record_id,
            "content": content,
            "domain": domain
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加决策记录失败: {str(e)}"
        }

# ============ 方法论管理 ============

@mcp.tool()
def add_methodology(content: str, type: str = None, effectiveness: str = 'experimental',
                   use_cases: str = None, reference_urls: List[str] = None,
                   category_id: int = None) -> Dict[str, Any]:
    """添加方法论记录"""
    try:
        record_id = db.insert_record('methodology',
                                   content=content,
                                   type=type,
                                   effectiveness=effectiveness,
                                   use_cases=use_cases,
                                   reference_urls=reference_urls or [],
                                   category_id=category_id)
        return {
            "success": True,
            "message": "成功添加方法论记录",
            "record_id": record_id,
            "content": content,
            "effectiveness": effectiveness
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加方法论记录失败: {str(e)}"
        }

# ============ 经验管理 ============

@mcp.tool()
def add_experience(content: str, field: str, expertise_level: str = 'beginner',
                  years: int = 0, key_learnings: str = None, 
                  reference_urls: List[str] = None, category_id: int = None) -> Dict[str, Any]:
    """添加经验记录"""
    try:
        record_id = db.insert_record('experience',
                                   content=content,
                                   field=field,
                                   expertise_level=expertise_level,
                                   years=years,
                                   key_learnings=key_learnings,
                                   reference_urls=reference_urls or [],
                                   category_id=category_id)
        return {
            "success": True,
            "message": "成功添加经验记录",
            "record_id": record_id,
            "content": content,
            "field": field,
            "expertise_level": expertise_level
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加经验记录失败: {str(e)}"
        }

# ============ 预测管理 ============

@mcp.tool()
def add_prediction(content: str, timeframe: str = None, basis: str = None,
                  verification_status: str = 'pending', reference_urls: List[str] = None,
                  category_id: int = None) -> Dict[str, Any]:
    """添加预测记录"""
    try:
        record_id = db.insert_record('prediction',
                                   content=content,
                                   timeframe=timeframe,
                                   basis=basis,
                                   verification_status=verification_status,
                                   reference_urls=reference_urls or [],
                                   category_id=category_id)
        return {
            "success": True,
            "message": "成功添加预测记录",
            "record_id": record_id,
            "content": content,
            "timeframe": timeframe
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加预测记录失败: {str(e)}"
        }

# ============ 关联关系管理 ============

@mcp.tool()
def add_relation(source_table: str, source_id: int, target_table: str, target_id: int,
                relation_type: str, strength: str = 'medium', note: str = None) -> Dict[str, Any]:
    """添加关联关系"""
    try:
        relation_id = db.add_relation(source_table, source_id, target_table, target_id,
                                    relation_type, strength, note)
        return {
            "success": True,
            "message": "成功添加关联关系",
            "relation_id": relation_id,
            "source": f"{source_table}#{source_id}",
            "target": f"{target_table}#{target_id}",
            "relation_type": relation_type
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"添加关联关系失败: {str(e)}"
        }

@mcp.tool()
def get_relations(table_name: str, record_id: int, relation_type: str = None) -> Dict[str, Any]:
    """获取记录的关联关系"""
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        relations = db.get_relations(table_name, record_id, relation_type)
        return {
            "success": True,
            "message": f"成功获取 {len(relations)} 个关联关系",
            "relations": relations
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"获取关联关系失败: {str(e)}"
        }

# ============ 通用CRUD操作 ============

@mcp.tool()
def update_record(table_name: str, record_id: int, **kwargs) -> Dict[str, Any]:
    """更新记录"""
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        success = db.update_record(table_name, record_id, **kwargs)
        
        if success:
            return {
                "success": True,
                "message": f"成功更新{TABLE_DESCRIPTIONS[table_name]}记录",
                "record_id": record_id,
                "table_name": table_name,
                "updated_fields": list(kwargs.keys())
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

@mcp.tool()
def search_records(table_name: str, keyword: str = None, category_id: int = None,
                  status: str = None, type: str = None, limit: int = 20, 
                  offset: int = 0, order_by: str = 'created_time', 
                  order_desc: bool = True) -> Dict[str, Any]:
    """搜索记录"""
    try:
        if table_name not in TABLE_DESCRIPTIONS:
            return {
                "success": False,
                "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
            }
        
        search_params = {
            'keyword': keyword,
            'category_id': category_id,
            'status': status,
            'type': type,
            'limit': limit,
            'offset': offset,
            'order_by': order_by,
            'order_desc': order_desc
        }
        
        # 移除None值
        search_params = {k: v for k, v in search_params.items() if v is not None}
        
        records = db.search_records(table_name, **search_params)
        
        return {
            "success": True,
            "message": f"在{TABLE_DESCRIPTIONS[table_name]}表中搜索到 {len(records)} 条记录",
            "table_name": table_name,
            "records": records,
            "search_params": search_params
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"搜索记录失败: {str(e)}"
        }

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

# ============ 统计和信息查询 ============

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
            all_stats = db.get_table_stats()
            for table, stats in all_stats.items():
                stats['table_description'] = TABLE_DESCRIPTIONS[table]
            
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

@mcp.tool()
def execute_custom_sql(sql: str, params: List[str] = None, fetch_results: bool = True) -> Dict[str, Any]:
    """执行自定义SQL语句"""
    try:
        result = db.execute_custom_sql(sql, params, fetch_results)
        return result
    except Exception as e:
        return {
            "success": False,
            "message": f"执行自定义SQL失败: {str(e)}"
        }

@mcp.tool()
def get_table_schema(table_name: str = None) -> Dict[str, Any]:
    """获取表结构信息"""
    try:
        if table_name:
            if table_name not in TABLE_DESCRIPTIONS:
                return {
                    "success": False,
                    "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                }
            
            schema_result = db.get_table_schema(table_name)
            return schema_result
        else:
            # 获取所有表的结构信息
            schema_result = db.get_table_schema()
            return schema_result
            
    except Exception as e:
        return {
            "success": False,
            "message": f"获取表结构失败: {str(e)}"
        }

# ============ 高级查询方法 ============

@mcp.tool()
def get_viewpoints_by_subject(subject: str, time_period: str = None) -> Dict[str, Any]:
    """根据主题获取观点"""
    try:
        search_params = {'keyword': subject}
        if time_period:
            search_params['time_period'] = time_period
        
        records = db.search_records('viewpoint', **search_params)
        
        return {
            "success": True,
            "message": f"找到 {len(records)} 个关于'{subject}'的观点",
            "subject": subject,
            "time_period": time_period,
            "viewpoints": records
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"查询观点失败: {str(e)}"
        }

@mcp.tool()
def get_active_focuses(priority_threshold: int = None) -> Dict[str, Any]:
    """获取活跃的关注点"""
    try:
        search_params = {'status': 'active'}
        if priority_threshold:
            # 这里需要用自定义SQL来实现优先级过滤
            sql = "SELECT * FROM focus WHERE status = 'active' AND priority >= ? ORDER BY priority DESC"
            result = db.execute_custom_sql(sql, [priority_threshold])
            if result['success']:
                records = result['results']
            else:
                return result
        else:
            records = db.search_records('focus', **search_params)
        
        return {
            "success": True,
            "message": f"找到 {len(records)} 个活跃的关注点",
            "focuses": records
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"查询关注点失败: {str(e)}"
        }

@mcp.tool()
def get_goals_by_status(status: str, type: str = None) -> Dict[str, Any]:
    """根据状态获取目标"""
    try:
        search_params = {'status': status}
        if type:
            search_params['type'] = type
        
        records = db.search_records('goal', **search_params)
        
        return {
            "success": True,
            "message": f"找到 {len(records)} 个状态为'{status}'的目标",
            "status": status,
            "type": type,
            "goals": records
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"查询目标失败: {str(e)}"
        }

@mcp.tool()
def get_high_impact_insights(limit: int = 10) -> Dict[str, Any]:
    """获取高影响力的洞察"""
    try:
        records = db.search_records('insight', impact_level='high', limit=limit)
        
        return {
            "success": True,
            "message": f"找到 {len(records)} 个高影响力的洞察",
            "insights": records
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"查询洞察失败: {str(e)}"
        }

@mcp.tool()
def get_expertise_areas() -> Dict[str, Any]:
    """获取专业领域分析"""
    try:
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
            return {
                "success": True,
                "message": f"成功分析专业领域，共 {len(result['results'])} 个领域级别组合",
                "expertise_analysis": result['results']
            }
        else:
            return result
            
    except Exception as e:
        return {
            "success": False,
            "message": f"分析专业领域失败: {str(e)}"
        }

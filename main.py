"""
FastMCP版本的个人画像数据管理系统
基于database 0.3.md和tools3.md的完整实现
"""

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional, Union
import json
import os
from pathlib import Path
from datetime import datetime

from Database.database import get_database

# 创建FastMCP服务器实例
mcp = FastMCP("个人画像数据管理系统")

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

# ============ 人物档案相关操作 ============

@mcp.tool()
def get_persona() -> Dict[str, Any]:
    """获取当前用户的核心画像信息。该信息用于AI进行个性化交互。系统中只有一个用户画像，ID固定为1。"""
    try:
        persona = db.get_persona()
        if not persona:
            return {
                "content": "未找到用户画像信息。",
                "raw_data": None
            }
        
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
        
        return {
            "content": content,
            "raw_data": persona
        }
        
    except Exception as e:
        return {
            "content": f"获取用户画像失败: {str(e)}",
            "raw_data": None
        }

@mcp.tool()
def save_persona(name: str = None, gender: str = None, personality: str = None, 
                avatar_url: str = None, bio: str = None, privacy_level: str = None) -> Dict[str, Any]:
    """保存（更新）当前用户的核心画像信息。由于ID固定为1，此操作主要用于更新现有画像。只需提供需要修改的字段。"""
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
        if privacy_level is not None:
            update_data['privacy_level'] = privacy_level
        
        if not update_data:
            return {
                "id": 1,
                "operation": "no_change",
                "timestamp": datetime.now().isoformat()
            }
        
        success = db.update_persona(**update_data)
        if success:
            return {
                "id": 1,
                "operation": "updated",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "id": 1,
                "operation": "failed",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "id": 1,
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# ============ II. Memory Tools (2 Tools) ============

@mcp.tool()
def query_memories(filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                  sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """查询符合指定条件的记忆数据。记忆是关于用户经历、学习、事件、互动等方面的记录。"""
    try:
        filter_conditions = {}
        
        if filter:
            for key, value in filter.items():
                if value is not None:
                    if key == 'ids':
                        filter_conditions['ids'] = value
                    elif key == 'content_contains':
                        filter_conditions['content_contains'] = value
                    elif key == 'memory_type_in':
                        filter_conditions['memory_type_in'] = value
                    elif key == 'importance_gte':
                        filter_conditions['importance_gte'] = value
                    elif key == 'importance_lte':
                        filter_conditions['importance_lte'] = value
                    elif key == 'related_people_contains':
                        filter_conditions['related_people_contains'] = value
                    elif key == 'location_contains':
                        filter_conditions['location_contains'] = value
                    elif key == 'memory_date_from':
                        filter_conditions['memory_date_from'] = value
                    elif key == 'memory_date_to':
                        filter_conditions['memory_date_to'] = value
                    elif key == 'keywords_contain_any':
                        filter_conditions['keywords_contain_any'] = value
                    elif key == 'keywords_contain_all':
                        filter_conditions['keywords_contain_all'] = value
                    elif key == 'source_app_is':
                        filter_conditions['source_app_is'] = value
                    elif key == 'privacy_level_is':
                        filter_conditions['privacy_level_is'] = value
                    elif key == 'created_time_from':
                        filter_conditions['created_time_from'] = value
                    elif key == 'created_time_to':
                        filter_conditions['created_time_to'] = value
        
        records, total_count = db.query_records('memory', filter_conditions, sort_by, sort_order, limit, offset)
        
        # 生成提示内容
        template = """# 用户记忆数据

以下是根据您的查询条件检索到的用户记忆记录：

{{#each raw_data}}
## 记忆记录 (ID: {{this.id}})
- **核心内容 (content)**: {{this.content}}
- **记忆类型 (memory_type)**: {{this.memory_type}} (可选值: experience/个人经历, event/重要事件, learning/学习体验, interaction/人际互动, achievement/成就记录, mistake/错误教训)
- **重要程度 (importance)**: {{this.importance}} (1-10，10为最重要)
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
- 当前显示 {{raw_data.length}} 条记录。"""
        
        content = generate_prompt_content(template, records)
        content = content.replace("{{total_count}}", str(total_count))
        
        return {
            "content": content,
            "raw_data": records,
            "total_count": total_count
        }
        
    except Exception as e:
        return {
            "content": f"查询记忆失败: {str(e)}",
            "raw_data": [],
            "total_count": 0
        }

@mcp.tool()
def save_memory(id: int = None, content: str = None, memory_type: str = None,
               importance: int = None, related_people: str = None, location: str = None,
               memory_date: str = None, keywords: List[str] = None, source_app: str = 'unknown',
               reference_urls: List[str] = None, privacy_level: str = 'public') -> Dict[str, Any]:
    """保存（添加或更新）一条记忆记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。"""
    try:
        if id is None:
            # 创建新记录
            if not content or not memory_type or importance is None:
                return {
                    "id": None,
                    "operation": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": "创建记忆记录需要提供 content、memory_type 和 importance"
                }
            
            record_id = db.insert_record('memory',
                                       content=content,
                                       memory_type=memory_type,
                                       importance=importance,
                                       related_people=related_people,
                                       location=location,
                                       memory_date=memory_date,
                                       keywords=keywords or [],
                                       source_app=source_app,
                                       reference_urls=reference_urls or [],
                                       privacy_level=privacy_level)
            
            return {
                "id": record_id,
                "operation": "created",
                "timestamp": datetime.now().isoformat()
            }
        else:
            # 更新现有记录
            update_data = {}
            if content is not None:
                update_data['content'] = content
            if memory_type is not None:
                update_data['memory_type'] = memory_type
            if importance is not None:
                update_data['importance'] = importance
            if related_people is not None:
                update_data['related_people'] = related_people
            if location is not None:
                update_data['location'] = location
            if memory_date is not None:
                update_data['memory_date'] = memory_date
            if keywords is not None:
                update_data['keywords'] = keywords
            if source_app != 'unknown':
                update_data['source_app'] = source_app
            if reference_urls is not None:
                update_data['reference_urls'] = reference_urls
            if privacy_level != 'public':
                update_data['privacy_level'] = privacy_level
            
            if not update_data:
                return {
                    "id": id,
                    "operation": "no_change",
                    "timestamp": datetime.now().isoformat()
                }
            
            success = db.update_record('memory', id, **update_data)
            if success:
                return {
                    "id": id,
                    "operation": "updated",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "id": id,
                    "operation": "failed",
                    "timestamp": datetime.now().isoformat()
                }
                
    except Exception as e:
        return {
            "id": id,
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# ============ III. Viewpoint Tools (2 Tools) ============

@mcp.tool()
def query_viewpoints(filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                    sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """查询符合指定条件的观点数据。观点代表用户对特定事物的看法或立场。"""
    try:
        filter_conditions = {}
        
        if filter:
            for key, value in filter.items():
                if value is not None:
                    if key == 'ids':
                        filter_conditions['ids'] = value
                    elif key == 'content_contains':
                        filter_conditions['content_contains'] = value
                    elif key == 'source_people_contains':
                        filter_conditions['source_people_contains'] = value
                    elif key == 'related_event_contains':
                        filter_conditions['related_event_contains'] = value
                    elif key == 'keywords_contain_any':
                        filter_conditions['keywords_contain_any'] = value
                    elif key == 'keywords_contain_all':
                        filter_conditions['keywords_contain_all'] = value
                    elif key == 'source_app_is':
                        filter_conditions['source_app_is'] = value
                    elif key == 'privacy_level_is':
                        filter_conditions['privacy_level_is'] = value
        
        records, total_count = db.query_records('viewpoint', filter_conditions, sort_by, sort_order, limit, offset)
        
        # 生成提示内容
        template = """# 用户观点数据

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
- 当前显示 {{raw_data.length}} 条记录。"""
        
        content = generate_prompt_content(template, records)
        content = content.replace("{{total_count}}", str(total_count))
        
        return {
            "content": content,
            "raw_data": records,
            "total_count": total_count
        }
        
    except Exception as e:
        return {
            "content": f"查询观点失败: {str(e)}",
            "raw_data": [],
            "total_count": 0
        }

@mcp.tool()
def save_viewpoint(id: int = None, content: str = None, source_people: str = None,
                  keywords: List[str] = None, source_app: str = 'unknown',
                  related_event: str = None, reference_urls: List[str] = None,
                  privacy_level: str = 'public') -> Dict[str, Any]:
    """保存（添加或更新）一条观点记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。"""
    try:
        if id is None:
            # 创建新记录
            if not content:
                return {
                    "id": None,
                    "operation": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": "创建观点记录需要提供 content"
                }
            
            record_id = db.insert_record('viewpoint',
                                       content=content,
                                       source_people=source_people,
                                       keywords=keywords or [],
                                       source_app=source_app,
                                       related_event=related_event,
                                       reference_urls=reference_urls or [],
                                       privacy_level=privacy_level)
            
            return {
                "id": record_id,
                "operation": "created",
                "timestamp": datetime.now().isoformat()
            }
        else:
            # 更新现有记录
            update_data = {}
            if content is not None:
                update_data['content'] = content
            if source_people is not None:
                update_data['source_people'] = source_people
            if keywords is not None:
                update_data['keywords'] = keywords
            if source_app != 'unknown':
                update_data['source_app'] = source_app
            if related_event is not None:
                update_data['related_event'] = related_event
            if reference_urls is not None:
                update_data['reference_urls'] = reference_urls
            if privacy_level != 'public':
                update_data['privacy_level'] = privacy_level
            
            if not update_data:
                return {
                    "id": id,
                    "operation": "no_change",
                    "timestamp": datetime.now().isoformat()
                }
            
            success = db.update_record('viewpoint', id, **update_data)
            if success:
                return {
                    "id": id,
                    "operation": "updated",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "id": id,
                    "operation": "failed",
                    "timestamp": datetime.now().isoformat()
                }
                
    except Exception as e:
        return {
            "id": id,
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# ============ IV. Insight Tools (2 Tools) ============

@mcp.tool()
def query_insights(filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                  sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """查询符合指定条件的洞察数据。洞察是用户经过深度思考和分析后得出的见解或感悟。"""
    try:
        filter_conditions = {}
        
        if filter:
            for key, value in filter.items():
                if value is not None:
                    if key == 'ids':
                        filter_conditions['ids'] = value
                    elif key == 'content_contains':
                        filter_conditions['content_contains'] = value
                    elif key == 'source_people_contains':
                        filter_conditions['source_people_contains'] = value
                    elif key == 'keywords_contain_any':
                        filter_conditions['keywords_contain_any'] = value
                    elif key == 'source_app_is':
                        filter_conditions['source_app_is'] = value
                    elif key == 'privacy_level_is':
                        filter_conditions['privacy_level_is'] = value
        
        records, total_count = db.query_records('insight', filter_conditions, sort_by, sort_order, limit, offset)
        
        # 生成提示内容
        template = """# 用户洞察数据

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
- 当前显示 {{raw_data.length}} 条记录。"""
        
        content = generate_prompt_content(template, records)
        content = content.replace("{{total_count}}", str(total_count))
        
        return {
            "content": content,
            "raw_data": records,
            "total_count": total_count
        }
        
    except Exception as e:
        return {
            "content": f"查询洞察失败: {str(e)}",
            "raw_data": [],
            "total_count": 0
        }

@mcp.tool()
def save_insight(id: int = None, content: str = None, source_people: str = None,
                keywords: List[str] = None, source_app: str = 'unknown',
                reference_urls: List[str] = None, privacy_level: str = 'public') -> Dict[str, Any]:
    """保存（添加或更新）一条洞察记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。"""
    try:
        if id is None:
            # 创建新记录
            if not content:
                return {
                    "id": None,
                    "operation": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": "创建洞察记录需要提供 content"
                }
            
            record_id = db.insert_record('insight',
                                       content=content,
                                       source_people=source_people,
                                       keywords=keywords or [],
                                       source_app=source_app,
                                       reference_urls=reference_urls or [],
                                       privacy_level=privacy_level)
            
            return {
                "id": record_id,
                "operation": "created",
                "timestamp": datetime.now().isoformat()
            }
        else:
            # 更新现有记录
            update_data = {}
            if content is not None:
                update_data['content'] = content
            if source_people is not None:
                update_data['source_people'] = source_people
            if keywords is not None:
                update_data['keywords'] = keywords
            if source_app != 'unknown':
                update_data['source_app'] = source_app
            if reference_urls is not None:
                update_data['reference_urls'] = reference_urls
            if privacy_level != 'public':
                update_data['privacy_level'] = privacy_level
            
            if not update_data:
                return {
                    "id": id,
                    "operation": "no_change",
                    "timestamp": datetime.now().isoformat()
                }
            
            success = db.update_record('insight', id, **update_data)
            if success:
                return {
                    "id": id,
                    "operation": "updated",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "id": id,
                    "operation": "failed",
                    "timestamp": datetime.now().isoformat()
                }
                
    except Exception as e:
        return {
            "id": id,
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# ============ V. Goal Tools (2 Tools) ============

@mcp.tool()
def query_goals(filter: Dict[str, Any] = None, sort_by: str = 'deadline', 
               sort_order: str = 'asc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """查询符合指定条件的目标数据。目标包括长期规划、短期计划以及具体的待办事项。"""
    try:
        filter_conditions = {}
        
        if filter:
            for key, value in filter.items():
                if value is not None:
                    if key == 'ids':
                        filter_conditions['ids'] = value
                    elif key == 'content_contains':
                        filter_conditions['content_contains'] = value
                    elif key == 'type_is':
                        filter_conditions['type_is'] = value
                    elif key == 'type_in':
                        filter_conditions['type_in'] = value
                    elif key == 'deadline_from':
                        filter_conditions['deadline_from'] = value
                    elif key == 'deadline_to':
                        filter_conditions['deadline_to'] = value
                    elif key == 'status_is':
                        filter_conditions['status_is'] = value
                    elif key == 'status_in':
                        filter_conditions['status_in'] = value
                    elif key == 'keywords_contain_any':
                        filter_conditions['keywords_contain_any'] = value
                    elif key == 'source_app_is':
                        filter_conditions['source_app_is'] = value
                    elif key == 'privacy_level_is':
                        filter_conditions['privacy_level_is'] = value
        
        records, total_count = db.query_records('goal', filter_conditions, sort_by, sort_order, limit, offset)
        
        # 生成提示内容
        template = """# 用户目标数据

以下是根据您的查询条件检索到的用户目标记录：

{{#each raw_data}}
## 目标记录 (ID: {{this.id}})
- **目标内容 (content)**: {{this.content}}
- **目标类型 (type)**: {{this.type}} (可选值: long_term/长期目标, short_term/短期目标, plan/计划, todo/待办事项)
- **截止日期 (deadline)**: {{this.deadline}}
- **当前状态 (status)**: {{this.status}} (可选值: planning/计划中, in_progress/进行中, completed/已完成, abandoned/已放弃)
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
- 当前显示 {{raw_data.length}} 条记录。"""
        
        content = generate_prompt_content(template, records)
        content = content.replace("{{total_count}}", str(total_count))
        
        return {
            "content": content,
            "raw_data": records,
            "total_count": total_count
        }
        
    except Exception as e:
        return {
            "content": f"查询目标失败: {str(e)}",
            "raw_data": [],
            "total_count": 0
        }

@mcp.tool()
def save_goal(id: int = None, content: str = None, type: str = None, deadline: str = None,
             status: str = 'planning', keywords: List[str] = None, source_app: str = 'unknown',
             privacy_level: str = 'public') -> Dict[str, Any]:
    """保存（添加或更新）一条目标、计划或待办事项。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。"""
    try:
        if id is None:
            # 创建新记录
            if not content or not type:
                return {
                    "id": None,
                    "operation": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": "创建目标记录需要提供 content 和 type"
                }
            
            record_id = db.insert_record('goal',
                                       content=content,
                                       type=type,
                                       deadline=deadline,
                                       status=status,
                                       keywords=keywords or [],
                                       source_app=source_app,
                                       privacy_level=privacy_level)
            
            return {
                "id": record_id,
                "operation": "created",
                "timestamp": datetime.now().isoformat()
            }
        else:
            # 更新现有记录
            update_data = {}
            if content is not None:
                update_data['content'] = content
            if type is not None:
                update_data['type'] = type
            if deadline is not None:
                update_data['deadline'] = deadline
            if status != 'planning':
                update_data['status'] = status
            if keywords is not None:
                update_data['keywords'] = keywords
            if source_app != 'unknown':
                update_data['source_app'] = source_app
            if privacy_level != 'public':
                update_data['privacy_level'] = privacy_level
            
            if not update_data:
                return {
                    "id": id,
                    "operation": "no_change",
                    "timestamp": datetime.now().isoformat()
                }
            
            success = db.update_record('goal', id, **update_data)
            if success:
                return {
                    "id": id,
                    "operation": "updated",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "id": id,
                    "operation": "failed",
                    "timestamp": datetime.now().isoformat()
                }
                
    except Exception as e:
        return {
            "id": id,
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# ============ VI. Preference Tools (2 Tools) ============

@mcp.tool()
def query_preferences(filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                     sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """查询符合指定条件的偏好数据。偏好描述了用户在特定情境下的喜好和习惯。"""
    try:
        filter_conditions = {}
        
        if filter:
            for key, value in filter.items():
                if value is not None:
                    if key == 'ids':
                        filter_conditions['ids'] = value
                    elif key == 'content_contains':
                        filter_conditions['content_contains'] = value
                    elif key == 'context_is':
                        filter_conditions['context_is'] = value
                    elif key == 'context_contains':
                        filter_conditions['context_contains'] = value
                    elif key == 'keywords_contain_any':
                        filter_conditions['keywords_contain_any'] = value
                    elif key == 'source_app_is':
                        filter_conditions['source_app_is'] = value
                    elif key == 'privacy_level_is':
                        filter_conditions['privacy_level_is'] = value
        
        records, total_count = db.query_records('preference', filter_conditions, sort_by, sort_order, limit, offset)
        
        # 生成提示内容
        template = """# 用户偏好数据

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
- 当前显示 {{raw_data.length}} 条记录。"""
        
        content = generate_prompt_content(template, records)
        content = content.replace("{{total_count}}", str(total_count))
        
        return {
            "content": content,
            "raw_data": records,
            "total_count": total_count
        }
        
    except Exception as e:
        return {
            "content": f"查询偏好失败: {str(e)}",
            "raw_data": [],
            "total_count": 0
        }

@mcp.tool()
def save_preference(id: int = None, content: str = None, context: str = None,
                   keywords: List[str] = None, source_app: str = 'unknown',
                   privacy_level: str = 'public') -> Dict[str, Any]:
    """保存（添加或更新）一条偏好记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。"""
    try:
        if id is None:
            # 创建新记录
            if not content:
                return {
                    "id": None,
                    "operation": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": "创建偏好记录需要提供 content"
                }
            
            record_id = db.insert_record('preference',
                                       content=content,
                                       context=context,
                                       keywords=keywords or [],
                                       source_app=source_app,
                                       privacy_level=privacy_level)
            
            return {
                "id": record_id,
                "operation": "created",
                "timestamp": datetime.now().isoformat()
            }
        else:
            # 更新现有记录
            update_data = {}
            if content is not None:
                update_data['content'] = content
            if context is not None:
                update_data['context'] = context
            if keywords is not None:
                update_data['keywords'] = keywords
            if source_app != 'unknown':
                update_data['source_app'] = source_app
            if privacy_level != 'public':
                update_data['privacy_level'] = privacy_level
            
            if not update_data:
                return {
                    "id": id,
                    "operation": "no_change",
                    "timestamp": datetime.now().isoformat()
                }
            
            success = db.update_record('preference', id, **update_data)
            if success:
                return {
                    "id": id,
                    "operation": "updated",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "id": id,
                    "operation": "failed",
                    "timestamp": datetime.now().isoformat()
                }
                
    except Exception as e:
        return {
            "id": id,
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# ============ VII. Methodology Tools (2 Tools) ============

@mcp.tool()
def query_methodologies(filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                       sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """查询符合指定条件的方法论数据。方法论是用户解决问题或进行决策时使用的框架或原则。"""
    try:
        filter_conditions = {}
        
        if filter:
            for key, value in filter.items():
                if value is not None:
                    if key == 'ids':
                        filter_conditions['ids'] = value
                    elif key == 'content_contains':
                        filter_conditions['content_contains'] = value
                    elif key == 'type_is':
                        filter_conditions['type_is'] = value
                    elif key == 'type_contains':
                        filter_conditions['type_contains'] = value
                    elif key == 'effectiveness_is':
                        filter_conditions['effectiveness_is'] = value
                    elif key == 'use_cases_contains':
                        filter_conditions['use_cases_contains'] = value
                    elif key == 'keywords_contain_any':
                        filter_conditions['keywords_contain_any'] = value
                    elif key == 'source_app_is':
                        filter_conditions['source_app_is'] = value
                    elif key == 'privacy_level_is':
                        filter_conditions['privacy_level_is'] = value
        
        records, total_count = db.query_records('methodology', filter_conditions, sort_by, sort_order, limit, offset)
        
        # 生成提示内容
        template = """# 用户方法论数据

以下是根据您的查询条件检索到的用户方法论记录：

{{#each raw_data}}
## 方法论记录 (ID: {{this.id}})
- **方法论内容 (content)**: {{this.content}}
- **类型 (type)**: {{this.type}}
- **有效性 (effectiveness)**: {{this.effectiveness}} (可选值: proven/已验证有效, experimental/实验性, theoretical/理论性)
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
- 当前显示 {{raw_data.length}} 条记录。"""
        
        content = generate_prompt_content(template, records)
        content = content.replace("{{total_count}}", str(total_count))
        
        return {
            "content": content,
            "raw_data": records,
            "total_count": total_count
        }
        
    except Exception as e:
        return {
            "content": f"查询方法论失败: {str(e)}",
            "raw_data": [],
            "total_count": 0
        }

@mcp.tool()
def save_methodology(id: int = None, content: str = None, type: str = None,
                    effectiveness: str = 'experimental', use_cases: str = None,
                    keywords: List[str] = None, source_app: str = 'unknown',
                    reference_urls: List[str] = None, privacy_level: str = 'public') -> Dict[str, Any]:
    """保存（添加或更新）一条方法论记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。"""
    try:
        if id is None:
            # 创建新记录
            if not content:
                return {
                    "id": None,
                    "operation": "error",
                    "timestamp": datetime.now().isoformat(),
                    "error": "创建方法论记录需要提供 content"
                }
            
            record_id = db.insert_record('methodology',
                                       content=content,
                                       type=type,
                                       effectiveness=effectiveness,
                                       use_cases=use_cases,
                                       keywords=keywords or [],
                                       source_app=source_app,
                                       reference_urls=reference_urls or [],
                                       privacy_level=privacy_level)
            
            return {
                "id": record_id,
                "operation": "created",
                "timestamp": datetime.now().isoformat()
            }
        else:
            # 更新现有记录
            update_data = {}
            if content is not None:
                update_data['content'] = content
            if type is not None:
                update_data['type'] = type
            if effectiveness != 'experimental':
                update_data['effectiveness'] = effectiveness
            if use_cases is not None:
                update_data['use_cases'] = use_cases
            if keywords is not None:
                update_data['keywords'] = keywords
            if source_app != 'unknown':
                update_data['source_app'] = source_app
            if reference_urls is not None:
                update_data['reference_urls'] = reference_urls
            if privacy_level != 'public':
                update_data['privacy_level'] = privacy_level
            
            if not update_data:
                return {
                    "id": id,
                    "operation": "no_change",
                    "timestamp": datetime.now().isoformat()
                }
            
            success = db.update_record('methodology', id, **update_data)
            if success:
                return {
                    "id": id,
                    "operation": "updated",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "id": id,
                    "operation": "failed",
                    "timestamp": datetime.now().isoformat()
                }
                
    except Exception as e:
        return {
            "id": id,
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# ============ 保留的工具方法 ============

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

# ============ VIII. Focus Tools (2 Tools) ============

@mcp.tool()
def query_focuses(filter: Dict[str, Any] = None, sort_by: str = 'priority', 
                 sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """查询符合指定条件的当前关注点数据。关注点是用户当前集中精力处理或学习的事项。"""
    try:
        filter_conditions = {}
        
        if filter:
            for key, value in filter.items():
                if value is not None:
                    if key == 'ids':
                        filter_conditions['ids'] = value
                    elif key == 'content_contains':
                        filter_conditions['content_contains'] = value
                    elif key == 'priority_gte':
                        filter_conditions['priority_gte'] = value
                    elif key == 'status_is':
                        filter_conditions['status_is'] = value
                    elif key == 'status_in':
                        filter_conditions['status_in'] = value
                    elif key == 'context_contains':
                        filter_conditions['context_contains'] = value
                    elif key == 'keywords_contain_any':
                        filter_conditions['keywords_contain_any'] = value
                    elif key == 'source_app_is':
                        filter_conditions['source_app_is'] = value
                    elif key == 'deadline_from':
                        filter_conditions['deadline_from'] = value
                    elif key == 'deadline_to':
                        filter_conditions['deadline_to'] = value
                    elif key == 'privacy_level_is':
                        filter_conditions['privacy_level_is'] = value
        
        records, total_count = db.query_records('focus', filter_conditions, sort_by, sort_order, limit, offset)
        
        # 生成提示内容
        template = """# 用户关注点数据

以下是根据您的查询条件检索到的用户当前关注点记录：

{{#each raw_data}}
## 关注点记录 (ID: {{this.id}})
- **关注内容 (content)**: {{this.content}}
- **优先级 (priority)**: {{this.priority}} (1-10，10为最高)
- **状态 (status)**: {{this.status}} (可选值: active/进行中, paused/暂停, completed/已完成)
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
- 当前显示 {{raw_data.length}} 条记录。"""
        
        content = generate_prompt_content(template, records)
        
        return {
            "content": content,
            "raw_data": records,
            "total_count": total_count
        }
        
    except Exception as e:
        return {
            "content": f"查询关注点失败: {str(e)}",
            "raw_data": [],
            "total_count": 0
        }

@mcp.tool()
def save_focus(id: int = None, content: str = None, priority: int = None, status: str = 'active',
              context: str = None, keywords: List[str] = None, source_app: str = 'unknown',
              deadline: str = None, privacy_level: str = 'public') -> Dict[str, Any]:
    """保存（添加或更新）一条关注点记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。"""
    try:
        if id:
            # 更新现有记录
            update_data = {}
            if content is not None:
                update_data['content'] = content
            if priority is not None:
                update_data['priority'] = priority
            if status is not None:
                update_data['status'] = status
            if context is not None:
                update_data['context'] = context
            if keywords is not None:
                update_data['keywords'] = keywords
            if source_app is not None:
                update_data['source_app'] = source_app
            if deadline is not None:
                update_data['deadline'] = deadline
            if privacy_level is not None:
                update_data['privacy_level'] = privacy_level
            
            success = db.update_record('focus', id, **update_data)
            if success:
                return {
                    "id": id,
                    "operation": "updated",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "id": id,
                    "operation": "failed",
                    "timestamp": datetime.now().isoformat()
                }
        else:
            # 创建新记录
            if not content or priority is None:
                return {
                    "id": None,
                    "operation": "failed",
                    "timestamp": datetime.now().isoformat(),
                    "error": "content和priority是必需字段"
                }
            
            record_data = {
                'content': content,
                'priority': priority,
                'status': status,
                'source_app': source_app,
                'privacy_level': privacy_level
            }
            
            if context is not None:
                record_data['context'] = context
            if keywords is not None:
                record_data['keywords'] = keywords
            if deadline is not None:
                record_data['deadline'] = deadline
            
            new_id = db.insert_record('focus', **record_data)
            return {
                "id": new_id,
                "operation": "created",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "id": id,
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# ============ IX. Prediction Tools (2 Tools) ============

@mcp.tool()
def query_predictions(filter: Dict[str, Any] = None, sort_by: str = 'created_time', 
                     sort_order: str = 'desc', limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """查询符合指定条件的预测数据。预测是用户对未来事件、趋势的判断记录。"""
    try:
        filter_conditions = {}
        
        if filter:
            for key, value in filter.items():
                if value is not None:
                    if key == 'ids':
                        filter_conditions['ids'] = value
                    elif key == 'content_contains':
                        filter_conditions['content_contains'] = value
                    elif key == 'timeframe_contains':
                        filter_conditions['timeframe_contains'] = value
                    elif key == 'basis_contains':
                        filter_conditions['basis_contains'] = value
                    elif key == 'verification_status_is':
                        filter_conditions['verification_status_is'] = value
                    elif key == 'keywords_contain_any':
                        filter_conditions['keywords_contain_any'] = value
                    elif key == 'source_app_is':
                        filter_conditions['source_app_is'] = value
                    elif key == 'privacy_level_is':
                        filter_conditions['privacy_level_is'] = value
        
        records, total_count = db.query_records('prediction', filter_conditions, sort_by, sort_order, limit, offset)
        
        # 生成提示内容
        template = """# 用户预测数据

以下是根据您的查询条件检索到的用户预测记录：

{{#each raw_data}}
## 预测记录 (ID: {{this.id}})
- **预测内容 (content)**: {{this.content}}
- **时间范围 (timeframe)**: {{this.timeframe}}
- **预测依据 (basis)**: {{this.basis}}
- **验证状态 (verification_status)**: {{this.verification_status}} (可选值: pending/待验证, correct/正确, incorrect/错误, partial/部分正确)
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
        
        content = generate_prompt_content(template, records)
        
        return {
            "content": content,
            "raw_data": records,
            "total_count": total_count
        }
        
    except Exception as e:
        return {
            "content": f"查询预测失败: {str(e)}",
            "raw_data": [],
            "total_count": 0
        }

@mcp.tool()
def save_prediction(id: int = None, content: str = None, timeframe: str = None, basis: str = None,
                   verification_status: str = 'pending', keywords: List[str] = None, 
                   source_app: str = 'unknown', reference_urls: List[str] = None,
                   privacy_level: str = 'public') -> Dict[str, Any]:
    """保存（添加或更新）一条预测记录。如果提供了 'id'，则尝试更新现有记录；否则，创建新记录。"""
    try:
        if id:
            # 更新现有记录
            update_data = {}
            if content is not None:
                update_data['content'] = content
            if timeframe is not None:
                update_data['timeframe'] = timeframe
            if basis is not None:
                update_data['basis'] = basis
            if verification_status is not None:
                update_data['verification_status'] = verification_status
            if keywords is not None:
                update_data['keywords'] = keywords
            if source_app is not None:
                update_data['source_app'] = source_app
            if reference_urls is not None:
                update_data['reference_urls'] = reference_urls
            if privacy_level is not None:
                update_data['privacy_level'] = privacy_level
            
            success = db.update_record('prediction', id, **update_data)
            if success:
                return {
                    "id": id,
                    "operation": "updated",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "id": id,
                    "operation": "failed",
                    "timestamp": datetime.now().isoformat()
                }
        else:
            # 创建新记录
            if not content or not timeframe or not basis:
                return {
                    "id": None,
                    "operation": "failed",
                    "timestamp": datetime.now().isoformat(),
                    "error": "content、timeframe和basis是必需字段"
                }
            
            record_data = {
                'content': content,
                'timeframe': timeframe,
                'basis': basis,
                'verification_status': verification_status,
                'source_app': source_app,
                'privacy_level': privacy_level
            }
            
            if keywords is not None:
                record_data['keywords'] = keywords
            if reference_urls is not None:
                record_data['reference_urls'] = reference_urls
            
            new_id = db.insert_record('prediction', **record_data)
            return {
                "id": new_id,
                "operation": "created",
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "id": id,
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# ============ 启动服务器 ============

if __name__ == "__main__":
    mcp.run()

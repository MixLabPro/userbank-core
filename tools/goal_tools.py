"""
目标工具
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools

class GoalTools(BaseTools):
    """目标工具类"""
    
    def query_goals(self, filter: Optional[Dict[str, Any]] = None, 
                   sort_by: str = 'deadline', sort_order: str = 'asc', 
                   limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """查询目标数据"""
        try:
            allowed_filters = [
                'ids', 'content_contains', 'type_is', 'type_in', 'deadline_from', 'deadline_to',
                'status_is', 'status_in', 'keywords_contain_any', 'source_app_is', 'privacy_level_is'
            ]
            
            filter_conditions = self._build_filter_conditions(filter or {}, allowed_filters)
            records, total_count = self.db.query_records('goal', filter_conditions, sort_by, sort_order, limit, offset)
            
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
            
            return self._generate_query_response(records, total_count, template)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    def save_goal(self, id: Optional[int] = None, content: Optional[str] = None, 
                 type: Optional[str] = None, deadline: Optional[str] = None,
                 status: str = 'planning', keywords: Optional[List[str]] = None,
                 source_app: str = 'unknown', privacy_level: str = 'public') -> Dict[str, Any]:
        """保存目标数据"""
        try:
            if id is None:
                # 创建新记录
                if not content or not type:
                    return self._create_error_response("创建目标记录需要提供 content 和 type")
                
                record_id = self.db.insert_record('goal',
                                               content=content,
                                               type=type,
                                               deadline=deadline,
                                               status=status,
                                               keywords=keywords or [],
                                               source_app=source_app,
                                               privacy_level=privacy_level)
                
                return self._create_success_response(record_id, "created")
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
                    return self._create_success_response(id, "no_change")
                
                success = self.db.update_record('goal', id, **update_data)
                if success:
                    return self._create_success_response(id, "updated")
                else:
                    return self._create_error_response("更新失败", id)
                    
        except Exception as e:
            return self._create_error_response(str(e)) 
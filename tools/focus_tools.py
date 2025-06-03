"""
关注点工具
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools

class FocusTools(BaseTools):
    """关注点工具类"""
    
    def query_focuses(self, filter: Optional[Dict[str, Any]] = None, 
                     sort_by: str = 'priority', sort_order: str = 'desc', 
                     limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """查询关注点数据"""
        try:
            allowed_filters = [
                'ids', 'content_contains', 'priority_gte', 'status_is', 'status_in',
                'context_contains', 'keywords_contain_any', 'source_app_is',
                'deadline_from', 'deadline_to', 'privacy_level_is'
            ]
            
            filter_conditions = self._build_filter_conditions(filter or {}, allowed_filters)
            records, total_count = self.db.query_records('focus', filter_conditions, sort_by, sort_order, limit, offset)
            
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
            
            return self._generate_query_response(records, total_count, template)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    def save_focus(self, id: Optional[int] = None, content: Optional[str] = None, 
                  priority: Optional[int] = None, status: str = 'active',
                  context: Optional[str] = None, keywords: Optional[List[str]] = None,
                  source_app: str = 'unknown', deadline: Optional[str] = None,
                  privacy_level: str = 'public') -> Dict[str, Any]:
        """保存关注点数据"""
        try:
            if id is None:
                # 创建新记录
                if not content or priority is None:
                    return self._create_error_response("创建关注点记录需要提供 content 和 priority")
                
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
                
                record_id = self.db.insert_record('focus', **record_data)
                return self._create_success_response(record_id, "created")
            else:
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
                
                if not update_data:
                    return self._create_success_response(id, "no_change")
                
                success = self.db.update_record('focus', id, **update_data)
                if success:
                    return self._create_success_response(id, "updated")
                else:
                    return self._create_error_response("更新失败", id)
                    
        except Exception as e:
            return self._create_error_response(str(e)) 
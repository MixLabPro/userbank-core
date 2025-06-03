"""
观点工具
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools

class ViewpointTools(BaseTools):
    """观点工具类"""
    
    def query_viewpoints(self, filter: Optional[Dict[str, Any]] = None, 
                        sort_by: str = 'created_time', sort_order: str = 'desc', 
                        limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """查询观点数据"""
        try:
            allowed_filters = [
                'ids', 'content_contains', 'source_people_contains', 'related_event_contains',
                'keywords_contain_any', 'keywords_contain_all', 'source_app_is', 'privacy_level_is'
            ]
            
            filter_conditions = self._build_filter_conditions(filter or {}, allowed_filters)
            records, total_count = self.db.query_records('viewpoint', filter_conditions, sort_by, sort_order, limit, offset)
            
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
            
            return self._generate_query_response(records, total_count, template)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    def save_viewpoint(self, id: Optional[int] = None, content: Optional[str] = None, 
                      source_people: Optional[str] = None, keywords: Optional[List[str]] = None,
                      source_app: str = 'unknown', related_event: Optional[str] = None,
                      reference_urls: Optional[List[str]] = None, privacy_level: str = 'public') -> Dict[str, Any]:
        """保存观点数据"""
        try:
            if id is None:
                # 创建新记录
                if not content:
                    return self._create_error_response("创建观点记录需要提供 content")
                
                record_id = self.db.insert_record('viewpoint',
                                               content=content,
                                               source_people=source_people,
                                               keywords=keywords or [],
                                               source_app=source_app,
                                               related_event=related_event,
                                               reference_urls=reference_urls or [],
                                               privacy_level=privacy_level)
                
                return self._create_success_response(record_id, "created")
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
                    return self._create_success_response(id, "no_change")
                
                success = self.db.update_record('viewpoint', id, **update_data)
                if success:
                    return self._create_success_response(id, "updated")
                else:
                    return self._create_error_response("更新失败", id)
                    
        except Exception as e:
            return self._create_error_response(str(e)) 
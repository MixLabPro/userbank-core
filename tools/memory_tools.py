"""
记忆工具
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools

class MemoryTools(BaseTools):
    """记忆工具类"""
    
    def query_memories(self, filter: Optional[Dict[str, Any]] = None, 
                      sort_by: str = 'created_time', sort_order: str = 'desc', 
                      limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """查询记忆数据"""
        try:
            allowed_filters = [
                'ids', 'content_contains', 'memory_type_in', 'importance_gte', 
                'importance_lte', 'related_people_contains', 'location_contains',
                'memory_date_from', 'memory_date_to', 'keywords_contain_any',
                'keywords_contain_all', 'source_app_is', 'privacy_level_is',
                'created_time_from', 'created_time_to'
            ]
            
            filter_conditions = self._build_filter_conditions(filter or {}, allowed_filters)
            records, total_count = self.db.query_records('memory', filter_conditions, sort_by, sort_order, limit, offset)
            
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
            
            return self._generate_query_response(records, total_count, template)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    def save_memory(self, id: Optional[int] = None, content: Optional[str] = None, 
                   memory_type: Optional[str] = None, importance: Optional[int] = None,
                   related_people: Optional[str] = None, location: Optional[str] = None,
                   memory_date: Optional[str] = None, keywords: Optional[List[str]] = None,
                   source_app: str = 'unknown', reference_urls: Optional[List[str]] = None,
                   privacy_level: str = 'public') -> Dict[str, Any]:
        """保存记忆数据"""
        try:
            if id is None:
                # 创建新记录
                if not content or not memory_type or importance is None:
                    return self._create_error_response("创建记忆记录需要提供 content、memory_type 和 importance")
                
                record_id = self.db.insert_record('memory',
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
                
                return self._create_success_response(record_id, "created")
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
                    return self._create_success_response(id, "no_change")
                
                success = self.db.update_record('memory', id, **update_data)
                if success:
                    return self._create_success_response(id, "updated")
                else:
                    return self._create_error_response("更新失败", id)
                    
        except Exception as e:
            return self._create_error_response(str(e)) 
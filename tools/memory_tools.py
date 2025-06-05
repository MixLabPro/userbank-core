"""
Memory tools
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools

class MemoryTools(BaseTools):
    """Memory tools class"""
    
    def query_memories(self, filter: Optional[Dict[str, Any]] = None, 
                      sort_by: str = 'created_time', sort_order: str = 'desc', 
                      limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Query memory data"""
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
            
            # Generate prompt content
            template = """# User Memory Data

The following are user memory records retrieved based on your query criteria:

{{#each raw_data}}
## Memory Record (ID: {{this.id}})
- **Core Content (content)**: {{this.content}}
- **Memory Type (memory_type)**: {{this.memory_type}} (Options: experience/personal experience, event/important event, learning/learning experience, interaction/interpersonal interaction, achievement/achievement record, mistake/lesson learned)
- **Importance Level (importance)**: {{this.importance}} (1-10, 10 is most important)
- **Related People (related_people)**: {{this.related_people}}
- **Location (location)**: {{this.location}}
- **Memory Date (memory_date)**: {{this.memory_date}}
- **Keywords (keywords)**: {{this.keywords}}
- **Source App (source_app)**: {{this.source_app}}
- **Reference URLs (reference_urls)**: {{this.reference_urls}}
- **Privacy Level (privacy_level)**: {{this.privacy_level}}
- **Created Time (created_time)**: {{this.created_time}}
- **Updated Time (updated_time)**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
No memory records found matching the criteria.
{{/if}}

**Query Summary:**
- Total {{total_count}} related records found.
- Currently displaying {{raw_data.length}} records."""
            
            return self._generate_query_response(records, total_count, template)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    def save_memory(self, id: Optional[int] = None, content: Optional[str] = None, 
                   memory_type: Optional[str] = None, importance: Optional[int] = None,
                   related_people: Optional[str] = None, location: Optional[str] = None,
                   memory_date: Optional[str] = None, keywords: Optional[List[str]] = None,
                   source_app: str = 'unknown', reference_urls: Optional[List[str]] = None,
                   privacy_level: str = 'public') -> Dict[str, Any]:
        """Save memory data"""
        try:
            if id is None:
                # Create new record
                if not content or not memory_type or importance is None:
                    return self._create_error_response("Creating memory record requires content, memory_type and importance")
                
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
                # Update existing record
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
                    return self._create_error_response("Update failed", id)
                    
        except Exception as e:
            return self._create_error_response(str(e)) 
"""
Viewpoint tools
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools

class ViewpointTools(BaseTools):
    """Viewpoint tools class"""
    
    def query_viewpoints(self, filter: Optional[Dict[str, Any]] = None, 
                        sort_by: str = 'created_time', sort_order: str = 'desc', 
                        limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Query viewpoint data"""
        try:
            allowed_filters = [
                'ids', 'content_contains', 'source_people_contains', 'related_event_contains',
                'keywords_contain_any', 'keywords_contain_all', 'source_app_is', 'privacy_level_is'
            ]
            
            filter_conditions = self._build_filter_conditions(filter or {}, allowed_filters)
            records, total_count = self.db.query_records('viewpoint', filter_conditions, sort_by, sort_order, limit, offset)
            
            template = """# User Viewpoint Data

The following are user viewpoint records retrieved based on your query criteria:

{{#each raw_data}}
## Viewpoint Record (ID: {{this.id}})
- **Core Viewpoint**: {{this.content}}
- **Source Person**: {{this.source_people}}
- **Related Event**: {{this.related_event}}
- **Keywords**: {{this.keywords}}
- **Source App**: {{this.source_app}}
- **Reference URLs**: {{this.reference_urls}}
- **Privacy Level**: {{this.privacy_level}}
- **Created Time**: {{this.created_time}}
- **Updated Time**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
No viewpoint records found matching the criteria.
{{/if}}

**Query Summary:**
- Total {{total_count}} related records found.
- Currently displaying {{raw_data.length}} records."""
            
            return self._generate_query_response(records, total_count, template)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    def save_viewpoint(self, id: Optional[int] = None, content: Optional[str] = None, 
                      source_people: Optional[str] = None, keywords: Optional[List[str]] = None,
                      source_app: str = 'unknown', related_event: Optional[str] = None,
                      reference_urls: Optional[List[str]] = None, privacy_level: str = 'public') -> Dict[str, Any]:
        """Save viewpoint data"""
        try:
            if id is None:
                # Create new record
                if not content:
                    return self._create_error_response("Creating viewpoint record requires content")
                
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
                # Update existing record
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
                    return self._create_error_response("Update failed", id)
                    
        except Exception as e:
            return self._create_error_response(str(e)) 
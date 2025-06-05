"""
Preference tools
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools

class PreferenceTools(BaseTools):
    """Preference tools class"""
    
    def query_preferences(self, filter: Optional[Dict[str, Any]] = None, 
                         sort_by: str = 'created_time', sort_order: str = 'desc', 
                         limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Query preference data"""
        try:
            allowed_filters = [
                'ids', 'content_contains', 'context_is', 'context_contains',
                'keywords_contain_any', 'source_app_is', 'privacy_level_is'
            ]
            
            filter_conditions = self._build_filter_conditions(filter or {}, allowed_filters)
            records, total_count = self.db.query_records('preference', filter_conditions, sort_by, sort_order, limit, offset)
            
            template = """# User Preference Data

The following are user preference records retrieved based on your query criteria:

{{#each raw_data}}
## Preference Record (ID: {{this.id}})
- **Preference Content**: {{this.content}}
- **Applicable Context**: {{this.context}}
- **Keywords**: {{this.keywords}}
- **Source App**: {{this.source_app}}
- **Privacy Level**: {{this.privacy_level}}
- **Created Time**: {{this.created_time}}
- **Updated Time**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
No preference records found matching the criteria.
{{/if}}

**Query Summary:**
- Total {{total_count}} related records found.
- Currently displaying {{raw_data.length}} records."""
            
            return self._generate_query_response(records, total_count, template)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    def save_preference(self, id: Optional[int] = None, content: Optional[str] = None, 
                       context: Optional[str] = None, keywords: Optional[List[str]] = None,
                       source_app: str = 'unknown', privacy_level: str = 'public') -> Dict[str, Any]:
        """Save preference data"""
        try:
            if id is None:
                # Create new record
                if not content:
                    return self._create_error_response("Creating preference record requires content")
                
                record_id = self.db.insert_record('preference',
                                               content=content,
                                               context=context,
                                               keywords=keywords or [],
                                               source_app=source_app,
                                               privacy_level=privacy_level)
                
                return self._create_success_response(record_id, "created")
            else:
                # Update existing record
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
                    return self._create_success_response(id, "no_change")
                
                success = self.db.update_record('preference', id, **update_data)
                if success:
                    return self._create_success_response(id, "updated")
                else:
                    return self._create_error_response("Update failed", id)
                    
        except Exception as e:
            return self._create_error_response(str(e)) 
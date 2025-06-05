"""
Focus tools
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools

class FocusTools(BaseTools):
    """Focus tools class"""
    
    def query_focuses(self, filter: Optional[Dict[str, Any]] = None, 
                     sort_by: str = 'priority', sort_order: str = 'desc', 
                     limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Query focus data"""
        try:
            allowed_filters = [
                'ids', 'content_contains', 'priority_gte', 'status_is', 'status_in',
                'context_contains', 'keywords_contain_any', 'source_app_is',
                'deadline_from', 'deadline_to', 'privacy_level_is'
            ]
            
            filter_conditions = self._build_filter_conditions(filter or {}, allowed_filters)
            records, total_count = self.db.query_records('focus', filter_conditions, sort_by, sort_order, limit, offset)
            
            template = """# User Focus Data

The following are user focus records retrieved based on your query criteria:

{{#each raw_data}}
## Focus Record (ID: {{this.id}})
- **Focus Content (content)**: {{this.content}}
- **Priority (priority)**: {{this.priority}} (1-10, 10 is highest)
- **Status (status)**: {{this.status}} (Options: active/in progress, paused/paused, completed/completed)
- **Context (context)**: {{this.context}}
- **Keywords (keywords)**: {{this.keywords}}
- **Source App (source_app)**: {{this.source_app}}
- **Deadline (deadline)**: {{this.deadline}}
- **Privacy Level (privacy_level)**: {{this.privacy_level}}
- **Created Time (created_time)**: {{this.created_time}}
- **Updated Time (updated_time)**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
No focus records found matching the criteria.
{{/if}}

**Query Summary:**
- Total {{total_count}} related records found.
- Currently displaying {{raw_data.length}} records."""
            
            return self._generate_query_response(records, total_count, template)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    def save_focus(self, id: Optional[int] = None, content: Optional[str] = None, 
                  priority: Optional[int] = None, status: str = 'active',
                  context: Optional[str] = None, keywords: Optional[List[str]] = None,
                  source_app: str = 'unknown', deadline: Optional[str] = None,
                  privacy_level: str = 'public') -> Dict[str, Any]:
        """Save focus data"""
        try:
            if id is None:
                # Create new record
                if not content or priority is None:
                    return self._create_error_response("Creating focus record requires content and priority")
                
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
                # Update existing record
                update_data = {}
                if content is not None:
                    update_data['content'] = content
                if priority is not None:
                    update_data['priority'] = priority
                if status != 'active':
                    update_data['status'] = status
                if context is not None:
                    update_data['context'] = context
                if keywords is not None:
                    update_data['keywords'] = keywords
                if source_app != 'unknown':
                    update_data['source_app'] = source_app
                if deadline is not None:
                    update_data['deadline'] = deadline
                if privacy_level != 'public':
                    update_data['privacy_level'] = privacy_level
                
                if not update_data:
                    return self._create_success_response(id, "no_change")
                
                success = self.db.update_record('focus', id, **update_data)
                if success:
                    return self._create_success_response(id, "updated")
                else:
                    return self._create_error_response("Update failed", id)
                    
        except Exception as e:
            return self._create_error_response(str(e)) 
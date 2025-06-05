"""
Goal tools
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools

class GoalTools(BaseTools):
    """Goal tools class"""
    
    def query_goals(self, filter: Optional[Dict[str, Any]] = None, 
                   sort_by: str = 'deadline', sort_order: str = 'asc', 
                   limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Query goal data"""
        try:
            allowed_filters = [
                'ids', 'content_contains', 'type_is', 'type_in', 'deadline_from', 'deadline_to',
                'status_is', 'status_in', 'keywords_contain_any', 'source_app_is', 'privacy_level_is'
            ]
            
            filter_conditions = self._build_filter_conditions(filter or {}, allowed_filters)
            records, total_count = self.db.query_records('goal', filter_conditions, sort_by, sort_order, limit, offset)
            
            template = """# User Goal Data

The following are user goal records retrieved based on your query criteria:

{{#each raw_data}}
## Goal Record (ID: {{this.id}})
- **Goal Content (content)**: {{this.content}}
- **Goal Type (type)**: {{this.type}} (Options: long_term/long-term goal, short_term/short-term goal, plan/plan, todo/todo item)
- **Deadline (deadline)**: {{this.deadline}}
- **Current Status (status)**: {{this.status}} (Options: planning/planning, in_progress/in progress, completed/completed, abandoned/abandoned)
- **Keywords (keywords)**: {{this.keywords}}
- **Source App (source_app)**: {{this.source_app}}
- **Privacy Level (privacy_level)**: {{this.privacy_level}}
- **Created Time (created_time)**: {{this.created_time}}
- **Updated Time (updated_time)**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
No goal records found matching the criteria.
{{/if}}

**Query Summary:**
- Total {{total_count}} related records found.
- Currently displaying {{raw_data.length}} records."""
            
            return self._generate_query_response(records, total_count, template)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    def save_goal(self, id: Optional[int] = None, content: Optional[str] = None, 
                 type: Optional[str] = None, deadline: Optional[str] = None,
                 status: str = 'planning', keywords: Optional[List[str]] = None,
                 source_app: str = 'unknown', privacy_level: str = 'public') -> Dict[str, Any]:
        """Save goal data"""
        try:
            if id is None:
                # Create new record
                if not content or not type:
                    return self._create_error_response("Creating goal record requires content and type")
                
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
                # Update existing record
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
                    return self._create_error_response("Update failed", id)
                    
        except Exception as e:
            return self._create_error_response(str(e)) 
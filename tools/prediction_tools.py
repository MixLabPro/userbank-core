"""
Prediction tools
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools

class PredictionTools(BaseTools):
    """Prediction tools class"""
    
    def query_predictions(self, filter: Optional[Dict[str, Any]] = None, 
                         sort_by: str = 'created_time', sort_order: str = 'desc', 
                         limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Query prediction data"""
        try:
            allowed_filters = [
                'ids', 'content_contains', 'timeframe_contains', 'basis_contains',
                'verification_status_is', 'keywords_contain_any', 'source_app_is', 'privacy_level_is'
            ]
            
            filter_conditions = self._build_filter_conditions(filter or {}, allowed_filters)
            records, total_count = self.db.query_records('prediction', filter_conditions, sort_by, sort_order, limit, offset)
            
            template = """# User Prediction Data

The following are user prediction records retrieved based on your query criteria:

{{#each raw_data}}
## Prediction Record (ID: {{this.id}})
- **Prediction Content**: {{this.content}}
- **Time Frame**: {{this.timeframe}}
- **Prediction Basis**: {{this.basis}}
- **Verification Status**: {{this.verification_status}} (Options: pending/pending verification, correct/correct, incorrect/incorrect, partial/partially correct)
- **Keywords**: {{this.keywords}}
- **Source App**: {{this.source_app}}
- **Reference URLs**: {{this.reference_urls}}
- **Privacy Level**: {{this.privacy_level}}
- **Created Time**: {{this.created_time}}
- **Updated Time**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
No prediction records found matching the criteria.
{{/if}}

**Query Summary:**
- Total {{total_count}} related records found.
- Currently displaying {{raw_data.length}} records."""
            
            return self._generate_query_response(records, total_count, template)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    def save_prediction(self, id: Optional[int] = None, content: Optional[str] = None, 
                       timeframe: Optional[str] = None, basis: Optional[str] = None,
                       verification_status: str = 'pending', keywords: Optional[List[str]] = None,
                       source_app: str = 'unknown', reference_urls: Optional[List[str]] = None,
                       privacy_level: str = 'public') -> Dict[str, Any]:
        """Save prediction data"""
        try:
            if id is None:
                # Create new record
                if not content or not timeframe or not basis:
                    return self._create_error_response("Creating prediction record requires content, timeframe and basis")
                
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
                
                record_id = self.db.insert_record('prediction', **record_data)
                return self._create_success_response(record_id, "created")
            else:
                # Update existing record
                update_data = {}
                if content is not None:
                    update_data['content'] = content
                if timeframe is not None:
                    update_data['timeframe'] = timeframe
                if basis is not None:
                    update_data['basis'] = basis
                if verification_status != 'pending':
                    update_data['verification_status'] = verification_status
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
                
                success = self.db.update_record('prediction', id, **update_data)
                if success:
                    return self._create_success_response(id, "updated")
                else:
                    return self._create_error_response("Update failed", id)
                    
        except Exception as e:
            return self._create_error_response(str(e)) 
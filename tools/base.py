"""
Base tool classes and common functions
"""

from typing import Any, Dict, List
from datetime import datetime
from Database.database import get_database

# Get database instance
db = get_database()

# Define mapping of all table names and English descriptions
TABLE_DESCRIPTIONS = {
    # Core tables
    'persona': 'User Profile',
    'category': 'Category System',
    'relations': 'General Relations',
    
    # Main data tables
    'viewpoint': 'Viewpoints',
    'insight': 'Insights',
    'focus': 'Focus Points',
    'goal': 'Goals',
    'preference': 'Preferences',
    'methodology': 'Methodologies',
    'prediction': 'Predictions',
    'memory': 'Memories'
}

def generate_prompt_content(template: str, data: Any) -> str:
    """Generate template-based prompt content"""
    if isinstance(data, list):
        if not data:
            return template.replace("{{#each raw_data}}", "").replace("{{/each}}", "").replace("{{#if (eq raw_data.length 0)}}", "").replace("{{/if}}", "No records found matching the criteria.")
        
        content_parts = []
        for item in data:
            item_content = template
            # Simple template replacement
            for key, value in item.items():
                if value is not None:
                    item_content = item_content.replace(f"{{{{this.{key}}}}}", str(value))
                else:
                    item_content = item_content.replace(f"{{{{this.{key}}}}}", "")
            content_parts.append(item_content)
        
        # Replace loop markers
        result = template.replace("{{#each raw_data}}", "").replace("{{/each}}", "\n".join(content_parts))
        result = result.replace("{{#if (eq raw_data.length 0)}}", "").replace("{{/if}}", "")
        result = result.replace("{{total_count}}", str(len(data)))
        result = result.replace("{{raw_data.length}}", str(len(data)))
        
        return result
    elif isinstance(data, dict):
        result = template
        for key, value in data.items():
            if value is not None:
                result = result.replace(f"{{{{{key}}}}}", str(value))
            else:
                result = result.replace(f"{{{{{key}}}}}", "")
        return result
    else:
        return template

class BaseTools:
    """Base tool class"""
    
    def __init__(self):
        self.db = db
        
    def _create_success_response(self, record_id: int, operation: str) -> Dict[str, Any]:
        """Create success response"""
        return {
            "id": record_id,
            "operation": operation,
            "timestamp": datetime.now().isoformat()
        }
        
    def _create_error_response(self, error_msg: str, record_id: int = None) -> Dict[str, Any]:
        """Create error response"""
        return {
            "id": record_id,
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": error_msg
        }
        
    def _build_filter_conditions(self, filter_dict: Dict[str, Any], allowed_filters: List[str]) -> Dict[str, Any]:
        """Build filter conditions"""
        filter_conditions = {}
        
        if filter_dict:
            for key, value in filter_dict.items():
                if value is not None and key in allowed_filters:
                    filter_conditions[key] = value
                    
        return filter_conditions
        
    def _generate_query_response(self, records: List[Dict], total_count: int, template: str) -> Dict[str, Any]:
        """Generate query response"""
        content = generate_prompt_content(template, records)
        content = content.replace("{{total_count}}", str(total_count))
        
        return {
            "content": content,
            "raw_data": records,
            "total_count": total_count
        } 
"""
Database tools
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools, TABLE_DESCRIPTIONS

class DatabaseTools(BaseTools):
    """Database tools class"""
    
    def execute_custom_sql(self, sql: str, params: Optional[List[str]] = None, 
                          fetch_results: bool = True) -> Dict[str, Any]:
        """Execute custom SQL statement"""
        try:
            result = self.db.execute_custom_sql(sql, params, fetch_results)
            return result
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to execute custom SQL: {str(e)}"
            }
    
    def get_table_schema(self, table_name: Optional[str] = None) -> Dict[str, Any]:
        """Get table schema information"""
        try:
            if table_name:
                if table_name not in TABLE_DESCRIPTIONS:
                    return {
                        "success": False,
                        "message": f"Invalid table name: {table_name}. Valid table names: {list(TABLE_DESCRIPTIONS.keys())}"
                    }
                
                schema_result = self.db.get_table_schema(table_name)
                return schema_result
            else:
                # Get schema information for all tables
                schema_result = self.db.get_table_schema()
                return schema_result
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to get table schema: {str(e)}"
            } 
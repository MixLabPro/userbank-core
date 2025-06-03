"""
数据库工具
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools, TABLE_DESCRIPTIONS

class DatabaseTools(BaseTools):
    """数据库工具类"""
    
    def execute_custom_sql(self, sql: str, params: Optional[List[str]] = None, 
                          fetch_results: bool = True) -> Dict[str, Any]:
        """执行自定义SQL语句"""
        try:
            result = self.db.execute_custom_sql(sql, params, fetch_results)
            return result
        except Exception as e:
            return {
                "success": False,
                "message": f"执行自定义SQL失败: {str(e)}"
            }
    
    def get_table_schema(self, table_name: Optional[str] = None) -> Dict[str, Any]:
        """获取表结构信息"""
        try:
            if table_name:
                if table_name not in TABLE_DESCRIPTIONS:
                    return {
                        "success": False,
                        "message": f"无效的表名: {table_name}。有效的表名: {list(TABLE_DESCRIPTIONS.keys())}"
                    }
                
                schema_result = self.db.get_table_schema(table_name)
                return schema_result
            else:
                # 获取所有表的结构信息
                schema_result = self.db.get_table_schema()
                return schema_result
                
        except Exception as e:
            return {
                "success": False,
                "message": f"获取表结构失败: {str(e)}"
            } 
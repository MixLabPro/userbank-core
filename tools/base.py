"""
基础工具类和通用函数
"""

from typing import Any, Dict, List
from datetime import datetime
from Database.database import get_database

# 获取数据库实例
db = get_database()

# 定义所有表名和中文描述的映射
TABLE_DESCRIPTIONS = {
    # 核心表
    'persona': '人物档案',
    'category': '分类体系',
    'relations': '通用关联',
    
    # 主要数据表
    'viewpoint': '观点',
    'insight': '洞察',
    'focus': '关注点',
    'goal': '目标',
    'preference': '偏好',
    'methodology': '方法论',
    'prediction': '预测',
    'memory': '记忆'
}

def generate_prompt_content(template: str, data: Any) -> str:
    """生成基于模板的提示内容"""
    if isinstance(data, list):
        if not data:
            return template.replace("{{#each raw_data}}", "").replace("{{/each}}", "").replace("{{#if (eq raw_data.length 0)}}", "").replace("{{/if}}", "未找到符合条件的记录。")
        
        content_parts = []
        for item in data:
            item_content = template
            # 简单的模板替换
            for key, value in item.items():
                if value is not None:
                    item_content = item_content.replace(f"{{{{this.{key}}}}}", str(value))
                else:
                    item_content = item_content.replace(f"{{{{this.{key}}}}}", "")
            content_parts.append(item_content)
        
        # 替换循环标记
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
    """基础工具类"""
    
    def __init__(self):
        self.db = db
        
    def _create_success_response(self, record_id: int, operation: str) -> Dict[str, Any]:
        """创建成功响应"""
        return {
            "id": record_id,
            "operation": operation,
            "timestamp": datetime.now().isoformat()
        }
        
    def _create_error_response(self, error_msg: str, record_id: int = None) -> Dict[str, Any]:
        """创建错误响应"""
        return {
            "id": record_id,
            "operation": "error",
            "timestamp": datetime.now().isoformat(),
            "error": error_msg
        }
        
    def _build_filter_conditions(self, filter_dict: Dict[str, Any], allowed_filters: List[str]) -> Dict[str, Any]:
        """构建过滤条件"""
        filter_conditions = {}
        
        if filter_dict:
            for key, value in filter_dict.items():
                if value is not None and key in allowed_filters:
                    filter_conditions[key] = value
                    
        return filter_conditions
        
    def _generate_query_response(self, records: List[Dict], total_count: int, template: str) -> Dict[str, Any]:
        """生成查询响应"""
        content = generate_prompt_content(template, records)
        content = content.replace("{{total_count}}", str(total_count))
        
        return {
            "content": content,
            "raw_data": records,
            "total_count": total_count
        } 
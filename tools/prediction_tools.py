"""
预测工具
"""

from typing import Dict, Any, Optional, List
from .base import BaseTools

class PredictionTools(BaseTools):
    """预测工具类"""
    
    def query_predictions(self, filter: Optional[Dict[str, Any]] = None, 
                         sort_by: str = 'created_time', sort_order: str = 'desc', 
                         limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """查询预测数据"""
        try:
            allowed_filters = [
                'ids', 'content_contains', 'timeframe_contains', 'basis_contains',
                'verification_status_is', 'keywords_contain_any', 'source_app_is', 'privacy_level_is'
            ]
            
            filter_conditions = self._build_filter_conditions(filter or {}, allowed_filters)
            records, total_count = self.db.query_records('prediction', filter_conditions, sort_by, sort_order, limit, offset)
            
            template = """# 用户预测数据

以下是根据您的查询条件检索到的用户预测记录：

{{#each raw_data}}
## 预测记录 (ID: {{this.id}})
- **预测内容 (content)**: {{this.content}}
- **时间范围 (timeframe)**: {{this.timeframe}}
- **预测依据 (basis)**: {{this.basis}}
- **验证状态 (verification_status)**: {{this.verification_status}} (可选值: pending/待验证, correct/正确, incorrect/错误, partial/部分正确)
- **关键词 (keywords)**: {{this.keywords}}
- **数据来源应用 (source_app)**: {{this.source_app}}
- **参考链接 (reference_urls)**: {{this.reference_urls}}
- **隐私级别 (privacy_level)**: {{this.privacy_level}}
- **记录创建时间 (created_time)**: {{this.created_time}}
- **记录更新时间 (updated_time)**: {{this.updated_time}}
---
{{/each}}

{{#if (eq raw_data.length 0)}}
未找到符合条件的预测记录。
{{/if}}

**查询摘要:**
- 总共找到 {{total_count}} 条相关记录。
- 当前显示 {{raw_data.length}} 条记录。"""
            
            return self._generate_query_response(records, total_count, template)
            
        except Exception as e:
            return self._create_error_response(str(e))
    
    def save_prediction(self, id: Optional[int] = None, content: Optional[str] = None, 
                       timeframe: Optional[str] = None, basis: Optional[str] = None,
                       verification_status: str = 'pending', keywords: Optional[List[str]] = None,
                       source_app: str = 'unknown', reference_urls: Optional[List[str]] = None,
                       privacy_level: str = 'public') -> Dict[str, Any]:
        """保存预测数据"""
        try:
            if id is None:
                # 创建新记录
                if not content or not timeframe or not basis:
                    return self._create_error_response("创建预测记录需要提供 content、timeframe 和 basis")
                
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
                # 更新现有记录
                update_data = {}
                if content is not None:
                    update_data['content'] = content
                if timeframe is not None:
                    update_data['timeframe'] = timeframe
                if basis is not None:
                    update_data['basis'] = basis
                if verification_status is not None:
                    update_data['verification_status'] = verification_status
                if keywords is not None:
                    update_data['keywords'] = keywords
                if source_app is not None:
                    update_data['source_app'] = source_app
                if reference_urls is not None:
                    update_data['reference_urls'] = reference_urls
                if privacy_level is not None:
                    update_data['privacy_level'] = privacy_level
                
                if not update_data:
                    return self._create_success_response(id, "no_change")
                
                success = self.db.update_record('prediction', id, **update_data)
                if success:
                    return self._create_success_response(id, "updated")
                else:
                    return self._create_error_response("更新失败", id)
                    
        except Exception as e:
            return self._create_error_response(str(e)) 
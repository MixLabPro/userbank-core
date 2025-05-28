"""
数据库管理模块
Database Management Module

负责创建和管理个人画像数据结构的SQLite数据库
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import os

class ProfileDatabase:
    """个人画像数据库管理类"""
    
    def __init__(self, db_path: str = "profile_data.db"):
        """
        初始化数据库连接
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        
        # 定义所有表名
        self.tables = [
            'belief',           # 信念
            'insight',          # 洞察
            'focus',           # 关注点
            'long_term_goal',   # 长期目标
            'short_term_goal',  # 短期目标
            'preference',       # 偏好
            'decision',         # 决策
            'methodology'       # 方法论
        ]
        
        try:
            # 检查数据库文件是否存在
            db_exists = Path(db_path).exists()
            
            self._connect()
            
            # 只有在数据库文件不存在或表不存在时才创建表
            if not db_exists or not self._check_tables_exist():
                self._create_tables()
                self._create_indexes()
            
        except Exception as e:
            raise
    
    def _connect(self):
        """建立数据库连接"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # 启用字典式访问
            self.cursor = self.connection.cursor()
        except Exception as e:
            raise
    
    def _check_tables_exist(self) -> bool:
        """
        检查所有必需的表是否存在
        
        Returns:
            如果所有表都存在返回True，否则返回False
        """
        try:
            for table_name in self.tables:
                # 查询表是否存在
                self.cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name=?
                """, (table_name,))
                
                if not self.cursor.fetchone():
                    return False
            
            return True
        except Exception as e:
            return False
    
    def _create_tables(self):
        """创建所有数据表"""
        # 通用表结构SQL模板
        table_sql_template = """
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            related TEXT,  -- JSON格式存储相关主题数组
            created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        try:
            for table_name in self.tables:
                sql = table_sql_template.format(table_name=table_name)
                self.cursor.execute(sql)
            
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise
    
    def _create_indexes(self):
        """创建数据库索引以提升查询性能"""
        try:
            for table_name in self.tables:
                # 为content字段创建索引（支持全文搜索）
                content_index_sql = f"""
                CREATE INDEX IF NOT EXISTS idx_{table_name}_content 
                ON {table_name}(content)
                """
                
                # 为created_time字段创建索引（支持时间范围查询）
                time_index_sql = f"""
                CREATE INDEX IF NOT EXISTS idx_{table_name}_created_time 
                ON {table_name}(created_time)
                """
                
                # 为related字段创建索引（支持主题搜索）
                related_index_sql = f"""
                CREATE INDEX IF NOT EXISTS idx_{table_name}_related 
                ON {table_name}(related)
                """
                
                self.cursor.execute(content_index_sql)
                self.cursor.execute(time_index_sql)
                self.cursor.execute(related_index_sql)
            
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise
    
    def insert_record(self, table_name: str, content: str, related: List[str] = None) -> int:
        """
        插入新记录
        
        Args:
            table_name: 表名
            content: 内容
            related: 相关主题列表
            
        Returns:
            新插入记录的ID
        """
        if table_name not in self.tables:
            raise ValueError(f"无效的表名: {table_name}")
        
        try:
            related_json = json.dumps(related or [], ensure_ascii=False)
            
            sql = f"""
            INSERT INTO {table_name} (content, related, created_time, updated_time)
            VALUES (?, ?, ?, ?)
            """
            
            current_time = datetime.now().isoformat()
            self.cursor.execute(sql, (content, related_json, current_time, current_time))
            self.connection.commit()
            
            record_id = self.cursor.lastrowid
            return record_id
            
        except Exception as e:
            self.connection.rollback()
            raise
    
    def update_record(self, table_name: str, record_id: int, content: str = None, related: List[str] = None) -> bool:
        """
        更新记录
        
        Args:
            table_name: 表名
            record_id: 记录ID
            content: 新内容（可选）
            related: 新相关主题列表（可选）
            
        Returns:
            是否更新成功
        """
        if table_name not in self.tables:
            raise ValueError(f"无效的表名: {table_name}")
        
        try:
            # 构建更新字段
            update_fields = []
            params = []
            
            if content is not None:
                update_fields.append("content = ?")
                params.append(content)
            
            if related is not None:
                update_fields.append("related = ?")
                params.append(json.dumps(related, ensure_ascii=False))
            
            if not update_fields:
                return False
            
            update_fields.append("updated_time = ?")
            params.append(datetime.now().isoformat())
            params.append(record_id)
            
            sql = f"""
            UPDATE {table_name} 
            SET {', '.join(update_fields)}
            WHERE id = ?
            """
            
            self.cursor.execute(sql, params)
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                return True
            else:
                return False
                
        except Exception as e:
            self.connection.rollback()
            raise
    
    def delete_record(self, table_name: str, record_id: int) -> bool:
        """
        删除记录
        
        Args:
            table_name: 表名
            record_id: 记录ID
            
        Returns:
            是否删除成功
        """
        if table_name not in self.tables:
            raise ValueError(f"无效的表名: {table_name}")
        
        try:
            sql = f"DELETE FROM {table_name} WHERE id = ?"
            self.cursor.execute(sql, (record_id,))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                return True
            else:
                return False
                
        except Exception as e:
            self.connection.rollback()
            raise
    
    def get_record(self, table_name: str, record_id: int) -> Optional[Dict[str, Any]]:
        """
        获取单条记录
        
        Args:
            table_name: 表名
            record_id: 记录ID
            
        Returns:
            记录字典或None
        """
        if table_name not in self.tables:
            raise ValueError(f"无效的表名: {table_name}")
        
        try:
            sql = f"SELECT * FROM {table_name} WHERE id = ?"
            self.cursor.execute(sql, (record_id,))
            row = self.cursor.fetchone()
            
            if row:
                record = dict(row)
                # 解析JSON格式的related字段
                if record['related']:
                    record['related'] = json.loads(record['related'])
                else:
                    record['related'] = []
                return record
            else:
                return None
                
        except Exception as e:
            raise
    
    def search_records(self, table_name: str, keyword: str = None, related_topic: str = None, 
                      limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        搜索记录
        
        Args:
            table_name: 表名
            keyword: 内容关键词
            related_topic: 相关主题
            limit: 返回记录数限制
            offset: 偏移量
            
        Returns:
            记录列表
        """
        if table_name not in self.tables:
            raise ValueError(f"无效的表名: {table_name}")
        
        try:
            conditions = []
            params = []
            
            if keyword:
                conditions.append("content LIKE ?")
                params.append(f"%{keyword}%")
            
            if related_topic:
                conditions.append("related LIKE ?")
                params.append(f"%{related_topic}%")
            
            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)
            
            sql = f"""
            SELECT * FROM {table_name} 
            {where_clause}
            ORDER BY created_time DESC 
            LIMIT ? OFFSET ?
            """
            
            params.extend([limit, offset])
            self.cursor.execute(sql, params)
            rows = self.cursor.fetchall()
            
            records = []
            for row in rows:
                record = dict(row)
                # 解析JSON格式的related字段
                if record['related']:
                    record['related'] = json.loads(record['related'])
                else:
                    record['related'] = []
                records.append(record)
            
            return records
            
        except Exception as e:
            raise
    
    def get_all_records(self, table_name: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        获取表中所有记录
        
        Args:
            table_name: 表名
            limit: 返回记录数限制
            offset: 偏移量
            
        Returns:
            记录列表
        """
        return self.search_records(table_name, limit=limit, offset=offset)
    
    def get_table_stats(self, table_name: str = None) -> Dict[str, Any]:
        """
        获取表统计信息
        
        Args:
            table_name: 表名（可选，不提供则获取所有表的统计信息）
            
        Returns:
            统计信息字典
        """
        try:
            if table_name:
                # 获取单个表的统计信息
                if table_name not in self.tables:
                    raise ValueError(f"无效的表名: {table_name}")
                
                # 获取记录总数
                self.cursor.execute(f"SELECT COUNT(*) as total FROM {table_name}")
                total = self.cursor.fetchone()['total']
                
                # 获取最新记录时间
                self.cursor.execute(f"SELECT MAX(created_time) as latest FROM {table_name}")
                latest = self.cursor.fetchone()['latest']
                
                # 获取最早记录时间
                self.cursor.execute(f"SELECT MIN(created_time) as earliest FROM {table_name}")
                earliest = self.cursor.fetchone()['earliest']
                
                return {
                    'table_name': table_name,
                    'total_records': total,
                    'latest_record': latest,
                    'earliest_record': earliest
                }
            else:
                # 获取所有表的统计信息
                all_stats = {}
                for table in self.tables:
                    # 递归调用自身获取单个表的统计信息
                    stats = self.get_table_stats(table)
                    all_stats[table] = stats
                
                return {
                    'message': '所有表的统计信息',
                    'table_count': len(all_stats),
                    'all_stats': all_stats
                }
                
        except Exception as e:
            raise
    
    def execute_custom_sql(self, sql: str, params: List[Any] = None, fetch_results: bool = True) -> Dict[str, Any]:
        """
        执行自定义SQL语句
        
        Args:
            sql: SQL语句
            params: SQL参数列表
            fetch_results: 是否获取查询结果（对于SELECT语句）
            
        Returns:
            执行结果字典，包含以下字段：
            - success: 是否执行成功
            - message: 执行消息
            - results: 查询结果（仅当fetch_results=True且为SELECT语句时）
            - affected_rows: 影响的行数（对于INSERT/UPDATE/DELETE语句）
            - last_insert_id: 最后插入的ID（对于INSERT语句）
        """
        if not sql or not sql.strip():
            return {
                "success": False,
                "message": "SQL语句不能为空",
                "results": None,
                "affected_rows": 0,
                "last_insert_id": None
            }
        
        # 安全检查：禁止某些危险操作
        sql_upper = sql.strip().upper()
        dangerous_keywords = ['DROP', 'TRUNCATE', 'ALTER TABLE', 'CREATE TABLE', 'CREATE INDEX']
        
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return {
                    "success": False,
                    "message": f"出于安全考虑，禁止执行包含 '{keyword}' 的SQL语句",
                    "results": None,
                    "affected_rows": 0,
                    "last_insert_id": None
                }
        
        try:
            # 执行SQL语句
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            
            result = {
                "success": True,
                "message": "SQL语句执行成功",
                "results": None,
                "affected_rows": self.cursor.rowcount,
                "last_insert_id": None
            }
            
            # 如果是查询语句且需要获取结果
            if fetch_results and sql_upper.startswith('SELECT'):
                rows = self.cursor.fetchall()
                results = []
                for row in rows:
                    record = dict(row)
                    # 尝试解析可能的JSON字段
                    for key, value in record.items():
                        if key == 'related' and value:
                            try:
                                record[key] = json.loads(value)
                            except (json.JSONDecodeError, TypeError):
                                pass  # 保持原值
                    results.append(record)
                result["results"] = results
                result["message"] = f"查询成功，返回 {len(results)} 条记录"
            
            # 如果是插入语句，获取最后插入的ID
            if sql_upper.startswith('INSERT'):
                result["last_insert_id"] = self.cursor.lastrowid
                result["message"] = f"插入成功，新记录ID: {result['last_insert_id']}"
            
            # 提交事务
            self.connection.commit()
            
            return result
            
        except Exception as e:
            # 回滚事务
            self.connection.rollback()
            return {
                "success": False,
                "message": f"SQL执行失败: {str(e)}",
                "results": None,
                "affected_rows": 0,
                "last_insert_id": None
            }
    
    def get_table_schema(self, table_name: str = None) -> Dict[str, Any]:
        """
        获取表结构信息
        
        Args:
            table_name: 表名（可选，不提供则获取所有表的结构）
            
        Returns:
            表结构信息字典
        """
        try:
            if table_name:
                if table_name not in self.tables:
                    return {
                        "success": False,
                        "message": f"无效的表名: {table_name}",
                        "schema": None
                    }
                
                # 获取单个表的结构
                self.cursor.execute(f"PRAGMA table_info({table_name})")
                columns = self.cursor.fetchall()
                
                schema_info = {
                    "table_name": table_name,
                    "columns": [dict(col) for col in columns]
                }
                
                return {
                    "success": True,
                    "message": f"成功获取表 {table_name} 的结构信息",
                    "schema": schema_info
                }
            else:
                # 获取所有表的结构
                all_schemas = {}
                for table in self.tables:
                    self.cursor.execute(f"PRAGMA table_info({table})")
                    columns = self.cursor.fetchall()
                    
                    all_schemas[table] = {
                        "table_name": table,
                        "columns": [dict(col) for col in columns]
                    }
                
                return {
                    "success": True,
                    "message": "成功获取所有表的结构信息",
                    "schema": all_schemas
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"获取表结构失败: {str(e)}",
                "schema": None
            }
    
    def close(self):
        """关闭数据库连接"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            pass
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


# 创建全局数据库实例
db_instance = None

def get_database() -> ProfileDatabase:
    """获取数据库实例（单例模式）"""
    global db_instance
    if db_instance is None:
        # 获取当前文件（database.py）的目录
        current_dir = Path(__file__).parent
        # 获取项目根目录（main.py所在目录）
        project_root = current_dir.parent
        # 构建数据库文件的绝对路径
        db_path = project_root / "profile_data.db"
        
        db_instance = ProfileDatabase(str(db_path))
    return db_instance
"""
数据库管理模块
Database Management Module

负责创建和管理个人画像数据结构的SQLite数据库
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            self._connect()
            self._create_tables()
            self._create_indexes()
            logger.info(f"数据库初始化成功: {db_path}")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    def _connect(self):
        """建立数据库连接"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # 启用字典式访问
            self.cursor = self.connection.cursor()
            logger.info("数据库连接建立成功")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise
    
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
                logger.info(f"表 {table_name} 创建成功")
            
            self.connection.commit()
            logger.info("所有数据表创建完成")
        except Exception as e:
            logger.error(f"创建数据表失败: {e}")
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
                
                logger.info(f"表 {table_name} 的索引创建成功")
            
            self.connection.commit()
            logger.info("所有索引创建完成")
        except Exception as e:
            logger.error(f"创建索引失败: {e}")
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
            logger.info(f"成功插入记录到表 {table_name}, ID: {record_id}")
            return record_id
            
        except Exception as e:
            logger.error(f"插入记录失败: {e}")
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
                logger.warning("没有提供要更新的字段")
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
                logger.info(f"成功更新表 {table_name} 中ID为 {record_id} 的记录")
                return True
            else:
                logger.warning(f"表 {table_name} 中未找到ID为 {record_id} 的记录")
                return False
                
        except Exception as e:
            logger.error(f"更新记录失败: {e}")
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
                logger.info(f"成功删除表 {table_name} 中ID为 {record_id} 的记录")
                return True
            else:
                logger.warning(f"表 {table_name} 中未找到ID为 {record_id} 的记录")
                return False
                
        except Exception as e:
            logger.error(f"删除记录失败: {e}")
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
            logger.error(f"获取记录失败: {e}")
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
            
            logger.info(f"在表 {table_name} 中搜索到 {len(records)} 条记录")
            return records
            
        except Exception as e:
            logger.error(f"搜索记录失败: {e}")
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
    
    def get_table_stats(self, table_name: str) -> Dict[str, Any]:
        """
        获取表统计信息
        
        Args:
            table_name: 表名
            
        Returns:
            统计信息字典
        """
        if table_name not in self.tables:
            raise ValueError(f"无效的表名: {table_name}")
        
        try:
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
            
        except Exception as e:
            logger.error(f"获取表统计信息失败: {e}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info("数据库连接已关闭")
        except Exception as e:
            logger.error(f"关闭数据库连接失败: {e}")
    
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
        db_instance = ProfileDatabase()
    return db_instance
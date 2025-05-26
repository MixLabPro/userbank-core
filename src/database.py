import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonalProfileDatabase:
    """个人画像数据库管理类"""
    
    def __init__(self, db_path: str = "personal_profile.db"):
        """
        初始化数据库连接
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self.init_database()
        logger.info(f"数据库初始化完成: {db_path}")
    
    def get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # 使查询结果可以通过列名访问
            return conn
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise
    
    def init_database(self):
        """初始化数据库表结构"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 创建信念表 (Belief)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS beliefs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        related TEXT NOT NULL,  -- JSON格式存储相关主题数组
                        emotion TEXT DEFAULT 'neutral',
                        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建洞察表 (Insight)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS insights (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        related TEXT NOT NULL,
                        emotion TEXT DEFAULT 'neutral',
                        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建关注点表 (Focus)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS focuses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        related TEXT NOT NULL,
                        emotion TEXT DEFAULT 'neutral',
                        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建长期目标表 (Long-term Goal)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS long_term_goals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        related TEXT NOT NULL,
                        emotion TEXT DEFAULT 'neutral',
                        status TEXT DEFAULT 'active',  -- active, completed, paused
                        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建短期目标表 (Short-term Goal)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS short_term_goals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        related TEXT NOT NULL,
                        emotion TEXT DEFAULT 'neutral',
                        status TEXT DEFAULT 'active',
                        deadline DATE,
                        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建偏好表 (Preference)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS preferences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        related TEXT NOT NULL,
                        emotion TEXT DEFAULT 'neutral',
                        strength INTEGER DEFAULT 5,  -- 偏好强度 1-10
                        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建决策表 (Decision)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS decisions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        related TEXT NOT NULL,
                        emotion TEXT DEFAULT 'neutral',
                        context TEXT,  -- 决策背景
                        outcome TEXT,  -- 决策结果
                        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建方法论表 (Methodology)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS methodologies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        related TEXT NOT NULL,
                        emotion TEXT DEFAULT 'neutral',
                        category TEXT,  -- 方法论分类
                        effectiveness INTEGER DEFAULT 5,  -- 有效性评分 1-10
                        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        update_time DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 创建索引以提高查询性能
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_beliefs_create_time ON beliefs(create_time)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_insights_create_time ON insights(create_time)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_focuses_create_time ON focuses(create_time)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_long_term_goals_create_time ON long_term_goals(create_time)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_short_term_goals_create_time ON short_term_goals(create_time)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_preferences_create_time ON preferences(create_time)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_decisions_create_time ON decisions(create_time)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_methodologies_create_time ON methodologies(create_time)')
                
                conn.commit()
                logger.info("数据库表结构创建成功")
                
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise
    
    def _format_related(self, related: List[str]) -> str:
        """将相关主题列表转换为JSON字符串"""
        return json.dumps(related, ensure_ascii=False)
    
    def _parse_related(self, related_str: str) -> List[str]:
        """将JSON字符串转换为相关主题列表"""
        try:
            return json.loads(related_str)
        except:
            return []
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """将数据库行转换为字典"""
        result = dict(row)
        if 'related' in result:
            result['related'] = self._parse_related(result['related'])
        return result
    
    # 通用的CRUD操作方法
    def insert_record(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        插入记录到指定表
        
        Args:
            table_name: 表名
            data: 要插入的数据字典
            
        Returns:
            插入记录的ID
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 处理related字段
                if 'related' in data and isinstance(data['related'], list):
                    data['related'] = self._format_related(data['related'])
                
                # 构建插入SQL
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['?' for _ in data])
                sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                cursor.execute(sql, list(data.values()))
                record_id = cursor.lastrowid
                
                logger.info(f"成功插入记录到 {table_name} 表，ID: {record_id}")
                return record_id
                
        except Exception as e:
            logger.error(f"插入记录失败: {e}")
            raise
    
    def get_records(self, table_name: str, limit: int = 100, offset: int = 0, 
                   order_by: str = "create_time DESC") -> List[Dict[str, Any]]:
        """
        获取表中的记录
        
        Args:
            table_name: 表名
            limit: 限制返回记录数
            offset: 偏移量
            order_by: 排序字段
            
        Returns:
            记录列表
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                sql = f"SELECT * FROM {table_name} ORDER BY {order_by} LIMIT ? OFFSET ?"
                cursor.execute(sql, (limit, offset))
                
                rows = cursor.fetchall()
                records = [self._row_to_dict(row) for row in rows]
                
                logger.info(f"从 {table_name} 表获取到 {len(records)} 条记录")
                return records
                
        except Exception as e:
            logger.error(f"获取记录失败: {e}")
            raise
    
    def search_records(self, table_name: str, keyword: str, 
                      limit: int = 50) -> List[Dict[str, Any]]:
        """
        在指定表中搜索包含关键词的记录
        
        Args:
            table_name: 表名
            keyword: 搜索关键词
            limit: 限制返回记录数
            
        Returns:
            匹配的记录列表
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                sql = f"""
                    SELECT * FROM {table_name} 
                    WHERE content LIKE ? OR related LIKE ?
                    ORDER BY create_time DESC 
                    LIMIT ?
                """
                search_term = f"%{keyword}%"
                cursor.execute(sql, (search_term, search_term, limit))
                
                rows = cursor.fetchall()
                records = [self._row_to_dict(row) for row in rows]
                
                logger.info(f"在 {table_name} 表中搜索 '{keyword}' 找到 {len(records)} 条记录")
                return records
                
        except Exception as e:
            logger.error(f"搜索记录失败: {e}")
            raise
    
    def update_record(self, table_name: str, record_id: int, 
                     data: Dict[str, Any]) -> bool:
        """
        更新指定记录
        
        Args:
            table_name: 表名
            record_id: 记录ID
            data: 要更新的数据
            
        Returns:
            是否更新成功
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 处理related字段
                if 'related' in data and isinstance(data['related'], list):
                    data['related'] = self._format_related(data['related'])
                
                # 添加更新时间
                data['update_time'] = datetime.now().isoformat()
                
                # 构建更新SQL
                set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
                sql = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
                
                cursor.execute(sql, list(data.values()) + [record_id])
                success = cursor.rowcount > 0
                
                if success:
                    logger.info(f"成功更新 {table_name} 表中ID为 {record_id} 的记录")
                else:
                    logger.warning(f"未找到 {table_name} 表中ID为 {record_id} 的记录")
                
                return success
                
        except Exception as e:
            logger.error(f"更新记录失败: {e}")
            raise
    
    def delete_record(self, table_name: str, record_id: int) -> bool:
        """
        删除指定记录
        
        Args:
            table_name: 表名
            record_id: 记录ID
            
        Returns:
            是否删除成功
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                sql = f"DELETE FROM {table_name} WHERE id = ?"
                cursor.execute(sql, (record_id,))
                success = cursor.rowcount > 0
                
                if success:
                    logger.info(f"成功删除 {table_name} 表中ID为 {record_id} 的记录")
                else:
                    logger.warning(f"未找到 {table_name} 表中ID为 {record_id} 的记录")
                
                return success
                
        except Exception as e:
            logger.error(f"删除记录失败: {e}")
            raise
    
    def get_statistics(self) -> Dict[str, int]:
        """
        获取数据库统计信息
        
        Returns:
            各表的记录数统计
        """
        try:
            tables = [
                'beliefs', 'insights', 'focuses', 'long_term_goals',
                'short_term_goals', 'preferences', 'decisions', 'methodologies'
            ]
            
            stats = {}
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    stats[table] = count
                
                logger.info(f"数据库统计信息: {stats}")
                return stats
                
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            raise 
"""
数据库管理模块
Database Management Module

负责创建和管理个人画像数据结构的SQLite数据库
基于database 0.3.md文档的完整实现
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Union
from pathlib import Path
import os

class ProfileDatabase:
    """个人画像数据库管理类"""
    
    def __init__(self, db_path: str = None):
        """
        初始化数据库连接
        
        Args:
            db_path: 数据库文件路径，如果为None则使用main.py同目录下的profile_data.db
        """
        if db_path is None:
            # 获取当前文件所在目录的上级目录（即main.py所在目录）
            current_dir = Path(__file__).parent.parent
            self.db_path = str(current_dir / "profile_data.db")
        else:
            self.db_path = db_path
        self.connection = None
        self.cursor = None
        
        # 定义所有表名和中文描述（基于database 0.3.md）
        self.tables = {
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
        
        try:
            # 检查数据库文件是否存在
            db_exists = Path(self.db_path).exists()
            
            self._connect()
            
            # 只有在数据库文件不存在或表不存在时才创建表
            if not db_exists or not self._check_tables_exist():
                self._create_tables()
                self._create_indexes()
                self._init_default_data()
            
        except Exception as e:
            raise
    
    def _connect(self):
        """建立数据库连接"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # 启用字典式访问
            self.cursor = self.connection.cursor()
            # 启用外键约束
            self.cursor.execute("PRAGMA foreign_keys = ON")
        except Exception as e:
            raise
    
    def _check_tables_exist(self) -> bool:
        """
        检查所有必需的表是否存在
        
        Returns:
            如果所有表都存在返回True，否则返回False
        """
        try:
            for table_name in self.tables.keys():
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
        """创建所有数据表（基于database 0.3.md）"""
        try:
            # 1. Persona（人物档案表）- 系统核心
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS persona (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    gender TEXT,
                    personality TEXT,
                    avatar_url TEXT,
                    bio TEXT,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 2. Category（分类体系表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS category (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_level TEXT NOT NULL,
                    second_level TEXT NOT NULL,
                    description TEXT,
                    is_active BOOLEAN DEFAULT true,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 3. Relations（通用关联表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS relations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_table TEXT NOT NULL,
                    source_id INTEGER NOT NULL,
                    target_table TEXT NOT NULL,
                    target_id INTEGER NOT NULL,
                    relation_type TEXT NOT NULL,
                    strength TEXT CHECK(strength IN ('strong', 'medium', 'weak')),
                    note TEXT,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 4. Viewpoint（观点表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS viewpoint (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    source_people TEXT,
                    keywords TEXT,
                    source_app TEXT DEFAULT 'unknown',
                    related_event TEXT,
                    reference_urls TEXT,
                    category_id INTEGER,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 5. Insight（洞察表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS insight (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    source_people TEXT,
                    keywords TEXT,
                    source_app TEXT DEFAULT 'unknown',
                    category_id INTEGER,
                    reference_urls TEXT,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 6. Focus（关注点表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS focus (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    priority INTEGER CHECK(priority >= 1 AND priority <= 10),
                    status TEXT CHECK(status IN ('active', 'paused', 'completed')),
                    context TEXT,
                    keywords TEXT,
                    source_app TEXT DEFAULT 'unknown',
                    category_id INTEGER,
                    deadline DATE,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 7. Goal（目标表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS goal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    type TEXT CHECK(type IN ('long_term', 'short_term', 'plan', 'todo')),
                    deadline DATE,
                    status TEXT CHECK(status IN ('planning', 'in_progress', 'completed', 'abandoned')),
                    keywords TEXT,
                    source_app TEXT DEFAULT 'unknown',
                    category_id INTEGER,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 8. Preference（偏好表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS preference (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    context TEXT,
                    keywords TEXT,
                    source_app TEXT DEFAULT 'unknown',
                    category_id INTEGER,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 9. Methodology（方法论表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS methodology (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    type TEXT,
                    effectiveness TEXT CHECK(effectiveness IN ('proven', 'experimental', 'theoretical')),
                    use_cases TEXT,
                    keywords TEXT,
                    source_app TEXT DEFAULT 'unknown',
                    reference_urls TEXT,
                    category_id INTEGER,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 10. Prediction（预测表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS prediction (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    timeframe TEXT,
                    basis TEXT,
                    verification_status TEXT CHECK(verification_status IN ('pending', 'correct', 'incorrect', 'partial')),
                    keywords TEXT,
                    source_app TEXT DEFAULT 'unknown',
                    reference_urls TEXT,
                    category_id INTEGER,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 11. Memory（记忆表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    memory_type TEXT CHECK(memory_type IN ('experience', 'event', 'learning', 'interaction', 'achievement', 'mistake')),
                    importance INTEGER CHECK(importance >= 1 AND importance <= 10),
                    related_people TEXT,
                    location TEXT,
                    memory_date DATE,
                    keywords TEXT,
                    source_app TEXT DEFAULT 'unknown',
                    reference_urls TEXT,
                    category_id INTEGER,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            self.connection.commit()
            
        except Exception as e:
            self.connection.rollback()
            raise
    
    def _create_indexes(self):
        """创建索引（基于database 0.3.md）"""
        try:
            # Persona表索引
            self.cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_persona_id ON persona(id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_persona_privacy ON persona(privacy_level)")
            
            # Category表索引
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_category_levels ON category(first_level, second_level)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_category_active ON category(is_active)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_category_privacy ON category(privacy_level)")
            
            # Relations表索引
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_source ON relations(source_table, source_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_target ON relations(target_table, target_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_type ON relations(relation_type)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_privacy ON relations(privacy_level)")
            
            # Viewpoint表索引
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_viewpoint_source_people ON viewpoint(source_people)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_viewpoint_source_app ON viewpoint(source_app)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_viewpoint_category ON viewpoint(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_viewpoint_privacy ON viewpoint(privacy_level)")
            
            # Insight表索引
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_insight_source_people ON insight(source_people)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_insight_source_app ON insight(source_app)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_insight_category ON insight(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_insight_time ON insight(created_time)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_insight_privacy ON insight(privacy_level)")
            
            # Focus表索引
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_focus_priority ON focus(priority)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_focus_status ON focus(status)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_focus_deadline ON focus(deadline)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_focus_category ON focus(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_focus_privacy ON focus(privacy_level)")
            
            # Goal表索引
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_goal_type ON goal(type)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_goal_status ON goal(status)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_goal_deadline ON goal(deadline)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_goal_category ON goal(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_goal_privacy ON goal(privacy_level)")
            
            # Preference表索引
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_preference_category ON preference(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_preference_privacy ON preference(privacy_level)")
            
            # Methodology表索引
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_methodology_type ON methodology(type)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_methodology_effectiveness ON methodology(effectiveness)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_methodology_category ON methodology(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_methodology_privacy ON methodology(privacy_level)")
            
            # Prediction表索引
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_prediction_timeframe ON prediction(timeframe)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_prediction_verification ON prediction(verification_status)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_prediction_category ON prediction(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_prediction_privacy ON prediction(privacy_level)")
            
            # Memory表索引
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_type ON memory(memory_type)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_importance ON memory(importance)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_date ON memory(memory_date)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_category ON memory(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_privacy ON memory(privacy_level)")
            
            self.connection.commit()
            
        except Exception as e:
            self.connection.rollback()
            raise
    
    def _init_default_data(self):
        """初始化默认数据"""
        try:
            # 检查是否已有persona记录
            self.cursor.execute("SELECT COUNT(*) FROM persona")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                # 插入默认的persona记录（ID固定为1）
                self.cursor.execute("""
                    INSERT INTO persona (id, name, gender, personality, bio, privacy_level)
                    VALUES (1, '用户', '未设置', '待完善', '个人画像待完善', 'private')
                """)
            
            # 插入一些默认分类
            default_categories = [
                ('技术', '编程开发', '软件开发相关技术'),
                ('技术', '系统架构', '系统设计和架构'),
                ('生活', '人际关系', '人际交往和关系管理'),
                ('生活', '健康管理', '身体和心理健康'),
                ('商业', '投资理财', '投资和财务管理'),
                ('商业', '创业管理', '创业和企业管理'),
                ('学习', '知识管理', '知识获取和管理'),
                ('学习', '技能提升', '个人技能发展')
            ]
            
            for first_level, second_level, description in default_categories:
                # 检查是否已存在
                self.cursor.execute("""
                    SELECT COUNT(*) FROM category 
                    WHERE first_level = ? AND second_level = ?
                """, (first_level, second_level))
                
                if self.cursor.fetchone()[0] == 0:
                    self.cursor.execute("""
                        INSERT INTO category (first_level, second_level, description)
                        VALUES (?, ?, ?)
                    """, (first_level, second_level, description))
            
            self.connection.commit()
            
        except Exception as e:
            self.connection.rollback()
            raise
    
    def insert_record(self, table_name: str, **kwargs) -> int:
        """
        插入记录到指定表
        
        Args:
            table_name: 表名
            **kwargs: 字段值
            
        Returns:
            插入记录的ID
        """
        try:
            if table_name not in self.tables:
                raise ValueError(f"未知的表名: {table_name}")
            
            # 处理JSON字段
            if 'keywords' in kwargs and isinstance(kwargs['keywords'], list):
                kwargs['keywords'] = json.dumps(kwargs['keywords'], ensure_ascii=False)
            if 'reference_urls' in kwargs and isinstance(kwargs['reference_urls'], list):
                kwargs['reference_urls'] = json.dumps(kwargs['reference_urls'], ensure_ascii=False)
            
            # 构建SQL语句
            fields = list(kwargs.keys())
            placeholders = ['?' for _ in fields]
            values = list(kwargs.values())
            
            sql = f"""
                INSERT INTO {table_name} ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
            """
            
            self.cursor.execute(sql, values)
            self.connection.commit()
            
            return self.cursor.lastrowid
            
        except Exception as e:
            self.connection.rollback()
            raise
    
    def update_record(self, table_name: str, record_id: int, **kwargs) -> bool:
        """
        更新指定记录
        
        Args:
            table_name: 表名
            record_id: 记录ID
            **kwargs: 要更新的字段值
            
        Returns:
            是否更新成功
        """
        try:
            if table_name not in self.tables:
                raise ValueError(f"未知的表名: {table_name}")
            
            if not kwargs:
                return True
            
            # 处理JSON字段
            if 'keywords' in kwargs and isinstance(kwargs['keywords'], list):
                kwargs['keywords'] = json.dumps(kwargs['keywords'], ensure_ascii=False)
            if 'reference_urls' in kwargs and isinstance(kwargs['reference_urls'], list):
                kwargs['reference_urls'] = json.dumps(kwargs['reference_urls'], ensure_ascii=False)
            
            # 添加更新时间
            kwargs['updated_time'] = datetime.now().isoformat()
            
            # 构建SQL语句
            set_clauses = [f"{field} = ?" for field in kwargs.keys()]
            values = list(kwargs.values()) + [record_id]
            
            sql = f"""
                UPDATE {table_name}
                SET {', '.join(set_clauses)}
                WHERE id = ?
            """
            
            self.cursor.execute(sql, values)
            self.connection.commit()
            
            return self.cursor.rowcount > 0
            
        except Exception as e:
            self.connection.rollback()
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
            if table_name not in self.tables:
                raise ValueError(f"未知的表名: {table_name}")
            
            self.cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (record_id,))
            self.connection.commit()
            
            return self.cursor.rowcount > 0
            
        except Exception as e:
            self.connection.rollback()
            raise
    
    def get_record(self, table_name: str, record_id: int) -> Optional[Dict[str, Any]]:
        """
        获取指定记录
        
        Args:
            table_name: 表名
            record_id: 记录ID
            
        Returns:
            记录数据字典，如果不存在返回None
        """
        try:
            if table_name not in self.tables:
                raise ValueError(f"未知的表名: {table_name}")
            
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (record_id,))
            row = self.cursor.fetchone()
            
            if row:
                result = dict(row)
                # 解析JSON字段
                if 'keywords' in result and result['keywords']:
                    try:
                        result['keywords'] = json.loads(result['keywords'])
                    except:
                        result['keywords'] = []
                if 'reference_urls' in result and result['reference_urls']:
                    try:
                        result['reference_urls'] = json.loads(result['reference_urls'])
                    except:
                        result['reference_urls'] = []
                return result
            
            return None
            
        except Exception as e:
            raise
    
    def query_records(self, table_name: str, filter_conditions: Dict[str, Any] = None, 
                     sort_by: str = 'created_time', sort_order: str = 'desc', 
                     limit: int = 20, offset: int = 0) -> Tuple[List[Dict[str, Any]], int]:
        """
        查询记录（支持复杂筛选条件）
        
        Args:
            table_name: 表名
            filter_conditions: 筛选条件字典
            sort_by: 排序字段
            sort_order: 排序顺序 ('asc' 或 'desc')
            limit: 返回记录数限制
            offset: 偏移量
            
        Returns:
            (记录列表, 总记录数) 元组
        """
        try:
            if table_name not in self.tables:
                raise ValueError(f"未知的表名: {table_name}")
            
            # 构建WHERE子句
            where_clauses = []
            params = []
            
            if filter_conditions:
                for key, value in filter_conditions.items():
                    if value is None:
                        continue
                        
                    if key == 'ids':
                        # ID列表筛选
                        placeholders = ','.join(['?' for _ in value])
                        where_clauses.append(f"id IN ({placeholders})")
                        params.extend(value)
                    elif key.endswith('_contains'):
                        # 包含文本筛选
                        field = key.replace('_contains', '')
                        where_clauses.append(f"{field} LIKE ?")
                        params.append(f"%{value}%")
                    elif key.endswith('_in'):
                        # 列表筛选
                        field = key.replace('_in', '')
                        placeholders = ','.join(['?' for _ in value])
                        where_clauses.append(f"{field} IN ({placeholders})")
                        params.extend(value)
                    elif key.endswith('_is'):
                        # 精确匹配
                        field = key.replace('_is', '')
                        where_clauses.append(f"{field} = ?")
                        params.append(value)
                    elif key.endswith('_gte'):
                        # 大于等于
                        field = key.replace('_gte', '')
                        where_clauses.append(f"{field} >= ?")
                        params.append(value)
                    elif key.endswith('_lte'):
                        # 小于等于
                        field = key.replace('_lte', '')
                        where_clauses.append(f"{field} <= ?")
                        params.append(value)
                    elif key.endswith('_from'):
                        # 日期范围起始
                        field = key.replace('_from', '')
                        where_clauses.append(f"{field} >= ?")
                        params.append(value)
                    elif key.endswith('_to'):
                        # 日期范围结束
                        field = key.replace('_to', '')
                        where_clauses.append(f"{field} <= ?")
                        params.append(value)
                    elif key == 'keywords_contain_any':
                        # 关键词包含任意一个
                        keyword_conditions = []
                        for keyword in value:
                            keyword_conditions.append("keywords LIKE ?")
                            params.append(f'%"{keyword}"%')
                        where_clauses.append(f"({' OR '.join(keyword_conditions)})")
                    elif key == 'keywords_contain_all':
                        # 关键词包含所有
                        for keyword in value:
                            where_clauses.append("keywords LIKE ?")
                            params.append(f'%"{keyword}"%')
            
            # 构建完整SQL
            where_sql = ""
            if where_clauses:
                where_sql = f"WHERE {' AND '.join(where_clauses)}"
            
            # 获取总记录数
            count_sql = f"SELECT COUNT(*) FROM {table_name} {where_sql}"
            self.cursor.execute(count_sql, params)
            total_count = self.cursor.fetchone()[0]
            
            # 获取记录
            order_sql = f"ORDER BY {sort_by} {sort_order.upper()}"
            limit_sql = f"LIMIT {limit} OFFSET {offset}"
            
            query_sql = f"SELECT * FROM {table_name} {where_sql} {order_sql} {limit_sql}"
            self.cursor.execute(query_sql, params)
            
            rows = self.cursor.fetchall()
            records = []
            
            for row in rows:
                record = dict(row)
                # 解析JSON字段
                if 'keywords' in record and record['keywords']:
                    try:
                        record['keywords'] = json.loads(record['keywords'])
                    except:
                        record['keywords'] = []
                if 'reference_urls' in record and record['reference_urls']:
                    try:
                        record['reference_urls'] = json.loads(record['reference_urls'])
                    except:
                        record['reference_urls'] = []
                records.append(record)
            
            return records, total_count
            
        except Exception as e:
            raise
    
    def get_persona(self) -> Optional[Dict[str, Any]]:
        """获取用户画像（ID固定为1）"""
        return self.get_record('persona', 1)
    
    def update_persona(self, **kwargs) -> bool:
        """更新用户画像"""
        return self.update_record('persona', 1, **kwargs)
    
    def get_categories(self, first_level: str = None) -> List[Dict[str, Any]]:
        """获取分类列表"""
        try:
            if first_level:
                self.cursor.execute("SELECT * FROM category WHERE first_level = ? AND is_active = 1", (first_level,))
            else:
                self.cursor.execute("SELECT * FROM category WHERE is_active = 1")
            
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            raise
    
    def add_relation(self, source_table: str, source_id: int, target_table: str, 
                    target_id: int, relation_type: str, strength: str = 'medium', 
                    note: str = None) -> int:
        """添加关联关系"""
        try:
            return self.insert_record('relations',
                                    source_table=source_table,
                                    source_id=source_id,
                                    target_table=target_table,
                                    target_id=target_id,
                                    relation_type=relation_type,
                                    strength=strength,
                                    note=note)
        except Exception as e:
            raise
    
    def get_relations(self, table_name: str, record_id: int, 
                     relation_type: str = None) -> List[Dict[str, Any]]:
        """获取关联关系"""
        try:
            if relation_type:
                self.cursor.execute("""
                    SELECT * FROM relations 
                    WHERE (source_table = ? AND source_id = ?) OR (target_table = ? AND target_id = ?)
                    AND relation_type = ?
                """, (table_name, record_id, table_name, record_id, relation_type))
            else:
                self.cursor.execute("""
                    SELECT * FROM relations 
                    WHERE (source_table = ? AND source_id = ?) OR (target_table = ? AND target_id = ?)
                """, (table_name, record_id, table_name, record_id))
            
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            raise
    
    def execute_custom_sql(self, sql: str, params: List[Any] = None, fetch_results: bool = True) -> Dict[str, Any]:
        """
        执行自定义SQL语句
        
        Args:
            sql: SQL语句
            params: 参数列表
            fetch_results: 是否获取结果
            
        Returns:
            执行结果字典
        """
        try:
            if params is None:
                params = []
            
            # 安全检查：只允许SELECT、INSERT、UPDATE、DELETE语句
            sql_upper = sql.strip().upper()
            allowed_operations = ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
            
            if not any(sql_upper.startswith(op) for op in allowed_operations):
                raise ValueError("只允许执行SELECT、INSERT、UPDATE、DELETE语句")
            
            # 禁止某些危险操作
            dangerous_keywords = ['DROP', 'ALTER', 'CREATE', 'TRUNCATE', 'REPLACE']
            if any(keyword in sql_upper for keyword in dangerous_keywords):
                raise ValueError("禁止执行可能危险的SQL操作")
            
            self.cursor.execute(sql, params)
            
            result = {
                "success": True,
                "rowcount": self.cursor.rowcount,
                "lastrowid": self.cursor.lastrowid,
                "data": None
            }
            
            if fetch_results and sql_upper.startswith('SELECT'):
                rows = self.cursor.fetchall()
                result["data"] = [dict(row) for row in rows]
                result["count"] = len(result["data"])
            
            # 如果是修改操作，提交事务
            if sql_upper.startswith(('INSERT', 'UPDATE', 'DELETE')):
                self.connection.commit()
            
            return result
            
        except Exception as e:
            if sql.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                self.connection.rollback()
            
            return {
                "success": False,
                "error": str(e),
                "rowcount": 0,
                "lastrowid": None,
                "data": None
            }
    
    def get_table_schema(self, table_name: str = None) -> Dict[str, Any]:
        """
        获取表结构信息
        
        Args:
            table_name: 表名，如果为None则返回所有表的结构
            
        Returns:
            表结构信息字典
        """
        try:
            if table_name:
                if table_name not in self.tables:
                    raise ValueError(f"未知的表名: {table_name}")
                
                # 获取指定表的结构
                self.cursor.execute(f"PRAGMA table_info({table_name})")
                columns = self.cursor.fetchall()
                
                return {
                    "table_name": table_name,
                    "description": self.tables[table_name],
                    "columns": [
                        {
                            "name": col[1],
                            "type": col[2],
                            "not_null": bool(col[3]),
                            "default_value": col[4],
                            "primary_key": bool(col[5])
                        }
                        for col in columns
                    ]
                }
            else:
                # 获取所有表的结构
                schemas = {}
                for table_name, description in self.tables.items():
                    self.cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = self.cursor.fetchall()
                    
                    schemas[table_name] = {
                        "description": description,
                        "columns": [
                            {
                                "name": col[1],
                                "type": col[2],
                                "not_null": bool(col[3]),
                                "default_value": col[4],
                                "primary_key": bool(col[5])
                            }
                            for col in columns
                        ]
                    }
                
                return {
                    "all_tables": schemas,
                    "table_count": len(schemas)
                }
                
        except Exception as e:
            raise
    
    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()

# 全局数据库实例
_database_instance = None

def get_database() -> ProfileDatabase:
    """获取数据库实例（单例模式）"""
    global _database_instance
    if _database_instance is None:
        _database_instance = ProfileDatabase()
    return _database_instance
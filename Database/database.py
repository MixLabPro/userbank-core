"""
数据库管理模块
Database Management Module

负责创建和管理个人画像数据结构的SQLite数据库
基于database.md文档的完整实现
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Union
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
        
        # 定义所有表名和中文描述
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
            'decision': '决策',
            'methodology': '方法论',
            'experience': '经验',
            'prediction': '预测'
        }
        
        try:
            # 检查数据库文件是否存在
            db_exists = Path(db_path).exists()
            
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
        """创建所有数据表"""
        try:
            # 1. Persona（人物档案表）- 系统核心
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS persona (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    name TEXT NOT NULL,
                    gender TEXT CHECK (gender IN ('male', 'female', 'other')),
                    personality TEXT,
                    avatar_url TEXT,
                    bio TEXT,
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 2. Category（分类体系表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS category (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_level TEXT NOT NULL,
                    second_level TEXT,
                    description TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(first_level, second_level)
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
                    relation_type TEXT NOT NULL CHECK (relation_type IN (
                        'inspired_by', 'conflicts_with', 'supports', 'leads_to', 
                        'based_on', 'similar_to', 'opposite_to', 'caused_by'
                    )),
                    strength TEXT DEFAULT 'medium' CHECK (strength IN ('strong', 'medium', 'weak')),
                    note TEXT,
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 4. Viewpoint（观点表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS viewpoint (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    stance INTEGER CHECK (stance BETWEEN -5 AND 5),  -- -5强烈反对到5强烈支持
                    source TEXT,
                    persona_id INTEGER DEFAULT 1,
                    time_period TEXT,
                    reference_urls TEXT,  -- JSON格式存储URL数组
                    category_id INTEGER,
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (persona_id) REFERENCES persona(id),
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 5. Insight（洞察表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS insight (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    trigger_event TEXT,
                    impact_level TEXT DEFAULT 'medium' CHECK (impact_level IN ('high', 'medium', 'low')),
                    category_id INTEGER,
                    reference_urls TEXT,  -- JSON格式存储URL数组
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
                    priority INTEGER CHECK (priority BETWEEN 1 AND 10),
                    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed')),
                    context TEXT,
                    category_id INTEGER,
                    deadline DATE,
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
                    type TEXT NOT NULL CHECK (type IN ('long_term', 'short_term')),
                    deadline DATE,
                    progress INTEGER DEFAULT 0 CHECK (progress BETWEEN 0 AND 100),
                    status TEXT DEFAULT 'planning' CHECK (status IN ('planning', 'in_progress', 'completed', 'abandoned')),
                    category_id INTEGER,
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
                    strength TEXT DEFAULT 'moderate' CHECK (strength IN ('strong', 'moderate', 'flexible')),
                    context TEXT,
                    category_id INTEGER,
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 9. Decision（决策表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS decision (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    reasoning TEXT,
                    outcome TEXT,
                    domain TEXT,
                    category_id INTEGER,
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 10. Methodology（方法论表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS methodology (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    type TEXT,
                    effectiveness TEXT DEFAULT 'experimental' CHECK (effectiveness IN ('proven', 'experimental', 'theoretical')),
                    use_cases TEXT,
                    persona_id INTEGER DEFAULT 1,
                    category_id INTEGER,
                    reference_urls TEXT,  -- JSON格式存储URL数组
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (persona_id) REFERENCES persona(id),
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 11. Experience（经验表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS experience (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    field TEXT NOT NULL,
                    expertise_level TEXT DEFAULT 'beginner' CHECK (expertise_level IN ('expert', 'proficient', 'intermediate', 'beginner')),
                    years INTEGER DEFAULT 0,
                    key_learnings TEXT,
                    category_id INTEGER,
                    reference_urls TEXT,  -- JSON格式存储URL数组
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 12. Prediction（预测表）
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS prediction (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    timeframe TEXT,
                    basis TEXT,
                    verification_status TEXT DEFAULT 'pending' CHECK (verification_status IN ('correct', 'incorrect', 'pending', 'partially_correct')),
                    reference_urls TEXT,  -- JSON格式存储URL数组
                    category_id INTEGER,
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
        """创建数据库索引以提升查询性能"""
        try:
            # 为主要查询字段创建索引
            indexes = [
                # Category表索引
                "CREATE INDEX IF NOT EXISTS idx_category_first_level ON category(first_level)",
                "CREATE INDEX IF NOT EXISTS idx_category_second_level ON category(second_level)",
                
                # Relations表索引
                "CREATE INDEX IF NOT EXISTS idx_relations_source ON relations(source_table, source_id)",
                "CREATE INDEX IF NOT EXISTS idx_relations_target ON relations(target_table, target_id)",
                "CREATE INDEX IF NOT EXISTS idx_relations_type ON relations(relation_type)",
                
                # Viewpoint表索引
                "CREATE INDEX IF NOT EXISTS idx_viewpoint_subject ON viewpoint(subject)",
                "CREATE INDEX IF NOT EXISTS idx_viewpoint_time_period ON viewpoint(time_period)",
                "CREATE INDEX IF NOT EXISTS idx_viewpoint_category ON viewpoint(category_id)",
                
                # Insight表索引
                "CREATE INDEX IF NOT EXISTS idx_insight_impact_level ON insight(impact_level)",
                "CREATE INDEX IF NOT EXISTS idx_insight_category ON insight(category_id)",
                
                # Focus表索引
                "CREATE INDEX IF NOT EXISTS idx_focus_status ON focus(status)",
                "CREATE INDEX IF NOT EXISTS idx_focus_priority ON focus(priority)",
                "CREATE INDEX IF NOT EXISTS idx_focus_deadline ON focus(deadline)",
                
                # Goal表索引
                "CREATE INDEX IF NOT EXISTS idx_goal_type ON goal(type)",
                "CREATE INDEX IF NOT EXISTS idx_goal_status ON goal(status)",
                "CREATE INDEX IF NOT EXISTS idx_goal_deadline ON goal(deadline)",
                
                # Decision表索引
                "CREATE INDEX IF NOT EXISTS idx_decision_domain ON decision(domain)",
                
                # Experience表索引
                "CREATE INDEX IF NOT EXISTS idx_experience_field ON experience(field)",
                "CREATE INDEX IF NOT EXISTS idx_experience_expertise ON experience(expertise_level)",
                
                # 通用时间索引
                "CREATE INDEX IF NOT EXISTS idx_viewpoint_created_time ON viewpoint(created_time)",
                "CREATE INDEX IF NOT EXISTS idx_insight_created_time ON insight(created_time)",
                "CREATE INDEX IF NOT EXISTS idx_focus_created_time ON focus(created_time)",
                "CREATE INDEX IF NOT EXISTS idx_goal_created_time ON goal(created_time)",
                "CREATE INDEX IF NOT EXISTS idx_preference_created_time ON preference(created_time)",
                "CREATE INDEX IF NOT EXISTS idx_decision_created_time ON decision(created_time)",
                "CREATE INDEX IF NOT EXISTS idx_methodology_created_time ON methodology(created_time)",
                "CREATE INDEX IF NOT EXISTS idx_experience_created_time ON experience(created_time)",
                "CREATE INDEX IF NOT EXISTS idx_prediction_created_time ON prediction(created_time)"
            ]
            
            for index_sql in indexes:
                self.cursor.execute(index_sql)
            
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise
    
    def _init_default_data(self):
        """初始化默认数据"""
        try:
            # 创建默认persona记录
            self.cursor.execute("""
                INSERT OR IGNORE INTO persona (id, name, gender, personality, bio)
                VALUES (1, '用户', 'other', '待完善', '个人画像系统用户')
            """)
            
            # 创建默认分类
            default_categories = [
                ('技术', '编程开发', '软件开发相关技术'),
                ('技术', '系统架构', '系统设计和架构'),
                ('技术', '数据科学', '数据分析和机器学习'),
                ('生活', '健康管理', '身体健康和运动'),
                ('生活', '人际关系', '社交和人际交往'),
                ('生活', '时间管理', '效率和时间规划'),
                ('商业', '投资理财', '财务管理和投资'),
                ('商业', '创业', '创业和商业机会'),
                ('商业', '职业发展', '职业规划和发展'),
                ('个人成长', '学习方法', '学习技巧和方法'),
                ('个人成长', '思维模式', '思维方式和认知'),
                ('个人成长', '目标管理', '目标设定和达成')
            ]
            
            for first_level, second_level, description in default_categories:
                self.cursor.execute("""
                    INSERT OR IGNORE INTO category (first_level, second_level, description)
                    VALUES (?, ?, ?)
                """, (first_level, second_level, description))
            
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise
    
    # 通用CRUD操作
    def insert_record(self, table_name: str, **kwargs) -> int:
        """
        插入新记录
        
        Args:
            table_name: 表名
            **kwargs: 字段值
            
        Returns:
            新插入记录的ID
        """
        if table_name not in self.tables:
            raise ValueError(f"无效的表名: {table_name}")
        
        try:
            # 处理JSON字段
            json_fields = ['reference_urls']
            for field in json_fields:
                if field in kwargs and isinstance(kwargs[field], list):
                    kwargs[field] = json.dumps(kwargs[field], ensure_ascii=False)
            
            # 添加时间戳
            current_time = datetime.now().isoformat()
            kwargs['created_time'] = current_time
            kwargs['updated_time'] = current_time
            
            # 构建SQL
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
        更新记录
        
        Args:
            table_name: 表名
            record_id: 记录ID
            **kwargs: 要更新的字段值
            
        Returns:
            是否更新成功
        """
        if table_name not in self.tables:
            raise ValueError(f"无效的表名: {table_name}")
        
        try:
            if not kwargs:
                return False
            
            # 处理JSON字段
            json_fields = ['reference_urls']
            for field in json_fields:
                if field in kwargs and isinstance(kwargs[field], list):
                    kwargs[field] = json.dumps(kwargs[field], ensure_ascii=False)
            
            # 添加更新时间
            kwargs['updated_time'] = datetime.now().isoformat()
            
            # 构建SQL
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
            
            return self.cursor.rowcount > 0
                
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
                # 解析JSON格式的字段
                json_fields = ['reference_urls']
                for field in json_fields:
                    if field in record and record[field]:
                        try:
                            record[field] = json.loads(record[field])
                        except (json.JSONDecodeError, TypeError):
                            record[field] = []
                    elif field in record:
                        record[field] = []
                return record
            else:
                return None
                
        except Exception as e:
            raise
    
    def search_records(self, table_name: str, **kwargs) -> List[Dict[str, Any]]:
        """
        搜索记录
        
        Args:
            table_name: 表名
            **kwargs: 搜索条件，支持：
                - keyword: 内容关键词
                - category_id: 分类ID
                - status: 状态
                - type: 类型
                - limit: 返回记录数限制
                - offset: 偏移量
                - order_by: 排序字段
                - order_desc: 是否降序
            
        Returns:
            记录列表
        """
        if table_name not in self.tables:
            raise ValueError(f"无效的表名: {table_name}")
        
        try:
            conditions = []
            params = []
            
            # 提取特殊参数
            limit = kwargs.pop('limit', 100)
            offset = kwargs.pop('offset', 0)
            order_by = kwargs.pop('order_by', 'created_time')
            order_desc = kwargs.pop('order_desc', True)
            keyword = kwargs.pop('keyword', None)
            
            # 关键词搜索
            if keyword:
                conditions.append("content LIKE ?")
                params.append(f"%{keyword}%")
            
            # 其他条件
            for field, value in kwargs.items():
                if value is not None:
                    conditions.append(f"{field} = ?")
                    params.append(value)
            
            # 构建WHERE子句
            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)
            
            # 构建ORDER BY子句
            order_direction = "DESC" if order_desc else "ASC"
            order_clause = f"ORDER BY {order_by} {order_direction}"
            
            sql = f"""
            SELECT * FROM {table_name} 
            {where_clause}
            {order_clause}
            LIMIT ? OFFSET ?
            """
            
            params.extend([limit, offset])
            self.cursor.execute(sql, params)
            rows = self.cursor.fetchall()
            
            records = []
            for row in rows:
                record = dict(row)
                # 解析JSON格式的字段
                json_fields = ['reference_urls']
                for field in json_fields:
                    if field in record and record[field]:
                        try:
                            record[field] = json.loads(record[field])
                        except (json.JSONDecodeError, TypeError):
                            record[field] = []
                    elif field in record:
                        record[field] = []
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
                    'latest_record_time': latest,
                    'earliest_record_time': earliest
                }
            else:
                # 获取所有表的统计信息
                all_stats = {}
                for table in self.tables.keys():
                    stats = self.get_table_stats(table)
                    all_stats[table] = stats
                
                return all_stats
                
        except Exception as e:
            raise
    
    # 特殊查询方法
    def get_persona(self) -> Optional[Dict[str, Any]]:
        """获取用户画像"""
        return self.get_record('persona', 1)
    
    def update_persona(self, **kwargs) -> bool:
        """更新用户画像"""
        return self.update_record('persona', 1, **kwargs)
    
    def get_categories(self, first_level: str = None) -> List[Dict[str, Any]]:
        """获取分类列表"""
        if first_level:
            return self.search_records('category', first_level=first_level, is_active=1)
        else:
            return self.search_records('category', is_active=1)
    
    def add_relation(self, source_table: str, source_id: int, target_table: str, 
                    target_id: int, relation_type: str, strength: str = 'medium', 
                    note: str = None) -> int:
        """添加关联关系"""
        return self.insert_record('relations',
                                source_table=source_table,
                                source_id=source_id,
                                target_table=target_table,
                                target_id=target_id,
                                relation_type=relation_type,
                                strength=strength,
                                note=note)
    
    def get_relations(self, table_name: str, record_id: int, 
                     relation_type: str = None) -> List[Dict[str, Any]]:
        """获取记录的关联关系"""
        conditions = {
            'source_table': table_name,
            'source_id': record_id
        }
        if relation_type:
            conditions['relation_type'] = relation_type
        
        return self.search_records('relations', **conditions)
    
    def execute_custom_sql(self, sql: str, params: List[Any] = None, fetch_results: bool = True) -> Dict[str, Any]:
        """
        执行自定义SQL语句
        
        Args:
            sql: SQL语句
            params: SQL参数列表
            fetch_results: 是否获取查询结果（对于SELECT语句）
            
        Returns:
            执行结果字典
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
                    json_fields = ['reference_urls']
                    for field in json_fields:
                        if field in record and record[field]:
                            try:
                                record[field] = json.loads(record[field])
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
                    "description": self.tables[table_name],
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
                for table in self.tables.keys():
                    self.cursor.execute(f"PRAGMA table_info({table})")
                    columns = self.cursor.fetchall()
                    
                    all_schemas[table] = {
                        "table_name": table,
                        "description": self.tables[table],
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
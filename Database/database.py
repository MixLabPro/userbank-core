"""
Database Management Module

Responsible for creating and managing SQLite database for personal profile data structure
"""

import sqlite3
import json
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional, Tuple, Union
from pathlib import Path
import os
import sys

# Add parent directory to path for importing config_manager
sys.path.append(str(Path(__file__).parent.parent))
import sys

# Add parent directory to path for importing config_manager
sys.path.append(str(Path(__file__).parent.parent))
from config_manager import get_config_manager

class ProfileDatabase:
    """Personal profile database management class"""
    
    def __init__(self, db_path: str = None, timezone_offset: int = None):
        """
        Initialize database connection
        
        Args:
            db_path: Database file path, read from config.json if None
            timezone_offset: Timezone offset (hours), read from config.json if None
        """
        # Import configuration manager
        try:
            from config_manager import get_config_manager
            config_manager = get_config_manager()
            
            if db_path is None:
                self.db_path = config_manager.get_database_path()
            else:
                self.db_path = db_path
                
            if timezone_offset is None:
                timezone_offset = config_manager.get_timezone_offset()
                
        except ImportError:
            # Use default values if unable to import configuration manager
            if db_path is None:
                current_dir = Path(__file__).parent.parent
                self.db_path = str(current_dir / "profile_data.db")
            else:
                self.db_path = db_path
                
            if timezone_offset is None:
                timezone_offset = 8
        
        self.connection = None
        self.cursor = None
        
        # Set timezone
        self.timezone = timezone(timedelta(hours=timezone_offset))
        self.timezone_offset = timezone_offset
        
        # Define all table names and English descriptions
        self.tables = {
            # Core tables
            'persona': 'Personal Profile',
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
        
        try:
            # Check if database file exists
            db_exists = Path(self.db_path).exists()
            
            self._connect()
            
            # Create tables only if database file doesn't exist or tables don't exist
            if not db_exists or not self._check_tables_exist():
                self._create_tables()
                self._create_indexes()
                self._init_default_data()
            
        except Exception as e:
            raise
    
    def _get_local_time(self) -> str:
        """Get local time string"""
        return datetime.now(self.timezone).isoformat()
    
    def _connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Enable dictionary-style access
            self.cursor = self.connection.cursor()
            # Enable foreign key constraints
            self.cursor.execute("PRAGMA foreign_keys = ON")
        except Exception as e:
            raise
    
    def _check_tables_exist(self) -> bool:
        """
        Check if all required tables exist
        
        Returns:
            True if all tables exist, False otherwise
        """
        try:
            for table_name in self.tables.keys():
                # Query if table exists
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
        """Create all data tables"""
        try:
            # 1. Persona (Personal Profile Table) - System Core
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS persona (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    gender TEXT,
                    personality TEXT,
                    avatar_url TEXT,
                    bio TEXT,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP,
                    updated_time TIMESTAMP
                )
            """)
            
            # 2. Category (Classification System Table)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS category (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_level TEXT NOT NULL,
                    second_level TEXT NOT NULL,
                    description TEXT,
                    is_active BOOLEAN DEFAULT true,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP,
                    updated_time TIMESTAMP
                )
            """)
            
            # 3. Relations (General Association Table)
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
                    created_time TIMESTAMP,
                    updated_time TIMESTAMP
                )
            """)
            
            # 4. Viewpoint (Viewpoint Table)
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
                    created_time TIMESTAMP,
                    updated_time TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 5. Insight (Insight Table)
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
                    created_time TIMESTAMP,
                    updated_time TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 6. Focus (Focus Point Table)
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
                    created_time TIMESTAMP,
                    updated_time TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 7. Goal (Goal Table)
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
                    created_time TIMESTAMP,
                    updated_time TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 8. Preference (Preference Table)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS preference (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    context TEXT,
                    keywords TEXT,
                    source_app TEXT DEFAULT 'unknown',
                    category_id INTEGER,
                    privacy_level TEXT CHECK(privacy_level IN ('public', 'private')) DEFAULT 'public',
                    created_time TIMESTAMP,
                    updated_time TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 9. Methodology (Methodology Table)
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
                    created_time TIMESTAMP,
                    updated_time TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 10. Prediction (Prediction Table)
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
                    created_time TIMESTAMP,
                    updated_time TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            # 11. Memory (Memory Table)
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
                    created_time TIMESTAMP,
                    updated_time TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES category(id)
                )
            """)
            
            self.connection.commit()
            
        except Exception as e:
            self.connection.rollback()
            raise
    
    def _create_indexes(self):
        """Create indexes"""
        try:
            # Persona table indexes
            self.cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_persona_id ON persona(id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_persona_privacy ON persona(privacy_level)")
            
            # Category table indexes
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_category_levels ON category(first_level, second_level)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_category_active ON category(is_active)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_category_privacy ON category(privacy_level)")
            
            # Relations table indexes
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_source ON relations(source_table, source_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_target ON relations(target_table, target_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_type ON relations(relation_type)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_relations_privacy ON relations(privacy_level)")
            
            # Viewpoint table indexes
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_viewpoint_source_people ON viewpoint(source_people)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_viewpoint_source_app ON viewpoint(source_app)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_viewpoint_category ON viewpoint(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_viewpoint_privacy ON viewpoint(privacy_level)")
            
            # Insight table indexes
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_insight_source_people ON insight(source_people)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_insight_source_app ON insight(source_app)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_insight_category ON insight(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_insight_time ON insight(created_time)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_insight_privacy ON insight(privacy_level)")
            
            # Focus table indexes
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_focus_priority ON focus(priority)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_focus_status ON focus(status)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_focus_deadline ON focus(deadline)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_focus_category ON focus(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_focus_privacy ON focus(privacy_level)")
            
            # Goal table indexes
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_goal_type ON goal(type)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_goal_status ON goal(status)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_goal_deadline ON goal(deadline)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_goal_category ON goal(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_goal_privacy ON goal(privacy_level)")
            
            # Preference table indexes
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_preference_category ON preference(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_preference_privacy ON preference(privacy_level)")
            
            # Methodology table indexes
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_methodology_type ON methodology(type)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_methodology_effectiveness ON methodology(effectiveness)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_methodology_category ON methodology(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_methodology_privacy ON methodology(privacy_level)")
            
            # Prediction table indexes
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_prediction_timeframe ON prediction(timeframe)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_prediction_verification ON prediction(verification_status)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_prediction_category ON prediction(category_id)")
            self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_prediction_privacy ON prediction(privacy_level)")
            
            # Memory table indexes
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
        """Initialize default data"""
        try:
            # Check if persona records already exist
            self.cursor.execute("SELECT COUNT(*) FROM persona")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                # Insert default persona record (ID fixed as 1)
                current_time = self._get_local_time()
                self.cursor.execute("""
                    INSERT INTO persona (id, name, gender, personality, bio, privacy_level, created_time, updated_time)
                    VALUES (1, 'User', 'Not Set', 'To be improved', 'Personal profile to be improved', 'private', ?, ?)
                """, (current_time, current_time))
            
            # Insert some default categories
            default_categories = [
                ('Technology', 'Programming Development', 'Software development related technologies'),
                ('Technology', 'System Architecture', 'System design and architecture'),
                ('Life', 'Interpersonal Relations', 'Interpersonal communication and relationship management'),
                ('Life', 'Health Management', 'Physical and mental health'),
                ('Business', 'Investment Finance', 'Investment and financial management'),
                ('Business', 'Entrepreneurship Management', 'Entrepreneurship and enterprise management'),
                ('Learning', 'Knowledge Management', 'Knowledge acquisition and management'),
                ('Learning', 'Skill Development', 'Personal skill development')
            ]
            
            for first_level, second_level, description in default_categories:
                # Check if already exists
                self.cursor.execute("""
                    SELECT COUNT(*) FROM category 
                    WHERE first_level = ? AND second_level = ?
                """, (first_level, second_level))
                
                if self.cursor.fetchone()[0] == 0:
                    current_time = self._get_local_time()
                    self.cursor.execute("""
                        INSERT INTO category (first_level, second_level, description, created_time, updated_time)
                        VALUES (?, ?, ?, ?, ?)
                    """, (first_level, second_level, description, current_time, current_time))
            
            self.connection.commit()
            
        except Exception as e:
            self.connection.rollback()
            raise
    
    def insert_record(self, table_name: str, **kwargs) -> int:
        """
        Insert record into specified table
        
        Args:
            table_name: Table name
            **kwargs: Field values
            
        Returns:
            ID of inserted record
        """
        try:
            if table_name not in self.tables:
                raise ValueError(f"Unknown table name: {table_name}")
            
            # Handle JSON fields
            if 'keywords' in kwargs and isinstance(kwargs['keywords'], list):
                kwargs['keywords'] = json.dumps(kwargs['keywords'], ensure_ascii=False)
            if 'reference_urls' in kwargs and isinstance(kwargs['reference_urls'], list):
                kwargs['reference_urls'] = json.dumps(kwargs['reference_urls'], ensure_ascii=False)
            
            # Automatically add creation time and update time (using local timezone)
            current_time = self._get_local_time()
            if 'created_time' not in kwargs:
                kwargs['created_time'] = current_time
            if 'updated_time' not in kwargs:
                kwargs['updated_time'] = current_time
            
            # Build SQL statement
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
        Update specified record
        
        Args:
            table_name: Table name
            record_id: Record ID
            **kwargs: Field values to update
            
        Returns:
            Whether update was successful
        """
        try:
            if table_name not in self.tables:
                raise ValueError(f"Unknown table name: {table_name}")
            
            if not kwargs:
                return True
            
            # Handle JSON fields
            if 'keywords' in kwargs and isinstance(kwargs['keywords'], list):
                kwargs['keywords'] = json.dumps(kwargs['keywords'], ensure_ascii=False)
            if 'reference_urls' in kwargs and isinstance(kwargs['reference_urls'], list):
                kwargs['reference_urls'] = json.dumps(kwargs['reference_urls'], ensure_ascii=False)
            
            # Add update time (using local timezone)
            kwargs['updated_time'] = self._get_local_time()
            
            # Build SQL statement
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
        Delete specified record
        
        Args:
            table_name: Table name
            record_id: Record ID
            
        Returns:
            Whether deletion was successful
        """
        try:
            if table_name not in self.tables:
                raise ValueError(f"Unknown table name: {table_name}")
            
            self.cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (record_id,))
            self.connection.commit()
            
            return self.cursor.rowcount > 0
            
        except Exception as e:
            self.connection.rollback()
            raise
    
    def get_record(self, table_name: str, record_id: int) -> Optional[Dict[str, Any]]:
        """
        Get specified record
        
        Args:
            table_name: Table name
            record_id: Record ID
            
        Returns:
            Record data dictionary, returns None if not exists
        """
        try:
            if table_name not in self.tables:
                raise ValueError(f"Unknown table name: {table_name}")
            
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (record_id,))
            row = self.cursor.fetchone()
            
            if row:
                result = dict(row)
                # Parse JSON fields
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
        Query records (supports complex filtering conditions)
        
        Args:
            table_name: Table name
            filter_conditions: Filter conditions dictionary
            sort_by: Sort field
            sort_order: Sort order ('asc' or 'desc')
            limit: Limit of returned records
            offset: Offset
            
        Returns:
            (Record list, total record count) tuple
        """
        try:
            if table_name not in self.tables:
                raise ValueError(f"Unknown table name: {table_name}")
            
            # Build WHERE clause
            where_clauses = []
            params = []
            
            if filter_conditions:
                for key, value in filter_conditions.items():
                    if value is None:
                        continue
                        
                    if key == 'ids':
                        # ID list filtering
                        placeholders = ','.join(['?' for _ in value])
                        where_clauses.append(f"id IN ({placeholders})")
                        params.extend(value)
                    elif key.endswith('_contains'):
                        # Text contains filtering
                        field = key.replace('_contains', '')
                        where_clauses.append(f"{field} LIKE ?")
                        params.append(f"%{value}%")
                    elif key.endswith('_in'):
                        # List filtering
                        field = key.replace('_in', '')
                        placeholders = ','.join(['?' for _ in value])
                        where_clauses.append(f"{field} IN ({placeholders})")
                        params.extend(value)
                    elif key.endswith('_is'):
                        # Exact match
                        field = key.replace('_is', '')
                        where_clauses.append(f"{field} = ?")
                        params.append(value)
                    elif key.endswith('_gte'):
                        # Greater than or equal
                        field = key.replace('_gte', '')
                        where_clauses.append(f"{field} >= ?")
                        params.append(value)
                    elif key.endswith('_lte'):
                        # Less than or equal
                        field = key.replace('_lte', '')
                        where_clauses.append(f"{field} <= ?")
                        params.append(value)
                    elif key.endswith('_from'):
                        # Date range start
                        field = key.replace('_from', '')
                        where_clauses.append(f"{field} >= ?")
                        params.append(value)
                    elif key.endswith('_to'):
                        # Date range end
                        field = key.replace('_to', '')
                        where_clauses.append(f"{field} <= ?")
                        params.append(value)
                    elif key == 'keywords_contain_any':
                        # Keywords contain any one
                        keyword_conditions = []
                        for keyword in value:
                            keyword_conditions.append("keywords LIKE ?")
                            params.append(f'%"{keyword}"%')
                        where_clauses.append(f"({' OR '.join(keyword_conditions)})")
                    elif key == 'keywords_contain_all':
                        # Keywords contain all
                        for keyword in value:
                            where_clauses.append("keywords LIKE ?")
                            params.append(f'%"{keyword}"%')
            
            # Build complete SQL
            where_sql = ""
            if where_clauses:
                where_sql = f"WHERE {' AND '.join(where_clauses)}"
            
            # Get total record count
            count_sql = f"SELECT COUNT(*) FROM {table_name} {where_sql}"
            self.cursor.execute(count_sql, params)
            total_count = self.cursor.fetchone()[0]
            
            # Get records
            order_sql = f"ORDER BY {sort_by} {sort_order.upper()}"
            limit_sql = f"LIMIT {limit} OFFSET {offset}"
            
            query_sql = f"SELECT * FROM {table_name} {where_sql} {order_sql} {limit_sql}"
            self.cursor.execute(query_sql, params)
            
            rows = self.cursor.fetchall()
            records = []
            
            for row in rows:
                record = dict(row)
                # Parse JSON fields
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
        """Get user profile (ID fixed as 1)"""
        return self.get_record('persona', 1)
    
    def update_persona(self, **kwargs) -> bool:
        """Update user profile"""
        return self.update_record('persona', 1, **kwargs)
    
    def get_categories(self, first_level: str = None) -> List[Dict[str, Any]]:
        """Get category list"""
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
        """Add relationship"""
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
        """Get relationships"""
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
        Execute custom SQL statement
        
        Args:
            sql: SQL statement
            params: Parameter list
            fetch_results: Whether to fetch results
            
        Returns:
            Execution result dictionary
        """
        try:
            if params is None:
                params = []
            
            # Security check: only allow SELECT, INSERT, UPDATE, DELETE statements
            sql_upper = sql.strip().upper()
            allowed_operations = ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
            
            if not any(sql_upper.startswith(op) for op in allowed_operations):
                raise ValueError("Only SELECT, INSERT, UPDATE, DELETE statements are allowed")
            
            # Prohibit certain truly dangerous operations (using more precise matching)
            import re
            dangerous_patterns = [
                r'\bDROP\s+TABLE\b',
                r'\bDROP\s+DATABASE\b', 
                r'\bALTER\s+TABLE\b',
                r'\bCREATE\s+TABLE\b',
                r'\bTRUNCATE\s+TABLE\b',
                r'\bDROP\s+INDEX\b'
            ]
            
            # Check if contains dangerous operations
            for pattern in dangerous_patterns:
                if re.search(pattern, sql_upper):
                    raise ValueError(f"Prohibited potentially dangerous SQL operation: matching pattern {pattern}")
            
            # Debug: print SQL statement (temporary)
            print(f"DEBUG: SQL statement passed security check: {sql_upper[:100]}...")
            
            # Temporary: check for other issues
            if 'UNION ALL' in sql_upper and len(sql_upper) > 500:
                print(f"DEBUG: Detected long UNION query, length: {len(sql_upper)}")
                # Allow to pass temporarily
                pass
            
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
            
            # If it's a modification operation, commit transaction
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
        Get table structure information
        
        Args:
            table_name: Table name, returns all table structures if None
            
        Returns:
            Table structure information dictionary
        """
        try:
            if table_name:
                if table_name not in self.tables:
                    raise ValueError(f"Unknown table name: {table_name}")
                
                # Get structure of specified table
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
                # Get structure of all tables
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
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

# Global database instance
_database_instance = None

def get_database() -> ProfileDatabase:
    """Get database instance (singleton pattern)"""
    global _database_instance
    if _database_instance is None:
        _database_instance = ProfileDatabase()
    return _database_instance
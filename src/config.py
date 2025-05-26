#!/usr/bin/env python3
"""
个人画像数据库系统配置文件
"""

import os
from pathlib import Path

# 数据库配置
DATABASE_CONFIG = {
    # 默认数据库文件路径
    "default_db_path": "personal_profile.db",
    
    # 测试数据库文件路径
    "test_db_path": "test_personal_profile.db",
    
    # 数据库连接超时时间（秒）
    "connection_timeout": 30,
    
    # 是否启用WAL模式（Write-Ahead Logging）
    "enable_wal_mode": True,
    
    # 查询结果默认限制
    "default_query_limit": 20,
    
    # 搜索结果默认限制
    "default_search_limit": 50,
    
    # 最大查询限制
    "max_query_limit": 200
}

# MCP服务器配置
MCP_SERVER_CONFIG = {
    # 服务器名称
    "server_name": "personal-profile-db",
    
    # 服务器版本
    "server_version": "1.0.0",
    
    # 服务器描述
    "server_description": "个人画像数据库MCP服务器，提供完整的个人思维模式和行为特征数据管理",
    
    # 是否启用详细日志
    "enable_verbose_logging": True,
    
    # 日志级别
    "log_level": "INFO",
    
    # 是否启用性能监控
    "enable_performance_monitoring": False
}

# 数据表配置
TABLE_CONFIG = {
    # 表名映射（用户友好名称 -> 实际表名）
    "table_mapping": {
        "belief": "beliefs",
        "beliefs": "beliefs",
        "insight": "insights", 
        "insights": "insights",
        "focus": "focuses",
        "focuses": "focuses",
        "long_term_goal": "long_term_goals",
        "long_term_goals": "long_term_goals",
        "short_term_goal": "short_term_goals", 
        "short_term_goals": "short_term_goals",
        "preference": "preferences",
        "preferences": "preferences",
        "decision": "decisions",
        "decisions": "decisions",
        "methodology": "methodologies",
        "methodologies": "methodologies"
    },
    
    # 表的中文名称映射
    "chinese_names": {
        "beliefs": "信念",
        "insights": "洞察", 
        "focuses": "关注点",
        "long_term_goals": "长期目标",
        "short_term_goals": "短期目标",
        "preferences": "偏好",
        "decisions": "决策",
        "methodologies": "方法论"
    },
    
    # 各表的特殊字段配置
    "special_fields": {
        "long_term_goals": ["status"],
        "short_term_goals": ["status", "deadline"],
        "preferences": ["strength"],
        "decisions": ["context", "outcome"],
        "methodologies": ["category", "effectiveness"]
    }
}

# 数据验证配置
VALIDATION_CONFIG = {
    # 内容字段最大长度
    "max_content_length": 2000,
    
    # 相关主题标签最大数量
    "max_related_tags": 10,
    
    # 单个标签最大长度
    "max_tag_length": 50,
    
    # 有效的情绪标签
    "valid_emotions": ["积极", "消极", "中性", "非常积极", "非常消极"],
    
    # 有效的状态标签
    "valid_statuses": ["active", "completed", "paused", "cancelled"],
    
    # 偏好强度范围
    "preference_strength_range": (1, 10),
    
    # 有效性评分范围
    "effectiveness_range": (1, 10)
}

# 分析配置
ANALYSIS_CONFIG = {
    # 支持的分析类型
    "analysis_types": [
        "emotion_distribution",    # 情绪分布分析
        "topic_frequency",        # 主题频率分析
        "time_trends",           # 时间趋势分析
        "goal_progress"          # 目标进度分析
    ],
    
    # 默认分析时间范围（天）
    "default_time_range": 30,
    
    # 最大分析时间范围（天）
    "max_time_range": 365,
    
    # 主题频率分析返回的最大主题数
    "max_topic_frequency_results": 20
}

def get_database_path(use_test_db: bool = False) -> str:
    """
    获取数据库文件路径
    
    Args:
        use_test_db: 是否使用测试数据库
        
    Returns:
        数据库文件路径
    """
    if use_test_db:
        return DATABASE_CONFIG["test_db_path"]
    
    # 检查环境变量
    env_db_path = os.getenv("PERSONAL_PROFILE_DB_PATH")
    if env_db_path:
        return env_db_path
    
    return DATABASE_CONFIG["default_db_path"]

def get_log_level() -> str:
    """
    获取日志级别
    
    Returns:
        日志级别字符串
    """
    return os.getenv("LOG_LEVEL", MCP_SERVER_CONFIG["log_level"])

def is_development_mode() -> bool:
    """
    检查是否为开发模式
    
    Returns:
        是否为开发模式
    """
    return os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"

def get_config_summary() -> dict:
    """
    获取配置摘要信息
    
    Returns:
        配置摘要字典
    """
    return {
        "database_path": get_database_path(),
        "server_name": MCP_SERVER_CONFIG["server_name"],
        "server_version": MCP_SERVER_CONFIG["server_version"],
        "log_level": get_log_level(),
        "development_mode": is_development_mode(),
        "supported_tables": list(TABLE_CONFIG["table_mapping"].values()),
        "supported_analysis_types": ANALYSIS_CONFIG["analysis_types"]
    } 
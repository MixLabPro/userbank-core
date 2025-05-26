#!/usr/bin/env python3
"""
个人画像数据库MCP服务器
提供对个人画像数据库的完整操作接口
"""

import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, date

# 使用标准的mcp包而不是fastmcp
from mcp.server.fastmcp import FastMCP
from database import PersonalProfileDatabase

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化数据库
try:
    db = PersonalProfileDatabase()
    logger.info("数据库初始化成功")
except Exception as e:
    logger.error(f"数据库初始化失败: {e}")
    raise

# 创建FastMCP服务器实例
try:
    mcp = FastMCP("personal-profile-db")
    logger.info("MCP服务器实例创建成功")
except Exception as e:
    logger.error(f"MCP服务器实例创建失败: {e}")
    raise

# 定义表名映射，便于用户使用
TABLE_MAPPING = {
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
}

def normalize_table_name(table_name: str) -> str:
    """标准化表名"""
    return TABLE_MAPPING.get(table_name.lower(), table_name.lower())

def validate_table_name(table_name: str) -> bool:
    """验证表名是否有效"""
    return normalize_table_name(table_name) in TABLE_MAPPING.values()

@mcp.tool()
def add_record(
    table_name: str,
    content: str,
    related: List[str],
    emotion: str = "中性",
    extra_fields: Optional[Dict[str, Any]] = None
) -> str:
    """
    向指定的个人画像数据表中添加新记录
    
    Args:
        table_name: 表名 (belief/insight/focus/long_term_goal/short_term_goal/preference/decision/methodology)
        content: 记录内容
        related: 相关主题标签数组
        emotion: 情绪标签 (积极/消极/中性)，默认为"中性"
        extra_fields: 额外字段 (如status, deadline, strength等)
    
    Returns:
        操作结果的JSON字符串
    """
    try:
        # 验证表名
        if not validate_table_name(table_name):
            return json.dumps({
                "success": False,
                "error": f"无效的表名: {table_name}。支持的表名: {list(TABLE_MAPPING.keys())}"
            }, ensure_ascii=False, indent=2)
        
        # 标准化表名
        normalized_table = normalize_table_name(table_name)
        
        # 准备记录数据
        record_data = {
            "content": content,
            "related": json.dumps(related, ensure_ascii=False),
            "emotion": emotion,
            "create_time": datetime.now().isoformat(),
            "update_time": datetime.now().isoformat()
        }
        
        # 添加额外字段
        if extra_fields:
            record_data.update(extra_fields)
        
        # 添加记录到数据库
        record_id = db.add_record(normalized_table, record_data)
        
        result = {
            "success": True,
            "record_id": record_id,
            "table": normalized_table,
            "message": f"成功添加记录到 {normalized_table} 表"
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"添加记录失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)

@mcp.tool()
def get_records(
    table_name: str,
    limit: int = 20,
    offset: int = 0,
    order_by: str = "create_time DESC"
) -> str:
    """
    从指定表中获取记录列表
    
    Args:
        table_name: 表名
        limit: 返回记录数限制，默认20，最大100
        offset: 偏移量，默认0
        order_by: 排序字段，默认"create_time DESC"
    
    Returns:
        记录列表的JSON字符串
    """
    try:
        # 验证表名
        if not validate_table_name(table_name):
            return json.dumps({
                "success": False,
                "error": f"无效的表名: {table_name}。支持的表名: {list(TABLE_MAPPING.keys())}"
            }, ensure_ascii=False, indent=2)
        
        # 限制limit的最大值
        limit = min(limit, 100)
        
        # 标准化表名
        normalized_table = normalize_table_name(table_name)
        
        # 获取记录
        records = db.get_records(normalized_table, limit=limit, offset=offset, order_by=order_by)
        
        result = {
            "success": True,
            "table": normalized_table,
            "count": len(records),
            "records": records
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"获取记录失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)

@mcp.tool()
def search_records(
    keyword: str,
    table_name: Optional[str] = None,
    limit: int = 20
) -> str:
    """
    在指定表中搜索包含关键词的记录
    
    Args:
        keyword: 搜索关键词
        table_name: 表名 (可选，不指定则搜索所有表)
        limit: 返回记录数限制，默认20，最大100
    
    Returns:
        搜索结果的JSON字符串
    """
    try:
        # 限制limit的最大值
        limit = min(limit, 100)
        
        if table_name and table_name != "all":
            # 验证表名
            if not validate_table_name(table_name):
                return json.dumps({
                    "success": False,
                    "error": f"无效的表名: {table_name}。支持的表名: {list(TABLE_MAPPING.keys())}"
                }, ensure_ascii=False, indent=2)
            
            # 标准化表名
            normalized_table = normalize_table_name(table_name)
            
            # 在指定表中搜索
            records = db.search_records(keyword, table_name=normalized_table, limit=limit)
            
            result = {
                "success": True,
                "keyword": keyword,
                "table": normalized_table,
                "count": len(records),
                "records": records
            }
        else:
            # 在所有表中搜索
            records = db.search_records(keyword, limit=limit)
            
            result = {
                "success": True,
                "keyword": keyword,
                "table": "all",
                "count": len(records),
                "records": records
            }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"搜索记录失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)

@mcp.tool()
def update_record(
    table_name: str,
    record_id: int,
    content: Optional[str] = None,
    related: Optional[List[str]] = None,
    emotion: Optional[str] = None,
    extra_fields: Optional[Dict[str, Any]] = None
) -> str:
    """
    更新指定记录
    
    Args:
        table_name: 表名
        record_id: 记录ID
        content: 新的记录内容 (可选)
        related: 新的相关主题标签数组 (可选)
        emotion: 新的情绪标签 (可选)
        extra_fields: 其他要更新的字段 (可选)
    
    Returns:
        操作结果的JSON字符串
    """
    try:
        # 验证表名
        if not validate_table_name(table_name):
            return json.dumps({
                "success": False,
                "error": f"无效的表名: {table_name}。支持的表名: {list(TABLE_MAPPING.keys())}"
            }, ensure_ascii=False, indent=2)
        
        # 标准化表名
        normalized_table = normalize_table_name(table_name)
        
        # 准备更新数据
        update_data = {"update_time": datetime.now().isoformat()}
        
        if content is not None:
            update_data["content"] = content
        if related is not None:
            update_data["related"] = json.dumps(related, ensure_ascii=False)
        if emotion is not None:
            update_data["emotion"] = emotion
        if extra_fields:
            update_data.update(extra_fields)
        
        # 更新记录
        success = db.update_record(normalized_table, record_id, update_data)
        
        if success:
            result = {
                "success": True,
                "record_id": record_id,
                "table": normalized_table,
                "message": f"成功更新 {normalized_table} 表中的记录 {record_id}"
            }
        else:
            result = {
                "success": False,
                "error": f"记录 {record_id} 在表 {normalized_table} 中不存在"
            }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"更新记录失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)

@mcp.tool()
def delete_record(table_name: str, record_id: int) -> str:
    """
    删除指定记录
    
    Args:
        table_name: 表名
        record_id: 记录ID
    
    Returns:
        操作结果的JSON字符串
    """
    try:
        # 验证表名
        if not validate_table_name(table_name):
            return json.dumps({
                "success": False,
                "error": f"无效的表名: {table_name}。支持的表名: {list(TABLE_MAPPING.keys())}"
            }, ensure_ascii=False, indent=2)
        
        # 标准化表名
        normalized_table = normalize_table_name(table_name)
        
        # 删除记录
        success = db.delete_record(normalized_table, record_id)
        
        if success:
            result = {
                "success": True,
                "record_id": record_id,
                "table": normalized_table,
                "message": f"成功删除 {normalized_table} 表中的记录 {record_id}"
            }
        else:
            result = {
                "success": False,
                "error": f"记录 {record_id} 在表 {normalized_table} 中不存在"
            }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"删除记录失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)

@mcp.tool()
def get_statistics(table_name: Optional[str] = None) -> str:
    """
    获取统计信息
    
    Args:
        table_name: 表名 (可选，不指定则获取所有表的统计信息)
    
    Returns:
        统计信息的JSON字符串
    """
    try:
        if table_name:
            # 验证表名
            if not validate_table_name(table_name):
                return json.dumps({
                    "success": False,
                    "error": f"无效的表名: {table_name}。支持的表名: {list(TABLE_MAPPING.keys())}"
                }, ensure_ascii=False, indent=2)
            
            # 标准化表名
            normalized_table = normalize_table_name(table_name)
            
            # 获取指定表的统计信息
            stats = db.get_statistics(normalized_table)
            
            result = {
                "success": True,
                "table": normalized_table,
                "statistics": stats
            }
        else:
            # 获取所有表的统计信息
            stats = db.get_statistics()
            
            # 计算总记录数
            total_records = sum(table_stats.get("total_records", 0) for table_stats in stats.values())
            
            # 构建详细统计信息
            detailed_stats = {}
            for table, table_stats in stats.items():
                detailed_stats[table] = {
                    "total_records": table_stats.get("total_records", 0),
                    "emotion_distribution": table_stats.get("emotion_distribution", {}),
                    "recent_activity": table_stats.get("recent_activity", {})
                }
            
            result = {
                "success": True,
                "total_records": total_records,
                "statistics": detailed_stats,
                "summary": f"数据库共有 {total_records} 条记录，分布在 {len(stats)} 个表中"
            }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)

@mcp.tool()
def get_recent_records(days: int = 7, limit: int = 50) -> str:
    """
    获取最近的记录
    
    Args:
        days: 天数，默认7天
        limit: 记录数限制，默认50
    
    Returns:
        最近记录的JSON字符串
    """
    try:
        # 计算日期范围
        from datetime import datetime, timedelta
        start_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        recent_records = {}
        total_found = 0
        
        # 从所有表中获取最近的记录
        for table in TABLE_MAPPING.values():
            try:
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    sql = f"""
                        SELECT * FROM {table} 
                        WHERE create_time >= ? 
                        ORDER BY create_time DESC 
                        LIMIT ?
                    """
                    cursor.execute(sql, (start_date, limit))
                    rows = cursor.fetchall()
                    
                    if rows:
                        records = [db._row_to_dict(row) for row in rows]
                        recent_records[table] = records
                        total_found += len(records)
                        
            except Exception as e:
                logger.error(f"获取 {table} 表最近记录失败: {e}")
        
        result = {
            "success": True,
            "time_range": f"最近 {days} 天",
            "total_found": total_found,
            "records_by_table": recent_records
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"获取最近记录失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)

@mcp.tool()
def analyze_patterns(
    analysis_type: str = "emotion_distribution",
    time_range: int = 30
) -> str:
    """
    分析数据模式
    
    Args:
        analysis_type: 分析类型 (emotion_distribution/topic_frequency/time_trends/goal_progress)
        time_range: 时间范围（天数），默认30天
    
    Returns:
        分析结果的JSON字符串
    """
    try:
        # 计算日期范围
        from datetime import datetime, timedelta
        start_date = (datetime.now() - timedelta(days=time_range)).isoformat()
        
        result = {"success": True, "analysis_type": analysis_type, "time_range": f"{time_range} 天"}
        
        if analysis_type == "emotion_distribution":
            # 情绪分布分析
            emotion_stats = {}
            
            for table in TABLE_MAPPING.values():
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    sql = f"""
                        SELECT emotion, COUNT(*) as count 
                        FROM {table} 
                        WHERE create_time >= ? 
                        GROUP BY emotion
                    """
                    cursor.execute(sql, (start_date,))
                    rows = cursor.fetchall()
                    
                    table_emotions = {}
                    for row in rows:
                        table_emotions[row[0]] = row[1]
                    
                    if table_emotions:
                        emotion_stats[table] = table_emotions
            
            result["emotion_distribution"] = emotion_stats
            
        elif analysis_type == "topic_frequency":
            # 主题频率分析
            topic_counts = {}
            
            for table in TABLE_MAPPING.values():
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    sql = f"SELECT related FROM {table} WHERE create_time >= ?"
                    cursor.execute(sql, (start_date,))
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        try:
                            topics = json.loads(row[0])
                            for topic in topics:
                                topic_counts[topic] = topic_counts.get(topic, 0) + 1
                        except:
                            continue
            
            # 按频率排序
            sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
            result["topic_frequency"] = dict(sorted_topics[:20])  # 取前20个
            
        elif analysis_type == "time_trends":
            # 时间趋势分析
            daily_counts = {}
            
            for table in TABLE_MAPPING.values():
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    sql = f"""
                        SELECT DATE(create_time) as date, COUNT(*) as count 
                        FROM {table} 
                        WHERE create_time >= ? 
                        GROUP BY DATE(create_time) 
                        ORDER BY date
                    """
                    cursor.execute(sql, (start_date,))
                    rows = cursor.fetchall()
                    
                    table_trends = {}
                    for row in rows:
                        table_trends[row[0]] = row[1]
                    
                    if table_trends:
                        daily_counts[table] = table_trends
            
            result["time_trends"] = daily_counts
            
        elif analysis_type == "goal_progress":
            # 目标进度分析
            goal_analysis = {}
            
            # 分析长期目标
            with db.get_connection() as conn:
                cursor = conn.cursor()
                sql = """
                    SELECT status, COUNT(*) as count 
                    FROM long_term_goals 
                    WHERE create_time >= ? 
                    GROUP BY status
                """
                cursor.execute(sql, (start_date,))
                rows = cursor.fetchall()
                goal_analysis["long_term_goals"] = dict(rows)
                
                # 分析短期目标
                sql = """
                    SELECT status, COUNT(*) as count 
                    FROM short_term_goals 
                    WHERE create_time >= ? 
                    GROUP BY status
                """
                cursor.execute(sql, (start_date,))
                rows = cursor.fetchall()
                goal_analysis["short_term_goals"] = dict(rows)
            
            result["goal_progress"] = goal_analysis
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"分析失败: {e}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)

def main():
    """启动MCP服务器"""
    try:
        logger.info("启动个人画像数据库MCP服务器...")
        logger.info(f"服务器名称: {mcp.name}")
        
        # FastMCP 没有直接的 _tools 属性，我们可以通过其他方式获取工具信息
        # 或者简单地记录服务器已启动
        logger.info("MCP服务器已配置完成，包含以下功能:")
        logger.info("- 添加记录 (add_record)")
        logger.info("- 获取记录 (get_records)")
        logger.info("- 搜索记录 (search_records)")
        logger.info("- 更新记录 (update_record)")
        logger.info("- 删除记录 (delete_record)")
        logger.info("- 获取统计信息 (get_statistics)")
        logger.info("- 获取最近记录 (get_recent_records)")
        logger.info("- 分析数据模式 (analyze_patterns)")
        
        # 启动服务器
        mcp.run()
        
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        raise

if __name__ == "__main__":
    main() 
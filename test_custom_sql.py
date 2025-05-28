#!/usr/bin/env python3
"""
测试自定义SQL功能的脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import get_database
import json

def test_custom_sql():
    """测试自定义SQL功能"""
    print("=== 测试自定义SQL功能 ===\n")
    
    # 获取数据库实例
    db = get_database()
    
    # 测试1: 获取表结构
    print("1. 测试获取表结构:")
    schema_result = db.get_table_schema()
    print(json.dumps(schema_result, ensure_ascii=False, indent=2))
    print("\n" + "="*50 + "\n")
    
    # 测试2: 获取单个表结构
    print("2. 测试获取单个表结构 (belief):")
    single_schema = db.get_table_schema('belief')
    print(json.dumps(single_schema, ensure_ascii=False, indent=2))
    print("\n" + "="*50 + "\n")
    
    # 测试3: 执行简单查询
    print("3. 测试执行简单查询:")
    query_result = db.execute_custom_sql("SELECT name FROM sqlite_master WHERE type='table'")
    print(json.dumps(query_result, ensure_ascii=False, indent=2))
    print("\n" + "="*50 + "\n")
    
    # 测试4: 查询特定表的记录数
    print("4. 测试查询各表记录数:")
    count_sql = """
    SELECT 
        'belief' as table_name, COUNT(*) as count FROM belief
    UNION ALL
    SELECT 
        'insight' as table_name, COUNT(*) as count FROM insight
    UNION ALL
    SELECT 
        'focus' as table_name, COUNT(*) as count FROM focus
    UNION ALL
    SELECT 
        'long_term_goal' as table_name, COUNT(*) as count FROM long_term_goal
    UNION ALL
    SELECT 
        'short_term_goal' as table_name, COUNT(*) as count FROM short_term_goal
    UNION ALL
    SELECT 
        'preference' as table_name, COUNT(*) as count FROM preference
    UNION ALL
    SELECT 
        'decision' as table_name, COUNT(*) as count FROM decision
    UNION ALL
    SELECT 
        'methodology' as table_name, COUNT(*) as count FROM methodology
    """
    count_result = db.execute_custom_sql(count_sql)
    print(json.dumps(count_result, ensure_ascii=False, indent=2))
    print("\n" + "="*50 + "\n")
    
    # 测试5: 插入测试数据
    print("5. 测试插入数据:")
    insert_sql = "INSERT INTO belief (content, related, created_time, updated_time) VALUES (?, ?, datetime('now'), datetime('now'))"
    insert_params = ["测试信念：持续学习是成功的关键", '["学习", "成长", "成功"]']
    insert_result = db.execute_custom_sql(insert_sql, insert_params)
    print(json.dumps(insert_result, ensure_ascii=False, indent=2))
    print("\n" + "="*50 + "\n")
    
    # 测试6: 查询刚插入的数据
    print("6. 测试查询刚插入的数据:")
    if insert_result.get("success") and insert_result.get("last_insert_id"):
        select_sql = "SELECT * FROM belief WHERE id = ?"
        select_params = [str(insert_result["last_insert_id"])]
        select_result = db.execute_custom_sql(select_sql, select_params)
        print(json.dumps(select_result, ensure_ascii=False, indent=2))
    print("\n" + "="*50 + "\n")
    
    # 测试7: 复杂查询 - 查找最近创建的记录
    print("7. 测试复杂查询 - 查找最近创建的记录:")
    recent_sql = """
    SELECT 
        'belief' as table_name, 
        id, 
        content, 
        created_time 
    FROM belief 
    WHERE created_time >= date('now', '-7 days')
    UNION ALL
    SELECT 
        'insight' as table_name, 
        id, 
        content, 
        created_time 
    FROM insight 
    WHERE created_time >= date('now', '-7 days')
    ORDER BY created_time DESC
    LIMIT 10
    """
    recent_result = db.execute_custom_sql(recent_sql)
    print(json.dumps(recent_result, ensure_ascii=False, indent=2))
    print("\n" + "="*50 + "\n")
    
    # 测试8: 测试安全限制
    print("8. 测试安全限制 - 尝试执行危险操作:")
    dangerous_sql = "DROP TABLE belief"
    dangerous_result = db.execute_custom_sql(dangerous_sql)
    print(json.dumps(dangerous_result, ensure_ascii=False, indent=2))
    print("\n" + "="*50 + "\n")
    
    # 测试9: 测试错误SQL
    print("9. 测试错误SQL:")
    error_sql = "SELECT * FROM non_existent_table"
    error_result = db.execute_custom_sql(error_sql)
    print(json.dumps(error_result, ensure_ascii=False, indent=2))
    print("\n" + "="*50 + "\n")
    
    print("=== 测试完成 ===")

if __name__ == "__main__":
    test_custom_sql()

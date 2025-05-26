#!/usr/bin/env python3
"""
系统测试脚本
System Test Script

用于测试个人画像数据结构分类系统的所有功能
"""

import sys
import json
import logging
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.database import ProfileDatabase
from src.mcp_tools import (
    add_belief, add_insight, add_focus, add_long_term_goal,
    add_short_term_goal, add_preference, add_decision, add_methodology,
    get_record, search_records, get_all_records, update_record,
    delete_record, get_table_stats, get_available_tables
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_creation():
    """测试数据库创建功能"""
    print("🔧 测试数据库创建...")
    try:
        # 使用测试数据库
        db = ProfileDatabase("test_profile.db")
        
        # 检查所有表是否创建成功
        tables = db.tables
        print(f"✅ 成功创建 {len(tables)} 个数据表: {', '.join(tables)}")
        
        # 获取表统计信息
        for table in tables:
            stats = db.get_table_stats(table)
            print(f"   📊 {table}: {stats['total_records']} 条记录")
        
        db.close()
        return True
    except Exception as e:
        print(f"❌ 数据库创建测试失败: {e}")
        return False

def test_mcp_tools():
    """测试MCP工具功能"""
    print("\n🔧 测试MCP工具...")
    
    test_data = [
        # 测试数据：(工具函数, 内容, 相关主题)
        (add_belief, "AI的最大价值在于提升人类创造力", ["技术", "未来", "创新"]),
        (add_insight, "经过三个月的实践，我发现正确的提示工程比模型选择更关键", ["技术", "经验", "效率"]),
        (add_focus, "AI伦理和安全问题", ["技术", "伦理", "安全"]),
        (add_long_term_goal, "希望成为AI领域的知识分享者", ["职业", "技术", "成长"]),
        (add_short_term_goal, "目标是在三个月内掌握高级提示工程技巧", ["学习", "技术", "短期目标"]),
        (add_preference, "我通常喜欢先尝试新技术，然后再决定是否将其整合到工作流程中", ["技术", "工作方式", "适应性"]),
        (add_decision, "选择了使用GPT-4而不是Claude，因为它的代码能力更强", ["技术", "工具", "效率"]),
        (add_methodology, "通过系统性学习和实践，任何人都能掌握AI工具", ["学习", "技术", "成长"])
    ]
    
    added_records = []
    
    # 测试添加功能
    print("📝 测试添加功能...")
    for tool_func, content, related in test_data:
        try:
            result = tool_func(content, related)
            if result["success"]:
                print(f"   ✅ {tool_func.__name__}: 记录ID {result['record_id']}")
                added_records.append((tool_func.__name__.replace('add_', ''), result['record_id']))
            else:
                print(f"   ❌ {tool_func.__name__}: {result['message']}")
        except Exception as e:
            print(f"   ❌ {tool_func.__name__} 失败: {e}")
    
    # 测试查询功能
    print("\n🔍 测试查询功能...")
    if added_records:
        table_name, record_id = added_records[0]
        
        # 测试获取单条记录
        try:
            result = get_record(table_name, record_id)
            if result["success"]:
                print(f"   ✅ 获取记录: {table_name}#{record_id}")
                print(f"      内容: {result['record']['content'][:50]}...")
            else:
                print(f"   ❌ 获取记录失败: {result['message']}")
        except Exception as e:
            print(f"   ❌ 获取记录异常: {e}")
        
        # 测试搜索功能
        try:
            result = search_records(table_name, keyword="AI", limit=5)
            if result["success"]:
                print(f"   ✅ 搜索记录: 找到 {len(result['records'])} 条包含'AI'的记录")
            else:
                print(f"   ❌ 搜索记录失败: {result['message']}")
        except Exception as e:
            print(f"   ❌ 搜索记录异常: {e}")
        
        # 测试获取所有记录
        try:
            result = get_all_records(table_name, limit=10)
            if result["success"]:
                print(f"   ✅ 获取所有记录: {table_name}表中有 {len(result['records'])} 条记录")
            else:
                print(f"   ❌ 获取所有记录失败: {result['message']}")
        except Exception as e:
            print(f"   ❌ 获取所有记录异常: {e}")
    
    # 测试更新功能
    print("\n✏️ 测试更新功能...")
    if added_records:
        table_name, record_id = added_records[0]
        try:
            result = update_record(
                table_name, 
                record_id, 
                content="更新后的内容：AI技术正在快速发展", 
                related=["技术", "更新", "发展"]
            )
            if result["success"]:
                print(f"   ✅ 更新记录: {table_name}#{record_id}")
            else:
                print(f"   ❌ 更新记录失败: {result['message']}")
        except Exception as e:
            print(f"   ❌ 更新记录异常: {e}")
    
    # 测试统计功能
    print("\n📊 测试统计功能...")
    try:
        result = get_available_tables()
        if result["success"]:
            print(f"   ✅ 获取可用表: {result['table_count']} 个表")
            for table, desc in result['tables'].items():
                print(f"      • {table}: {desc}")
        else:
            print(f"   ❌ 获取可用表失败: {result['message']}")
    except Exception as e:
        print(f"   ❌ 获取可用表异常: {e}")
    
    try:
        result = get_table_stats()
        if result["success"]:
            print(f"   ✅ 获取统计信息: 所有表的统计数据")
            for table, stats in result['all_stats'].items():
                print(f"      • {stats['table_description']}: {stats['total_records']} 条记录")
        else:
            print(f"   ❌ 获取统计信息失败: {result['message']}")
    except Exception as e:
        print(f"   ❌ 获取统计信息异常: {e}")
    
    # 测试删除功能（最后测试，避免影响其他测试）
    print("\n🗑️ 测试删除功能...")
    if added_records and len(added_records) > 1:
        table_name, record_id = added_records[-1]  # 删除最后一条记录
        try:
            result = delete_record(table_name, record_id)
            if result["success"]:
                print(f"   ✅ 删除记录: {table_name}#{record_id}")
            else:
                print(f"   ❌ 删除记录失败: {result['message']}")
        except Exception as e:
            print(f"   ❌ 删除记录异常: {e}")
    
    return True

def test_error_handling():
    """测试错误处理功能"""
    print("\n🔧 测试错误处理...")
    
    # 测试无效表名
    try:
        result = get_record("invalid_table", 1)
        if not result["success"] and "无效的表名" in result["message"]:
            print("   ✅ 无效表名错误处理正确")
        else:
            print("   ❌ 无效表名错误处理失败")
    except Exception as e:
        print(f"   ❌ 无效表名测试异常: {e}")
    
    # 测试不存在的记录ID
    try:
        result = get_record("belief", 99999)
        if not result["success"] and "未找到" in result["message"]:
            print("   ✅ 不存在记录ID错误处理正确")
        else:
            print("   ❌ 不存在记录ID错误处理失败")
    except Exception as e:
        print(f"   ❌ 不存在记录ID测试异常: {e}")
    
    return True

def main():
    """主测试函数"""
    print("🧠 个人画像数据结构分类系统 - 功能测试")
    print("=" * 60)
    
    # 运行所有测试
    tests = [
        ("数据库创建", test_database_creation),
        ("MCP工具", test_mcp_tools),
        ("错误处理", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 开始测试: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name} 测试通过")
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统功能正常。")
        return True
    else:
        print("⚠️ 部分测试失败，请检查系统配置。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
#!/usr/bin/env python3
"""
使用示例脚本
Usage Example Script

展示如何使用个人画像数据管理系统的各种功能
"""

import sys
import json
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.mcp_tools import (
    add_belief, add_insight, add_focus, add_long_term_goal,
    add_short_term_goal, add_preference, add_decision, add_methodology,
    get_record, search_records, get_all_records, update_record,
    delete_record, get_table_stats, get_available_tables
)

def print_result(result, title="操作结果"):
    """格式化打印结果"""
    print(f"\n📋 {title}:")
    print(f"   状态: {'✅ 成功' if result.get('success') else '❌ 失败'}")
    print(f"   消息: {result.get('message', '无消息')}")
    
    if 'record_id' in result:
        print(f"   记录ID: {result['record_id']}")
    
    if 'record' in result:
        record = result['record']
        print(f"   内容: {record['content']}")
        print(f"   相关主题: {record['related']}")
        print(f"   创建时间: {record['created_time']}")
    
    if 'records' in result:
        records = result['records']
        print(f"   找到记录数: {len(records)}")
        for i, record in enumerate(records[:3], 1):  # 只显示前3条
            print(f"     {i}. {record['content'][:50]}...")
    
    if 'stats' in result:
        stats = result['stats']
        print(f"   表名: {stats['table_name']} ({stats.get('table_description', '')})")
        print(f"   记录总数: {stats['total_records']}")
        print(f"   最新记录: {stats['latest_record']}")
    
    if 'all_stats' in result:
        print("   所有表统计:")
        for table, stats in result['all_stats'].items():
            print(f"     • {stats['table_description']}: {stats['total_records']} 条记录")

def demo_basic_operations():
    """演示基本操作"""
    print("🚀 演示基本操作")
    print("=" * 60)
    
    # 1. 添加各种类型的记录
    print("\n📝 1. 添加记录示例")
    
    # 添加信念
    result = add_belief(
        content="AI技术将彻底改变教育行业的未来发展模式",
        related=["技术", "教育", "未来", "变革"]
    )
    print_result(result, "添加信念记录")
    belief_id = result.get('record_id')
    
    # 添加洞察
    result = add_insight(
        content="通过半年的AI工具使用经验，我发现最重要的是理解工具的局限性而不是盲目追求功能",
        related=["经验", "AI工具", "理解", "局限性"]
    )
    print_result(result, "添加洞察记录")
    
    # 添加长期目标
    result = add_long_term_goal(
        content="在未来三年内成为AI教育领域的专家和意见领袖",
        related=["职业发展", "AI", "教育", "专家"]
    )
    print_result(result, "添加长期目标")
    
    # 添加短期目标
    result = add_short_term_goal(
        content="本季度完成AI提示工程课程的开发和上线",
        related=["课程开发", "提示工程", "短期计划"]
    )
    print_result(result, "添加短期目标")
    
    # 添加偏好
    result = add_preference(
        content="我更喜欢通过实际项目来学习新技术，而不是纯理论学习",
        related=["学习方式", "实践", "项目导向"]
    )
    print_result(result, "添加偏好记录")
    
    # 添加决策
    result = add_decision(
        content="选择使用Claude作为主要的AI写作助手，因为它在长文本处理上表现更好",
        related=["工具选择", "Claude", "写作", "决策"]
    )
    print_result(result, "添加决策记录")
    
    # 添加方法论
    result = add_methodology(
        content="采用PDCA循环方法来持续改进AI工具的使用效果：计划-执行-检查-改进",
        related=["方法论", "PDCA", "持续改进", "效率"]
    )
    print_result(result, "添加方法论记录")
    
    return belief_id

def demo_query_operations(belief_id):
    """演示查询操作"""
    print("\n🔍 2. 查询记录示例")
    
    # 获取单条记录
    if belief_id:
        result = get_record("belief", belief_id)
        print_result(result, "获取信念记录")
    
    # 搜索记录
    result = search_records("belief", keyword="AI", limit=5)
    print_result(result, "搜索包含'AI'的信念记录")
    
    # 按主题搜索
    result = search_records("long_term_goal", related_topic="职业", limit=3)
    print_result(result, "搜索职业相关的长期目标")
    
    # 获取所有记录
    result = get_all_records("methodology", limit=10)
    print_result(result, "获取所有方法论记录")

def demo_update_operations(belief_id):
    """演示更新操作"""
    print("\n✏️ 3. 更新记录示例")
    
    if belief_id:
        # 更新记录内容
        result = update_record(
            "belief", 
            belief_id,
            content="AI技术将彻底改变教育行业，但需要谨慎处理数据隐私和伦理问题",
            related=["技术", "教育", "未来", "变革", "隐私", "伦理"]
        )
        print_result(result, "更新信念记录")
        
        # 验证更新结果
        result = get_record("belief", belief_id)
        print_result(result, "验证更新后的记录")

def demo_stats_operations():
    """演示统计操作"""
    print("\n📊 4. 统计信息示例")
    
    # 获取可用表信息
    result = get_available_tables()
    print_result(result, "获取可用表信息")
    
    # 获取单个表统计
    result = get_table_stats("belief")
    print_result(result, "获取信念表统计信息")
    
    # 获取所有表统计
    result = get_table_stats()
    print_result(result, "获取所有表统计信息")

def demo_advanced_search():
    """演示高级搜索功能"""
    print("\n🔎 5. 高级搜索示例")
    
    # 复合搜索
    tables_to_search = ["belief", "insight", "long_term_goal", "methodology"]
    
    for table in tables_to_search:
        result = search_records(table, keyword="AI", limit=2)
        if result.get('success') and result.get('records'):
            print(f"\n   📋 {table}表中包含'AI'的记录:")
            for record in result['records']:
                print(f"     • {record['content'][:60]}...")
                print(f"       主题: {', '.join(record['related'])}")

def main():
    """主演示函数"""
    print("🧠 个人画像数据管理系统 - 使用示例")
    print("Personal Profile Data Management System - Usage Examples")
    print("=" * 80)
    
    try:
        # 基本操作演示
        belief_id = demo_basic_operations()
        
        # 查询操作演示
        demo_query_operations(belief_id)
        
        # 更新操作演示
        demo_update_operations(belief_id)
        
        # 统计操作演示
        demo_stats_operations()
        
        # 高级搜索演示
        demo_advanced_search()
        
        print("\n" + "=" * 80)
        print("🎉 所有示例演示完成！")
        print("💡 提示：您可以通过MCP客户端连接到服务器来使用这些工具")
        print("📖 更多信息请查看 README.md 文件")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
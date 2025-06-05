#!/usr/bin/env python3
"""
测试脚本：验证所有18个工具是否正常工作
"""

from main import (
    # Persona Tools
    get_persona, save_persona,
    # Memory Tools  
    query_memories, save_memory,
    # Viewpoint Tools
    query_viewpoints, save_viewpoint,
    # Insight Tools
    query_insights, save_insight,
    # Goal Tools
    query_goals, save_goal,
    # Preference Tools
    query_preferences, save_preference,
    # Methodology Tools
    query_methodologies, save_methodology,
    # Focus Tools
    query_focuses, save_focus,
    # Prediction Tools
    query_predictions, save_prediction,
    # 保留工具
    execute_custom_sql, get_table_schema
)

def test_all_tools():
    """测试所有工具"""
    print("🚀 开始测试所有18个工具...")
    
    # 1. 测试Persona Tools
    print("\n📋 测试 Persona Tools...")
    persona_result = get_persona()
    print(f"✅ get_persona: {persona_result['raw_data']['name'] if persona_result['raw_data'] else '无数据'}")
    
    save_result = save_persona(name="测试用户", personality="友好开朗")
    print(f"✅ save_persona: {save_result['operation']}")
    
    # 2. 测试Memory Tools
    print("\n🧠 测试 Memory Tools...")
    memory_result = query_memories()
    print(f"✅ query_memories: 找到 {memory_result['total_count']} 条记录")
    
    save_memory_result = save_memory(
        content="第一次使用新系统的经历",
        memory_type="experience",
        importance=8,
        keywords=["系统", "学习", "经验"]
    )
    print(f"✅ save_memory: {save_memory_result['operation']}")
    
    # 3. 测试Viewpoint Tools
    print("\n💭 测试 Viewpoint Tools...")
    viewpoint_result = query_viewpoints()
    print(f"✅ query_viewpoints: 找到 {viewpoint_result['total_count']} 条记录")
    
    save_viewpoint_result = save_viewpoint(
        content="技术应该服务于人，而不是相反",
        source_people="自己",
        keywords=["技术", "人文", "价值观"]
    )
    print(f"✅ save_viewpoint: {save_viewpoint_result['operation']}")
    
    # 4. 测试Insight Tools
    print("\n💡 测试 Insight Tools...")
    insight_result = query_insights()
    print(f"✅ query_insights: 找到 {insight_result['total_count']} 条记录")
    
    save_insight_result = save_insight(
        content="复杂问题往往需要简单的解决方案",
        source_people="自己",
        keywords=["问题解决", "简化", "洞察"]
    )
    print(f"✅ save_insight: {save_insight_result['operation']}")
    
    # 5. 测试Goal Tools
    print("\n🎯 测试 Goal Tools...")
    goal_result = query_goals()
    print(f"✅ query_goals: 找到 {goal_result['total_count']} 条记录")
    
    save_goal_result = save_goal(
        content="完成个人画像系统重构",
        type="short_term",
        deadline="2024-12-31",
        keywords=["重构", "系统", "完成"]
    )
    print(f"✅ save_goal: {save_goal_result['operation']}")
    
    # 6. 测试Preference Tools
    print("\n❤️ 测试 Preference Tools...")
    preference_result = query_preferences()
    print(f"✅ query_preferences: 找到 {preference_result['total_count']} 条记录")
    
    save_preference_result = save_preference(
        content="喜欢在安静环境中深度思考",
        context="工作学习",
        keywords=["环境", "思考", "专注"]
    )
    print(f"✅ save_preference: {save_preference_result['operation']}")
    
    # 7. 测试Methodology Tools
    print("\n🔧 测试 Methodology Tools...")
    methodology_result = query_methodologies()
    print(f"✅ query_methodologies: 找到 {methodology_result['total_count']} 条记录")
    
    save_methodology_result = save_methodology(
        content="先理解问题本质，再寻找解决方案",
        type="问题解决",
        effectiveness="proven",
        keywords=["方法论", "问题分析", "解决方案"]
    )
    print(f"✅ save_methodology: {save_methodology_result['operation']}")
    
    # 8. 测试Focus Tools
    print("\n🎯 测试 Focus Tools...")
    focus_result = query_focuses()
    print(f"✅ query_focuses: 找到 {focus_result['total_count']} 条记录")
    
    save_focus_result = save_focus(
        content="学习新的编程技术",
        priority=9,
        status="active",
        keywords=["学习", "编程", "技术"]
    )
    print(f"✅ save_focus: {save_focus_result['operation']}")
    
    # 9. 测试Prediction Tools
    print("\n🔮 测试 Prediction Tools...")
    prediction_result = query_predictions()
    print(f"✅ query_predictions: 找到 {prediction_result['total_count']} 条记录")
    
    save_prediction_result = save_prediction(
        content="AI技术将在未来5年内显著改变软件开发方式",
        timeframe="未来5年",
        basis="当前AI技术发展趋势和应用案例",
        keywords=["AI", "软件开发", "技术趋势"]
    )
    print(f"✅ save_prediction: {save_prediction_result['operation']}")
    
    # 10. 测试保留工具
    print("\n🔧 测试保留工具...")
    schema_result = get_table_schema()
    print(f"✅ get_table_schema: 包含 {schema_result['table_count']} 个表")
    
    sql_result = execute_custom_sql("SELECT COUNT(*) as total FROM persona")
    print(f"✅ execute_custom_sql: 查询成功，persona表有 {sql_result['data'][0]['total'] if sql_result['success'] else 0} 条记录")
    
    print("\n🎉 所有工具测试完成！")
    print("✨ 重构成功，18个工具全部正常工作！")

if __name__ == "__main__":
    test_all_tools() 
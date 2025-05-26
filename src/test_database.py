#!/usr/bin/env python3
"""
个人画像数据库测试脚本
用于测试数据库功能并插入示例数据
"""

import json
import logging
from datetime import datetime, timedelta
from database import PersonalProfileDatabase

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_database_operations():
    """测试数据库基本操作"""
    try:
        # 初始化数据库
        logger.info("=== 开始测试数据库操作 ===")
        db = PersonalProfileDatabase("test_personal_profile.db")
        
        # 测试插入示例数据
        logger.info("1. 测试插入示例数据...")
        insert_sample_data(db)
        
        # 测试查询操作
        logger.info("2. 测试查询操作...")
        test_query_operations(db)
        
        # 测试搜索功能
        logger.info("3. 测试搜索功能...")
        test_search_operations(db)
        
        # 测试更新操作
        logger.info("4. 测试更新操作...")
        test_update_operations(db)
        
        # 测试统计功能
        logger.info("5. 测试统计功能...")
        test_statistics(db)
        
        logger.info("=== 数据库测试完成 ===")
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")
        raise

def insert_sample_data(db: PersonalProfileDatabase):
    """插入示例数据"""
    
    # 信念数据
    beliefs_data = [
        {
            "content": "AI的最大价值在于提升人类创造力",
            "related": ["技术", "未来", "创新"],
            "emotion": "积极"
        },
        {
            "content": "持续学习是个人成长的关键",
            "related": ["学习", "成长", "自我提升"],
            "emotion": "积极"
        },
        {
            "content": "简约设计比复杂设计更有效",
            "related": ["设计", "简约", "效率"],
            "emotion": "中性"
        }
    ]
    
    for belief in beliefs_data:
        record_id = db.insert_record("beliefs", belief)
        logger.info(f"插入信念记录，ID: {record_id}")
    
    # 洞察数据
    insights_data = [
        {
            "content": "经过三个月的实践，我发现正确的提示工程比模型选择更关键",
            "related": ["技术", "经验", "效率"],
            "emotion": "中性"
        },
        {
            "content": "在团队协作中，沟通频率比沟通质量更重要",
            "related": ["团队", "沟通", "协作"],
            "emotion": "中性"
        }
    ]
    
    for insight in insights_data:
        record_id = db.insert_record("insights", insight)
        logger.info(f"插入洞察记录，ID: {record_id}")
    
    # 关注点数据
    focuses_data = [
        {
            "content": "AI伦理和安全问题",
            "related": ["AI", "伦理", "安全"],
            "emotion": "中性"
        },
        {
            "content": "可持续发展和环保技术",
            "related": ["环保", "可持续", "技术"],
            "emotion": "积极"
        }
    ]
    
    for focus in focuses_data:
        record_id = db.insert_record("focuses", focus)
        logger.info(f"插入关注点记录，ID: {record_id}")
    
    # 长期目标数据
    long_term_goals_data = [
        {
            "content": "希望成为AI领域的知识分享者",
            "related": ["职业", "技术", "成长"],
            "emotion": "积极",
            "status": "active"
        },
        {
            "content": "建立一个可持续发展的科技企业",
            "related": ["创业", "可持续", "科技"],
            "emotion": "积极",
            "status": "active"
        }
    ]
    
    for goal in long_term_goals_data:
        record_id = db.insert_record("long_term_goals", goal)
        logger.info(f"插入长期目标记录，ID: {record_id}")
    
    # 短期目标数据
    short_term_goals_data = [
        {
            "content": "目标是在三个月内掌握高级提示工程技巧",
            "related": ["学习", "技术", "短期目标"],
            "emotion": "积极",
            "status": "active",
            "deadline": (datetime.now() + timedelta(days=90)).date().isoformat()
        },
        {
            "content": "完成个人画像数据库项目",
            "related": ["项目", "开发", "数据库"],
            "emotion": "积极",
            "status": "active",
            "deadline": (datetime.now() + timedelta(days=30)).date().isoformat()
        }
    ]
    
    for goal in short_term_goals_data:
        record_id = db.insert_record("short_term_goals", goal)
        logger.info(f"插入短期目标记录，ID: {record_id}")
    
    # 偏好数据
    preferences_data = [
        {
            "content": "我通常喜欢先尝试新技术，然后再决定是否将其整合到工作流程中",
            "related": ["技术", "工作方式", "适应性"],
            "emotion": "中性",
            "strength": 8
        },
        {
            "content": "偏爱安静的工作环境胜过嘈杂的开放空间",
            "related": ["工作环境", "专注", "效率"],
            "emotion": "中性",
            "strength": 9
        }
    ]
    
    for preference in preferences_data:
        record_id = db.insert_record("preferences", preference)
        logger.info(f"插入偏好记录，ID: {record_id}")
    
    # 决策数据
    decisions_data = [
        {
            "content": "选择了使用GPT-4而不是Claude，因为它的代码能力更强",
            "related": ["技术", "工具", "效率"],
            "emotion": "中性",
            "context": "为项目选择AI助手",
            "outcome": "提高了代码质量和开发效率"
        },
        {
            "content": "决定采用SQLite作为个人画像数据库的存储方案",
            "related": ["技术", "数据库", "项目"],
            "emotion": "积极",
            "context": "个人画像系统技术选型",
            "outcome": "简化了部署和维护"
        }
    ]
    
    for decision in decisions_data:
        record_id = db.insert_record("decisions", decision)
        logger.info(f"插入决策记录，ID: {record_id}")
    
    # 方法论数据
    methodologies_data = [
        {
            "content": "通过系统性学习和实践，任何人都能掌握AI工具",
            "related": ["学习", "技术", "成长"],
            "emotion": "积极",
            "category": "学习方法",
            "effectiveness": 8
        },
        {
            "content": "采用敏捷开发方法，每周进行一次迭代和回顾",
            "related": ["开发", "敏捷", "迭代"],
            "emotion": "积极",
            "category": "开发方法",
            "effectiveness": 9
        },
        {
            "content": "使用番茄工作法来提高专注度和工作效率",
            "related": ["效率", "专注", "时间管理"],
            "emotion": "积极",
            "category": "时间管理",
            "effectiveness": 7
        }
    ]
    
    for methodology in methodologies_data:
        record_id = db.insert_record("methodologies", methodology)
        logger.info(f"插入方法论记录，ID: {record_id}")

def test_query_operations(db: PersonalProfileDatabase):
    """测试查询操作"""
    
    # 测试获取各表记录
    tables = ["beliefs", "insights", "focuses", "long_term_goals", 
              "short_term_goals", "preferences", "decisions", "methodologies"]
    
    for table in tables:
        records = db.get_records(table, limit=5)
        logger.info(f"从 {table} 表获取到 {len(records)} 条记录")
        
        if records:
            logger.info(f"示例记录: {records[0]['content'][:50]}...")

def test_search_operations(db: PersonalProfileDatabase):
    """测试搜索操作"""
    
    # 测试关键词搜索
    keywords = ["技术", "学习", "AI", "效率"]
    
    for keyword in keywords:
        # 在所有表中搜索
        results = []
        for table in ["beliefs", "insights", "focuses", "long_term_goals", 
                     "short_term_goals", "preferences", "decisions", "methodologies"]:
            table_results = db.search_records(table, keyword, limit=10)
            results.extend(table_results)
        
        logger.info(f"搜索关键词 '{keyword}' 找到 {len(results)} 条记录")

def test_update_operations(db: PersonalProfileDatabase):
    """测试更新操作"""
    
    # 获取一条信念记录进行更新测试
    beliefs = db.get_records("beliefs", limit=1)
    if beliefs:
        belief_id = beliefs[0]["id"]
        
        # 更新记录
        update_data = {
            "emotion": "非常积极",
            "related": ["技术", "未来", "创新", "更新测试"]
        }
        
        success = db.update_record("beliefs", belief_id, update_data)
        logger.info(f"更新记录 ID {belief_id}: {'成功' if success else '失败'}")
        
        # 验证更新
        updated_record = db.get_records("beliefs", limit=1, 
                                       order_by=f"id = {belief_id}")
        if updated_record:
            logger.info(f"更新后的记录: {updated_record[0]}")

def test_statistics(db: PersonalProfileDatabase):
    """测试统计功能"""
    
    # 获取统计信息
    stats = db.get_statistics()
    logger.info("数据库统计信息:")
    
    total_records = sum(stats.values())
    logger.info(f"总记录数: {total_records}")
    
    for table, count in stats.items():
        percentage = (count / total_records * 100) if total_records > 0 else 0
        logger.info(f"  {table}: {count} 条记录 ({percentage:.1f}%)")

def create_sample_json_export(db: PersonalProfileDatabase):
    """创建示例JSON导出文件"""
    
    logger.info("创建示例JSON导出文件...")
    
    export_data = {
        "export_time": datetime.now().isoformat(),
        "statistics": db.get_statistics(),
        "data": {}
    }
    
    # 导出所有表的数据
    tables = ["beliefs", "insights", "focuses", "long_term_goals", 
              "short_term_goals", "preferences", "decisions", "methodologies"]
    
    for table in tables:
        records = db.get_records(table, limit=100)
        export_data["data"][table] = records
    
    # 保存到文件
    with open("sample_personal_profile_export.json", "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    logger.info("示例数据已导出到 sample_personal_profile_export.json")

if __name__ == "__main__":
    try:
        # 运行测试
        test_database_operations()
        
        # 创建示例导出文件
        db = PersonalProfileDatabase("test_personal_profile.db")
        create_sample_json_export(db)
        
        print("\n" + "="*50)
        print("测试完成！")
        print("数据库文件: test_personal_profile.db")
        print("示例导出文件: sample_personal_profile_export.json")
        print("="*50)
        
    except Exception as e:
        logger.error(f"测试失败: {e}")
        raise
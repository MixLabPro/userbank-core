#!/usr/bin/env python3
"""
测试新功能脚本
Test New Features Script

测试数据库文件检查和新增的MCP工具功能
"""

import sys
import os
import logging
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.database import ProfileDatabase
from src.mcp_tools import (
    get_all_table_contents, 
    get_table_names_with_details, 
    export_table_data,
    add_belief,
    add_insight
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_database_file_check():
    """测试数据库文件存在性检查功能"""
    print("=" * 60)
    print("🧪 测试数据库文件检查功能")
    print("=" * 60)
    
    test_db_path = "test_new_features.db"
    
    try:
        # 删除测试数据库文件（如果存在）
        if Path(test_db_path).exists():
            os.remove(test_db_path)
            print(f"🗑️ 删除已存在的测试数据库: {test_db_path}")
        
        # 第一次创建数据库（应该创建表）
        print("\n📝 第一次创建数据库...")
        db1 = ProfileDatabase(test_db_path)
        print("✅ 第一次数据库创建成功")
        db1.close()
        
        # 第二次打开数据库（应该跳过表创建）
        print("\n📝 第二次打开数据库...")
        db2 = ProfileDatabase(test_db_path)
        print("✅ 第二次数据库打开成功")
        db2.close()
        
        print("\n🎯 数据库文件检查功能测试完成")
        
    except Exception as e:
        logger.error(f"❌ 数据库文件检查测试失败: {e}")
        return False
    
    finally:
        # 清理测试文件
        try:
            if Path(test_db_path).exists():
                os.remove(test_db_path)
                print(f"🧹 清理测试数据库文件: {test_db_path}")
        except:
            pass
    
    return True

def test_new_mcp_tools():
    """测试新增的MCP工具"""
    print("\n" + "=" * 60)
    print("🧪 测试新增的MCP工具")
    print("=" * 60)
    
    try:
        # 添加一些测试数据
        print("\n📝 添加测试数据...")
        
        # 添加信念记录
        belief_result = add_belief(
            content="持续学习是成功的关键",
            related=["学习", "成长", "成功"]
        )
        print(f"✅ 添加信念: {belief_result}")
        
        # 添加洞察记录
        insight_result = add_insight(
            content="技术的发展需要与人文关怀相结合",
            related=["技术", "人文", "平衡"]
        )
        print(f"✅ 添加洞察: {insight_result}")
        
        # 测试获取表名详细信息
        print("\n📋 测试获取表名详细信息...")
        table_names_result = get_table_names_with_details()
        print(f"✅ 表名详细信息: {table_names_result['message']}")
        if table_names_result['success']:
            for table_name, details in table_names_result['table_details'].items():
                print(f"  📊 {table_name} ({details['chinese_name']}): {details['total_records']} 条记录")
        
        # 测试获取所有表内容
        print("\n📦 测试获取所有表内容...")
        all_contents_result = get_all_table_contents(include_empty=False, limit_per_table=10)
        print(f"✅ 所有表内容: {all_contents_result['message']}")
        if all_contents_result['success']:
            print(f"  📊 总表数: {all_contents_result['table_count']}")
            print(f"  📊 总记录数: {all_contents_result['total_records']}")
        
        # 测试导出表数据（JSON格式）
        print("\n📤 测试导出表数据 (JSON)...")
        export_json_result = export_table_data("belief", "json")
        print(f"✅ JSON导出: {export_json_result['message']}")
        
        # 测试导出表数据（CSV格式）
        print("\n📤 测试导出表数据 (CSV)...")
        export_csv_result = export_table_data("belief", "csv")
        print(f"✅ CSV导出: {export_csv_result['message']}")
        if export_csv_result['success']:
            print("📄 CSV数据预览:")
            csv_lines = export_csv_result['data'].split('\n')[:3]  # 只显示前3行
            for line in csv_lines:
                print(f"    {line}")
        
        print("\n🎯 新增MCP工具测试完成")
        return True
        
    except Exception as e:
        logger.error(f"❌ MCP工具测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始测试新功能...")
    
    try:
        # 测试数据库文件检查
        db_test_success = test_database_file_check()
        
        # 测试新增的MCP工具
        mcp_test_success = test_new_mcp_tools()
        
        # 总结测试结果
        print("\n" + "=" * 60)
        print("📊 测试结果总结")
        print("=" * 60)
        print(f"🔍 数据库文件检查: {'✅ 通过' if db_test_success else '❌ 失败'}")
        print(f"🔧 新增MCP工具: {'✅ 通过' if mcp_test_success else '❌ 失败'}")
        
        if db_test_success and mcp_test_success:
            print("\n🎉 所有测试通过！新功能工作正常。")
            return True
        else:
            print("\n⚠️ 部分测试失败，请检查错误信息。")
            return False
            
    except Exception as e:
        logger.error(f"❌ 测试过程中发生错误: {e}")
        print(f"\n❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
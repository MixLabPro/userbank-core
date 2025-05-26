#!/usr/bin/env python3
"""
个人画像数据库测试运行脚本
"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from test_database import test_database_operations, create_sample_json_export
    from database import PersonalProfileDatabase
    import logging
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    def main():
        """主测试函数"""
        print("=" * 60)
        print("个人画像数据库测试")
        print("=" * 60)
        
        try:
            # 运行数据库操作测试
            print("开始运行数据库测试...")
            test_database_operations()
            
            # 创建示例导出文件
            print("\n创建示例导出文件...")
            db = PersonalProfileDatabase("test_personal_profile.db")
            create_sample_json_export(db)
            
            print("\n" + "=" * 60)
            print("✅ 所有测试通过！")
            print("=" * 60)
            print("生成的文件:")
            print("  • test_personal_profile.db - 测试数据库文件")
            print("  • sample_personal_profile_export.json - 示例导出文件")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ 测试失败: {e}")
            sys.exit(1)
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装所有依赖包:")
    print("pip install -r requirements.txt")
    sys.exit(1) 
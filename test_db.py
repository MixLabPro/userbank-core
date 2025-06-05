#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import sys
import os

print("开始测试数据库...")

try:
    from Database.database import get_database
    print("成功导入数据库模块")
    
    db = get_database()
    print("数据库初始化成功")
    
    print("表列表:", list(db.tables.keys()))
    
    # 测试获取用户画像
    persona = db.get_persona()
    print("用户画像:", persona)
    
    # 测试获取分类
    categories = db.get_categories()
    print("分类数量:", len(categories))
    
    print("所有测试通过!")
    
except Exception as e:
    print(f"错误: {e}")
    print("详细错误信息:")
    traceback.print_exc() 
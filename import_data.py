#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的数据库测试脚本
"""

import sys
import os

# 添加 backend 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from database import db
from grade1_data import import_grade1_data, show_grade1_summary

def main():
    print("="*60)
    print("家庭教育AI辅导 - 数据导入工具")
    print("="*60)
    
    # 导入一年级数据
    import_grade1_data()
    
    # 显示摘要
    show_grade1_summary()
    
    print("\n✅ 数据导入完成！")
    print("\n现在可以运行 'cd backend && python -m uvicorn main:app --reload' 来启动应用")

if __name__ == "__main__":
    main()

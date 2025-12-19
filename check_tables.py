#!/usr/bin/env python
"""
检查指定的数据库表是否存在
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "community_management.settings")

import django
django.setup()

from django.db import connection

# 要检查的表名
tables_to_check = [
    'api_userprofile',
    'api_socialworker', 
    'api_cadre'
]

def check_tables():
    with connection.cursor() as cursor:
        # 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        print("现有表:")
        for table in existing_tables:
            print(f"  - {table}")
        
        print("\n检查结果:")
        for table in tables_to_check:
            if table in existing_tables:
                print(f"  ✅ {table}: 存在")
            else:
                print(f"  ❌ {table}: 不存在")

if __name__ == "__main__":
    check_tables()

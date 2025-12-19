#!/usr/bin/env python
"""
重置指定的数据库表
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "community_management.settings")

import django

django.setup()

from django.db import connection

# 要删除的表名
tables_to_drop = ['api_userprofile', 'api_socialworker', 'api_cadre']


def reset_tables():
    with connection.cursor() as cursor:
        for table in tables_to_drop:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table};")
                print(f"已删除表: {table}")
            except Exception as e:
                print(f"删除表 {table} 失败: {e}")


if __name__ == "__main__":
    reset_tables()

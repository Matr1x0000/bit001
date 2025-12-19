#!/usr/bin/env python
"""
使用Django ORM重新创建指定的模型表
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "community_management.settings")

import django
django.setup()

from django.db import connection, migrations
from django.db.migrations.state import ProjectState

# 导入模型
from api.models import UserProfile, SocialWorker, Cadre

def create_tables():
    print("开始重新创建表...")
    
    # 获取模型的schema编辑器
    with connection.schema_editor() as schema_editor:
        # 重新创建表
        schema_editor.create_model(UserProfile)
        print("✅ 创建表: api_userprofile")
        
        schema_editor.create_model(SocialWorker)
        print("✅ 创建表: api_socialworker")
        
        schema_editor.create_model(Cadre)
        print("✅ 创建表: api_cadre")
    
    print("\n表创建完成！")

if __name__ == "__main__":
    create_tables()

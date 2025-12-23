# -*- coding: utf-8 -*-
"""
Django 上下文处理器

此文件包含向所有 Django 模板添加自定义变量和函数的上下文处理器。
目前，它提供了一个用于模板中的权限检查函数。
"""

# 导入权限常量字典，用于权限级别定义
from api.permissions import PERMISSIONS


def user_permissions(request):
    """
    上下文处理器：向所有模板添加用户权限检查函数
    
    此处理器允许在模板中直接使用 has_permission() 函数来检查用户权限，
    无需在每个视图中单独传递权限信息。
    
    Args:
        request: Django HTTP 请求对象，包含当前用户信息
    
    Returns:
        dict: 包含 has_permission 函数的上下文字典
    """

    def has_permission(operation):
        """
        检查当前用户是否有权执行特定操作
        
        权限检查逻辑：
        1. 未登录用户没有任何权限
        2. 从用户的 UserProfile 中获取角色级别
        3. 如果操作不在权限定义中，默认允许访问
        4. 比较用户角色级别与操作所需的最低级别（角色值越小，权限越高）
        5. 任何异常情况下返回 False，确保安全
        
        Args:
            operation: 要检查的操作名称，例如 'DELETE_RESIDENT'
            
        Returns:
            bool: 如果用户有权限返回 True，否则返回 False
        """
        # 检查用户是否已登录
        if not request.user.is_authenticated:
            return False

        try:
            # 获取用户角色级别（1-5，值越小权限越高）
            user_role = request.user.userprofile.role

            # 如果操作不在权限字典中，默认允许访问
            if operation not in PERMISSIONS:
                return True

            # 获取操作所需的最低权限级别
            required_level = PERMISSIONS[operation]

            # 比较用户角色与所需权限级别
            # 角色值 <= 所需级别值表示拥有足够权限
            return user_role <= required_level
        except Exception:
            # 任何异常情况下返回 False，确保安全
            return False

    # 将 has_permission 函数添加到模板上下文
    return {'has_permission': has_permission}

"""
集中权限配置文件
定义系统中所有操作的权限要求和验证逻辑
"""

import logging
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import Notification

# 设置日志记录器
logger = logging.getLogger(__name__)

# 角色级别定义
ROLE_LEVELS = {
    'SUPER_ADMIN': 1,
    'ADMIN': 2,
    'SECRETARY': 3,
    'SOCIAL_WORKER': 4
}

# 权限配置矩阵
# 格式: 操作名称 -> 所需角色级别
PERMISSIONS = {
    # Level 3+ 权限 (书记及以上)
    'DELETE_RESIDENT': ROLE_LEVELS['SECRETARY'],
    'DELETE_FAMILY': ROLE_LEVELS['SECRETARY'],

    # Level 2+ 权限 (管理员及以上)
    'PUBLISH_NOTIFICATION': ROLE_LEVELS['ADMIN'],
    'DELETE_NOTIFICATION': ROLE_LEVELS['ADMIN'],

    # 所有角色都可以执行的操作 (Level 1-4)
    'VIEW_RESIDENTS': ROLE_LEVELS['SOCIAL_WORKER'],
    'ADD_RESIDENT': ROLE_LEVELS['SOCIAL_WORKER'],
    'EDIT_RESIDENT': ROLE_LEVELS['SOCIAL_WORKER'],
    'VIEW_FAMILIES': ROLE_LEVELS['SOCIAL_WORKER'],
    'ADD_FAMILY': ROLE_LEVELS['SOCIAL_WORKER'],
    'EDIT_FAMILY': ROLE_LEVELS['SOCIAL_WORKER'],
    'VIEW_NOTIFICATIONS': ROLE_LEVELS['SOCIAL_WORKER'],
    'VIEW_COMMUNITIES': ROLE_LEVELS['SOCIAL_WORKER'],
    'VIEW_STATISTICS': ROLE_LEVELS['SOCIAL_WORKER'],
    'VIEW_PROFILE': ROLE_LEVELS['SOCIAL_WORKER'],
    'UPDATE_PROFILE': ROLE_LEVELS['SOCIAL_WORKER'],
}

# 需要额外条件检查的操作
CONDITIONAL_PERMISSIONS = {
    'DELETE_NOTIFICATION': 'check_notification_ownership',
}

# 操作名称到API端点的映射
OPERATION_TO_ENDPOINT = {
    'DELETE_RESIDENT': 'DELETE /api/residents/<id>/',
    'DELETE_FAMILY': 'DELETE /api/families/<id>/',
    'PUBLISH_NOTIFICATION': 'POST /api/notifications/',
    'DELETE_NOTIFICATION': 'DELETE /api/notifications/<id>/',
    'VIEW_RESIDENTS': 'GET /api/residents/',
    'ADD_RESIDENT': 'POST /api/residents/',
    'EDIT_RESIDENT': 'PUT /api/residents/<id>/',
    'VIEW_FAMILIES': 'GET /api/families/',
    'ADD_FAMILY': 'POST /api/families/',
    'EDIT_FAMILY': 'PUT /api/families/<id>/',
    'VIEW_NOTIFICATIONS': 'GET /api/notifications/',
    'VIEW_COMMUNITIES': 'GET /api/communities/',
    'VIEW_STATISTICS': 'GET /api/statistics/',
    'VIEW_PROFILE': 'GET /api/profile/',
    'UPDATE_PROFILE': 'PUT /api/profile/',
}


# 权限检查类
class RoleBasedPermission(permissions.BasePermission):
    """
    基于角色的权限检查类
    """

    def __init__(self, operation_name):
        self.operation_name = operation_name

    def has_permission(self, request, view):
        """
        检查用户是否有权限执行操作
        """
        # 确保用户已认证
        if not request.user.is_authenticated:
            return False

        # 获取用户角色级别
        user_role = request.user.userprofile.role

        # 检查操作是否需要权限
        if self.operation_name not in PERMISSIONS:
            # 默认为允许所有认证用户
            return True

        # 获取操作所需的角色级别
        required_level = PERMISSIONS[self.operation_name]

        # 检查用户角色级别是否满足要求
        # 角色级别数字越小，权限越高
        if user_role <= required_level:
            # 记录权限检查成功
            logger.info(
                f"权限检查成功: 用户ID={request.user.id}, 角色级别={user_role}, 操作={self.operation_name}"
            )
            return True
        else:
            # 记录权限检查失败
            logger.warning(
                f"权限检查失败: 用户ID={request.user.id}, 角色级别={user_role}, 操作={self.operation_name}, 原因=角色级别不足"
            )
            return False

    def has_object_permission(self, request, view, obj):
        """
        检查用户是否有权限操作特定对象
        """
        # 首先检查基本权限
        if not self.has_permission(request, view):
            return False

        # 检查是否需要额外的条件检查
        if self.operation_name in CONDITIONAL_PERMISSIONS:
            check_func_name = CONDITIONAL_PERMISSIONS[self.operation_name]
            check_func = globals().get(check_func_name)
            if check_func and not check_func(request, obj):
                logger.warning(
                    f"权限检查失败: 用户ID={request.user.id}, 操作={self.operation_name}, 原因=条件检查失败"
                )
                return False

        return True


# 条件检查函数


def check_notification_ownership(request, notification):
    """
    检查通知删除权限：只有发布者可以删除自己的通知
    """
    return notification.publisher == request.user


# 快捷权限类


class CanDeleteResident(RoleBasedPermission):

    def __init__(self):
        super().__init__('DELETE_RESIDENT')


class CanDeleteFamily(RoleBasedPermission):

    def __init__(self):
        super().__init__('DELETE_FAMILY')


class CanPublishNotification(RoleBasedPermission):

    def __init__(self):
        super().__init__('PUBLISH_NOTIFICATION')


class CanDeleteNotification(RoleBasedPermission):

    def __init__(self):
        super().__init__('DELETE_NOTIFICATION')


class CanViewResidents(RoleBasedPermission):

    def __init__(self):
        super().__init__('VIEW_RESIDENTS')


class CanAddResident(RoleBasedPermission):

    def __init__(self):
        super().__init__('ADD_RESIDENT')


class CanEditResident(RoleBasedPermission):

    def __init__(self):
        super().__init__('EDIT_RESIDENT')


class CanViewFamilies(RoleBasedPermission):

    def __init__(self):
        super().__init__('VIEW_FAMILIES')


class CanAddFamily(RoleBasedPermission):

    def __init__(self):
        super().__init__('ADD_FAMILY')


class CanEditFamily(RoleBasedPermission):

    def __init__(self):
        super().__init__('EDIT_FAMILY')


class CanViewNotifications(RoleBasedPermission):

    def __init__(self):
        super().__init__('VIEW_NOTIFICATIONS')

from django import template
from api.permissions import PERMISSIONS

register = template.Library()

@register.filter(name='has_permission')
def has_permission(user, operation):
    """
    检查用户是否有权限执行某个操作
    
    参数:
        user: 当前登录用户对象
        operation: 操作名称，如 'DELETE_RESIDENT'
    
    返回:
        bool: True 表示有权限，False 表示无权限
    """
    try:
        # 获取用户角色级别
        user_role = user.userprofile.role
        
        # 检查操作是否存在于权限配置中
        if operation not in PERMISSIONS:
            # 如果操作未配置权限，默认允许所有用户执行
            return True
        
        # 获取操作所需的角色级别
        required_level = PERMISSIONS[operation]
        
        # 检查用户角色级别是否满足要求
        # 角色级别数字越小，权限越高
        return user_role <= required_level
    except Exception as e:
        # 如果发生任何错误，默认返回 False，确保安全
        return False

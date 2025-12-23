"""utils.py - 社区数字化信息系统工具函数

本文件定义了系统中常用的工具函数，主要用于权限管理和数据处理。
当前包含的功能：
1. 用户权限检查函数

这些工具函数被多个视图和组件复用，确保了代码的DRY原则。
"""

from api.permissions import PERMISSIONS

def check_user_permissions(user):
    """计算用户的所有权限并返回权限字典
    
    该函数根据用户的角色级别，检查用户对所有定义操作的权限，
    返回一个字典，其中键是操作名称，值是布尔值，表示用户是否有该权限。
    
    权限检查逻辑：
    - 未登录用户没有任何权限
    - 登录用户根据其角色级别（1-5，值越小权限越高）检查权限
    - 任何异常情况下默认返回无权限，确保安全
    
    Args:
        user: 用户对象，包含用户的认证状态和用户扩展信息
        
    Returns:
        dict: 权限字典，键为操作名称，值为布尔值
        
    示例：
        >>> check_user_permissions(user)
        {
            'DELETE_RESIDENT': True,
            'PUBLISH_NOTIFICATION': False,
            'VIEW_RESIDENTS': True
        }
    """
    # 初始化权限字典
    permissions = {}
    
    # 未登录用户没有任何权限
    if not user.is_authenticated:
        for operation in PERMISSIONS.keys():
            permissions[operation] = False
        return permissions
    
    try:
        # 获取用户角色级别（1-5，值越小权限越高）
        user_role = user.userprofile.role
        
        # 检查每个操作的权限
        for operation, required_level in PERMISSIONS.items():
            # 用户角色级别 <= 操作所需级别，表示有足够权限
            permissions[operation] = user_role <= required_level
        
        return permissions
    except Exception:
        # 任何异常情况下默认返回无权限，确保安全
        for operation in PERMISSIONS.keys():
            permissions[operation] = False
        return permissions

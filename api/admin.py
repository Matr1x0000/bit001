"""admin.py - Django管理后台配置文件

本文件定义了社区数字化信息系统所有模型的管理后台配置，包括：
1. 管理站点基本设置
2. 各模型的管理类定义
3. 模型与管理类的注册

通过自定义ModelAdmin类，实现了对各模型数据的灵活管理和展示。
"""

from django_admin_index.models import AppGroup, ContentTypeProxy
from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import (Community, SocialWorker, HousingEstate, Building, Unit,
                     Apartment, Hutong, SingleHouse, ResidentialAddress,
                     UserProfile, Resident, Family, Notification, Cadre,
                     NotificationRead, NotificationAttachment)

# =============================================================================
# 管理站点基本设置
# =============================================================================
# 使用默认的admin.site实例，确保与django_admin_index正确集成
# 应用自定义的AdminSite设置到默认实例
admin.site.site_header = "社区数字化信息系统 管理后台"  # 管理后台标题
admin.site.site_title = "社区数字化信息系统 管理后台登录"  # 浏览器标签页标题
admin.site.index_title = "社区数字化信息系统 管理后台首页"  # 管理后台首页标题


# =============================================================================
# 自定义Admin类 - 社区基本信息管理
# =============================================================================
class CommunityAdmin(admin.ModelAdmin):
    """社区信息管理类
    
    用于在管理后台中管理社区基本信息，包括社区名称、办公地址、联系电话等。
    """
    list_display = ('name', 'office_address', 'office_phone', 'created_at',
                    'is_deleted')  # 列表页显示字段
    search_fields = ('name', 'office_address')  # 搜索字段
    list_filter = ('created_at', 'is_deleted')  # 筛选字段


class HousingEstateAdmin(admin.ModelAdmin):
    """小区信息管理类
    
    用于在管理后台中管理小区信息，包括小区名称、所属社区、物业公司等。
    """
    list_display = ('name', 'community', 'property_company', 'property_phone',
                    'is_deleted')  # 列表页显示字段
    search_fields = ('name', 'address')  # 搜索字段
    list_filter = ('community', 'is_deleted')  # 筛选字段


class BuildingAdmin(admin.ModelAdmin):
    """楼栋信息管理类
    
    用于在管理后台中管理楼栋信息，包括楼栋名称、所属小区、建筑类型等。
    """
    list_display = ('estate', 'name', 'building_type', 'total_floors',
                    'units_per_floor', 'is_deleted')  # 列表页显示字段
    search_fields = ('name', )  # 搜索字段
    list_filter = ('estate', 'building_type', 'is_deleted')  # 筛选字段


class UnitAdmin(admin.ModelAdmin):
    """单元信息管理类
    
    用于在管理后台中管理单元信息，包括单元名称、所属楼栋等。
    """
    list_display = ('building', 'name', 'is_deleted')  # 列表页显示字段
    search_fields = ('name', )  # 搜索字段
    list_filter = ('building', 'is_deleted')  # 筛选字段


# =============================================================================
# 自定义Admin类 - 房屋信息管理
# =============================================================================
class ApartmentAdmin(admin.ModelAdmin):
    """公寓信息管理类
    
    用于在管理后台中管理公寓信息，包括房号、所属单元等。
    """
    list_display = ('unit', 'house_number', 'is_deleted')  # 列表页显示字段
    search_fields = ('house_number', )  # 搜索字段
    list_filter = ('unit__building__estate', 'is_deleted')  # 筛选字段，支持跨表关联筛选


class HutongAdmin(admin.ModelAdmin):
    """胡同信息管理类
    
    用于在管理后台中管理胡同信息，包括胡同名称、所属社区等。
    """
    list_display = ('name', 'community', 'is_deleted')  # 列表页显示字段
    search_fields = ('name', )  # 搜索字段
    list_filter = ('community', 'is_deleted')  # 筛选字段


class SingleHouseAdmin(admin.ModelAdmin):
    """平房信息管理类
    
    用于在管理后台中管理平房信息，包括房号、所属胡同等。
    """
    list_display = ('hutong', 'house_number', 'is_deleted')  # 列表页显示字段
    search_fields = ('house_number', )  # 搜索字段
    list_filter = ('hutong__community', 'is_deleted')  # 筛选字段，支持跨表关联筛选


class ResidentialAddressAdmin(admin.ModelAdmin):
    """居住地址管理类
    
    用于在管理后台中管理居住地址信息，包括地址类型、是否为居民地址等。
    """
    list_display = ('address_type', 'is_resident', 'get_full_address',
                    'is_deleted')  # 列表页显示字段
    search_fields = ('estate__name', 'building__name', 'hutong__name'
                     )  # 搜索字段，支持跨表关联搜索
    list_filter = ('address_type', 'is_resident', 'is_deleted')  # 筛选字段

    def get_full_address(self, obj):
        """获取完整地址
        
        Args:
            obj: ResidentialAddress实例
            
        Returns:
            str: 完整地址字符串
            
        示例:
            >>> get_full_address(address_instance)
            '北京市朝阳区XX小区1号楼1单元101室'
        """
        return str(obj)

    get_full_address.short_description = '完整地址'  # 自定义字段显示名称


# =============================================================================
# 自定义Admin类 - 人员信息管理
# =============================================================================
class SocialWorkerAdmin(admin.ModelAdmin):
    """社工信息管理类
    
    用于在管理后台中管理社工信息，包括姓名、所属社区、联系方式等。
    """
    list_display = ('name', 'community', 'gender', 'phone', 'birth_date',
                    'is_secretary', 'is_baned', 'is_deleted')  # 列表页显示字段
    search_fields = ('name', 'phone')  # 搜索字段
    list_filter = ('community', 'gender', 'is_secretary', 'is_baned',
                   'is_deleted')  # 筛选字段


class CadreAdmin(admin.ModelAdmin):
    """干部信息管理类
    
    用于在管理后台中管理干部信息，包括姓名、职务、联系方式等。
    """
    list_display = ('name', 'position', 'phone', 'is_baned', 'is_deleted'
                    )  # 列表页显示字段
    search_fields = ('name', 'phone')  # 搜索字段
    list_filter = ('position', 'is_baned', 'is_deleted')  # 筛选字段


class UserProfileAdmin(admin.ModelAdmin):
    """用户资料管理类
    
    用于在管理后台中管理用户资料信息，包括用户角色、所属部门等。
    """
    list_display = ('user', 'role', 'department', 'is_baned', 'is_deleted'
                    )  # 列表页显示字段
    search_fields = ('user__username', )  # 搜索字段，关联到User模型的username字段
    list_filter = ('role', 'department', 'is_baned', 'is_deleted')  # 筛选字段


class ResidentAdmin(admin.ModelAdmin):
    """居民信息管理类
    
    用于在管理后台中管理居民信息，包括姓名、身份证号、联系方式、家庭信息等。
    """
    list_display = ('name', 'gender', 'nationality', 'id_card', 'phone',
                    'family', 'political_status', 'marital_status',
                    'education', 'job', 'is_dead', 'is_deleted')  # 列表页显示字段
    search_fields = ('name', 'id_card', 'phone')  # 搜索字段
    list_filter = ('gender', 'nationality', 'political_status',
                   'marital_status', 'education', 'job', 'is_dead',
                   'is_deleted')  # 筛选字段
    readonly_fields = ('id_card', )  # 只读字段，防止身份证号被修改


class FamilyAdmin(admin.ModelAdmin):
    """家庭信息管理类
    
    用于在管理后台中管理家庭信息，包括户号、户主姓名、居住地址等。
    """
    list_display = ('household_number', 'owner_name', 'residential_address',
                    'contact_phone', 'is_deleted')  # 列表页显示字段
    search_fields = ('household_number', 'owner_name')  # 搜索字段
    list_filter = ('residential_address__address_type', 'is_deleted'
                   )  # 筛选字段，支持跨表关联筛选


# =============================================================================
# 自定义Admin类 - 通知管理
# =============================================================================
class NotificationAdmin(admin.ModelAdmin):
    """通知信息管理类
    
    用于在管理后台中管理通知信息，包括标题、内容、发布者、发布时间等。
    """
    list_display = ('title', 'notification_type', 'publisher', 'publish_time',
                    'valid_until', 'view_count')  # 列表页显示字段
    search_fields = ('title', 'content')  # 搜索字段
    list_filter = ('notification_type', 'publisher', 'publish_time')  # 筛选字段
    readonly_fields = ('publish_time', 'view_count')  # 只读字段，由系统自动生成


class NotificationReadAdmin(admin.ModelAdmin):
    """通知阅读记录管理类
    
    用于在管理后台中管理通知阅读记录，包括通知、阅读用户、阅读状态等。
    """
    list_display = ('notification', 'user', 'is_read', 'read_time')  # 列表页显示字段
    search_fields = ('notification__title', 'user__username')  # 搜索字段，支持跨表关联搜索
    list_filter = ('is_read', 'read_time')  # 筛选字段


class NotificationAttachmentAdmin(admin.ModelAdmin):
    """通知附件管理类
    
    用于在管理后台中管理通知附件，包括附件文件名、上传时间等。
    """
    list_display = ('notification', 'filename', 'upload_time')  # 列表页显示字段
    search_fields = ('notification__title', 'filename')  # 搜索字段，支持跨表关联搜索
    list_filter = ('notification__notification_type', )  # 筛选字段，支持跨表关联筛选


# =============================================================================
# 注册所有模型到admin站点
# =============================================================================
# 社区基本信息管理
admin.site.register(Community, CommunityAdmin)  # 注册社区模型
admin.site.register(HousingEstate, HousingEstateAdmin)  # 注册小区模型
admin.site.register(Building, BuildingAdmin)  # 注册楼栋模型
admin.site.register(Unit, UnitAdmin)  # 注册单元模型

# 房屋信息管理
admin.site.register(Apartment, ApartmentAdmin)  # 注册公寓模型
admin.site.register(Hutong, HutongAdmin)  # 注册胡同模型
admin.site.register(SingleHouse, SingleHouseAdmin)  # 注册平房模型
admin.site.register(ResidentialAddress, ResidentialAddressAdmin)  # 注册居住地址模型

# 人员信息管理
admin.site.register(SocialWorker, SocialWorkerAdmin)  # 注册社工模型
admin.site.register(UserProfile, UserProfileAdmin)  # 注册用户资料模型
admin.site.register(Resident, ResidentAdmin)  # 注册居民模型
admin.site.register(Family, FamilyAdmin)  # 注册家庭模型
admin.site.register(Cadre, CadreAdmin)  # 注册干部模型

# 通知管理
admin.site.register(Notification, NotificationAdmin)  # 注册通知模型
admin.site.register(NotificationRead, NotificationReadAdmin)  # 注册通知阅读记录模型
admin.site.register(NotificationAttachment,
                    NotificationAttachmentAdmin)  # 注册通知附件模型

from django_admin_index.models import AppGroup, ContentTypeProxy
from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import (Community, SocialWorker, HousingEstate, Building, Unit,
                     Apartment, Hutong, SingleHouse, ResidentialAddress,
                     UserProfile, Resident, Family, Notification, Cadre,
                     NotificationRead, NotificationAttachment)

# 使用默认的admin.site实例，确保与django_admin_index正确集成
# 应用自定义的AdminSite设置到默认实例
admin.site.site_header = "社区数字化信息系统 管理后台"
admin.site.site_title = "社区数字化信息系统 管理后台登录"
admin.site.index_title = "社区数字化信息系统 管理后台首页"


# 自定义Admin类
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'office_address', 'office_phone', 'created_at')
    search_fields = ('name', 'office_address')
    list_filter = ('created_at', )


class SocialWorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'community', 'gender', 'phone', 'birth_date',
                    'is_secretary', 'is_baned')
    search_fields = ('name', 'phone')
    list_filter = ('community', 'gender', 'is_secretary', 'is_baned')


class CadreAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'phone', 'is_baned')
    search_fields = ('name', 'phone')
    list_filter = ('position', 'is_baned')


class HousingEstateAdmin(admin.ModelAdmin):
    list_display = ('name', 'community', 'property_company', 'property_phone')
    search_fields = ('name', 'address')
    list_filter = ('community', )


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('estate', 'name', 'building_type', 'total_floors',
                    'units_per_floor')
    search_fields = ('name', )
    list_filter = ('estate', 'building_type')


class UnitAdmin(admin.ModelAdmin):
    list_display = ('building', 'name')
    search_fields = ('name', )
    list_filter = ('building', )


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('unit', 'house_number')
    search_fields = ('house_number', )
    list_filter = ('unit__building__estate', )


class HutongAdmin(admin.ModelAdmin):
    list_display = ('name', 'community')
    search_fields = ('name', )
    list_filter = ('community', )


class SingleHouseAdmin(admin.ModelAdmin):
    list_display = ('hutong', 'house_number')
    search_fields = ('house_number', )
    list_filter = ('hutong__community', )


class ResidentialAddressAdmin(admin.ModelAdmin):
    list_display = ('address_type', 'is_resident', 'get_full_address')
    search_fields = ('estate__name', 'building__name', 'hutong__name')
    list_filter = ('address_type', 'is_resident')

    def get_full_address(self, obj):
        return str(obj)

    get_full_address.short_description = '完整地址'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'is_baned')
    search_fields = ('user__username', )
    list_filter = ('role', 'department', 'is_baned')


class ResidentAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'nationality', 'id_card', 'phone',
                    'family', 'political_status', 'marital_status',
                    'education', 'job', 'is_dead')
    search_fields = ('name', 'id_card', 'phone')
    list_filter = ('gender', 'nationality', 'political_status',
                   'marital_status', 'education', 'job', 'is_dead')
    readonly_fields = ('id_card', )


class FamilyAdmin(admin.ModelAdmin):
    list_display = ('household_number', 'owner_name', 'residential_address',
                    'contact_phone')
    search_fields = ('household_number', 'owner_name')
    list_filter = ('residential_address__address_type', )


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'publisher', 'publish_time',
                    'valid_until', 'view_count')
    search_fields = ('title', 'content')
    list_filter = ('notification_type', 'publisher', 'publish_time')
    readonly_fields = ('publish_time', 'view_count')


class NotificationReadAdmin(admin.ModelAdmin):
    list_display = ('notification', 'user', 'is_read', 'read_time')
    search_fields = ('notification__title', 'user__username')
    list_filter = ('is_read', 'read_time')


class NotificationAttachmentAdmin(admin.ModelAdmin):
    list_display = ('notification', 'filename', 'upload_time')
    search_fields = ('notification__title', 'filename')
    list_filter = ('notification__notification_type', )


# 注册所有模型到admin站点
# 社区基本信息管理
admin.site.register(Community, CommunityAdmin)
admin.site.register(HousingEstate, HousingEstateAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Unit, UnitAdmin)

# 房屋信息管理
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Hutong, HutongAdmin)
admin.site.register(SingleHouse, SingleHouseAdmin)
admin.site.register(ResidentialAddress, ResidentialAddressAdmin)

# 人员信息管理
admin.site.register(SocialWorker, SocialWorkerAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Resident, ResidentAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Cadre, CadreAdmin)

# 通知管理
admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationRead, NotificationReadAdmin)
admin.site.register(NotificationAttachment, NotificationAttachmentAdmin)

# 使用django_admin_index配置应用模块顺序和分组
# 注意：在Django管理后台中，可以通过"应用组"菜单手动调整模块顺序和分组
# 以下是通过代码配置的示例，实际使用中可以通过管理后台界面进行可视化配置

# 配置说明：
# 1. 登录Django管理后台，会看到新增的"应用组"菜单
# 2. 通过"应用组"菜单可以创建和管理应用分组
# 3. 每个分组可以添加多个模型，并通过拖拽调整顺序
# 4. 可以设置分组的名称、slug和包含的模型
# 5. 可以为分组添加自定义链接

# 配置示例（实际使用中建议通过管理后台界面配置）：

# 创建社区管理分组
# community_group, created = AppGroup.objects.get_or_create(
#     name="社区管理",
#     slug="community-management"
# )

# # 批量添加多个模型到分组
# # 先获取多个ContentTypeProxy实例
# community_content_types = ContentTypeProxy.objects.filter(
#     app_label="api", model__in=["community", "socialworker"])
# # 然后批量添加到分组
# community_group.models.add(*community_content_types)

# # 创建地址管理分组
# address_group, created = AppGroup.objects.get_or_create(
#     name="地址管理",
#     slug="address-management"
# )
# # 批量添加多个模型到分组
# # 先获取多个ContentTypeProxy实例
# address_content_types = ContentTypeProxy.objects.filter(
#     app_label="api", model__in=["housingestate", "building", "unit", "apartment", "hutong", "singlehouse", "residentialaddress"])
# # 然后批量添加到分组
# address_group.models.add(*address_content_types)

# # 创建居民管理分组
# resident_group, created = AppGroup.objects.get_or_create(
#     name="居民管理",
#     slug="resident-management"
# )
# # 批量添加多个模型到分组
# # 先获取多个ContentTypeProxy实例
# resident_content_types = ContentTypeProxy.objects.filter(
#     app_label="api", model__in=["resident", "family"])
# # 然后批量添加到分组
# resident_group.models.add(*resident_content_types)

# # 创建系统管理分组
# system_group, created = AppGroup.objects.get_or_create(
#     name="系统管理",
#     slug="system-management"
# )
# # 批量添加多个模型到分组
# # 先获取多个ContentTypeProxy实例
# system_content_types = ContentTypeProxy.objects.filter(
#     app_label="api", model__in=["userprofile", "notification", "notificationread"])
# # 然后批量添加到分组
# system_group.models.add(*system_content_types)

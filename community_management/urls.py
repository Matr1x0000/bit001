"""
URL configuration for community_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from api.views import (
    CommunityViewSet, SocialWorkerViewSet, HousingEstateViewSet,
    BuildingViewSet, UnitViewSet, ApartmentViewSet, HutongViewSet,
    SingleHouseViewSet, ResidentialAddressViewSet, UserProfileViewSet,
    ResidentViewSet, FamilyViewSet, NotificationViewSet,
    NotificationReadViewSet, NotificationAttachmentViewSet, test_view, index,
    dashboard, residents_view, families_view, notifications_view,
    analytics_view, addresses_view, settings_view, test_auth, add_resident,
    edit_resident, delete_resident, add_family, edit_family,
    notification_read_status)

# 创建路由器并注册我们的视图集
# 创建 DRF 默认路由器，用于自动注册视图集并生成对应的 RESTful API 路由
router = DefaultRouter()
# 注册社区相关的 RESTful API 路由，访问路径为 /api/communities/
router.register(r'communities', CommunityViewSet)
router.register(r'social-workers', SocialWorkerViewSet)
router.register(r'housing-estates', HousingEstateViewSet)
router.register(r'buildings', BuildingViewSet)
router.register(r'units', UnitViewSet)
router.register(r'apartments', ApartmentViewSet)
router.register(r'hutongs', HutongViewSet)
router.register(r'single-houses', SingleHouseViewSet)
router.register(r'residential-addresses', ResidentialAddressViewSet)
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'residents', ResidentViewSet)
router.register(r'families', FamilyViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'notification-reads', NotificationReadViewSet)
router.register(r'notification-attachments', NotificationAttachmentViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('login/',
         auth_views.LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(next_page='login'),
         name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('addresses/', addresses_view, name='addresses'),
    path('residents/', residents_view, name='residents'),
    path('families/', families_view, name='families'),
    path('notifications/', notifications_view, name='notifications'),
    path('analytics/', analytics_view, name='analytics'),
    path('settings/', settings_view, name='settings'),
    path('test-auth/', test_auth, name='test_auth'),
    # API routes
    path('api/', include(router.urls)),
    # 测试路由
    path('test/', test_view, name='test'),
    # 通知已读状态API
    path('api/notification-read-status/<int:notification_id>/',
         notification_read_status,
         name='notification_read_status'),
    # 添加居民路由
    path('add-resident/', add_resident, name='add_resident'),
    # 添加家庭路由
    path('add-family/', add_family, name='add_family'),
    # 编辑家庭路由
    path('edit-family/<int:family_id>/', edit_family, name='edit_family'),
    # 编辑居民路由
    path('edit-resident/<int:resident_id>/',
         edit_resident,
         name='edit_resident'),
    # 删除居民路由
    path('delete-resident/<int:resident_id>/',
         delete_resident,
         name='delete_resident'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

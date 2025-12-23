# 开发贡献指南 (Contributing Guidelines)

## 目录
- [开发贡献指南 (Contributing Guidelines)](#开发贡献指南-contributing-guidelines)
  - [目录](#目录)
  - [前言](#前言)
  - [开发环境搭建](#开发环境搭建)
    - [环境要求](#环境要求)
    - [项目初始化](#项目初始化)
    - [开发工具配置](#开发工具配置)
  - [代码规范](#代码规范)
    - [Python编码规范](#python编码规范)
    - [Django开发规范](#django开发规范)
    - [数据库设计规范](#数据库设计规范)
    - [API设计规范](#api设计规范)
    - [前端开发规范](#前端开发规范)
  - [Git工作流](#git工作流)
    - [分支管理策略](#分支管理策略)
    - [提交信息规范](#提交信息规范)
    - [代码审查流程](#代码审查流程)
  - [开发流程](#开发流程)
    - [功能开发流程](#功能开发流程)
    - [Bug修复流程](#bug修复流程)
    - [代码测试要求](#代码测试要求)
  - [文档规范](#文档规范)
    - [代码文档](#代码文档)
    - [API文档](#api文档)
    - [用户文档](#用户文档)
  - [安全规范](#安全规范)
    - [代码安全](#代码安全)
    - [数据安全](#数据安全)
    - [部署安全](#部署安全)
  - [性能优化](#性能优化)
    - [数据库优化](#数据库优化)
    - [缓存策略](#缓存策略)
    - [查询优化](#查询优化)
  - [故障排除](#故障排除)
    - [常见问题](#常见问题)
    - [调试技巧](#调试技巧)
    - [日志记录](#日志记录)
  - [发布流程](#发布流程)
    - [版本管理](#版本管理)
    - [发布准备](#发布准备)
    - [回滚策略](#回滚策略)

## 前言

欢迎参与社区管理系统的开发！本指南旨在帮助开发者快速了解项目规范，确保代码质量和团队协作效率。请在开始开发前仔细阅读本指南。

## 开发环境搭建

### 环境要求

#### 必需环境
- **Python**: 3.11+
- **pip**: Python包管理器
- **Git**: 版本控制系统
- **Virtual Environment**: 虚拟环境工具

#### 推荐开发工具
- **IDE**: PyCharm / VS Code
- **数据库工具**: DBeaver / pgAdmin
- **API测试**: Postman / Insomnia
- **Git客户端**: GitKraken / SourceTree

### 项目初始化

#### 1. 克隆项目
```bash
git clone [项目仓库地址]
cd bit002
```

#### 2. 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

#### 3. 安装依赖包
```bash
# 安装Django及相关包
pip install django==5.2.8
django-admin startproject community_management .
pip install djangorestframework
django-admin startapp api
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install django-filter
pip install django-admin-index
pip install django-ordered-model

# 建议创建requirements.txt文件
echo "Django==5.2.8" > requirements.txt
echo "djangorestframework" >> requirements.txt
echo "djangorestframework-simplejwt" >> requirements.txt
echo "django-cors-headers" >> requirements.txt
echo "django-filter" >> requirements.txt
echo "django-admin-index" >> requirements.txt
echo "django-ordered-model" >> requirements.txt
```

#### 4. 数据库配置
```bash
# 运行迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

#### 5. 启动开发服务器
```bash
python manage.py runserver
```

### 开发工具配置

#### VS Code配置
创建 `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

#### PyCharm配置
1. 设置Python解释器为虚拟环境
2. 启用Django支持
3. 配置运行/调试配置
4. 设置代码检查工具

## 代码规范

### Python编码规范

#### 1. 遵循PEP 8
```python
# 正确的命名规范
class Community(models.Model):
    name = models.CharField(max_length=50, verbose_name="社区名称")
    
    def get_full_name(self):
        return f"平泉市 - {self.name}"

# 错误的命名规范
class community(models.Model):
    Name = models.CharField(max_length=50)
    
    def getFullName(self):
        return "平泉市 - " + self.name
```

#### 2. 导入规范
```python
# 标准库导入
import os
import sys
from datetime import datetime

# 第三方库导入
from django.db import models
from rest_framework import serializers

# 本地应用导入
from api.permissions import PERMISSIONS
from .models import Community
```

#### 3. 文档字符串
```python
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
    pass
```

### Django开发规范

#### 1. 模型设计规范
```python
# 良好的模型设计
class Community(models.Model):
    name = models.CharField(max_length=50, verbose_name="社区名称")
    office_address = models.CharField(max_length=100, verbose_name="办公地址", null=True, blank=True)
    is_deleted = models.BooleanField(default=False, verbose_name="是否已删除", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "1.社区"
        verbose_name_plural = "1.社区列表"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_deleted', 'created_at']),
        ]

    def __str__(self):
        return f"平泉市 - {self.name}"
```

#### 2. 视图开发规范
```python
# 基于类的视图
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.filter(is_deleted=False)
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'office_address']
    
    def get_queryset(self):
        # 添加权限过滤逻辑
        if self.request.user.userprofile.role <= 2:
            return Community.objects.filter(is_deleted=False)
        return Community.objects.filter(
            is_deleted=False,
            id=self.request.user.userprofile.community_id
        )
```

#### 3. URL配置规范
```python
# 版本化的API URL
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'communities', CommunityViewSet)
router.register(r'residents', ResidentViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('api.urls.auth')),
]
```

### 数据库设计规范

#### 1. 命名规范
- 表名使用小写，多个单词用下划线分隔
- 字段名使用小写，多个单词用下划线分隔
- 外键字段使用 `_id` 后缀
- 布尔字段使用 `is_` 前缀

#### 2. 字段设计
```python
# 推荐的字段设计
is_deleted = models.BooleanField(
    default=False,
    verbose_name="是否已删除",
    db_index=True,
    help_text="逻辑删除标记，用于软删除"
)

# 不推荐的字段设计
deleted = models.BooleanField(default=False)  # 缺少详细配置
```

#### 3. 索引优化
```python
class Meta:
    indexes = [
        models.Index(fields=['is_deleted', 'created_at']),
        models.Index(fields=['community', 'name']),
    ]
```

### API设计规范

#### 1. RESTful设计
```python
# 标准的RESTful接口
GET    /api/v1/communities/          # 获取列表
POST   /api/v1/communities/          # 创建
GET    /api/v1/communities/{id}/     # 获取详情
PUT    /api/v1/communities/{id}/     # 更新
DELETE /api/v1/communities/{id}/     # 删除
```

#### 2. 响应格式
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "name": "阳光社区",
        "office_address": "平泉市阳光街道1号"
    },
    "pagination": {
        "total": 100,
        "page": 1,
        "page_size": 10
    }
}
```

#### 3. 错误处理
```python
from rest_framework.exceptions import APIException

class CommunityNotFound(APIException):
    status_code = 404
    default_detail = '社区不存在或已被删除'
    default_code = 'community_not_found'
```

### 前端开发规范

#### 1. JavaScript规范
```javascript
// 使用ES6+语法
const getResidents = async (communityId) => {
    try {
        const response = await fetch(`/api/v1/communities/${communityId}/residents/`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('获取居民数据失败:', error);
        throw error;
    }
};
```

#### 2. HTML模板规范
```html
<!-- 使用Django模板规范 -->
{% extends "base.html" %}
{% load static %}

{% block title %}社区管理{% endblock %}

{% block content %}
<div class="container">
    <h1>{{ community.name }}</h1>
    {% if has_permission 'EDIT_COMMUNITY' %}
        <button class="btn btn-primary" onclick="editCommunity()">编辑</button>
    {% endif %}
</div>
{% endblock %}
```

## Git工作流

### 分支管理策略

#### 主要分支
- `main`: 生产环境代码
- `develop`: 开发环境代码
- `feature/*`: 功能开发分支
- `bugfix/*`: Bug修复分支
- `hotfix/*`: 紧急修复分支
- `release/*`: 发布准备分支

#### 分支命名规范
```bash
# 功能分支
feature/user-authentication
feature/community-management

# Bug修复分支
bugfix/login-error
bugfix/data-validation

# 热修复分支
hotfix/security-patch
hotfix/critical-bug
```

### 提交信息规范

#### 提交格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 提交类型
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

#### 提交示例
```
feat(auth): 添加JWT认证功能

- 实现用户登录认证
- 添加令牌刷新机制
- 配置权限验证中间件

Closes #123
```

### 代码审查流程

#### 1. 创建Pull Request
- 从功能分支向develop分支发起PR
- 填写详细的PR描述
- 关联相关的Issue

#### 2. 代码审查要点
- 功能完整性
- 代码规范性
- 测试覆盖率
- 性能影响
- 安全考虑

#### 3. 审查通过标准
- 至少1人审查通过
- 所有CI检查通过
- 无冲突可合并

## 开发流程

### 功能开发流程

#### 1. 需求分析
- 理解业务需求
- 评估技术可行性
- 制定开发计划

#### 2. 设计阶段
- 数据库设计
- API接口设计
- 前端界面设计

#### 3. 编码实现
- 遵循代码规范
- 编写单元测试
- 添加必要注释

#### 4. 测试验证
- 单元测试
- 集成测试
- 功能测试

#### 5. 代码审查
- 自我审查
- 同事审查
- 修改优化

### Bug修复流程

#### 1. Bug报告
- 详细描述问题
- 提供重现步骤
- 标注优先级

#### 2. 问题分析
- 定位问题原因
- 评估影响范围
- 制定修复方案

#### 3. 修复实施
- 编写修复代码
- 添加回归测试
- 验证修复效果

#### 4. 代码合并
- 提交修复代码
- 通过代码审查
- 合并到主分支

### 代码测试要求

#### 1. 测试类型
- **单元测试**: 测试单个函数或类
- **集成测试**: 测试模块间交互
- **功能测试**: 测试完整功能流程
- **性能测试**: 测试系统性能指标

#### 2. 测试覆盖率
- 核心业务逻辑: 90%+
- 数据模型: 95%+
- API接口: 85%+
- 工具函数: 80%+

#### 3. 测试编写规范
```python
# 测试文件命名
class CommunityModelTest(TestCase):
    def setUp(self):
        self.community = Community.objects.create(name="测试社区")
    
    def test_community_creation(self):
        """测试社区创建功能"""
        self.assertEqual(self.community.name, "测试社区")
        self.assertFalse(self.community.is_deleted)
    
    def test_community_string_representation(self):
        """测试社区字符串表示"""
        self.assertEqual(str(self.community), "平泉市 - 测试社区")
```

## 文档规范

### 代码文档

#### 1. 函数文档
```python
def has_permission(operation):
    """
    检查当前用户是否有权执行特定操作
    
    权限检查逻辑：
    1. 未登录用户没有任何权限
    2. 从用户的 UserProfile 中获取角色级别
    3. 如果操作不在权限定义中，默认允许访问
    4. 比较用户角色级别与操作所需的最低级别
    5. 任何异常情况下返回 False，确保安全
    
    Args:
        operation: 要检查的操作名称，例如 'DELETE_RESIDENT'
        
    Returns:
        bool: 如果用户有权限返回 True，否则返回 False
        
    Raises:
        ValueError: 当操作名称为空时
    """
    pass
```

#### 2. 类文档
```python
class Community(models.Model):
    """
    社区模型，用于存储社区基本信息
    
    该模型包含社区的名称、地址、联系方式等基本信息，
    支持逻辑删除和软删除功能。
    
    Attributes:
        name: 社区名称，最大长度50字符
        office_address: 办公地址，可选字段
        office_phone: 办公电话，可选字段
        is_deleted: 逻辑删除标记，默认False
        created_at: 创建时间，自动设置
        updated_at: 更新时间，自动更新
    
    Examples:
        >>> community = Community(name="阳光社区")
        >>> community.save()
        >>> str(community)
        '平泉市 - 阳光社区'
    """
    pass
```

### API文档

#### 1. 接口说明
```markdown
## 获取社区列表

### 描述
获取系统中的所有社区列表，支持分页和过滤。

### 请求信息
- **URL**: `/api/v1/communities/`
- **方法**: `GET`
- **认证**: 需要JWT令牌

### 请求参数
| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认10 |
| name | string | 否 | 社区名称过滤 |

### 响应示例
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "id": 1,
            "name": "阳光社区",
            "office_address": "平泉市阳光街道1号",
            "office_phone": "0314-1234567",
            "created_at": "2025-01-01T00:00:00Z"
        }
    ],
    "pagination": {
        "total": 50,
        "page": 1,
        "page_size": 10,
        "pages": 5
    }
}
```
```

### 用户文档

#### 1. 功能说明文档
```markdown
## 社区管理功能

### 功能概述
社区管理功能允许管理员创建、编辑、删除和查看社区信息。

### 使用步骤
1. 登录系统
2. 点击左侧菜单"社区管理"
3. 点击"新建社区"按钮
4. 填写社区信息
5. 点击"保存"按钮

### 注意事项
- 社区名称不能为空
- 办公电话格式需要正确
- 只有超级管理员可以删除社区
```

## 安全规范

### 代码安全

#### 1. 输入验证
```python
# 正确的输入验证
def create_resident(request):
    serializer = ResidentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# 错误的输入验证
def create_resident(request):
    name = request.data.get('name')
    # 没有验证直接保存
    Resident.objects.create(name=name)
```

#### 2. SQL注入防护
```python
# 使用ORM，避免SQL注入
residents = Resident.objects.filter(name__contains=search_term)

# 避免原始SQL
# 错误示例：
# cursor.execute(f"SELECT * FROM residents WHERE name LIKE '%{search_term}%'")
```

#### 3. XSS防护
```python
# Django自动转义，不要关闭
{{ user_input }}  # 安全
{{ user_input|safe }}  # 危险，需要确保内容安全
```

### 数据安全

#### 1. 敏感信息处理
```python
# 环境变量中存储敏感信息
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')

# 不要在代码中硬编码
# 错误：SECRET_KEY = 'hardcoded-secret-key'
```

#### 2. 数据加密
```python
# 敏感数据加密存储
from cryptography.fernet import Fernet

cipher = Fernet(key)
encrypted_data = cipher.encrypt(sensitive_data.encode())
```

#### 3. 访问控制
```python
# 严格的权限检查
def delete_community(request, community_id):
    if not request.user.userprofile.role == 1:  # 只有超级管理员
        return Response({'error': '权限不足'}, status=403)
    # 删除逻辑
```

### 部署安全

#### 1. 配置安全
```python
# 生产环境配置
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

#### 2. 依赖安全
```bash
# 定期检查依赖漏洞
pip install safety
safety check

# 更新依赖包
pip list --outdated
pip install --upgrade package_name
```

## 性能优化

### 数据库优化

#### 1. 查询优化
```python
# 使用select_related优化外键查询
communities = Community.objects.select_related('admin').all()

# 使用prefetch_related优化多对多查询
communities = Community.objects.prefetch_related('residents').all()

# 避免N+1查询问题
# 错误：
for community in Community.objects.all():
    print(community.admin.name)  # 每次都会查询数据库
```

#### 2. 索引优化
```python
# 为常用查询字段添加索引
class Resident(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    id_card = models.CharField(max_length=18, unique=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['community', 'name']),
            models.Index(fields=['id_card']),
        ]
```

#### 3. 分页优化
```python
# 使用游标分页提高大数据集性能
from rest_framework.pagination import CursorPagination

class ResidentPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at'
```

### 缓存策略

#### 1. Django缓存框架
```python
# 视图缓存
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 缓存15分钟
def community_list(request):
    communities = Community.objects.all()
    return render(request, 'communities.html', {'communities': communities})
```

#### 2. 数据库查询缓存
```python
# 缓存常用查询结果
from django.core.cache import cache

def get_community_stats():
    stats = cache.get('community_stats')
    if stats is None:
        stats = calculate_community_stats()
        cache.set('community_stats', stats, 300)  # 缓存5分钟
    return stats
```

### 查询优化

#### 1. 使用values()和values_list()
```python
# 只需要特定字段时
resident_names = Resident.objects.filter(community=community).values_list('name', flat=True)

# 需要多个字段时
resident_info = Resident.objects.values('name', 'phone', 'address')
```

#### 2. 避免不必要的查询
```python
# 使用exists()检查存在性
if Resident.objects.filter(community=community).exists():
    # 执行某些操作

# 使用count()获取数量
resident_count = Resident.objects.filter(community=community).count()
```

## 故障排除

### 常见问题

#### 1. 数据库连接问题
```python
# 检查数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 检查数据库文件权限
# 确保SQLite文件有读写权限
```

#### 2. 静态文件问题
```bash
# 收集静态文件
python manage.py collectstatic

# 检查静态文件配置
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

#### 3. 迁移问题
```bash
# 如果迁移出错，可以尝试
python manage.py migrate --fake  # 标记为已应用
python manage.py migrate --fake-initial  # 初始迁移
python manage.py showmigrations  # 查看迁移状态
```

### 调试技巧

#### 1. Django调试工具
```python
# 使用pdb调试
import pdb; pdb.set_trace()

# 使用Django调试工具栏
# 安装django-debug-toolbar
pip install django-debug-toolbar

# 配置settings.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

#### 2. 日志记录
```python
# 配置日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# 在代码中使用日志
import logging
logger = logging.getLogger(__name__)
logger.debug('调试信息')
logger.error('错误信息')
```

### 日志记录

#### 1. 业务日志
```python
# 记录重要业务操作
import logging

logger = logging.getLogger('business')

def create_resident(resident_data):
    resident = Resident.objects.create(**resident_data)
    logger.info(f'创建居民档案: {resident.name} (ID: {resident.id})')
    return resident
```

#### 2. 错误日志
```python
# 记录异常信息
def delete_community(community_id):
    try:
        community = Community.objects.get(id=community_id)
        community.delete()
    except Community.DoesNotExist:
        logger.error(f'删除社区失败: 社区不存在 (ID: {community_id})')
        raise
    except Exception as e:
        logger.error(f'删除社区失败: {str(e)} (ID: {community_id})')
        raise
```

## 发布流程

### 版本管理

#### 1. 语义化版本
- **主版本号(Major)**: 不兼容的API修改
- **次版本号(Minor)**: 向下兼容的功能性新增
- **修订号(Patch)**: 向下兼容的问题修正

格式: `主版本号.次版本号.修订号` (如: 1.2.3)

#### 2. 版本标签
```bash
# 创建版本标签
git tag -a v1.0.0 -m "发布版本1.0.0"
git push origin v1.0.0

# 查看标签
git tag -l
```

### 发布准备

#### 1. 发布检查清单
- [ ] 所有功能测试通过
- [ ] 代码审查完成
- [ ] 文档更新完成
- [ ] 数据库迁移测试
- [ ] 性能测试通过
- [ ] 安全扫描通过

#### 2. 发布说明
```markdown
# 版本 1.0.0 发布说明

## 新功能
- 社区管理功能
- 居民档案管理
- 权限控制系统

## 改进
- 优化数据库查询性能
- 改进用户界面体验

## 修复
- 修复登录页面样式问题
- 修复数据导出功能异常

## 已知问题
- 暂无
```

### 回滚策略

#### 1. 代码回滚
```bash
# 回滚到上一个版本
git revert HEAD

# 回滚到指定版本
git reset --hard v0.9.0
git push origin main --force
```

#### 2. 数据库回滚
```bash
# 回滚迁移
python manage.py migrate api 0004

# 备份恢复
pg_restore -d community_db backup.sql
```

#### 3. 紧急回滚流程
1. 立即停止服务
2. 回滚代码版本
3. 回滚数据库迁移
4. 恢复数据备份
5. 重新启动服务
6. 验证系统状态

---

## 联系方式

如果您在开发过程中遇到问题，可以通过以下方式联系项目维护者：

- **Issue跟踪**: 在GitHub仓库提交Issue
- **邮件联系**: [项目维护者邮箱]
- **技术讨论**: [技术讨论群组]

## 更新记录

- 2025-12-29: 创建开发贡献指南
- 文档版本: v1.0.0

---

**感谢您对社区管理系统开发的贡献！**
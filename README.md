# 社区管理系统 (Community Management System)

## 项目简介

社区管理系统是一个基于Django框架开发的现代化社区管理平台，专为平泉市社区管理设计。系统提供完整的社区信息管理、居民档案管理、社区工作者管理等功能，支持多角色权限控制和数据可视化分析。

## 主要功能

### 🏘️ 社区管理
- 社区基本信息管理
- 办公地址和联系方式维护
- 社区状态管理（正常/删除）

### 👥 居民管理
- 居民档案信息管理
- 居民与家庭关系管理
- 居民状态跟踪
- 批量导入导出功能

### 👨‍💼 社区工作者管理
- 社区工作者信息管理
- 角色权限分配
- 工作职责记录

### 🏠 住房管理
- 小区信息管理
- 楼栋信息管理
- 单元和房屋信息管理
- 住房状态跟踪

### 📊 数据分析
- 社区数据统计
- 居民分布分析
- 可视化图表展示
- 数据导出功能

### 🔐 权限管理
- 多级角色权限控制（1-5级，数值越小权限越高）
- 基于角色的访问控制（RBAC）
- 细粒度权限检查
- 安全的JWT认证

## 技术栈

### 后端技术
- **Django 5.2.8**: Python Web框架
- **Django REST Framework**: API开发框架
- **djangorestframework-simplejwt**: JWT认证
- **django-cors-headers**: CORS跨域支持
- **django-filter**: 数据过滤
- **django-admin-index**: 后台管理优化
- **SQLite**: 开发数据库

### 前端技术
- **HTML5/CSS3/JavaScript**: 基础前端技术
- **Bootstrap**: UI框架（通过Django Admin）
- **Chart.js**: 数据可视化（推测）

### 开发工具
- **Python 3.11+**: 编程语言
- **Git**: 版本控制
- **VS Code/PyCharm**: 开发环境

## 项目结构

```
community_management/     # Django项目配置
├── __init__.py
├── settings.py          # 项目配置
├── urls.py              # URL路由配置
├── wsgi.py              # WSGI配置
└── asgi.py              # ASGI配置

api/                     # 核心业务应用
├── models.py            # 数据模型
├── views/               # 视图模块
│   ├── auth.py         # 认证相关视图
│   ├── communities.py  # 社区管理视图
│   ├── residents.py    # 居民管理视图
│   ├── housing.py      # 住房管理视图
│   └── ...
├── serializers.py       # 数据序列化
├── permissions.py       # 权限定义
├── context_processors.py # 模板上下文处理器
└── migrations/         # 数据库迁移文件

static/                  # 静态文件
├── css/                # 样式文件
└── js/                 # JavaScript文件

templates/               # HTML模板文件
├── base.html           # 基础模板
├── dashboard.html      # 仪表板
├── login.html          # 登录页面
└── ...

manage.py               # Django管理脚本
db.sqlite3              # SQLite数据库文件
```

## 快速开始

### 环境要求
- Python 3.11+
- pip包管理器
- Git

### 安装步骤

1. **克隆项目**
```bash
git clone [项目仓库地址]
cd bit002
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install django==5.2.8
django-admin startproject community_management .
pip install djangorestframework
django-admin startapp api
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install django-filter
pip install django-admin-index
pip install django-ordered-model
```

4. **数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **创建超级用户**
```bash
python manage.py createsuperuser
```

6. **运行开发服务器**
```bash
python manage.py runserver
```

7. **访问应用**
- 管理后台: http://127.0.0.1:8000/admin/
- 应用主页: http://127.0.0.1:8000/

## 配置说明

### 主要配置项

#### 数据库配置
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### 认证配置
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

#### JWT配置
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

#### 国际化配置
```python
LANGUAGE_CODE = 'Zh-hans'
TIME_ZONE = 'Asia/Shanghai'
```

## API接口

系统提供RESTful API接口，主要包括：

### 认证接口
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/logout/` - 用户登出
- `POST /api/auth/refresh/` - JWT令牌刷新

### 社区管理接口
- `GET /api/communities/` - 获取社区列表
- `POST /api/communities/` - 创建社区
- `GET /api/communities/{id}/` - 获取社区详情
- `PUT /api/communities/{id}/` - 更新社区信息
- `DELETE /api/communities/{id}/` - 删除社区

### 居民管理接口
- `GET /api/residents/` - 获取居民列表
- `POST /api/residents/` - 创建居民档案
- `GET /api/residents/{id}/` - 获取居民详情
- `PUT /api/residents/{id}/` - 更新居民信息
- `DELETE /api/residents/{id}/` - 删除居民

### 数据分析接口
- `GET /api/analytics/dashboard/` - 获取仪表板数据
- `GET /api/analytics/statistics/` - 获取统计数据
- `GET /api/analytics/export/` - 导出数据报告

详细API文档请参考 [API文档](docs/API.md)。

## 权限系统

系统采用基于角色的访问控制（RBAC），权限级别分为5级：

| 级别 | 角色 | 权限范围 |
|------|------|----------|
| 1 | 超级管理员 | 系统所有功能 |
| 2 | 社区管理员 | 社区管理、居民管理 |
| 3 | 社区工作者 | 居民信息管理、数据统计 |
| 4 | 普通用户 | 查看个人信息 |
| 5 | 访客 | 只读访问 |

权限检查通过自定义的上下文处理器实现，在模板中可直接使用：
```html
{% if has_permission 'DELETE_RESIDENT' %}
    <button class="btn btn-danger">删除</button>
{% endif %}
```

## 数据模型

### 核心模型

#### Community（社区）
- `name`: 社区名称
- `office_address`: 办公地址
- `office_phone`: 办公电话
- `is_deleted`: 逻辑删除标记
- `remark`: 备注信息

#### UserProfile（用户档案）
- `user`: 关联Django用户
- `role`: 角色级别（1-5）
- `phone`: 联系电话
- `community`: 所属社区

#### Resident（居民）
- `name`: 居民姓名
- `id_card`: 身份证号
- `phone`: 联系电话
- `address`: 居住地址
- `family`: 所属家庭

详细数据模型请参考 [数据模型文档](docs/MODELS.md)。

## 开发规范

### 代码规范
- 遵循PEP8 Python编码规范
- 使用有意义的变量名和函数名
- 添加必要的代码注释和文档字符串
- 保持代码结构清晰，避免过长的函数

### Git提交规范
- 使用清晰的提交信息
- 遵循约定式提交规范（Conventional Commits）
- 定期推送到远程仓库
- 使用功能分支进行开发

详细开发规范请参考 [开发规范文档](CONTRIBUTING.md)。

## 测试

### 运行测试
```bash
python manage.py test
```

### 测试覆盖
- 模型测试：验证数据模型的正确性
- 视图测试：测试API接口功能
- 权限测试：验证权限控制逻辑
- 集成测试：测试系统整体功能

详细测试文档请参考 [测试策略文档](docs/TESTING.md)。

## 部署

### 生产环境要求
- Python 3.11+
- PostgreSQL/MySQL数据库
- Nginx/Apache Web服务器
- Redis缓存（可选）
- SSL证书

### 部署步骤
1. 准备生产环境
2. 配置数据库连接
3. 设置环境变量
4. 收集静态文件
5. 配置Web服务器
6. 设置反向代理
7. 配置HTTPS

详细部署指南请参考 [部署文档](DEPLOYMENT.md)。

## 贡献指南

我们欢迎社区成员贡献代码和文档。请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目开发。

## 许可证

本项目采用 MIT 许可证。详情请参见 [LICENSE](LICENSE) 文件。

## 支持

如果您在使用过程中遇到问题或有建议，请通过以下方式联系我们：
- 提交Issue
- 发送邮件至项目维护者
- 参与社区讨论

## 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解项目的更新历史和版本变化。

---

**开发团队**: 平泉市社区管理系统开发组  
**最后更新**: 2025年12月29日
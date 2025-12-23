# API文档

## 1. 概述

社区管理系统提供RESTful API接口，支持系统的各种功能操作。本文档详细描述了系统的API接口设计、请求格式、响应格式和使用示例。

## 2. 基本信息

### 2.1 API版本

当前API版本：`v1`

### 2.2 基础URL

- 开发环境：`http://127.0.0.1:8000/api/v1/`
- 生产环境：`https://yourdomain.com/api/v1/`

### 2.3 认证方式

系统采用JWT（JSON Web Token）认证机制，所有需要认证的接口都需要在请求头中携带`Authorization`字段。

```
Authorization: Bearer <your-jwt-token>
```

### 2.4 响应格式

所有API接口返回统一的JSON格式：

```json
{
    "code": 200,
    "message": "success",
    "data": {},
    "pagination": {
        "total": 100,
        "page": 1,
        "page_size": 10,
        "pages": 10
    }
}
```

### 2.5 错误码

| 错误码 | 描述 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证或认证失败 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 3. 认证接口

### 3.1 用户登录

**功能描述**：用户登录，获取JWT令牌

**请求信息**：
- **URL**：`/api/v1/auth/login/`
- **方法**：`POST`
- **认证**：无需认证

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `username` | `string` | `Yes` | 用户名 |
| `password` | `string` | `Yes` | 密码 |

**请求示例**：

```json
{
    "username": "admin",
    "password": "password123"
}
```

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "first_name": "",
            "last_name": "",
            "userprofile": {
                "id": 1,
                "role": 1,
                "phone": "13800138000",
                "community": null,
                "is_active": true
            }
        }
    }
}
```

### 3.2 用户登出

**功能描述**：用户登出，将令牌加入黑名单

**请求信息**：
- **URL**：`/api/v1/auth/logout/`
- **方法**：`POST`
- **认证**：需要JWT令牌

**请求参数**：无

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": null
}
```

### 3.3 刷新令牌

**功能描述**：使用刷新令牌获取新的访问令牌

**请求信息**：
- **URL**：`/api/v1/auth/refresh/`
- **方法**：`POST`
- **认证**：需要刷新令牌

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `refresh` | `string` | `Yes` | 刷新令牌 |

**请求示例**：

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
}
```

## 4. 社区管理接口

### 4.1 获取社区列表

**功能描述**：获取系统中的所有社区列表，支持分页和过滤

**请求信息**：
- **URL**：`/api/v1/communities/`
- **方法**：`GET`
- **认证**：需要JWT令牌

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `page` | `int` | `No` | 页码，默认1 |
| `page_size` | `int` | `No` | 每页数量，默认10 |
| `name` | `string` | `No` | 社区名称过滤 |
| `is_deleted` | `bool` | `No` | 是否包含已删除社区，默认false |

**响应示例**：

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
            "is_deleted": false,
            "remark": "",
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z"
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

### 4.2 创建社区

**功能描述**：创建新的社区

**请求信息**：
- **URL**：`/api/v1/communities/`
- **方法**：`POST`
- **认证**：需要JWT令牌，角色级别<=2

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `name` | `string` | `Yes` | 社区名称 |
| `office_address` | `string` | `No` | 办公地址 |
| `office_phone` | `string` | `No` | 办公电话 |
| `remark` | `string` | `No` | 备注信息 |

**请求示例**：

```json
{
    "name": "阳光社区",
    "office_address": "平泉市阳光街道1号",
    "office_phone": "0314-1234567",
    "remark": "新建社区"
}
```

**响应示例**：

```json
{
    "code": 201,
    "message": "success",
    "data": {
        "id": 1,
        "name": "阳光社区",
        "office_address": "平泉市阳光街道1号",
        "office_phone": "0314-1234567",
        "is_deleted": false,
        "remark": "新建社区",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z"
    }
}
```

### 4.3 获取社区详情

**功能描述**：获取指定社区的详细信息

**请求信息**：
- **URL**：`/api/v1/communities/{id}/`
- **方法**：`GET`
- **认证**：需要JWT令牌

**请求参数**：无

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "name": "阳光社区",
        "office_address": "平泉市阳光街道1号",
        "office_phone": "0314-1234567",
        "is_deleted": false,
        "remark": "新建社区",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z"
    }
}
```

### 4.4 更新社区信息

**功能描述**：更新指定社区的信息

**请求信息**：
- **URL**：`/api/v1/communities/{id}/`
- **方法**：`PUT`
- **认证**：需要JWT令牌，角色级别<=2

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `name` | `string` | `No` | 社区名称 |
| `office_address` | `string` | `No` | 办公地址 |
| `office_phone` | `string` | `No` | 办公电话 |
| `remark` | `string` | `No` | 备注信息 |

**请求示例**：

```json
{
    "name": "阳光社区（更新）",
    "office_phone": "0314-7654321"
}
```

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "name": "阳光社区（更新）",
        "office_address": "平泉市阳光街道1号",
        "office_phone": "0314-7654321",
        "is_deleted": false,
        "remark": "新建社区",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-02T00:00:00Z"
    }
}
```

### 4.5 删除社区

**功能描述**：删除指定社区（逻辑删除）

**请求信息**：
- **URL**：`/api/v1/communities/{id}/`
- **方法**：`DELETE`
- **认证**：需要JWT令牌，角色级别<=1

**请求参数**：无

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": null
}
```

## 5. 居民管理接口

### 5.1 获取居民列表

**功能描述**：获取系统中的所有居民列表，支持分页和过滤

**请求信息**：
- **URL**：`/api/v1/residents/`
- **方法**：`GET`
- **认证**：需要JWT令牌

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `page` | `int` | `No` | 页码，默认1 |
| `page_size` | `int` | `No` | 每页数量，默认10 |
| `name` | `string` | `No` | 居民姓名过滤 |
| `id_card` | `string` | `No` | 身份证号过滤 |
| `community` | `int` | `No` | 社区ID过滤 |
| `family` | `int` | `No` | 家庭ID过滤 |
| `status` | `int` | `No` | 居民状态过滤 |
| `is_deleted` | `bool` | `No` | 是否包含已删除居民，默认false |

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "id": 1,
            "name": "张三",
            "id_card": "130823199001011234",
            "gender": "男",
            "birth_date": "1990-01-01",
            "phone": "13800138000",
            "address": "阳光小区1号楼1单元101室",
            "family": {
                "id": 1,
                "family_name": "张三家庭",
                "community": 1
            },
            "community": {
                "id": 1,
                "name": "阳光社区"
            },
            "status": 1,
            "is_deleted": false,
            "remark": "",
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z"
        }
    ],
    "pagination": {
        "total": 100,
        "page": 1,
        "page_size": 10,
        "pages": 10
    }
}
```

### 5.2 创建居民档案

**功能描述**：创建新的居民档案

**请求信息**：
- **URL**：`/api/v1/residents/`
- **方法**：`POST`
- **认证**：需要JWT令牌，角色级别<=3

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `name` | `string` | `Yes` | 居民姓名 |
| `id_card` | `string` | `Yes` | 身份证号 |
| `gender` | `string` | `No` | 性别（男/女） |
| `birth_date` | `date` | `No` | 出生日期（YYYY-MM-DD） |
| `phone` | `string` | `No` | 联系电话 |
| `address` | `string` | `No` | 居住地址 |
| `family` | `int` | `No` | 家庭ID |
| `community` | `int` | `Yes` | 社区ID |
| `status` | `int` | `No` | 居民状态，默认1 |
| `remark` | `string` | `No` | 备注信息 |

**请求示例**：

```json
{
    "name": "张三",
    "id_card": "130823199001011234",
    "gender": "男",
    "birth_date": "1990-01-01",
    "phone": "13800138000",
    "address": "阳光小区1号楼1单元101室",
    "family": 1,
    "community": 1,
    "status": 1,
    "remark": ""
}
```

**响应示例**：

```json
{
    "code": 201,
    "message": "success",
    "data": {
        "id": 1,
        "name": "张三",
        "id_card": "130823199001011234",
        "gender": "男",
        "birth_date": "1990-01-01",
        "phone": "13800138000",
        "address": "阳光小区1号楼1单元101室",
        "family": {
            "id": 1,
            "family_name": "张三家庭",
            "community": 1
        },
        "community": {
            "id": 1,
            "name": "阳光社区"
        },
        "status": 1,
        "is_deleted": false,
        "remark": "",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z"
    }
}
```

### 5.3 获取居民详情

**功能描述**：获取指定居民的详细信息

**请求信息**：
- **URL**：`/api/v1/residents/{id}/`
- **方法**：`GET`
- **认证**：需要JWT令牌

**请求参数**：无

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "name": "张三",
        "id_card": "130823199001011234",
        "gender": "男",
        "birth_date": "1990-01-01",
        "phone": "13800138000",
        "address": "阳光小区1号楼1单元101室",
        "family": {
            "id": 1,
            "family_name": "张三家庭",
            "community": 1
        },
        "community": {
            "id": 1,
            "name": "阳光社区"
        },
        "status": 1,
        "is_deleted": false,
        "remark": "",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z"
    }
}
```

### 5.4 更新居民信息

**功能描述**：更新指定居民的信息

**请求信息**：
- **URL**：`/api/v1/residents/{id}/`
- **方法**：`PUT`
- **认证**：需要JWT令牌，角色级别<=3

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `name` | `string` | `No` | 居民姓名 |
| `id_card` | `string` | `No` | 身份证号 |
| `gender` | `string` | `No` | 性别（男/女） |
| `birth_date` | `date` | `No` | 出生日期（YYYY-MM-DD） |
| `phone` | `string` | `No` | 联系电话 |
| `address` | `string` | `No` | 居住地址 |
| `family` | `int` | `No` | 家庭ID |
| `community` | `int` | `No` | 社区ID |
| `status` | `int` | `No` | 居民状态 |
| `remark` | `string` | `No` | 备注信息 |

**请求示例**：

```json
{
    "phone": "13900139000",
    "address": "阳光小区1号楼1单元102室"
}
```

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "name": "张三",
        "id_card": "130823199001011234",
        "gender": "男",
        "birth_date": "1990-01-01",
        "phone": "13900139000",
        "address": "阳光小区1号楼1单元102室",
        "family": {
            "id": 1,
            "family_name": "张三家庭",
            "community": 1
        },
        "community": {
            "id": 1,
            "name": "阳光社区"
        },
        "status": 1,
        "is_deleted": false,
        "remark": "",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-02T00:00:00Z"
    }
}
```

### 5.5 删除居民

**功能描述**：删除指定居民（逻辑删除）

**请求信息**：
- **URL**：`/api/v1/residents/{id}/`
- **方法**：`DELETE`
- **认证**：需要JWT令牌，角色级别<=2

**请求参数**：无

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": null
}
```

## 6. 家庭管理接口

### 6.1 获取家庭列表

**功能描述**：获取系统中的所有家庭列表，支持分页和过滤

**请求信息**：
- **URL**：`/api/v1/families/`
- **方法**：`GET`
- **认证**：需要JWT令牌

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `page` | `int` | `No` | 页码，默认1 |
| `page_size` | `int` | `No` | 每页数量，默认10 |
| `family_name` | `string` | `No` | 家庭名称过滤 |
| `community` | `int` | `No` | 社区ID过滤 |
| `is_deleted` | `bool` | `No` | 是否包含已删除家庭，默认false |

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "id": 1,
            "family_name": "张三家庭",
            "community": {
                "id": 1,
                "name": "阳光社区"
            },
            "address": "阳光小区1号楼1单元101室",
            "is_deleted": false,
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z"
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

### 6.2 创建家庭

**功能描述**：创建新的家庭

**请求信息**：
- **URL**：`/api/v1/families/`
- **方法**：`POST`
- **认证**：需要JWT令牌，角色级别<=3

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `family_name` | `string` | `Yes` | 家庭名称 |
| `community` | `int` | `Yes` | 社区ID |
| `address` | `string` | `No` | 家庭地址 |

**请求示例**：

```json
{
    "family_name": "张三家庭",
    "community": 1,
    "address": "阳光小区1号楼1单元101室"
}
```

**响应示例**：

```json
{
    "code": 201,
    "message": "success",
    "data": {
        "id": 1,
        "family_name": "张三家庭",
        "community": {
            "id": 1,
            "name": "阳光社区"
        },
        "address": "阳光小区1号楼1单元101室",
        "is_deleted": false,
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z"
    }
}
```

## 7. 住房管理接口

### 7.1 获取小区列表

**功能描述**：获取系统中的所有小区列表，支持分页和过滤

**请求信息**：
- **URL**：`/api/v1/housing-complexes/`
- **方法**：`GET`
- **认证**：需要JWT令牌

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `page` | `int` | `No` | 页码，默认1 |
| `page_size` | `int` | `No` | 每页数量，默认10 |
| `name` | `string` | `No` | 小区名称过滤 |
| `community` | `int` | `No` | 社区ID过滤 |
| `is_deleted` | `bool` | `No` | 是否包含已删除小区，默认false |

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "id": 1,
            "name": "阳光小区",
            "community": {
                "id": 1,
                "name": "阳光社区"
            },
            "address": "平泉市阳光街道1号",
            "is_deleted": false,
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z"
        }
    ],
    "pagination": {
        "total": 20,
        "page": 1,
        "page_size": 10,
        "pages": 2
    }
}
```

### 7.2 获取楼栋列表

**功能描述**：获取系统中的所有楼栋列表，支持分页和过滤

**请求信息**：
- **URL**：`/api/v1/buildings/`
- **方法**：`GET`
- **认证**：需要JWT令牌

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `page` | `int` | `No` | 页码，默认1 |
| `page_size` | `int` | `No` | 每页数量，默认10 |
| `building_number` | `string` | `No` | 楼栋号过滤 |
| `housing_complex` | `int` | `No` | 小区ID过滤 |
| `is_deleted` | `bool` | `No` | 是否包含已删除楼栋，默认false |

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "id": 1,
            "building_number": "1号楼",
            "housing_complex": {
                "id": 1,
                "name": "阳光小区"
            },
            "is_deleted": false,
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z"
        }
    ],
    "pagination": {
        "total": 100,
        "page": 1,
        "page_size": 10,
        "pages": 10
    }
}
```

### 7.3 获取房屋列表

**功能描述**：获取系统中的所有房屋列表，支持分页和过滤

**请求信息**：
- **URL**：`/api/v1/houses/`
- **方法**：`GET`
- **认证**：需要JWT令牌

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `page` | `int` | `No` | 页码，默认1 |
| `page_size` | `int` | `No` | 每页数量，默认10 |
| `room_number` | `string` | `No` | 房间号过滤 |
| `unit` | `int` | `No` | 单元ID过滤 |
| `owner` | `int` | `No` | 业主ID过滤 |
| `status` | `int` | `No` | 房屋状态过滤 |
| `is_deleted` | `bool` | `No` | 是否包含已删除房屋，默认false |

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "id": 1,
            "room_number": "101室",
            "unit": {
                "id": 1,
                "unit_number": "1",
                "building": {
                    "id": 1,
                    "building_number": "1号楼",
                    "housing_complex": {
                        "id": 1,
                        "name": "阳光小区"
                    }
                }
            },
            "area": 100.5,
            "house_type": "两室一厅",
            "owner": {
                "id": 1,
                "name": "张三"
            },
            "status": 1,
            "is_deleted": false,
            "remark": "",
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z"
        }
    ],
    "pagination": {
        "total": 500,
        "page": 1,
        "page_size": 10,
        "pages": 50
    }
}
```

## 8. 数据分析接口

### 8.1 获取仪表板数据

**功能描述**：获取系统的仪表板数据，包括社区数量、居民数量、房屋数量等统计信息

**请求信息**：
- **URL**：`/api/v1/analytics/dashboard/`
- **方法**：`GET`
- **认证**：需要JWT令牌

**请求参数**：无

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "community_count": 10,
        "resident_count": 1000,
        "family_count": 500,
        "house_count": 800,
        "active_resident_count": 950,
        "move_out_count": 50,
        "community_stats": [
            {
                "community_id": 1,
                "community_name": "阳光社区",
                "resident_count": 150
            },
            {
                "community_id": 2,
                "community_name": "幸福社区",
                "resident_count": 200
            }
        ],
        "recent_residents": [
            {
                "id": 1001,
                "name": "李四",
                "created_at": "2025-01-02T10:00:00Z"
            }
        ]
    }
}
```

### 8.2 获取统计数据

**功能描述**：获取系统的统计数据，支持按时间范围、社区等条件过滤

**请求信息**：
- **URL**：`/api/v1/analytics/statistics/`
- **方法**：`GET`
- **认证**：需要JWT令牌

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `start_date` | `date` | `No` | 开始日期（YYYY-MM-DD） |
| `end_date` | `date` | `No` | 结束日期（YYYY-MM-DD） |
| `community` | `int` | `No` | 社区ID |
| `type` | `string` | `No` | 统计类型（resident/house/family） |

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total_count": 1000,
        "daily_stats": [
            {
                "date": "2025-01-01",
                "count": 10
            },
            {
                "date": "2025-01-02",
                "count": 15
            }
        ],
        "gender_stats": {
            "male": 600,
            "female": 400
        },
        "age_group_stats": {
            "0-18": 200,
            "19-35": 300,
            "36-59": 350,
            "60+": 150
        }
    }
}
```

### 8.3 导出数据报告

**功能描述**：导出系统数据报告，支持多种格式

**请求信息**：
- **URL**：`/api/v1/analytics/export/`
- **方法**：`GET`
- **认证**：需要JWT令牌

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `format` | `string` | `No` | 导出格式（csv/excel/pdf），默认csv |
| `type` | `string` | `Yes` | 导出类型（resident/house/family/statistics） |
| `start_date` | `date` | `No` | 开始日期（YYYY-MM-DD） |
| `end_date` | `date` | `No` | 结束日期（YYYY-MM-DD） |
| `community` | `int` | `No` | 社区ID |

**响应示例**：

```
# 文件下载响应，Content-Disposition: attachment; filename="residents_20250102.csv"
```

## 9. 系统管理接口

### 9.1 获取用户列表

**功能描述**：获取系统中的所有用户列表，支持分页和过滤

**请求信息**：
- **URL**：`/api/v1/users/`
- **方法**：`GET`
- **认证**：需要JWT令牌，角色级别<=2

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `page` | `int` | `No` | 页码，默认1 |
| `page_size` | `int` | `No` | 每页数量，默认10 |
| `username` | `string` | `No` | 用户名过滤 |
| `email` | `string` | `No` | 邮箱过滤 |
| `role` | `int` | `No` | 角色级别过滤 |
| `community` | `int` | `No` | 社区ID过滤 |
| `is_active` | `bool` | `No` | 是否激活过滤 |

**响应示例**：

```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "first_name": "",
            "last_name": "",
            "is_active": true,
            "userprofile": {
                "id": 1,
                "role": 1,
                "phone": "13800138000",
                "community": null,
                "is_active": true
            }
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

### 9.2 创建用户

**功能描述**：创建新的系统用户

**请求信息**：
- **URL**：`/api/v1/users/`
- **方法**：`POST`
- **认证**：需要JWT令牌，角色级别<=2

**请求参数**：

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `username` | `string` | `Yes` | 用户名 |
| `password` | `string` | `Yes` | 密码 |
| `email` | `string` | `No` | 邮箱 |
| `first_name` | `string` | `No` | 名 |
| `last_name` | `string` | `No` | 姓 |
| `role` | `int` | `Yes` | 角色级别 |
| `phone` | `string` | `No` | 联系电话 |
| `community` | `int` | `No` | 社区ID |
| `is_active` | `bool` | `No` | 是否激活，默认true |

**请求示例**：

```json
{
    "username": "user1",
    "password": "password123",
    "email": "user1@example.com",
    "role": 3,
    "phone": "13800138001",
    "community": 1,
    "is_active": true
}
```

**响应示例**：

```json
{
    "code": 201,
    "message": "success",
    "data": {
        "id": 2,
        "username": "user1",
        "email": "user1@example.com",
        "first_name": "",
        "last_name": "",
        "is_active": true,
        "userprofile": {
            "id": 2,
            "role": 3,
            "phone": "13800138001",
            "community": {
                "id": 1,
                "name": "阳光社区"
            },
            "is_active": true
        }
    }
}
```

## 10. API使用示例

### 10.1 使用Python请求API

```python
import requests
import json

# 登录获取令牌
def get_token():
    url = "http://127.0.0.1:8000/api/v1/auth/login/"
    data = {
        "username": "admin",
        "password": "password123"
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["data"]["access"]
    return None

# 获取居民列表
def get_residents():
    token = get_token()
    if not token:
        print("获取令牌失败")
        return
    
    url = "http://127.0.0.1:8000/api/v1/residents/"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    print(f"获取居民列表失败: {response.status_code}")
    return None

# 使用示例
if __name__ == "__main__":
    residents = get_residents()
    if residents:
        print(f"共获取到 {residents['pagination']['total']} 名居民")
        for resident in residents["data"]:
            print(f"姓名: {resident['name']}, 身份证号: {resident['id_card']}")
```

### 10.2 使用JavaScript请求API

```javascript
// 登录获取令牌
async function getToken() {
    const response = await fetch('http://127.0.0.1:8000/api/v1/auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: 'admin',
            password: 'password123'
        })
    });
    
    if (response.ok) {
        const data = await response.json();
        return data.data.access;
    }
    return null;
}

// 获取居民列表
async function getResidents() {
    const token = await getToken();
    if (!token) {
        console.error('获取令牌失败');
        return;
    }
    
    const response = await fetch('http://127.0.0.1:8000/api/v1/residents/', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    if (response.ok) {
        return await response.json();
    }
    console.error(`获取居民列表失败: ${response.status}`);
    return null;
}

// 使用示例
getResidents().then(residents => {
    if (residents) {
        console.log(`共获取到 ${residents.pagination.total} 名居民`);
        residents.data.forEach(resident => {
            console.log(`姓名: ${resident.name}, 身份证号: ${resident.id_card}`);
        });
    }
});
```

## 11. 最佳实践

1. **使用HTTPS**：在生产环境中，始终使用HTTPS协议保护API通信
2. **合理使用缓存**：对频繁访问的接口结果进行缓存，提高系统性能
3. **分页查询**：对大量数据的查询使用分页，避免一次性返回过多数据
4. **错误处理**：合理处理API调用过程中的错误，提供友好的错误信息
5. **请求频率限制**：在生产环境中，对API请求频率进行限制，防止恶意攻击
6. **日志记录**：记录API调用日志，便于问题排查和性能分析
7. **版本控制**：API版本化管理，便于后续功能扩展和兼容性维护
8. **文档更新**：API变更后及时更新文档，保持文档与实际代码一致

## 12. 常见问题

### 12.1 如何获取JWT令牌？

通过调用登录接口`/api/v1/auth/login/`，使用正确的用户名和密码即可获取JWT令牌。

### 12.2 令牌过期怎么办？

使用刷新令牌调用刷新令牌接口`/api/v1/auth/refresh/`，获取新的访问令牌。

### 12.3 如何处理401未认证错误？

检查请求头中的Authorization字段是否正确，令牌是否过期或无效。

### 12.4 如何处理403权限不足错误？

检查当前用户的角色级别是否满足接口的权限要求。

### 12.5 如何获取更多的调试信息？

在开发环境中，可以查看服务器日志获取详细的错误信息。

## 13. 文档更新记录

| 更新日期 | 版本 | 更新内容 |
|----------|------|----------|
| 2025-01-01 | v1.0 | 初始版本，包含认证、社区、居民、家庭、住房管理等接口 |
| 2025-01-02 | v1.1 | 添加数据分析接口和系统管理接口 |
| 2025-01-03 | v1.2 | 添加API使用示例和最佳实践 |
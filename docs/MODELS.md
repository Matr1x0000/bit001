# 数据模型文档

## 1. 概述

社区管理系统采用Django ORM进行数据库建模，主要数据模型包括社区、居民、住房、用户档案等核心实体。本文档详细描述了系统的数据模型结构、字段定义、关系映射和使用说明。

## 2. 核心数据模型

### 2.1 Community（社区）

**功能描述**：存储社区的基本信息，包括名称、地址、联系方式等。

**数据结构**：

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| `id` | `AutoField` | `Primary Key` | 社区唯一标识 |
| `name` | `CharField(50)` | `Not Null` | 社区名称 |
| `office_address` | `CharField(100)` | `Null, Blank` | 办公地址 |
| `office_phone` | `CharField(20)` | `Null, Blank` | 办公电话 |
| `is_deleted` | `BooleanField` | `Default: False` | 逻辑删除标记 |
| `remark` | `TextField` | `Null, Blank` | 备注信息 |
| `created_at` | `DateTimeField` | `Auto Now Add` | 创建时间 |
| `updated_at` | `DateTimeField` | `Auto Now` | 更新时间 |

**模型代码**：
```python
class Community(models.Model):
    """
    社区模型，用于存储社区基本信息
    """
    name = models.CharField(max_length=50, verbose_name="社区名称")
    office_address = models.CharField(max_length=100, verbose_name="办公地址", null=True, blank=True)
    office_phone = models.CharField(max_length=20, verbose_name="办公电话", null=True, blank=True)
    is_deleted = models.BooleanField(default=False, verbose_name="是否已删除", db_index=True)
    remark = models.TextField(verbose_name="备注", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
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

### 2.2 UserProfile（用户档案）

**功能描述**：扩展Django内置User模型，存储用户的角色、联系方式和所属社区等信息。

**数据结构**：

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| `id` | `AutoField` | `Primary Key` | 用户档案唯一标识 |
| `user` | `OneToOneField(User)` | `Primary Key` | 关联Django用户 |
| `role` | `IntegerField` | `Default: 5` | 角色级别（1-5，数值越小权限越高） |
| `phone` | `CharField(20)` | `Null, Blank` | 联系电话 |
| `community` | `ForeignKey(Community)` | `Null, Blank` | 所属社区 |
| `is_active` | `BooleanField` | `Default: True` | 账号状态 |
| `created_at` | `DateTimeField` | `Auto Now Add` | 创建时间 |
| `updated_at` | `DateTimeField` | `Auto Now` | 更新时间 |

**角色定义**：

| 角色级别 | 角色名称 | 权限范围 |
|----------|----------|----------|
| 1 | 超级管理员 | 系统所有功能 |
| 2 | 社区管理员 | 社区管理、居民管理 |
| 3 | 社区工作者 | 居民信息管理、数据统计 |
| 4 | 普通用户 | 查看个人信息 |
| 5 | 访客 | 只读访问 |

**模型代码**：
```python
class UserProfile(models.Model):
    """
    用户档案模型，扩展Django内置User模型
    """
    ROLE_CHOICES = [
        (1, '超级管理员'),
        (2, '社区管理员'),
        (3, '社区工作者'),
        (4, '普通用户'),
        (5, '访客'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile', verbose_name="关联用户")
    role = models.IntegerField(choices=ROLE_CHOICES, default=5, verbose_name="角色级别")
    phone = models.CharField(max_length=20, verbose_name="联系电话", null=True, blank=True)
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="所属社区")
    is_active = models.BooleanField(default=True, verbose_name="账号状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "2.用户档案"
        verbose_name_plural = "2.用户档案列表"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
```

### 2.3 Family（家庭）

**功能描述**：存储家庭基本信息，作为居民的所属单位。

**数据结构**：

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| `id` | `AutoField` | `Primary Key` | 家庭唯一标识 |
| `family_name` | `CharField(50)` | `Not Null` | 家庭名称 |
| `community` | `ForeignKey(Community)` | `Not Null` | 所属社区 |
| `address` | `CharField(100)` | `Null, Blank` | 家庭地址 |
| `is_deleted` | `BooleanField` | `Default: False` | 逻辑删除标记 |
| `created_at` | `DateTimeField` | `Auto Now Add` | 创建时间 |
| `updated_at` | `DateTimeField` | `Auto Now` | 更新时间 |

**模型代码**：
```python
class Family(models.Model):
    """
    家庭模型，用于存储家庭基本信息
    """
    family_name = models.CharField(max_length=50, verbose_name="家庭名称")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name="所属社区")
    address = models.CharField(max_length=100, verbose_name="家庭地址", null=True, blank=True)
    is_deleted = models.BooleanField(default=False, verbose_name="是否已删除", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "3.家庭"
        verbose_name_plural = "3.家庭列表"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['community', 'is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.family_name} ({self.community.name})"
```

### 2.4 Resident（居民）

**功能描述**：存储居民的详细档案信息，包括个人基本信息、家庭关系、居住信息等。

**数据结构**：

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| `id` | `AutoField` | `Primary Key` | 居民唯一标识 |
| `name` | `CharField(50)` | `Not Null` | 居民姓名 |
| `id_card` | `CharField(18)` | `Unique, Not Null` | 身份证号 |
| `gender` | `CharField(1)` | `Null, Blank` | 性别（男/女） |
| `birth_date` | `DateField` | `Null, Blank` | 出生日期 |
| `phone` | `CharField(20)` | `Null, Blank` | 联系电话 |
| `address` | `CharField(100)` | `Null, Blank` | 居住地址 |
| `family` | `ForeignKey(Family)` | `Null, Blank` | 所属家庭 |
| `community` | `ForeignKey(Community)` | `Not Null` | 所属社区 |
| `status` | `IntegerField` | `Default: 1` | 居民状态（1-正常，2-迁出，3-其他） |
| `is_deleted` | `BooleanField` | `Default: False` | 逻辑删除标记 |
| `remark` | `TextField` | `Null, Blank` | 备注信息 |
| `created_at` | `DateTimeField` | `Auto Now Add` | 创建时间 |
| `updated_at` | `DateTimeField` | `Auto Now` | 更新时间 |

**模型代码**：
```python
class Resident(models.Model):
    """
    居民模型，用于存储居民详细档案信息
    """
    STATUS_CHOICES = [
        (1, '正常'),
        (2, '迁出'),
        (3, '其他'),
    ]
    
    name = models.CharField(max_length=50, verbose_name="居民姓名")
    id_card = models.CharField(max_length=18, unique=True, verbose_name="身份证号")
    gender = models.CharField(max_length=1, verbose_name="性别", null=True, blank=True)
    birth_date = models.DateField(verbose_name="出生日期", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="联系电话", null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name="居住地址", null=True, blank=True)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="所属家庭")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name="所属社区")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="居民状态")
    is_deleted = models.BooleanField(default=False, verbose_name="是否已删除", db_index=True)
    remark = models.TextField(verbose_name="备注", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "4.居民"
        verbose_name_plural = "4.居民列表"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['community', 'is_deleted']),
            models.Index(fields=['family', 'is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.id_card})"
```

### 2.5 HousingComplex（小区）

**功能描述**：存储小区的基本信息，包括名称、地址、所属社区等。

**数据结构**：

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| `id` | `AutoField` | `Primary Key` | 小区唯一标识 |
| `name` | `CharField(50)` | `Not Null` | 小区名称 |
| `community` | `ForeignKey(Community)` | `Not Null` | 所属社区 |
| `address` | `CharField(100)` | `Null, Blank` | 小区地址 |
| `is_deleted` | `BooleanField` | `Default: False` | 逻辑删除标记 |
| `created_at` | `DateTimeField` | `Auto Now Add` | 创建时间 |
| `updated_at` | `DateTimeField` | `Auto Now` | 更新时间 |

**模型代码**：
```python
class HousingComplex(models.Model):
    """
    小区模型，用于存储小区基本信息
    """
    name = models.CharField(max_length=50, verbose_name="小区名称")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name="所属社区")
    address = models.CharField(max_length=100, verbose_name="小区地址", null=True, blank=True)
    is_deleted = models.BooleanField(default=False, verbose_name="是否已删除", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "5.小区"
        verbose_name_plural = "5.小区列表"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['community', 'is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.community.name})"
```

### 2.6 Building（楼栋）

**功能描述**：存储楼栋的基本信息，包括楼栋号、所属小区等。

**数据结构**：

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| `id` | `AutoField` | `Primary Key` | 楼栋唯一标识 |
| `building_number` | `CharField(20)` | `Not Null` | 楼栋号 |
| `housing_complex` | `ForeignKey(HousingComplex)` | `Not Null` | 所属小区 |
| `is_deleted` | `BooleanField` | `Default: False` | 逻辑删除标记 |
| `created_at` | `DateTimeField` | `Auto Now Add` | 创建时间 |
| `updated_at` | `DateTimeField` | `Auto Now` | 更新时间 |

**模型代码**：
```python
class Building(models.Model):
    """
    楼栋模型，用于存储楼栋基本信息
    """
    building_number = models.CharField(max_length=20, verbose_name="楼栋号")
    housing_complex = models.ForeignKey(HousingComplex, on_delete=models.CASCADE, verbose_name="所属小区")
    is_deleted = models.BooleanField(default=False, verbose_name="是否已删除", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "6.楼栋"
        verbose_name_plural = "6.楼栋列表"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['housing_complex', 'is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.building_number} ({self.housing_complex.name})"
```

### 2.7 Unit（单元）

**功能描述**：存储单元的基本信息，包括单元号、所属楼栋等。

**数据结构**：

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| `id` | `AutoField` | `Primary Key` | 单元唯一标识 |
| `unit_number` | `CharField(10)` | `Not Null` | 单元号 |
| `building` | `ForeignKey(Building)` | `Not Null` | 所属楼栋 |
| `is_deleted` | `BooleanField` | `Default: False` | 逻辑删除标记 |
| `created_at` | `DateTimeField` | `Auto Now Add` | 创建时间 |
| `updated_at` | `DateTimeField` | `Auto Now` | 更新时间 |

**模型代码**：
```python
class Unit(models.Model):
    """
    单元模型，用于存储单元基本信息
    """
    unit_number = models.CharField(max_length=10, verbose_name="单元号")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="所属楼栋")
    is_deleted = models.BooleanField(default=False, verbose_name="是否已删除", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "7.单元"
        verbose_name_plural = "7.单元列表"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['building', 'is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.unit_number}单元 ({self.building.building_number})"
```

### 2.8 House（房屋）

**功能描述**：存储房屋的基本信息，包括房间号、面积、所属单元等。

**数据结构**：

| 字段名 | 数据类型 | 约束 | 描述 |
|--------|----------|------|------|
| `id` | `AutoField` | `Primary Key` | 房屋唯一标识 |
| `room_number` | `CharField(20)` | `Not Null` | 房间号 |
| `unit` | `ForeignKey(Unit)` | `Not Null` | 所属单元 |
| `area` | `DecimalField(8,2)` | `Null, Blank` | 房屋面积 |
| `house_type` | `CharField(20)` | `Null, Blank` | 房屋类型（如：两室一厅） |
| `owner` | `ForeignKey(Resident)` | `Null, Blank` | 房屋业主 |
| `status` | `IntegerField` | `Default: 1` | 房屋状态（1-已入住，2-未入住，3-出租，4-其他） |
| `is_deleted` | `BooleanField` | `Default: False` | 逻辑删除标记 |
| `remark` | `TextField` | `Null, Blank` | 备注信息 |
| `created_at` | `DateTimeField` | `Auto Now Add` | 创建时间 |
| `updated_at` | `DateTimeField` | `Auto Now` | 更新时间 |

**模型代码**：
```python
class House(models.Model):
    """
    房屋模型，用于存储房屋基本信息
    """
    STATUS_CHOICES = [
        (1, '已入住'),
        (2, '未入住'),
        (3, '出租'),
        (4, '其他'),
    ]
    
    room_number = models.CharField(max_length=20, verbose_name="房间号")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name="所属单元")
    area = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="房屋面积", null=True, blank=True)
    house_type = models.CharField(max_length=20, verbose_name="房屋类型", null=True, blank=True)
    owner = models.ForeignKey(Resident, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="房屋业主")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="房屋状态")
    is_deleted = models.BooleanField(default=False, verbose_name="是否已删除", db_index=True)
    remark = models.TextField(verbose_name="备注", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "8.房屋"
        verbose_name_plural = "8.房屋列表"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['unit', 'is_deleted']),
        ]
    
    def __str__(self):
        return f"{self.room_number} ({self.unit.building.building_number})"
```

## 3. 模型关系图

```
┌─────────────────┐      ┌─────────────────┐
│   Community     │      │      User       │
├─────────────────┤      └─────────────────┘
│ id              │              │
│ name            │              │ 1:1
│ office_address  │              ▼
│ office_phone    │      ┌─────────────────┐
│ is_deleted      │      │  UserProfile    │
└─────────────────┘      ├─────────────────┤
          │              │ id              │
          │ 1:N          │ user            │
          ▼              │ role            │
┌─────────────────┐      │ phone           │
│    Family       │      │ community       │
├─────────────────┤      │ is_active       │
│ id              │      └─────────────────┘
│ family_name     │
│ community       │
│ address         │
│ is_deleted      │
└─────────────────┘
          │
          │ 1:N
          ▼
┌─────────────────┐      ┌─────────────────┐
│   Resident      │      │ HousingComplex  │
├─────────────────┤      ├─────────────────┤
│ id              │      │ id              │
│ name            │      │ name            │
│ id_card         │      │ community       │
│ gender          │      │ address         │
│ birth_date      │      │ is_deleted      │
│ phone           │      └─────────────────┘
│ address         │              │
│ family          │              │ 1:N
│ community       │              ▼
│ status          │      ┌─────────────────┐
│ is_deleted      │      │    Building     │
└─────────────────┘      ├─────────────────┤
          │              │ id              │
          │ 1:N          │ building_number │
          ▼              │ housing_complex │
┌─────────────────┐      │ is_deleted      │
│    House        │      └─────────────────┘
├─────────────────┤              │
│ id              │              │ 1:N
│ room_number     │              ▼
│ unit            │      ┌─────────────────┐
│ area            │      │      Unit       │
│ house_type      │      ├─────────────────┤
│ owner           │      │ id              │
│ status          │      │ unit_number     │
│ is_deleted      │      │ building        │
└─────────────────┘      │ is_deleted      │
                         └─────────────────┘
                                   │
                                   │ 1:N
                                   ▼
                            ┌─────────────────┐
                            │     House       │
                            └─────────────────┘
```

## 4. 数据模型使用说明

### 4.1 数据查询示例

**查询某个社区的所有居民**：
```python
from api.models import Community, Resident

# 获取社区
community = Community.objects.get(name="阳光社区")

# 查询该社区的所有正常居民
residents = Resident.objects.filter(community=community, is_deleted=False, status=1)

# 遍历居民列表
for resident in residents:
    print(f"姓名: {resident.name}, 身份证号: {resident.id_card}, 联系电话: {resident.phone}")
```

**查询某个家庭的所有成员**：
```python
from api.models import Family, Resident

# 获取家庭
family = Family.objects.get(family_name="张三家庭")

# 查询该家庭的所有成员
family_members = Resident.objects.filter(family=family, is_deleted=False)

# 遍历家庭成员
for member in family_members:
    print(f"姓名: {member.name}, 性别: {member.gender}, 出生日期: {member.birth_date}")
```

**查询某个小区的所有楼栋**：
```python
from api.models import HousingComplex, Building

# 获取小区
complex = HousingComplex.objects.get(name="阳光小区")

# 查询该小区的所有楼栋
buildings = Building.objects.filter(housing_complex=complex, is_deleted=False)

# 遍历楼栋
for building in buildings:
    print(f"楼栋号: {building.building_number}")
```

### 4.2 数据创建示例

**创建新社区**：
```python
from api.models import Community

# 创建社区
community = Community.objects.create(
    name="阳光社区",
    office_address="平泉市阳光街道1号",
    office_phone="0314-1234567",
    remark="新建社区"
)

print(f"社区创建成功: {community}")
```

**创建新居民**：
```python
from api.models import Community, Family, Resident
from datetime import date

# 获取社区
community = Community.objects.get(name="阳光社区")

# 获取或创建家庭
family, created = Family.objects.get_or_create(
    family_name="张三家庭",
    community=community,
    defaults={"address": "阳光小区1号楼1单元101室"}
)

# 创建居民
resident = Resident.objects.create(
    name="张三",
    id_card="130823199001011234",
    gender="男",
    birth_date=date(1990, 1, 1),
    phone="13800138000",
    address="阳光小区1号楼1单元101室",
    family=family,
    community=community,
    status=1
)

print(f"居民创建成功: {resident}")
```

## 5. 数据模型设计原则

1. **范式化设计**：遵循数据库设计范式，减少数据冗余
2. **逻辑删除**：采用`is_deleted`字段实现软删除，保留历史数据
3. **时间戳追踪**：所有模型均包含`created_at`和`updated_at`字段，记录数据生命周期
4. **索引优化**：为常用查询字段添加索引，提高查询性能
5. **外键约束**：使用外键维护数据完整性
6. **字段验证**：通过Django ORM字段约束实现数据验证
7. **枚举类型**：使用`choices`参数定义枚举类型，提高数据一致性
8. **命名规范**：采用清晰的命名规则，提高代码可读性

## 6. 数据库迁移管理

### 6.1 创建迁移文件

```bash
python manage.py makemigrations
```

### 6.2 应用迁移

```bash
python manage.py migrate
```

### 6.3 查看迁移状态

```bash
python manage.py showmigrations
```

### 6.4 回滚迁移

```bash
python manage.py migrate api <迁移文件编号>
```

## 7. 数据安全与隐私

1. **敏感数据保护**：身份证号、联系方式等敏感数据应加密存储
2. **访问控制**：通过权限系统限制数据访问
3. **数据备份**：定期备份数据库，确保数据安全
4. **隐私合规**：遵循相关数据隐私法规
5. **审计日志**：记录重要数据操作，便于追溯

## 8. 性能优化建议

1. **查询优化**：使用`select_related`和`prefetch_related`优化关联查询
2. **分页查询**：对大量数据查询使用分页
3. **缓存策略**：对频繁访问的数据使用缓存
4. **批量操作**：对大量数据操作使用批量处理
5. **索引优化**：根据查询模式优化索引设计
6. **避免N+1查询**：合理使用ORM查询方法，避免产生N+1查询问题

## 9. 数据模型变更管理

1. **变更流程**：数据模型变更需经过设计评审、开发、测试、部署等流程
2. **向后兼容**：模型变更应保持向后兼容，避免影响现有功能
3. **迁移测试**：迁移文件需经过充分测试，确保数据完整性
4. **变更文档**：记录数据模型变更，包括变更原因、影响范围等

## 10. 总结

社区管理系统的数据模型设计覆盖了社区管理、居民管理、住房管理等核心业务领域，采用了规范化的设计原则和良好的命名规范。通过合理的模型关系设计和索引优化，确保了系统的性能和可扩展性。

本文档详细描述了系统的数据模型结构、字段定义、关系映射和使用说明，为开发人员提供了清晰的数据模型参考，便于系统的开发、维护和扩展。
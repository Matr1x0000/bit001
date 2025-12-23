from ast import boolop
from django.db import models
from django.contrib.auth.models import User
from django.forms.widgets import boolean_check
from django.utils import timezone
from django.core.validators import RegexValidator

# 社区模型


class Community(models.Model):
    name = models.CharField(max_length=50, verbose_name="社区名称")
    office_address = models.CharField(max_length=100,
                                      verbose_name="办公地址",
                                      null=True,
                                      blank=True)
    office_phone = models.CharField(max_length=15,
                                    verbose_name="办公电话",
                                    null=True,
                                    blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "1.社区"
        verbose_name_plural = "1.社区列表"

    def __str__(self):
        return f"平泉市 - {self.name}"


# 社区工作者模型


class SocialWorker(models.Model):
    community = models.ForeignKey(Community,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  verbose_name="所属社区")
    name = models.CharField(max_length=20, verbose_name="姓名")
    gender = models.SmallIntegerField(choices=[(1, "男"), (2, "女")],
                                      default=1,
                                      verbose_name="性别")
    phone = models.CharField(max_length=15,
                             verbose_name="联系电话",
                             null=True,
                             blank=True)
    birth_date = models.DateField(verbose_name="出生年月", null=True, blank=True)
    is_secretary = models.BooleanField(default=False, verbose_name="是否为书记")
    is_baned = models.BooleanField(default=True,
                                   verbose_name="是否在职（True:在职, False:离职）")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "2.社区工作者"
        verbose_name_plural = "2.社区工作者列表"

    def __str__(self):
        return f" {self.community.name} - {self.name}({self.gender}) - {self.phone}"


# 小区模型


class HousingEstate(models.Model):
    name = models.CharField(max_length=50, verbose_name="小区名称")
    address = models.CharField(max_length=100,
                               verbose_name="小区地址",
                               null=True,
                               blank=True)
    community = models.ForeignKey(Community,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  verbose_name="所属社区")
    property_company = models.CharField(max_length=50,
                                        verbose_name="物业公司",
                                        null=True,
                                        blank=True)
    property_phone = models.CharField(max_length=15,
                                      verbose_name="物业电话",
                                      null=True,
                                      blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "1.小区"
        verbose_name_plural = "1.小区列表"
        unique_together = [('name', 'community')]

    def __str__(self):
        return f"{self.community.name} - {self.name}"


# 楼栋模型


class Building(models.Model):
    estate = models.ForeignKey(HousingEstate,
                               on_delete=models.CASCADE,
                               verbose_name="所属小区")
    name = models.CharField(max_length=20, verbose_name="楼栋名称/编号")
    building_type = models.SmallIntegerField(choices=[(1, "多层"), (2, "高层")],
                                             verbose_name="建筑类型",
                                             null=True,
                                             blank=True)
    total_floors = models.IntegerField(verbose_name="总层数",
                                       null=True,
                                       blank=True)
    units_per_floor = models.IntegerField(verbose_name="一层几户",
                                          null=True,
                                          blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "2.楼栋"
        verbose_name_plural = "2.楼栋列表"

    def __str__(self):
        return f"{self.estate.name} - {self.name}({self.building_type})"


# 单元模型


class Unit(models.Model):
    building = models.ForeignKey(Building,
                                 on_delete=models.CASCADE,
                                 verbose_name="所属楼栋")
    name = models.CharField(max_length=10, verbose_name="单元名称/编号")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "3.单元"
        verbose_name_plural = "3.单元列表"

    def __str__(self):
        return f"{self.building} - {self.name}"


# 楼房房号模型


class Apartment(models.Model):
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             verbose_name="所属单元")
    house_number = models.CharField(max_length=10, verbose_name="房号")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "4.楼房房号"
        verbose_name_plural = "4.楼房房号列表"

    def __str__(self):
        return f"{self.unit} - {self.house_number}"


# 胡同模型


class Hutong(models.Model):
    name = models.CharField(max_length=50, verbose_name="胡同名称/编号")
    community = models.ForeignKey(Community,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  verbose_name="所属社区")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "5.胡同"
        verbose_name_plural = "5.胡同列表"

    def __str__(self):
        return self.name


# 平房房号模型


class SingleHouse(models.Model):
    hutong = models.ForeignKey(Hutong,
                               on_delete=models.CASCADE,
                               verbose_name="所属胡同")
    house_number = models.CharField(max_length=10, verbose_name="房号")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "6.平房房号"
        verbose_name_plural = "6.平房房号列表"

    def __str__(self):
        return f"{self.hutong.name} - {self.house_number}"


# 居住地址模型


class ResidentialAddress(models.Model):
    ADDRESS_TYPE_CHOICES = [(1, "楼房"), (2, "平房")]
    IS_RESIDENT_CHOICES = [(1, "自住"), (2, "租住"), (3, "空房")]
    address_type = models.SmallIntegerField(choices=ADDRESS_TYPE_CHOICES,
                                            verbose_name="地址类型")

    # 楼房地址关联
    estate = models.ForeignKey(HousingEstate,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               verbose_name="所属小区")
    building = models.ForeignKey(Building,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name="所属楼栋")
    unit = models.ForeignKey(Unit,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             verbose_name="所属单元")
    apartment = models.ForeignKey(Apartment,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  verbose_name="楼房房号")

    # 平房地址关联
    hutong = models.ForeignKey(Hutong,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               verbose_name="所属胡同")
    single_house = models.ForeignKey(SingleHouse,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True,
                                     verbose_name="平房房号")

    # 居住状态
    is_resident = models.SmallIntegerField(choices=IS_RESIDENT_CHOICES,
                                           default=3,
                                           verbose_name="居住状态")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "7.居住地址"
        verbose_name_plural = "7.居住地址列表"

    def __str__(self):
        if self.address_type == 1:  # 楼房
            return f"{self.estate.name} - {self.building.name} - {self.unit.name} - {self.apartment.house_number}" if self.estate and self.building and self.unit and self.apartment else "未设置完整地址"
        else:  # 平房
            return f"{self.hutong.name} - {self.single_house.house_number}" if self.hutong and self.single_house else "未设置完整地址"


# 扩展User模型，添加角色字段


class UserProfile(models.Model):
    ROLE_CHOICES = [(1, "超级管理员"), (2, "管理员"), (3, "书记"), (4, "社工")]
    DEPARTMENT_CHOICES = [(1, "社区办"), (2, "社区"), (3, "其他")]

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name="关联用户")
    role = models.SmallIntegerField(choices=ROLE_CHOICES,
                                    default=2,
                                    verbose_name="角色")
    name = models.CharField(max_length=20,
                            verbose_name="姓名",
                            blank=True,
                            null=True)
    phone = models.CharField(max_length=15,
                             verbose_name="联系电话",
                             blank=True,
                             null=True)
    department = models.SmallIntegerField(choices=DEPARTMENT_CHOICES,
                                          default=3,
                                          verbose_name="部门")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "1. 用户扩展信息"  # 添加序号来控制顺序
        verbose_name_plural = "1. 用户扩展信息列表"

    def __str__(self):
        return f"{self.department} - {self.user.username} - {self.phone}"


# 居民模型


class Resident(models.Model):
    GENDER_CHOICES = [(1, "男"), (2, "女")]

    POLITICAL_STATUS_CHOICES = [(1, "中国共产党党员"), (2, "中国共产党预备党员"),
                                (3, "中国共产主义青年团团员"), (4, "中国国民党革命委员会党员"),
                                (5, "中国民主同盟盟员"), (6, "中国民主建国会会员"),
                                (7, "中国民主促进会会员"), (8, "中国农工民主党党员"),
                                (9, "中国致公党党员"), (10, "九三学社社员"),
                                (11, "台湾民主自治同盟盟员"), (12, "无党派民主人士"),
                                (13, "群众")]
    MARITAL_STATUS_CHOICES = [(1, "未婚"), (2, "已婚"), (3, "离异"), (4, "丧偶")]
    EDUCATION_CHOICES = [(1, "文盲"), (2, "小学"), (3, "初中"), (4, "高中"), (5, "大专"),
                         (6, "本科"), (7, "硕士"), (8, "博士"), (9, "其他")]
    NATIONALITY_CHOICES = [(1, "汉族"), (2, "蒙古族"), (3, "回族"), (4, "藏族"),
                           (5, "维吾尔族"), (6, "苗族"), (7, "彝族"), (8, "壮族"),
                           (9, "布依族"), (10, "朝鲜族"), (11, "满族"), (12, "侗族"),
                           (13, "瑶族"), (14, "白族"), (15, "土家族"), (16, "哈尼族"),
                           (17, "哈萨克族"), (18, "傣族"), (19, "黎族"), (20, "傈僳族"),
                           (21, "佤族"), (22, "畲族"), (23, "高山族"), (24, "拉祜族"),
                           (25, "水族"), (26, "东乡族"), (27, "纳西族"), (28, "景颇族"),
                           (29, "柯尔克孜族"), (30, "土族"),
                           (31, "达斡尔族"), (32, "仫佬族"), (33, "羌族"), (34, "布朗族"),
                           (35, "撒拉族"), (36, "毛难族"), (37, "仡佬族"), (38, "锡伯族"),
                           (39, "阿昌族"), (40, "普米族"), (41, "塔吉克族"), (42, "怒族"),
                           (43, "乌孜别克族"), (44, "俄罗斯族"), (45, "鄂温克族"),
                           (46, "崩龙族"), (47, "保安族"), (48, "裕固族"), (49, "京族"),
                           (50, "塔塔尔族"), (51, "独龙族"), (52, "鄂伦春族"),
                           (53, "赫哲族"), (54, "门巴族"), (55, "珞巴族"), (56, "基诺族"),
                           (57, "其他")]
    name = models.CharField(max_length=20, verbose_name="姓名")
    gender = models.SmallIntegerField(choices=GENDER_CHOICES,
                                      verbose_name="性别",
                                      null=True,
                                      blank=True)
    nationality = models.SmallIntegerField(choices=NATIONALITY_CHOICES,
                                           verbose_name="民族",
                                           null=True,
                                           blank=True)
    id_card = models.CharField(max_length=18,
                               unique=True,
                               verbose_name="身份证号",
                               validators=[
                                   RegexValidator(regex=r'^\d{17}[\dXx]$',
                                                  message='身份证号格式不正确',
                                                  code='invalid_id_card')
                               ])
    phone = models.CharField(max_length=15,
                             verbose_name="联系电话",
                             null=True,
                             blank=True)
    family = models.ForeignKey('Family',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               verbose_name="所属家庭")
    political_status = models.SmallIntegerField(
        choices=POLITICAL_STATUS_CHOICES,
        verbose_name="政治面貌",
        blank=True,
        null=True)
    marital_status = models.SmallIntegerField(choices=MARITAL_STATUS_CHOICES,
                                              verbose_name="婚姻状态",
                                              blank=True,
                                              null=True)
    education = models.SmallIntegerField(choices=EDUCATION_CHOICES,
                                         verbose_name="学历",
                                         blank=True,
                                         null=True)
    job = models.BooleanField(default=False, verbose_name="是否有工作")
    is_dead = models.BooleanField(default=False, verbose_name="是否死亡")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "1.居民"
        verbose_name_plural = "1.居民列表"
        indexes = [
            models.Index(fields=['id_card'], name='idx_resident_id_card'),
        ]

    def __str__(self):
        return f"{self.name} - {self.id_card}"


# 家庭模型


class Family(models.Model):
    household_number = models.CharField(max_length=15,
                                        unique=True,
                                        verbose_name="户号")
    owner_name = models.CharField(max_length=20, verbose_name="房主姓名")
    residential_address = models.ForeignKey(ResidentialAddress,
                                            on_delete=models.SET_NULL,
                                            null=True,
                                            blank=True,
                                            verbose_name="居住地址")
    contact_phone = models.CharField(max_length=15,
                                     verbose_name="联系电话",
                                     null=True,
                                     blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "2.家庭"
        verbose_name_plural = "2.家庭列表"
        indexes = [
            models.Index(fields=['household_number'],
                         name='idx_family_household_number'),
        ]

    def __str__(self):
        return f"{self.household_number} - {self.owner_name}"


# 通知模型


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [(1, "紧急"), (2, "普通"), (3, "活动")]
    NOTIFICATION_TIME_TYPE_CHOICES = [(1, "长期"), (2, "定期")]
    title = models.CharField(max_length=100, verbose_name="通知标题")
    content = models.TextField(verbose_name="通知内容")
    notification_type = models.SmallIntegerField(
        choices=NOTIFICATION_TYPE_CHOICES, verbose_name="通知类型")
    publisher = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  verbose_name="发布人")
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    notification_time_type = models.SmallIntegerField(
        default=1,
        choices=NOTIFICATION_TIME_TYPE_CHOICES,
        verbose_name="通知时间类型")
    valid_until = models.DateTimeField(verbose_name="有效期至",
                                       blank=True,
                                       null=True)
    view_count = models.IntegerField(default=0, verbose_name="阅读次数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "2. 通知"  # 添加序号来控制顺序
        verbose_name_plural = "2. 通知列表"
        ordering = ['-publish_time']

    def __str__(self):
        return f"***{self.notification_type}***{self.title} - {self.publish_time}"


# 通知附件模型


import os
from django.utils import timezone

def upload_to_notification_attachments(instance, filename):
    """自定义附件上传路径和文件名，防止重名"""
    # 获取文件扩展名
    ext = os.path.splitext(filename)[1]
    # 使用时间戳和随机数生成唯一文件名
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S%f')
    unique_filename = f'{timestamp}{ext}'
    # 返回完整的上传路径
    return f'notification_attachments/{unique_filename}'

class NotificationAttachment(models.Model):
    notification = models.ForeignKey(Notification,
                                     on_delete=models.CASCADE,
                                     verbose_name="关联通知",
                                     related_name="attachments")
    file = models.FileField(upload_to=upload_to_notification_attachments, verbose_name="附件文件")
    filename = models.CharField(max_length=255, verbose_name="原始文件名")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="附件描述")
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "3. 通知附件"  # 添加序号来控制顺序
        verbose_name_plural = "3. 通知附件列表"

    def __str__(self):
        return f"{self.notification.title} - {self.filename}"


# 通知阅读状态模型


class NotificationRead(models.Model):
    notification = models.ForeignKey(Notification,
                                     on_delete=models.CASCADE,
                                     verbose_name="通知")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    read_time = models.DateTimeField(null=True,
                                     blank=True,
                                     verbose_name="阅读时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # 备注字段
    remark = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        verbose_name = "4. 通知阅读状态"  # 更新序号来控制顺序
        verbose_name_plural = "4. 通知阅读状态列表"
        unique_together = ('notification', 'user')

    def __str__(self):
        return f"{self.is_read} - {self.user.username} - {self.read_time} - {self.notification.title}"

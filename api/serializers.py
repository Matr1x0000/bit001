"""serializers.py - 社区数字化信息系统序列化器

本文件定义了所有模型的序列化器，用于将Django模型实例转换为JSON等格式，
或从JSON数据创建/更新模型实例。序列化器是Django REST Framework的核心组件，
负责数据的序列化和反序列化，以及数据验证。

所有序列化器均继承自ModelSerializer，自动生成字段映射和验证逻辑，
提高了开发效率并保持了代码的一致性。
"""

from rest_framework import serializers
from .models import (
    Community, SocialWorker, HousingEstate, Building, Unit,
    Apartment, Hutong, SingleHouse, ResidentialAddress,
    UserProfile, Resident, Family, Notification,
    NotificationRead, NotificationAttachment
)


class CommunitySerializer(serializers.ModelSerializer):
    """社区信息序列化器
    
    用于将Community模型实例序列化为JSON等格式，或从JSON数据创建/更新Community实例。
    序列化所有字段，包括社区名称、办公地址、联系电话等。
    """
    class Meta:
        model = Community  # 指定关联的模型为Community
        fields = '__all__'  # 序列化所有字段


class SocialWorkerSerializer(serializers.ModelSerializer):
    """社区工作者序列化器
    
    用于将SocialWorker模型实例序列化为JSON等格式，或从JSON数据创建/更新SocialWorker实例。
    序列化所有字段，包括姓名、性别、联系方式、所属社区等。
    """
    class Meta:
        model = SocialWorker  # 指定关联的模型为SocialWorker
        fields = '__all__'  # 序列化所有字段


class HousingEstateSerializer(serializers.ModelSerializer):
    """小区信息序列化器
    
    用于将HousingEstate模型实例序列化为JSON等格式，或从JSON数据创建/更新HousingEstate实例。
    序列化所有字段，包括小区名称、所属社区、物业公司等。
    """
    class Meta:
        model = HousingEstate  # 指定关联的模型为HousingEstate
        fields = '__all__'  # 序列化所有字段


class BuildingSerializer(serializers.ModelSerializer):
    """楼栋信息序列化器
    
    用于将Building模型实例序列化为JSON等格式，或从JSON数据创建/更新Building实例。
    序列化所有字段，包括楼栋名称、所属小区、建筑类型等。
    """
    class Meta:
        model = Building  # 指定关联的模型为Building
        fields = '__all__'  # 序列化所有字段


class UnitSerializer(serializers.ModelSerializer):
    """单元信息序列化器
    
    用于将Unit模型实例序列化为JSON等格式，或从JSON数据创建/更新Unit实例。
    序列化所有字段，包括单元名称、所属楼栋等。
    """
    class Meta:
        model = Unit  # 指定关联的模型为Unit
        fields = '__all__'  # 序列化所有字段


class ApartmentSerializer(serializers.ModelSerializer):
    """楼房房号序列化器
    
    用于将Apartment模型实例序列化为JSON等格式，或从JSON数据创建/更新Apartment实例。
    序列化所有字段，包括房号、所属单元等。
    """
    class Meta:
        model = Apartment  # 指定关联的模型为Apartment
        fields = '__all__'  # 序列化所有字段


class HutongSerializer(serializers.ModelSerializer):
    """胡同信息序列化器
    
    用于将Hutong模型实例序列化为JSON等格式，或从JSON数据创建/更新Hutong实例。
    序列化所有字段，包括胡同名称、所属社区等。
    """
    class Meta:
        model = Hutong  # 指定关联的模型为Hutong
        fields = '__all__'  # 序列化所有字段


class SingleHouseSerializer(serializers.ModelSerializer):
    """平房房号序列化器
    
    用于将SingleHouse模型实例序列化为JSON等格式，或从JSON数据创建/更新SingleHouse实例。
    序列化所有字段，包括房号、所属胡同等。
    """
    class Meta:
        model = SingleHouse  # 指定关联的模型为SingleHouse
        fields = '__all__'  # 序列化所有字段


class ResidentialAddressSerializer(serializers.ModelSerializer):
    """居住地址序列化器
    
    用于将ResidentialAddress模型实例序列化为JSON等格式，或从JSON数据创建/更新ResidentialAddress实例。
    序列化所有字段，包括地址类型、所属小区/胡同、居住状态等。
    """
    class Meta:
        model = ResidentialAddress  # 指定关联的模型为ResidentialAddress
        fields = '__all__'  # 序列化所有字段


class UserProfileSerializer(serializers.ModelSerializer):
    """用户扩展信息序列化器
    
    用于将UserProfile模型实例序列化为JSON等格式，或从JSON数据创建/更新UserProfile实例。
    序列化所有字段，包括用户角色、部门、账户状态等。
    """
    class Meta:
        model = UserProfile  # 指定关联的模型为UserProfile
        fields = '__all__'  # 序列化所有字段


class FamilySerializer(serializers.ModelSerializer):
    """家庭信息序列化器
    
    用于将Family模型实例序列化为JSON等格式，或从JSON数据创建/更新Family实例。
    序列化所有字段，包括户号、房主姓名、居住地址等。
    """
    class Meta:
        model = Family  # 指定关联的模型为Family
        fields = '__all__'  # 序列化所有字段


class ResidentSerializer(serializers.ModelSerializer):
    """居民信息序列化器
    
    用于将Resident模型实例序列化为JSON等格式，或从JSON数据创建/更新Resident实例。
    包含嵌套的FamilySerializer，用于序列化关联的家庭数据。
    
    特殊字段：
    - family: 嵌套序列化家庭数据，只读
    """
    family = FamilySerializer(read_only=True)  # 嵌套序列化家庭数据，只读

    class Meta:
        model = Resident  # 指定关联的模型为Resident
        fields = '__all__'  # 序列化所有字段


class NotificationSerializer(serializers.ModelSerializer):
    """通知信息序列化器
    
    用于将Notification模型实例序列化为JSON等格式，或从JSON数据创建/更新Notification实例。
    序列化所有字段，包括通知标题、内容、发布者、发布时间等。
    """
    class Meta:
        model = Notification  # 指定关联的模型为Notification
        fields = '__all__'  # 序列化所有字段


class NotificationReadSerializer(serializers.ModelSerializer):
    """通知阅读记录序列化器
    
    用于将NotificationRead模型实例序列化为JSON等格式，或从JSON数据创建/更新NotificationRead实例。
    序列化所有字段，包括通知、用户、阅读状态、阅读时间等。
    """
    class Meta:
        model = NotificationRead  # 指定关联的模型为NotificationRead
        fields = '__all__'  # 序列化所有字段


class NotificationAttachmentSerializer(serializers.ModelSerializer):
    """通知附件序列化器
    
    用于将NotificationAttachment模型实例序列化为JSON等格式，或从JSON数据创建/更新NotificationAttachment实例。
    包含自定义字段，用于获取文件大小和完整URL。
    
    自定义字段：
    - file_size: 获取文件大小，单位为字节
    - file: 获取文件的完整URL
    """
    # 计算文件大小的自定义字段
    file_size = serializers.SerializerMethodField()
    # 获取文件完整URL的自定义字段
    file = serializers.SerializerMethodField()

    class Meta:
        model = NotificationAttachment  # 指定关联的模型为NotificationAttachment
        # 自定义序列化字段列表
        fields = [
            'id', 'notification', 'filename', 'file', 'file_size',
            'upload_time'
        ]

    def get_file_size(self, obj):
        """获取文件大小
        
        Args:
            obj: NotificationAttachment实例
            
        Returns:
            int: 文件大小，单位为字节，获取失败返回0
        """
        try:
            return obj.file.size
        except:
            return 0

    def get_file(self, obj):
        """获取文件的完整URL
        
        Args:
            obj: NotificationAttachment实例
            
        Returns:
            str: 文件的完整URL，获取失败返回空字符串
        """
        try:
            return obj.file.url
        except:
            return ''

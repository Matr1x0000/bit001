from rest_framework import serializers
from .models import (Community, SocialWorker, HousingEstate, Building, Unit,
                     Apartment, Hutong, SingleHouse, ResidentialAddress,
                     UserProfile, Resident, Family, Notification,
                     NotificationRead, NotificationAttachment)


# 社区信息序列化器：用于将 Community 模型实例序列化为 JSON 等格式，或反序列化创建/更新 Community 实例
class CommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community  # 指定关联的模型为 Community
        fields = '__all__'  # 序列化所有字段


class SocialWorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialWorker
        fields = '__all__'


class HousingEstateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HousingEstate
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Unit
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Apartment
        fields = '__all__'


class HutongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hutong
        fields = '__all__'


class SingleHouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = SingleHouse
        fields = '__all__'


class ResidentialAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResidentialAddress
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class FamilySerializer(serializers.ModelSerializer):

    class Meta:
        model = Family
        fields = '__all__'


class ResidentSerializer(serializers.ModelSerializer):
    family = FamilySerializer(read_only=True)  # 嵌套序列化家庭数据

    class Meta:
        model = Resident
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationRead
        fields = '__all__'


class NotificationAttachmentSerializer(serializers.ModelSerializer):
    # 计算文件大小
    file_size = serializers.SerializerMethodField()
    # 获取文件URL
    file = serializers.SerializerMethodField()

    class Meta:
        model = NotificationAttachment
        fields = [
            'id', 'notification', 'filename', 'file', 'file_size',
            'upload_time'
        ]

    def get_file_size(self, obj):
        # 获取文件大小
        try:
            return obj.file.size
        except:
            return 0

    def get_file(self, obj):
        # 获取文件的完整URL
        try:
            return obj.file.url
        except:
            return ''

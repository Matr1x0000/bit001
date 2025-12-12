from rest_framework import serializers
from .models import (
    Community, SocialWorker, HousingEstate, Building, Unit,
    Apartment, Hutong, SingleHouse, ResidentialAddress, UserProfile,
    Resident, Family, Notification, NotificationRead
)


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


class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = '__all__'


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationRead
        fields = '__all__'

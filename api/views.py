import logging
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import (Community, SocialWorker, HousingEstate, Building, Unit,
                     Apartment, Hutong, SingleHouse, ResidentialAddress,
                     UserProfile, Resident, Family, Notification,
                     NotificationRead, NotificationAttachment, Cadre)
from .serializers import (
    CommunitySerializer, SocialWorkerSerializer, HousingEstateSerializer,
    BuildingSerializer, UnitSerializer, ApartmentSerializer, HutongSerializer,
    SingleHouseSerializer, ResidentialAddressSerializer, UserProfileSerializer,
    ResidentSerializer, FamilySerializer, NotificationSerializer,
    NotificationReadSerializer, NotificationAttachmentSerializer)
from .permissions import (CanDeleteResident, CanDeleteFamily,
                          CanPublishNotification, CanDeleteNotification,
                          CanViewResidents, CanAddResident, CanEditResident,
                          CanViewFamilies, CanAddFamily, CanEditFamily,
                          CanViewNotifications)

# 设置日志记录器
logger = logging.getLogger(__name__)


# 逻辑删除Mixin，用于将物理删除改为逻辑删除
class SoftDeleteMixin:

    def destroy(self, request, *args, **kwargs):
        # 获取要删除的对象
        instance = self.get_object()

        # 获取对象信息用于日志记录
        object_type = type(instance).__name__
        object_id = instance.id

        # 逻辑删除：更新is_deleted字段为True
        instance.is_deleted = True
        instance.save()

        # 记录删除操作日志
        logger.info(
            f"删除操作成功: 用户ID={request.user.id}, 角色级别={request.user.userprofile.role}, 操作=DELETE_{object_type}, 对象ID={object_id}"
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


# 社区视图集：提供社区模型的增删改查接口，仅允许已认证用户访问
class CommunityViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = Community.objects.filter(is_deleted=False)  # 只获取未删除的社区数据
    serializer_class = CommunitySerializer  # 指定序列化器
    permission_classes = [permissions.IsAuthenticated]  # 设置权限为仅已认证用户


class SocialWorkerViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = SocialWorker.objects.filter(is_deleted=False)
    serializer_class = SocialWorkerSerializer
    permission_classes = [permissions.IsAuthenticated]


class HousingEstateViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = HousingEstate.objects.filter(is_deleted=False)
    serializer_class = HousingEstateSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 添加过滤支持，允许通过community参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['community']


class BuildingViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = Building.objects.filter(is_deleted=False)
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 添加过滤支持，允许通过estate参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estate']


class UnitViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = Unit.objects.filter(is_deleted=False)
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 添加过滤支持，允许通过building参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['building']


class ApartmentViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = Apartment.objects.filter(is_deleted=False)
    serializer_class = ApartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 添加过滤支持，允许通过unit参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['unit']


class HutongViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = Hutong.objects.filter(is_deleted=False)
    serializer_class = HutongSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 添加过滤支持，允许通过community参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['community']


class SingleHouseViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = SingleHouse.objects.filter(is_deleted=False)
    serializer_class = SingleHouseSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 添加过滤支持，允许通过hutong参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['hutong']


class ResidentialAddressViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = ResidentialAddress.objects.filter(is_deleted=False)
    serializer_class = ResidentialAddressSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProfileViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = UserProfile.objects.filter(is_deleted=False)
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResidentViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = Resident.objects.filter(is_deleted=False)
    serializer_class = ResidentSerializer
    permission_classes = [permissions.IsAuthenticated, CanViewResidents]
    # 添加过滤支持，允许通过family参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['family']

    def get_permissions(self):
        """
        根据请求方法动态设置权限
        """
        if self.action == 'destroy':
            return [permissions.IsAuthenticated(), CanDeleteResident()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), CanAddResident()]
        return super().get_permissions()


class FamilyViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = Family.objects.filter(is_deleted=False)
    serializer_class = FamilySerializer
    permission_classes = [permissions.IsAuthenticated, CanViewFamilies]
    # 添加搜索支持，允许通过household_number、owner_name、contact_phone搜索
    filter_backends = [filters.SearchFilter]
    search_fields = ['household_number', 'owner_name', 'contact_phone']

    def get_permissions(self):
        """
        根据请求方法动态设置权限
        """
        if self.action == 'destroy':
            return [permissions.IsAuthenticated(), CanDeleteFamily()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), CanAddFamily()]
        return super().get_permissions()


class NotificationViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = Notification.objects.filter(is_deleted=False)
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, CanViewNotifications]

    def get_permissions(self):
        """
        根据请求方法动态设置权限
        """
        if self.action in ['create', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), CanPublishNotification()]
        elif self.action == 'destroy':
            return [permissions.IsAuthenticated(), CanDeleteNotification()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        # 获取通知数据
        data = request.data.copy()

        # 创建通知对象
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        notification = serializer.save()

        # 处理附件上传
        if 'attachments' in request.FILES:
            files = request.FILES.getlist('attachments')
            for file in files:
                # 创建附件对象
                NotificationAttachment.objects.create(
                    notification=notification, file=file, filename=file.name)

        # 记录发布通知操作日志
        logger.info(
            f"发布通知操作成功: 用户ID={request.user.id}, 角色级别={request.user.userprofile.role}, 通知ID={notification.id}, 通知标题={notification.title}"
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """
        删除通知，需要验证所有权
        """
        # 调用SoftDeleteMixin的destroy方法
        return super().destroy(request, *args, **kwargs)


class NotificationReadViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = NotificationRead.objects.filter(is_deleted=False)
    serializer_class = NotificationReadSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationAttachmentViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    queryset = NotificationAttachment.objects.filter(is_deleted=False)
    serializer_class = NotificationAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_unread_notifications_api(request):
    """获取当前用户的未读通知数量
    
    API端点，用于获取当前登录用户的未读通知数量。
    计算方式：总通知数 - 已读通知数
    
    Args:
        request: HTTP请求对象
        
    Returns:
        Response: JSON响应，包含未读通知数量
        
    示例:
        GET /api/unread-notifications/
        Response: {"unread_count": 3}
    """
    # 获取当前用户的通知总数（排除已删除的通知）
    total_notifications = Notification.objects.filter(is_deleted=False).count()

    # 获取当前用户的已读通知数量（排除已删除的通知）
    read_notifications = NotificationRead.objects.filter(
        user=request.user, notification__is_deleted=False).count()

    # 计算未读通知数量
    unread_count = total_notifications - read_notifications

    return Response({'unread_count': unread_count})


@login_required
def add_resident(request):
    """添加新居民
    
    处理添加新居民的请求，支持AJAX和传统表单提交。
    
    Args:
        request: HTTP请求对象，包含居民信息表单数据
        
    Returns:
        JsonResponse: 当请求为AJAX时，返回JSON响应
        HttpResponseRedirect: 当请求为GET时，重定向到居民列表页面
    """
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        nationality = request.POST.get('nationality')
        id_card = request.POST.get('id_card')
        phone = request.POST.get('phone')
        family_id = request.POST.get('family')
        political_status = request.POST.get('political_status')
        marital_status = request.POST.get('marital_status')
        education = request.POST.get('education')
        job = request.POST.get('job') == 'true'  # 转换为布尔值
        is_dead = request.POST.get('is_dead') == 'true'  # 转换为布尔值
        remark = request.POST.get('remark')

        # 验证必填字段
        if not name or not id_card:
            return JsonResponse({'success': False, 'message': '姓名和身份证号不能为空'})

        try:
            # 创建居民对象
            resident = Resident(
                name=name,
                gender=gender if gender else None,
                nationality=nationality if nationality else None,
                id_card=id_card,
                phone=phone,
                family_id=family_id if family_id else None,
                political_status=political_status
                if political_status else None,
                marital_status=marital_status if marital_status else None,
                education=education if education else None,
                job=job,
                is_dead=is_dead,
                remark=remark)
            resident.save()
            return JsonResponse({'success': True, 'message': '居民添加成功'})
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'添加失败: {str(e)}'
            })

    # GET 请求，重定向到居民列表页面
    return redirect('residents')


@login_required
def profile_view(request):
    """查看和编辑个人资料
    
    显示当前登录用户的个人资料，包括基本信息、社区工作者信息和干部信息。
    
    Args:
        request: HTTP请求对象
        
    Returns:
        HttpResponse: 渲染个人资料页面
    """
    # 获取与用户关联的社区工作者和干部信息
    social_worker = None
    cadre = None
    try:
        # 使用filter.first()替代get()，避免DoesNotExist异常
        social_worker = SocialWorker.objects.filter(
            user_profile=request.user.userprofile).first()
        cadre = Cadre.objects.filter(
            user_profile=request.user.userprofile).first()
    except Exception as e:
        print(f"获取关联信息失败: {e}")

    # 准备上下文数据
    context = {
        'user': request.user,  # 用户基本信息
        'is_authenticated': request.user.is_authenticated,  # 认证状态
        'user_profile': request.user.userprofile,  # 用户扩展信息
        'social_worker': social_worker,  # 社区工作者信息（如果有）
        'cadre': cadre,  # 干部信息（如果有）
    }

    return render(request, 'profile.html', context)


@login_required
def profile_update(request):
    """更新用户个人资料
    
    处理更新用户个人资料的请求，支持JSON和表单数据格式，
    同时更新用户的社区工作者信息和干部信息（如果有）。
    
    Args:
        request: HTTP请求对象，包含更新的个人资料数据
        
    Returns:
        JsonResponse: 当请求为AJAX时，返回JSON响应
        HttpResponseRedirect: 当请求为传统表单提交时，重定向到个人资料页面
        HttpResponse: 当请求为GET时，渲染个人资料页面
    """
    if request.method == 'POST':
        try:
            # 检查请求类型，支持JSON和表单数据
            if request.headers.get('Content-Type') == 'application/json':
                # 获取JSON数据
                data = json.loads(request.body)
            else:
                # 获取表单数据
                data = request.POST.dict()

            # 更新用户资料的不同部分
            user_profile = request.user.userprofile

            # 1. 更新社区工作者信息（如果用户是社区工作者）
            social_worker = SocialWorker.objects.filter(
                user_profile=user_profile).first()
            if social_worker:
                social_worker.name = data.get('sw_name', social_worker.name)
                social_worker.gender = data.get('sw_gender',
                                                social_worker.gender)
                social_worker.phone = data.get('sw_phone', social_worker.phone)

                # 处理是否为书记（转换为布尔值）
                sw_is_secretary = data.get('sw_is_secretary',
                                           social_worker.is_secretary)
                if isinstance(sw_is_secretary, str):
                    sw_is_secretary = sw_is_secretary.lower(
                    ) == 'true' or sw_is_secretary == '1'
                social_worker.is_secretary = sw_is_secretary

                # 处理出生年月
                sw_birth_date = data.get('sw_birth_date')
                if sw_birth_date:
                    social_worker.birth_date = sw_birth_date
                social_worker.save()

            # 2. 更新干部信息（如果用户是干部）
            cadre = Cadre.objects.filter(user_profile=user_profile).first()
            if cadre:
                cadre.name = data.get('cadre_name', cadre.name)
                cadre.gender = data.get('cadre_gender', cadre.gender)
                cadre.phone = data.get('cadre_phone', cadre.phone)
                cadre.position = data.get('cadre_position', cadre.position)

                # 处理出生年月
                cadre_birth_date = data.get('cadre_birth_date')
                if cadre_birth_date:
                    cadre.birth_date = cadre_birth_date
                cadre.save()

            # 返回响应，根据请求类型选择不同的响应方式
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': '个人资料更新成功'})
            else:
                messages.success(request, '个人资料更新成功')
                return redirect('profile')
        except Exception as e:
            # 处理异常情况
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'更新失败: {str(e)}'
                })
            else:
                messages.error(request, f'更新失败: {str(e)}')
                return redirect('profile')

    # GET 请求，返回个人资料页面
    return render(request, 'profile.html')


@login_required
def edit_resident(request, resident_id):
    """编辑现有居民信息
    
    处理编辑现有居民信息的请求，仅支持PUT方法，返回JSON响应。
    
    Args:
        request: HTTP请求对象，包含更新的居民信息
        resident_id: 居民ID，用于标识要编辑的居民
        
    Returns:
        JsonResponse: JSON响应，包含操作结果和消息
        HttpResponseRedirect: 当请求为GET时，重定向到居民列表页面
    """
    # 获取要编辑的居民对象，不存在则返回404
    resident = get_object_or_404(Resident, id=resident_id)

    if request.method == 'PUT':
        # 获取PUT请求数据（JSON格式）
        import json
        data = json.loads(request.body)

        # 提取更新字段
        name = data.get('name')
        gender = data.get('gender')
        nationality = data.get('nationality')
        id_card = data.get('id_card')
        phone = data.get('phone')
        family_id = data.get('family')
        political_status = data.get('political_status')
        marital_status = data.get('marital_status')
        education = data.get('education')
        job = data.get('job') == 'true'  # 转换为布尔值
        is_dead = data.get('is_dead') == 'true'  # 转换为布尔值
        remark = data.get('remark')

        # 验证必填字段
        if not name or not id_card:
            return JsonResponse({'success': False, 'message': '姓名和身份证号不能为空'})

        try:
            # 更新居民对象字段
            resident.name = name
            resident.gender = gender if gender else None
            resident.nationality = nationality if nationality else None
            resident.id_card = id_card
            resident.phone = phone
            resident.family_id = family_id if family_id else None
            resident.political_status = political_status if political_status else None
            resident.marital_status = marital_status if marital_status else None
            resident.education = education if education else None
            resident.job = job
            resident.is_dead = is_dead
            resident.remark = remark
            resident.save()

            return JsonResponse({'success': True, 'message': '居民信息更新成功'})
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'更新失败: {str(e)}'
            })

    # GET 请求，重定向到居民列表页面
    return redirect('residents')


@login_required
def delete_resident(request, resident_id):
    """删除现有居民（逻辑删除）
    
    处理删除居民的请求，实现逻辑删除（将is_deleted字段设置为True），
    而不是物理删除数据库记录。
    
    Args:
        request: HTTP请求对象
        resident_id: 居民ID，用于标识要删除的居民
        
    Returns:
        HttpResponseRedirect: 重定向回居民列表页面
    """
    # 获取要删除的居民对象（仅获取未删除的记录）
    resident = get_object_or_404(Resident, id=resident_id, is_deleted=False)

    try:
        # 执行逻辑删除：更新is_deleted字段为True
        resident.is_deleted = True
        resident.save()
        messages.success(request, '居民删除成功')
    except Exception as e:
        messages.error(request, f'删除失败: {str(e)}')

    # 重定向回居民列表页面
    return redirect('residents')


@login_required
def add_family(request):
    """添加新家庭
    
    处理添加新家庭的请求，同时支持创建或关联居住地址。
    支持楼房和平房两种地址类型。
    
    Args:
        request: HTTP请求对象，包含家庭信息和地址信息表单数据
        
    Returns:
        HttpResponseRedirect: 当家庭添加成功时，重定向到家庭列表页面
        HttpResponse: 当请求为GET时，渲染添加家庭表单页面
    """
    if request.method == 'POST':
        # 获取家庭基本信息表单数据
        household_number = request.POST.get('household_number')
        owner_name = request.POST.get('owner_name')
        contact_phone = request.POST.get('contact_phone')
        remark = request.POST.get('remark')

        # 获取地址信息
        address_type = request.POST.get('address_type')  # 1-楼房，2-平房
        community_id = request.POST.get('community')
        estate_id = request.POST.get('estate')
        building_id = request.POST.get('building')
        unit_id = request.POST.get('unit')
        apartment_id = request.POST.get('apartment')
        hutong_id = request.POST.get('hutong')
        single_house_id = request.POST.get('single_house')

        residential_address = None

        # 如果选择了地址类型，创建或获取居住地址
        if address_type:
            if address_type == '1':
                # 处理楼房地址
                if estate_id and building_id and unit_id and apartment_id:
                    try:
                        # 尝试获取现有的居住地址，如果不存在则创建
                        from .models import Apartment
                        apartment = Apartment.objects.get(id=apartment_id)
                        residential_address, created = ResidentialAddress.objects.get_or_create(
                            address_type=1,
                            estate_id=estate_id,
                            building_id=building_id,
                            unit_id=unit_id,
                            apartment=apartment)
                    except Exception as e:
                        messages.error(request, f'创建居住地址失败: {str(e)}')
                        # 只获取未删除的社区
                        communities = Community.objects.filter(
                            is_deleted=False)
                        return render(request, 'add_family.html',
                                      {'communities': communities})
            elif address_type == '2':
                # 处理平房地址
                if hutong_id and single_house_id:
                    try:
                        # 尝试获取现有的居住地址，如果不存在则创建
                        from .models import SingleHouse
                        single_house = SingleHouse.objects.get(
                            id=single_house_id)
                        residential_address, created = ResidentialAddress.objects.get_or_create(
                            address_type=2,
                            hutong_id=hutong_id,
                            single_house=single_house)
                    except Exception as e:
                        messages.error(request, f'创建居住地址失败: {str(e)}')
                        return render(request, 'add_family.html',
                                      {'communities': Community.objects.all()})

        # 验证家庭必填字段
        if not household_number or not owner_name:
            messages.error(request, '户号和房主姓名不能为空')
            return render(
                request, 'add_family.html',
                {'communities': Community.objects.filter(is_deleted=False)})

        try:
            # 创建家庭对象
            family = Family(household_number=household_number,
                            owner_name=owner_name,
                            residential_address=residential_address,
                            contact_phone=contact_phone,
                            remark=remark)
            family.save()
            messages.success(request, '家庭添加成功')
            return redirect('families')
        except Exception as e:
            messages.error(request, f'添加失败: {str(e)}')
            # 只获取未删除的社区
            communities = Community.objects.filter(is_deleted=False)
            return render(request, 'add_family.html',
                          {'communities': communities})

    # GET 请求，显示添加家庭表单
    # 只获取未删除的社区
    communities = Community.objects.filter(is_deleted=False)
    return render(request, 'add_family.html', {'communities': communities})


@login_required
def delete_family(request, family_id):
    """删除现有家庭（逻辑删除）
    
    处理删除家庭的请求，实现逻辑删除（将is_deleted字段设置为True）。
    具有以下特性：
    1. 只有未删除的家庭才能被删除
    2. 如果家庭下有未删除的居民，则不允许删除
    3. 支持AJAX和传统请求
    
    Args:
        request: HTTP请求对象
        family_id: 家庭ID，用于标识要删除的家庭
        
    Returns:
        JsonResponse: 当请求为AJAX时，返回JSON响应
        HttpResponseRedirect: 当请求为传统请求时，重定向回家庭列表页面
    """
    # 获取要删除的家庭对象（仅获取未删除的记录）
    family = get_object_or_404(Family, id=family_id, is_deleted=False)

    try:
        # 检查是否有居民关联到该家庭（只检查未删除的居民）
        resident_count = Resident.objects.filter(family=family,
                                                 is_deleted=False).count()

        if resident_count > 0:
            # 如果有居民关联，不允许删除
            error_msg = f'删除失败：该家庭下还有 {resident_count} 名未删除的居民'

            # 检查是否为AJAX请求，返回不同的响应格式
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': error_msg
                },
                                    status=400)
            messages.error(request, error_msg)
            return redirect('families')

        # 执行逻辑删除：更新is_deleted字段为True
        family.is_deleted = True
        family.save()

        success_msg = '家庭删除成功'

        # 检查是否为AJAX请求，返回不同的响应格式
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': success_msg})

        messages.success(request, success_msg)
    except Exception as e:
        error_msg = f'删除失败: {str(e)}'

        # 检查是否为AJAX请求，返回不同的响应格式
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': error_msg
            },
                                status=500)

        messages.error(request, error_msg)

    # 重定向回家庭列表页面
    return redirect('families')


@login_required
def edit_family(request, family_id):
    """编辑现有家庭信息
    
    处理编辑现有家庭信息的请求，支持修改家庭基本信息和居住地址。
    支持楼房和平房两种地址类型。
    
    Args:
        request: HTTP请求对象，包含更新的家庭信息表单数据
        family_id: 家庭ID，用于标识要编辑的家庭
        
    Returns:
        HttpResponseRedirect: 当家庭更新成功时，重定向到家庭列表页面
        HttpResponse: 当请求为GET时，渲染编辑家庭表单页面
    """
    # 获取要编辑的家庭对象（仅获取未删除的记录）
    family = get_object_or_404(Family, id=family_id, is_deleted=False)

    if request.method == 'POST':
        # 获取家庭基本信息表单数据
        household_number = request.POST.get('household_number')
        owner_name = request.POST.get('owner_name')
        contact_phone = request.POST.get('contact_phone')
        remark = request.POST.get('remark')

        # 获取地址信息
        address_type = request.POST.get('address_type')  # 1-楼房，2-平房
        community_id = request.POST.get('community')
        estate_id = request.POST.get('estate')
        building_id = request.POST.get('building')
        unit_id = request.POST.get('unit')
        apartment_id = request.POST.get('apartment')
        hutong_id = request.POST.get('hutong')
        single_house_id = request.POST.get('single_house')

        residential_address = None

        # 如果选择了地址类型，创建或获取居住地址
        if address_type:
            if address_type == '1':
                # 处理楼房地址更新
                if estate_id and building_id and unit_id and apartment_id:
                    try:
                        # 尝试获取现有的居住地址，如果不存在则创建
                        from .models import Apartment
                        apartment = Apartment.objects.get(id=apartment_id)
                        residential_address, created = ResidentialAddress.objects.get_or_create(
                            address_type=1,
                            estate_id=estate_id,
                            building_id=building_id,
                            unit_id=unit_id,
                            apartment=apartment)
                    except Exception as e:
                        messages.error(request, f'创建居住地址失败: {str(e)}')
                        return render(
                            request, 'edit_family.html', {
                                'family': family,
                                'communities': Community.objects.all()
                            })
            elif address_type == '2':
                # 处理平房地址更新
                if hutong_id and single_house_id:
                    try:
                        # 尝试获取现有的居住地址，如果不存在则创建
                        from .models import SingleHouse
                        single_house = SingleHouse.objects.get(
                            id=single_house_id)
                        residential_address, created = ResidentialAddress.objects.get_or_create(
                            address_type=2,
                            hutong_id=hutong_id,
                            single_house=single_house)
                    except Exception as e:
                        messages.error(request, f'创建居住地址失败: {str(e)}')
                        return render(
                            request, 'edit_family.html', {
                                'family':
                                family,
                                'communities':
                                Community.objects.filter(is_deleted=False)
                            })

        # 验证家庭必填字段
        if not household_number or not owner_name:
            messages.error(request, '户号和房主姓名不能为空')
            return render(
                request, 'edit_family.html', {
                    'family': family,
                    'communities': Community.objects.filter(is_deleted=False)
                })

        try:
            # 更新家庭对象字段
            family.household_number = household_number
            family.owner_name = owner_name
            family.residential_address = residential_address
            family.contact_phone = contact_phone
            family.remark = remark
            family.save()

            messages.success(request, '家庭更新成功')
            return redirect('families')
        except Exception as e:
            messages.error(request, f'更新失败: {str(e)}')
            return render(
                request, 'edit_family.html', {
                    'family': family,
                    'communities': Community.objects.filter(is_deleted=False)
                })

    # GET 请求，显示编辑家庭表单
    return render(
        request, 'edit_family.html', {
            'family': family,
            'communities': Community.objects.filter(is_deleted=False)
        })


@login_required
def index(request):
    """首页视图
    
    简单的重定向视图，将用户从首页重定向到仪表盘页面。
    
    Args:
        request: HTTP请求对象
        
    Returns:
        HttpResponseRedirect: 重定向到仪表盘页面
    """
    return redirect('dashboard')


@login_required
def dashboard(request):
    """仪表盘视图
    
    系统的主仪表盘页面，展示多种数据统计和功能模块：
    1. 社区人口与家庭数据统计
    2. 通讯录管理功能
    3. 用户未读通知计数
    4. 社区列表展示
    
    根据用户的部门（社区办/社区）显示不同的数据范围。
    
    Args:
        request: HTTP请求对象，包含分页、搜索和排序参数
        
    Returns:
        HttpResponse: 渲染仪表盘页面
    """

    # 社区人口与家庭数据展示功能
    def get_community_data():
        """获取社区人口与家庭数据
        
        根据用户部门返回不同范围的数据：
        - 社区办：显示所有社区的总人口和总家庭数
        - 社区：显示用户所属社区的人口和家庭数
        
        Returns:
            dict: 包含总人口、总家庭数和数据源的字典
        """
        # 初始化数据结构
        community_data = {
            'total_population': '-',
            'total_families': '-',
            'data_source': ''
        }

        # 获取用户的部门信息
        user_profile = request.user.userprofile
        department = user_profile.get_department_display()

        if department == '社区办':
            # 社区办用户：显示所有社区的汇总数据
            total_population = Resident.objects.count()
            total_families = Family.objects.count()

            community_data = {
                'total_population': total_population,
                'total_families': total_families,
                'data_source': '系统数据库'
            }
        elif department == '社区':
            # 社区用户：显示所属社区的数据
            try:
                # 查找用户关联的社区工作者
                social_worker = SocialWorker.objects.get(
                    user_profile=user_profile)
                community = social_worker.community

                # 查询该社区的总人口数和总家庭数
                total_population = Resident.objects.filter(
                    family__residential_address__estate__community=community
                ).count()
                total_families = Family.objects.filter(
                    residential_address__estate__community=community).count()

                community_data = {
                    'total_population': total_population,
                    'total_families': total_families,
                    'data_source': f'{community.name}社区数据库'
                }
            except SocialWorker.DoesNotExist:
                # 如果用户没有关联社区工作者，保持默认数据
                pass

        return community_data

    # 通讯录管理功能
    def get_contacts_data(search_query=None,
                          page=1,
                          page_size=20,
                          sort_field=None,
                          sort_order=None):
        """获取通讯录数据
        
        查询所有未离职的社区工作者和干部信息，支持搜索、分页和排序。
        
        Args:
            search_query: 搜索关键词
            page: 当前页码
            page_size: 每页记录数
            sort_field: 排序字段（name/department/phone/type）
            sort_order: 排序顺序（asc/desc）
            
        Returns:
            dict: 包含通讯录数据、分页信息和统计数据的字典
        """
        # 查询条件：只获取未离职的人员
        social_worker_query = Q(is_baned=True)
        cadre_query = Q(is_baned=True)

        # 添加搜索条件
        if search_query:
            social_worker_query &= (Q(name__icontains=search_query)
                                    | Q(phone__icontains=search_query))
            cadre_query &= (Q(name__icontains=search_query)
                            | Q(phone__icontains=search_query))

        # 查询社区工作者，预取社区信息以减少数据库查询
        social_workers = SocialWorker.objects.filter(
            social_worker_query).select_related('community').order_by('name')

        # 查询干部
        cadres = Cadre.objects.filter(cadre_query).order_by('name')

        # 合并结果
        all_contacts = list(social_workers) + list(cadres)

        # 定义排序函数
        def get_sort_key(contact):
            """获取排序关键字
            
            根据sort_field返回不同的排序值，支持按姓名、部门、电话和类型排序。
            使用拼音排序确保中文排序正确。
            """
            if sort_field == 'name':
                # 按姓名拼音排序
                return ''.join(lazy_pinyin(contact.name))
            elif sort_field == 'department':
                if isinstance(contact, SocialWorker):
                    # 按社区名称拼音排序
                    department_name = contact.community.name if contact.community else ''
                    return ''.join(lazy_pinyin(department_name))
                else:
                    return ''.join(lazy_pinyin('社区办'))
            elif sort_field == 'phone':
                return contact.phone or ''
            elif sort_field == 'type':
                if isinstance(contact, SocialWorker):
                    return ''.join(lazy_pinyin('社工'))
                else:
                    # 按职务拼音排序
                    position = contact.position if contact.position else '无职务'
                    return ''.join(lazy_pinyin(position))
            else:
                # 默认按姓名排序
                return ''.join(lazy_pinyin(contact.name))

        # 执行排序
        if sort_field is not None:
            reverse = True if sort_order == 'desc' else False
            all_contacts.sort(key=get_sort_key, reverse=reverse)

        # 分页处理
        paginator = Paginator(all_contacts, page_size)
        page_obj = paginator.get_page(page)

        # 格式化数据
        formatted_contacts = []
        for contact in page_obj.object_list:
            # 确定部门和职位
            if isinstance(contact, SocialWorker):
                department = contact.community.name if contact.community else '未分配社区'
                position = '社工'
            else:
                department = '社区办'
                position = contact.position if contact.position else '无职务'

            formatted_contacts.append({
                'id': contact.id,
                'name': contact.name,
                'department': department,
                'phone': contact.phone,
                'type': position
            })

        return {
            'contacts': formatted_contacts,
            'page_obj': page_obj,
            'total_pages': paginator.num_pages,
            'total_contacts': paginator.count,
            'current_page': page_obj.number
        }

    # 用户未读通知计数功能
    def get_unread_notifications_count():
        """获取用户未读通知数量
        
        计算当前用户的未读通知数量：总通知数 - 已读通知数
        
        Returns:
            int: 未读通知数量
        """
        # 获取当前用户的通知总数（排除已删除的通知）
        total_notifications = Notification.objects.filter(
            is_deleted=False).count()

        # 获取当前用户的已读通知数量（排除已删除的通知）
        read_notifications = NotificationRead.objects.filter(
            user=request.user, notification__is_deleted=False).count()

        # 计算未读通知数量
        unread_count = total_notifications - read_notifications

        return unread_count

    # 社区列表展示功能
    def get_community_list(page=1, page_size=10):
        """获取社区列表数据
        
        查询所有社区信息，支持分页。
        
        Args:
            page: 当前页码
            page_size: 每页记录数
            
        Returns:
            dict: 包含社区列表、分页信息和统计数据的字典
        """
        # 查询所有社区，按名称排序
        communities = Community.objects.all().order_by('name')

        # 分页处理
        paginator = Paginator(communities, page_size)
        page_obj = paginator.get_page(page)

        # 格式化数据
        formatted_communities = []
        for community in page_obj.object_list:
            formatted_communities.append({
                'id':
                community.id,
                'name':
                community.name,
                'address':
                community.office_address or '',
                'phone':
                community.office_phone or ''
            })

        return {
            'communities': formatted_communities,
            'page_obj': page_obj,
            'total_pages': paginator.num_pages,
            'total_communities': paginator.count,
            'current_page': page_obj.number
        }

    # 获取请求参数
    contacts_page = request.GET.get('contacts_page', 1)
    communities_page = request.GET.get('communities_page', 1)
    page_size = request.GET.get('page_size', 10)
    search_query = request.GET.get('search_query')
    sort_field = request.GET.get('sort_field', 'name')
    sort_order = request.GET.get('sort_order', 'asc')

    # 获取各功能模块数据
    community_data = get_community_data()
    unread_notifications_count = get_unread_notifications_count()
    contacts_data = get_contacts_data(search_query, contacts_page, page_size,
                                      sort_field, sort_order)
    community_list_data = get_community_list(communities_page, page_size)

    # 准备上下文数据
    context = {
        # 社区人口与家庭数据
        'community_data': community_data,

        # 用户未读通知数量
        'unread_notifications_count': unread_notifications_count,

        # 通讯录管理
        'contacts': contacts_data['contacts'],
        'contacts_page_obj': contacts_data['page_obj'],
        'total_contacts': contacts_data['total_contacts'],
        'contacts_total_pages': contacts_data['total_pages'],
        'current_contacts_page': contacts_data['current_page'],

        # 社区列表
        'communities': community_list_data['communities'],
        'communities_page_obj': community_list_data['page_obj'],
        'total_communities': community_list_data['total_communities'],
        'communities_total_pages': community_list_data['total_pages'],
        'current_communities_page': community_list_data['current_page'],

        # 搜索和排序参数，用于模板中保持状态
        'search_query': search_query,
        'sort_field': sort_field,
        'sort_order': sort_order,
    }

    return render(request, 'dashboard.html', context)


@login_required
def residents_view(request):
    """居民数据列表视图
    
    展示居民数据，支持分页、多条件筛选和搜索功能。
    筛选条件包括：
    - 政治面貌
    - 年龄段（基于身份证号自动计算）
    - 民族
    - 学历
    
    搜索功能支持：
    - 姓名
    - 身份证号
    - 手机号
    
    Args:
        request: HTTP请求对象，包含分页、筛选和搜索参数
        
    Returns:
        HttpResponse: 渲染居民列表页面，包含分页、筛选和搜索功能
    """
    from django.core.paginator import Paginator
    from django.db.models import Q
    from django.db.models.functions import Substr
    from datetime import datetime

    # 获取前端传来的分页参数
    page_number = request.GET.get('page', 1)  # 当前页码，默认为1
    page_size = request.GET.get('page_size', 10)  # 每页记录数，默认为10
    # 转换为字符串，确保模板中的比较正常工作
    page_size = str(page_size)

    # 获取前端传来的筛选参数
    political_status = request.GET.get('political_status')  # 政治面貌
    age_group = request.GET.get('age_group')  # 年龄段
    nationality = request.GET.get('nationality')  # 民族
    education = request.GET.get('education')  # 学历
    search_query = request.GET.get('search_query')  # 搜索关键词
    family_id = request.GET.get('family_id')  # 家庭ID
    household_number = request.GET.get('household_number')  # 户号

    # 查询所有未删除的居民数据，并按ID排序，确保分页结果一致
    residents_list = Resident.objects.filter(is_deleted=False).order_by('id')

    # 政治面貌筛选
    if political_status:
        try:
            political_status = int(political_status)
            residents_list = residents_list.filter(
                political_status=political_status)
        except ValueError:
            # 如果参数格式不正确，忽略该筛选条件
            pass

    # 年龄段筛选（基于身份证号的出生年份计算）
    if age_group:
        today = datetime.today()
        current_year = today.year

        # 根据不同的年龄段，计算对应的出生年份范围
        if age_group == '0-14':
            # 14岁以下，出生年份 >= 当前年份 - 14
            min_birth_year = current_year - 14
            # 使用Substr函数截取身份证号的第7-10位作为出生年份
            residents_list = residents_list.annotate(
                birth_year=Substr('id_card', 7, 4)).filter(
                    birth_year__gte=str(min_birth_year))
        elif age_group == '15-18':
            # 15-18岁，出生年份在 [当前年份 - 18, 当前年份 - 15]
            min_birth_year = current_year - 18
            max_birth_year = current_year - 15
            residents_list = residents_list.annotate(
                birth_year=Substr('id_card', 7, 4)).filter(
                    birth_year__lte=str(max_birth_year),
                    birth_year__gte=str(min_birth_year))
        elif age_group == '15-64':
            # 15-64岁，出生年份在 [当前年份 - 64, 当前年份 - 15]
            min_birth_year = current_year - 64
            max_birth_year = current_year - 15
            residents_list = residents_list.annotate(
                birth_year=Substr('id_card', 7, 4)).filter(
                    birth_year__lte=str(max_birth_year),
                    birth_year__gte=str(min_birth_year))
        elif age_group == '65+':
            # 65岁以上，出生年份 <= 当前年份 - 65
            max_birth_year = current_year - 65
            residents_list = residents_list.annotate(
                birth_year=Substr('id_card', 7, 4)).filter(
                    birth_year__lte=str(max_birth_year))
        elif age_group == '80+':
            # 80岁以上，出生年份 <= 当前年份 - 80
            max_birth_year = current_year - 80
            residents_list = residents_list.annotate(
                birth_year=Substr('id_card', 7, 4)).filter(
                    birth_year__lte=str(max_birth_year))

    # 民族筛选
    if nationality:
        if nationality == 'other':
            # 其他少数民族，排除汉族、满族、蒙古族、回族
            residents_list = residents_list.exclude(
                nationality__in=[1, 2, 3, 4])
        else:
            try:
                nationality = int(nationality)
                residents_list = residents_list.filter(nationality=nationality)
            except ValueError:
                # 如果参数格式不正确，忽略该筛选条件
                pass

    # 学历筛选
    if education:
        try:
            education = int(education)
            residents_list = residents_list.filter(education=education)
        except ValueError:
            # 如果参数格式不正确，忽略该筛选条件
            pass

    # 搜索功能：支持姓名、身份证号、手机号搜索
    if search_query:
        residents_list = residents_list.filter(
            Q(name__icontains=search_query)  # 按姓名搜索
            | Q(id_card__icontains=search_query)  # 按身份证号搜索
            | Q(phone__icontains=search_query))  # 按手机号搜索

    # 家庭ID筛选
    if family_id:
        residents_list = residents_list.filter(family_id=family_id)

    # 户号筛选（通过家庭关联查询）
    if household_number:
        residents_list = residents_list.filter(
            family__household_number__icontains=household_number)

    # 创建分页器实例
    paginator = Paginator(residents_list, page_size)

    # 获取指定页码的数据
    page_obj = paginator.get_page(page_number)

    # 准备筛选选项，用于模板中的下拉选择框
    political_status_choices = Resident.POLITICAL_STATUS_CHOICES  # 政治面貌选项
    nationality_choices = [  # 民族选项，包含常用民族和其他少数民族
        (1, "汉族"), (2, "满族"), (3, "蒙古族"), (4, "回族"), ('other', "其他少数民族")
    ]
    age_group_choices = [  # 年龄段选项
        ('0-14', "0-14岁"), ('15-18', "15-18岁"), ('15-64', "15-64岁"),
        ('65+', "65岁以上"), ('80+', "80岁以上")
    ]
    education_choices = Resident.EDUCATION_CHOICES  # 学历选项

    # 获取用户权限信息
    from .utils import check_user_permissions
    user_permissions = check_user_permissions(request.user)

    # 准备上下文数据，传递给模板
    context = {
        'page_obj': page_obj,  # 分页对象
        'residents': page_obj.object_list,  # 当前页的居民数据列表
        'user': request.user,  # 当前登录用户
        'is_authenticated': request.user.is_authenticated,  # 用户认证状态
        'page_number': page_obj.number,  # 当前页码
        'total_pages': paginator.num_pages,  # 总页数
        'total_residents': paginator.count,  # 总居民数
        'page_size': page_size,  # 每页记录数

        # 筛选参数，用于保持当前筛选状态
        'political_status': political_status,
        'age_group': age_group,
        'nationality': nationality,
        'education': education,
        'search_query': search_query,

        # 筛选选项，用于模板中的下拉选择框
        'political_status_choices': political_status_choices,
        'nationality_choices': nationality_choices,
        'age_group_choices': age_group_choices,
        'education_choices': education_choices,
        'permissions': user_permissions  # 用户权限信息
    }

    # 渲染居民列表页面
    return render(request, 'residents.html', context)


@login_required
def families_view(request):
    """家庭数据列表视图
    
    展示家庭数据，支持分页、多条件筛选和搜索功能。
    筛选条件包括：
    - 社区
    - 小区
    - 胡同
    
    搜索功能支持：
    - 户号
    - 房主姓名
    - 联系电话
    
    Args:
        request: HTTP请求对象，包含分页、筛选和搜索参数
        
    Returns:
        HttpResponse: 渲染家庭列表页面，包含分页、筛选和搜索功能
    """
    from django.core.paginator import Paginator
    from django.db.models import Q

    # 获取前端传来的分页参数
    page_number = request.GET.get('page', 1)  # 当前页码，默认为1
    page_size = request.GET.get('page_size', 10)  # 每页记录数，默认为10
    # 转换为字符串，确保模板中的比较正常工作
    page_size = str(page_size)

    # 获取前端传来的筛选参数
    community_id = request.GET.get('community')  # 社区ID
    estate_id = request.GET.get('estate')  # 小区ID
    hutong_id = request.GET.get('hutong')  # 胡同ID
    search_query = request.GET.get('search_query')  # 搜索关键词

    # 获取所有未删除的社区数据，用于模板中的社区选择下拉框
    communities = Community.objects.filter(is_deleted=False).order_by('name')

    # 根据选择的社区，获取对应的小区数据
    if community_id:
        # 只获取指定社区下的小区
        estates = HousingEstate.objects.filter(
            community_id=community_id, is_deleted=False).order_by('name')
        # 根据选择的社区，获取对应的胡同数据
        hutongs = Hutong.objects.filter(community_id=community_id,
                                        is_deleted=False).order_by('name')
    else:
        # 获取所有未删除的小区
        estates = HousingEstate.objects.filter(
            is_deleted=False).order_by('name')
        # 获取所有未删除的胡同
        hutongs = Hutong.objects.filter(is_deleted=False).order_by('name')

    # 构建查询条件，用于筛选家庭数据
    query = Q()

    # 添加未删除条件，只显示未删除的家庭
    query &= Q(is_deleted=False)

    # 根据社区筛选家庭
    if community_id:
        # 同时筛选属于该社区的小区和胡同的家庭
        # 家庭可以关联楼房地址（通过小区）或平房地址（通过胡同）
        query &= Q(
            Q(residential_address__estate__community_id=community_id) | \
            Q(residential_address__hutong__community_id=community_id)
        )

    # 根据小区筛选家庭
    if estate_id:
        query &= Q(residential_address__estate_id=estate_id)

    # 根据胡同筛选家庭
    if hutong_id:
        query &= Q(residential_address__hutong_id=hutong_id)

    # 根据搜索关键词筛选家庭
    if search_query:
        query &= Q(household_number__icontains=search_query) | \
                Q(owner_name__icontains=search_query) | \
                Q(contact_phone__icontains=search_query)

    # 获取过滤后的家庭数据，并按ID排序，确保分页结果一致
    families_list = Family.objects.filter(query).order_by('id')

    # 创建分页器实例
    paginator = Paginator(families_list, page_size)

    # 获取指定页码的数据
    page_obj = paginator.get_page(page_number)

    # 获取用户权限信息
    from .utils import check_user_permissions
    user_permissions = check_user_permissions(request.user)

    # 准备上下文数据，传递给模板
    context = {
        'page_obj': page_obj,  # 分页对象
        'families': page_obj.object_list,  # 当前页的家庭数据列表
        'user': request.user,  # 当前登录用户
        'is_authenticated': request.user.is_authenticated,  # 用户认证状态
        'page_number': page_obj.number,  # 当前页码
        'total_pages': paginator.num_pages,  # 总页数
        'total_families': paginator.count,  # 总家庭数
        'page_size': page_size,  # 每页记录数
        'communities': communities,  # 所有社区列表
        'estates': estates,  # 过滤后的小区列表
        'hutongs': hutongs,  # 过滤后的胡同列表
        'selected_community': community_id,  # 当前选中的社区ID
        'selected_estate': estate_id,  # 当前选中的小区ID
        'selected_hutong': hutong_id,  # 当前选中的胡同ID
        'search_query': search_query,  # 当前搜索关键词
        'permissions': user_permissions  # 用户权限信息
    }

    # 渲染家庭列表页面
    return render(request, 'families.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def notification_read_status(request, notification_id):
    """通知阅读状态API端点
    
    用于检查或更新通知的阅读状态。
    支持两种HTTP方法：
    - GET: 检查通知是否已读
    - POST: 更新通知阅读状态（标记为已读）
    
    Args:
        request: HTTP请求对象
        notification_id: 通知ID，用于标识要操作的通知
        
    Returns:
        JsonResponse: 包含操作结果和状态信息的JSON响应
    """
    from django.http import JsonResponse

    try:
        # 获取指定ID的通知对象
        notification = Notification.objects.get(id=notification_id)

        if request.method == 'GET':
            # 检查通知是否已读
            is_read = NotificationRead.objects.filter(
                user=request.user, notification=notification).exists()
            return JsonResponse({
                'success': True,
                'is_read': is_read,
                'notification_id': notification_id
            })
        elif request.method == 'POST':
            # 更新通知已读状态
            action = request.POST.get('action', 'read')

            if action == 'read':
                # 标记为已读：获取或创建阅读记录
                notification_read, created = NotificationRead.objects.get_or_create(
                    user=request.user, notification=notification)
                # 如果是新创建的记录，更新阅读时间和通知的阅读次数
                if created:
                    notification_read.read_time = timezone.now()
                    notification_read.save()
                    # 更新通知的阅读次数
                    notification.view_count = notification.view_count + 1
                    notification.save()
                return JsonResponse({
                    'success': True,
                    'message': '通知已标记为已读',
                    'is_read': True,
                    'notification_id': notification_id
                })
            elif action == 'unread':
                # 标记为未读
                NotificationRead.objects.filter(
                    user=request.user, notification=notification).delete()
                return JsonResponse({
                    'success': True,
                    'message': '通知已标记为未读',
                    'is_read': False,
                    'notification_id': notification_id
                })
            else:
                return JsonResponse(
                    {
                        'success': False,
                        'message': '无效的操作类型',
                        'notification_id': notification_id
                    },
                    status=400)
    except Notification.DoesNotExist:
        return JsonResponse(
            {
                'success': False,
                'message': '通知不存在',
                'notification_id': notification_id
            },
            status=404)
    except Exception as e:
        return JsonResponse(
            {
                'success': False,
                'message': f'处理请求时发生错误: {str(e)}',
                'notification_id': notification_id
            },
            status=500)


def notifications_view(request):
    """通知视图，用于显示带分页、过滤和搜索功能的通知数据"""
    from django.core.paginator import Paginator
    from django.db.models import Q

    # 获取前端传来的分页参数，默认为第1页，每页10条
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    # 转换为字符串，确保模板中的比较正常工作
    page_size = str(page_size)

    # 获取筛选参数
    search_query = request.GET.get('search_query')
    notification_type = request.GET.get('notification_type')
    is_expired = request.GET.get('is_expired')

    # 构建查询条件
    query = Q()

    # 添加未删除条件
    query &= Q(is_deleted=False)

    # 根据搜索关键词筛选
    if search_query:
        query &= Q(
            Q(title__icontains=search_query)
            | Q(content__icontains=search_query)
            | Q(publisher__username__icontains=search_query))

    # 根据通知类型筛选
    if notification_type:
        query &= Q(notification_type=notification_type)

    # 根据是否过期筛选
    if is_expired:
        from django.utils import timezone
        now = timezone.now()
        if is_expired == '1':
            query &= Q(valid_until__lt=now)
        elif is_expired == '0':
            query &= Q(valid_until__gte=now)

    # 获取过滤后的通知数据
    notifications_list = list(Notification.objects.filter(query))

    # 准备上下文数据
    # 获取当前用户的已读通知ID列表
    user_read_notifications = set()
    if request.user.is_authenticated:
        from api.models import NotificationRead
        user_read_notifications = set(
            NotificationRead.objects.filter(user=request.user).values_list(
                'notification_id', flat=True))

    # 自定义排序：先按未读/已读分组，再按发布时间倒序
    def custom_sort(notification):
        # 第一优先级：未读状态（未读排在前面）
        # 第二优先级：发布时间（最新的排在前面）
        is_read = notification.id in user_read_notifications
        return (is_read, -notification.publish_time.timestamp())

    # 应用自定义排序
    notifications_list.sort(key=custom_sort)

    # 创建分页器实例
    paginator = Paginator(notifications_list, page_size)

    # 获取指定页码的数据
    page_obj = paginator.get_page(page_number)

    from .utils import check_user_permissions

    # 计算用户权限
    user_permissions = check_user_permissions(request.user)

    context = {
        'page_obj': page_obj,
        'notifications': page_obj.object_list,
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'page_number': page_obj.number,
        'total_pages': paginator.num_pages,
        'total_notifications': paginator.count,
        'page_size': page_size,
        'search_query': search_query,
        'selected_notification_type': notification_type,
        'selected_is_expired': is_expired,
        'user_read_notifications': user_read_notifications,
        # 用户权限
        'permissions': user_permissions
    }

    return render(request, 'notifications.html', context)


@login_required
def analytics_view(request):
    """统计分析视图，用于显示统计数据"""
    import requests
    import json
    from pypinyin import lazy_pinyin
    from django.core.cache import cache
    from django.core.paginator import Paginator
    from django.db.models import Q, Count, Sum, Case, When, IntegerField, F
    from django.utils import timezone
    from datetime import timedelta, datetime

    # 获取用户的department属性
    user_profile = request.user.userprofile
    department = user_profile.get_department_display()

    # 初始化查询集
    resident_queryset = Resident.objects.all()
    community_queryset = Community.objects.all()

    # 根据用户权限过滤数据
    if department == '社区':
        try:
            # 查找用户关联的社区工作者
            social_worker = SocialWorker.objects.get(user_profile=user_profile)
            community = social_worker.community
            # 过滤社区内的居民数据
            resident_queryset = resident_queryset.filter(
                family__residential_address__estate__community=community)
            # 只显示该社区的数据
            community_queryset = Community.objects.filter(id=community.id)
        except SocialWorker.DoesNotExist:
            pass

    # 1. 民族构成比例
    nationality_counts = resident_queryset.values('nationality').annotate(
        count=Count('id')).order_by('-count')
    nationality_data = []
    other_minorities_count = 0

    # 定义需要单独显示的民族
    major_nationalities = [1, 2, 3, 11]  # 汉族、蒙古族、回族、满族

    for item in nationality_counts:
        if item['nationality']:
            if item['nationality'] in major_nationalities:
                nationality_name = dict(Resident.NATIONALITY_CHOICES).get(
                    item['nationality'], '未知')
                nationality_data.append({
                    'name': nationality_name,
                    'value': item['count']
                })
            else:
                # 将其他民族合并为"其他少数民族"
                other_minorities_count += item['count']

    # 添加"其他少数民族"到数据中
    if other_minorities_count > 0:
        nationality_data.append({
            'name': '其他少数民族',
            'value': other_minorities_count
        })

    # 2. 性别分布比例
    gender_counts = resident_queryset.values('gender').annotate(
        count=Count('id')).order_by('-count')
    gender_data = []
    for item in gender_counts:
        if item['gender']:
            gender_name = dict(Resident.GENDER_CHOICES).get(
                item['gender'], '未知')
            gender_data.append({'name': gender_name, 'value': item['count']})

    # 3. 政治面貌分布比例
    political_counts = resident_queryset.values('political_status').annotate(
        count=Count('id')).order_by('-count')
    political_data = []
    other_parties_count = 0

    # 定义需要单独显示的政治面貌
    major_political_status = [1, 2, 3, 12,
                              13]  # 中国共产党党员、中国共产党预备党员、中国共产主义青年团团员、无党派民主人士、群众
    # 定义需要合并为"其他民主党派"的政治面貌
    other_parties = [
        4, 5, 6, 7, 8, 9, 10, 11
    ]  # 中国国民党革命委员会党员、中国民主同盟盟员、中国民主建国会会员、中国民主促进会会员、中国农工民主党党员、中国致公党党员、九三学社社员、台湾民主自治同盟盟员

    for item in political_counts:
        if item['political_status']:
            if item['political_status'] in major_political_status:
                political_name = dict(Resident.POLITICAL_STATUS_CHOICES).get(
                    item['political_status'], '未知')
                political_data.append({
                    'name': political_name,
                    'value': item['count']
                })
            elif item['political_status'] in other_parties:
                # 将其他民主党派合并
                other_parties_count += item['count']

    # 添加"其他民主党派"到数据中
    if other_parties_count > 0:
        political_data.append({'name': '其他民主党派', 'value': other_parties_count})

    # 4. 学历层次分布比例
    education_counts = resident_queryset.values('education').annotate(
        count=Count('id')).order_by('-count')
    education_data = []
    for item in education_counts:
        if item['education']:
            education_name = dict(Resident.EDUCATION_CHOICES).get(
                item['education'], '未知')
            education_data.append({
                'name': education_name,
                'value': item['count']
            })

    # 5. 婚姻状况分布比例
    marital_counts = resident_queryset.values('marital_status').annotate(
        count=Count('id')).order_by('-count')
    marital_data = []
    for item in marital_counts:
        if item['marital_status']:
            marital_name = dict(Resident.MARITAL_STATUS_CHOICES).get(
                item['marital_status'], '未知')
            marital_data.append({'name': marital_name, 'value': item['count']})

    # 6. 年龄结构分布比例
    today = datetime.today()
    current_year = today.year

    # 定义年龄段
    age_groups = [{
        'name': '0-14岁',
        'min': 0,
        'max': 14
    }, {
        'name': '15-65岁',
        'min': 15,
        'max': 65
    }, {
        'name': '65-79岁',
        'min': 66,
        'max': 79
    }, {
        'name': '80+',
        'min': 80,
        'max': 150
    }]

    # 计算年龄分布
    age_data = []
    for group in age_groups:
        # 使用身份证号计算年龄
        min_birth_year = current_year - group['max']
        max_birth_year = current_year - group['min']

        # 使用身份证号计算年龄，根据出生年份范围过滤
        # 身份证号格式：前6位是地址码，接下来8位是出生日期（YYYYMMDD）
        # 使用SQL函数提取出生年份进行比较
        from django.db.models.functions import Substr
        count = resident_queryset.annotate(
            birth_year=Substr('id_card', 7, 4)).filter(
                birth_year__gte=str(min_birth_year)[:4],
                birth_year__lte=str(max_birth_year)[:4]).count()

        age_data.append({'name': group['name'], 'value': count})

    # 准备统计数据
    statistics_data = {
        'nationality': nationality_data,
        'gender': gender_data,
        'political': political_data,
        'education': education_data,
        'marital': marital_data,
        'age': age_data
    }

    # 获取社区统计数据
    communities = community_queryset
    community_statistics = []

    for community in communities:
        # 获取社区内的居民数据
        residents = Resident.objects.filter(
            family__residential_address__estate__community=community)

        # 获取社区内的家庭数据
        families = Family.objects.filter(
            residential_address__estate__community=community)

        # 获取社区内的居住地址数据
        addresses = ResidentialAddress.objects.filter(
            Q(estate__community=community)
            | Q(hutong__community=community))

        # 计算各项统计指标
        total_population = residents.count()
        total_families = families.count()

        # 男女比例计算（以比的形式，分子固定为1）
        male_count = residents.filter(gender=1).count()
        female_count = residents.filter(gender=2).count()
        gender_ratio = 0
        if male_count > 0 and female_count > 0:
            # 计算男:女的比例，固定分子为1
            gender_ratio = round(female_count / male_count, 2)
        elif male_count > 0:
            # 只有男性时，比例为1:0
            gender_ratio = 0
        elif female_count > 0:
            # 只有女性时，比例为0:1
            gender_ratio = 9999  # 使用一个特殊值表示只有女性

        # 就业人口比计算（15-64岁人口中就业人口的比例）
        today = datetime.today()
        current_year = today.year
        min_birth_year = current_year - 64
        max_birth_year = current_year - 15

        # 根据出生年份范围过滤15-64岁人口
        from django.db.models.functions import Substr
        working_age_residents = residents.annotate(
            birth_year=Substr('id_card', 7, 4)).filter(
                birth_year__gte=str(min_birth_year)[:4],
                birth_year__lte=str(max_birth_year)[:4])

        working_age_count = working_age_residents.count()
        employed_count = working_age_residents.filter(job=True).count()
        employment_ratio = 0
        if working_age_count > 0:
            employment_ratio = round(
                (employed_count / working_age_count) * 100, 2)

        # 空房比计算
        total_addresses = addresses.count()
        empty_houses = addresses.filter(is_resident=3).count()
        empty_house_ratio = 0
        if total_addresses > 0:
            empty_house_ratio = round((empty_houses / total_addresses) * 100,
                                      2)

        # 租户比计算
        rented_houses = addresses.filter(is_resident=2).count()
        rented_ratio = 0
        if total_addresses > 0:
            rented_ratio = round((rented_houses / total_addresses) * 100, 2)

        # 未婚人口比计算
        # 22岁以上男性未婚人数
        male_min_birth_year = current_year - 22
        male_unmarried = residents.filter(gender=1, marital_status=1).annotate(
            birth_year=Substr('id_card', 7, 4)).filter(
                birth_year__lte=str(male_min_birth_year)[:4]).count()

        # 20岁以上女性未婚人数
        female_min_birth_year = current_year - 20
        female_unmarried = residents.filter(
            gender=2, marital_status=1).annotate(
                birth_year=Substr('id_card', 7, 4)).filter(
                    birth_year__lte=str(female_min_birth_year)[:4]).count()

        # 22岁以上男性总人数
        male_total = residents.filter(gender=1).annotate(
            birth_year=Substr('id_card', 7, 4)).filter(
                birth_year__lte=str(male_min_birth_year)[:4]).count()

        # 20岁以上女性总人数
        female_total = residents.filter(gender=2).annotate(
            birth_year=Substr('id_card', 7, 4)).filter(
                birth_year__lte=str(female_min_birth_year)[:4]).count()

        # 计算未婚人口比
        unmarried_ratio = 0
        total_eligible = male_total + female_total
        if total_eligible > 0:
            unmarried_ratio = round(
                ((male_unmarried + female_unmarried) / total_eligible) * 100,
                2)

        # 添加社区统计数据，包括分子值用于前端显示
        community_statistics.append({
            'community_name': community.name,
            'total_population': total_population,
            'total_families': total_families,
            'gender_ratio': gender_ratio,
            'gender_male_count': male_count,
            'gender_female_count': female_count,
            'employment_ratio': employment_ratio,
            'employed_count': employed_count,
            'working_age_count': working_age_count,
            'empty_house_ratio': empty_house_ratio,
            'empty_houses': empty_houses,
            'total_addresses': total_addresses,
            'rented_ratio': rented_ratio,
            'rented_houses': rented_houses,
            'unmarried_ratio': unmarried_ratio,
            'unmarried_count': male_unmarried + female_unmarried,
            'eligible_count': male_total + female_total,
            'is_total': False  # 添加标识，区分普通行和总行
        })

    # 计算总数据
    if community_statistics:
        # 根据用户权限获取总人口数，与dashboard保持一致
        if department == '社区办':
            # 显示所有社区的总人口数
            total_total_population = Resident.objects.count()
        elif department == '社区':
            try:
                # 查找用户关联的社区工作者
                social_worker = SocialWorker.objects.get(
                    user_profile=user_profile)
                community = social_worker.community
                # 查询该社区的总人口数
                total_total_population = Resident.objects.filter(
                    family__residential_address__estate__community=community
                ).count()
            except SocialWorker.DoesNotExist:
                total_total_population = 0
        else:
            total_total_population = 0

        total_total_families = sum(item['total_families']
                                   for item in community_statistics)
        total_gender_male_count = sum(item['gender_male_count']
                                      for item in community_statistics)
        total_gender_female_count = sum(item['gender_female_count']
                                        for item in community_statistics)
        total_employed_count = sum(item['employed_count']
                                   for item in community_statistics)
        total_working_age_count = sum(item['working_age_count']
                                      for item in community_statistics)
        total_empty_houses = sum(item['empty_houses']
                                 for item in community_statistics)
        total_total_addresses = sum(item['total_addresses']
                                    for item in community_statistics)
        total_rented_houses = sum(item['rented_houses']
                                  for item in community_statistics)
        total_unmarried_count = sum(item['unmarried_count']
                                    for item in community_statistics)
        total_eligible_count = sum(item['eligible_count']
                                   for item in community_statistics)

        # 计算总比例
        total_gender_ratio = 0
        if total_gender_male_count > 0 and total_gender_female_count > 0:
            total_gender_ratio = round(
                total_gender_female_count / total_gender_male_count, 2)
        elif total_gender_male_count > 0:
            total_gender_ratio = 0
        elif total_gender_female_count > 0:
            total_gender_ratio = 9999

        total_employment_ratio = 0
        if total_working_age_count > 0:
            total_employment_ratio = round(
                (total_employed_count / total_working_age_count) * 100, 2)

        total_empty_house_ratio = 0
        if total_total_addresses > 0:
            total_empty_house_ratio = round(
                (total_empty_houses / total_total_addresses) * 100, 2)

        total_rented_ratio = 0
        if total_total_addresses > 0:
            total_rented_ratio = round(
                (total_rented_houses / total_total_addresses) * 100, 2)

        total_unmarried_ratio = 0
        if total_eligible_count > 0:
            total_unmarried_ratio = round(
                (total_unmarried_count / total_eligible_count) * 100, 2)

        # 添加总数据行
        community_statistics.insert(
            0,
            {
                'community_name': '总计',
                'total_population': total_total_population,
                'total_families': total_total_families,
                'gender_ratio': total_gender_ratio,
                'gender_male_count': total_gender_male_count,
                'gender_female_count': total_gender_female_count,
                'employment_ratio': total_employment_ratio,
                'employed_count': total_employed_count,
                'working_age_count': total_working_age_count,
                'empty_house_ratio': total_empty_house_ratio,
                'empty_houses': total_empty_houses,
                'total_addresses': total_total_addresses,
                'rented_ratio': total_rented_ratio,
                'rented_houses': total_rented_houses,
                'unmarried_ratio': total_unmarried_ratio,
                'unmarried_count': total_unmarried_count,
                'eligible_count': total_eligible_count,
                'is_total': True  # 添加标识，区分普通行和总行
            })

    # 准备上下文数据
    context = {
        # 用户信息
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'user_profile': request.user.userprofile,

        # 统计数据（用于饼图展示）
        'statistics_data': statistics_data,

        # 社区统计数据列表
        'community_statistics': community_statistics,
    }

    return render(request, 'analytics.html', context)


@login_required
def addresses_view(request):
    """地址视图，用于显示带分页、过滤和搜索功能的地址数据"""
    from django.core.paginator import Paginator
    from django.db.models import Q

    # 获取前端传来的分页参数，默认为第1页，每页10条
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    # 转换为字符串，确保模板中的比较正常工作
    page_size = str(page_size)

    # 获取筛选参数
    community_id = request.GET.get('community')
    estate_id = request.GET.get('estate')
    hutong_id = request.GET.get('hutong')
    address_type = request.GET.get('address_type')
    is_resident = request.GET.get('is_resident')
    search_query = request.GET.get('search_query')
    address_id = request.GET.get('address_id')

    # 获取所有未删除的社区数据
    communities = Community.objects.filter(is_deleted=False).order_by('name')

    # 根据选择的社区，获取对应的小区数据
    if community_id:
        estates = HousingEstate.objects.filter(
            community_id=community_id, is_deleted=False).order_by('name')
        # 根据选择的社区，获取对应的胡同数据
        hutongs = Hutong.objects.filter(community_id=community_id,
                                        is_deleted=False).order_by('name')
    else:
        estates = HousingEstate.objects.filter(
            is_deleted=False).order_by('name')
        hutongs = Hutong.objects.filter(is_deleted=False).order_by('name')

    # 构建查询条件
    query = Q()

    # 添加未删除条件
    query &= Q(is_deleted=False)

    # 根据地址ID筛选
    if address_id:
        query &= Q(id=address_id)
    else:
        # 根据社区筛选
        if community_id:
            # 同时筛选属于该社区的小区和胡同的地址
            query &= Q(
                Q(estate__community_id=community_id)
                | Q(hutong__community_id=community_id))

        # 根据小区筛选
        if estate_id:
            query &= Q(estate_id=estate_id)

        # 根据胡同筛选
        if hutong_id:
            query &= Q(hutong_id=hutong_id)

        # 根据地址类型筛选
        if address_type:
            query &= Q(address_type=address_type)

        # 根据居住状态筛选
        if is_resident:
            query &= Q(is_resident=is_resident)

        # 根据搜索关键词筛选
        if search_query:
            # 搜索地址相关字段
            query &= Q(
                Q(estate__name__icontains=search_query)
                | Q(building__name__icontains=search_query)
                | Q(unit__name__icontains=search_query)
                | Q(apartment__house_number__icontains=search_query)
                | Q(hutong__name__icontains=search_query)
                | Q(single_house__house_number__icontains=search_query))

    # 获取过滤后的地址数据，按ID排序
    addresses_list = ResidentialAddress.objects.filter(query).order_by('id')

    # 创建分页器实例
    paginator = Paginator(addresses_list, page_size)

    # 获取指定页码的数据
    page_obj = paginator.get_page(page_number)

    # 准备上下文数据
    context = {
        'page_obj': page_obj,
        'addresses': page_obj.object_list,
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'page_number': page_obj.number,
        'total_pages': paginator.num_pages,
        'total_addresses': paginator.count,
        'page_size': page_size,
        'communities': communities,
        'estates': estates,
        'hutongs': hutongs,
        'selected_community': community_id,
        'selected_estate': estate_id,
        'selected_hutong': hutong_id,
        'selected_address_type': address_type,
        'selected_is_resident': is_resident,
        'search_query': search_query
    }

    return render(request, 'addresses.html', context)

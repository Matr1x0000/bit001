from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import (Community, SocialWorker, HousingEstate, Building, Unit,
                     Apartment, Hutong, SingleHouse, ResidentialAddress,
                     UserProfile, Resident, Family, Notification,
                     NotificationRead)
from .serializers import (CommunitySerializer, SocialWorkerSerializer,
                          HousingEstateSerializer, BuildingSerializer,
                          UnitSerializer, ApartmentSerializer,
                          HutongSerializer, SingleHouseSerializer,
                          ResidentialAddressSerializer, UserProfileSerializer,
                          ResidentSerializer, FamilySerializer,
                          NotificationSerializer, NotificationReadSerializer)


# 社区视图集：提供社区模型的增删改查接口，仅允许已认证用户访问
class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()  # 获取所有社区数据
    serializer_class = CommunitySerializer  # 指定序列化器
    permission_classes = [permissions.IsAuthenticated]  # 设置权限为仅已认证用户


class SocialWorkerViewSet(viewsets.ModelViewSet):
    queryset = SocialWorker.objects.all()
    serializer_class = SocialWorkerSerializer
    permission_classes = [permissions.IsAuthenticated]


class HousingEstateViewSet(viewsets.ModelViewSet):
    queryset = HousingEstate.objects.all()
    serializer_class = HousingEstateSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 添加过滤支持，允许通过community参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['community']


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticated]


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class HutongViewSet(viewsets.ModelViewSet):
    queryset = Hutong.objects.all()
    serializer_class = HutongSerializer
    permission_classes = [permissions.IsAuthenticated]


class SingleHouseViewSet(viewsets.ModelViewSet):
    queryset = SingleHouse.objects.all()
    serializer_class = SingleHouseSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResidentialAddressViewSet(viewsets.ModelViewSet):
    queryset = ResidentialAddress.objects.all()
    serializer_class = ResidentialAddressSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    permission_classes = [permissions.IsAuthenticated]


class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationReadViewSet(viewsets.ModelViewSet):
    queryset = NotificationRead.objects.all()
    serializer_class = NotificationReadSerializer
    permission_classes = [permissions.IsAuthenticated]


@login_required
def test_view(request):
    """Test view to render the test template with family data"""
    from django.core.paginator import Paginator
    from django.db.models import Q
    
    # 获取前端传来的分页参数，默认为第1页，每页10条
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    
    # 获取筛选参数
    community_id = request.GET.get('community')
    estate_id = request.GET.get('estate')
    search_query = request.GET.get('search_query')
    
    # 获取所有社区数据
    communities = Community.objects.all().order_by('name')
    
    # 根据选择的社区，获取对应的小区数据
    if community_id:
        estates = HousingEstate.objects.filter(community_id=community_id).order_by('name')
    else:
        estates = HousingEstate.objects.all().order_by('name')
    
    # 构建查询条件
    query = Q()
    
    # 根据社区筛选
    if community_id:
        query &= Q(residential_address__estate__community_id=community_id)
    
    # 根据小区筛选
    if estate_id:
        query &= Q(residential_address__estate_id=estate_id)
    
    # 根据搜索关键词筛选
    if search_query:
        query &= Q(household_number__icontains=search_query) | \
                Q(owner_name__icontains=search_query) | \
                Q(contact_phone__icontains=search_query)
    
    # 获取过滤后的家庭数据，按ID排序
    families_list = Family.objects.filter(query).order_by('id')
    
    # 创建分页器实例
    paginator = Paginator(families_list, page_size)
    
    # 获取指定页码的数据
    page_obj = paginator.get_page(page_number)
    
    # 准备上下文数据
    context = {
        'page_obj': page_obj,
        'families': page_obj.object_list,
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'page_number': page_obj.number,
        'total_pages': paginator.num_pages,
        'total_families': paginator.count,
        'page_size': page_size,
        'communities': communities,
        'estates': estates,
        'selected_community': community_id,
        'selected_estate': estate_id,
        'search_query': search_query
    }
    
    return render(request, 'test.html', context)


@login_required
def add_resident(request):
    """View to add a new resident"""
    from django.shortcuts import redirect
    from django.contrib import messages
    from .models import Family

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
        job = request.POST.get('job') == 'on'
        is_dead = request.POST.get('is_dead') == 'on'
        remark = request.POST.get('remark')

        # 验证必填字段
        if not name or not id_card:
            messages.error(request, '姓名和身份证号不能为空')
            return render(request, 'add_resident.html',
                          {'families': Family.objects.all()})

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
            messages.success(request, '居民添加成功')
            return redirect('test')
        except Exception as e:
            messages.error(request, f'添加失败: {str(e)}')
            return render(request, 'add_resident.html',
                          {'families': Family.objects.all()})

    # GET 请求，显示添加居民表单
    return render(request, 'add_resident.html',
                  {'families': Family.objects.all()})


@login_required
def edit_resident(request, resident_id):
    """View to edit an existing resident"""
    from django.shortcuts import redirect, get_object_or_404
    from django.contrib import messages
    from .models import Family

    # 获取要编辑的居民对象
    resident = get_object_or_404(Resident, id=resident_id)

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
        job = request.POST.get('job') == 'on'
        is_dead = request.POST.get('is_dead') == 'on'
        remark = request.POST.get('remark')

        # 验证必填字段
        if not name or not id_card:
            messages.error(request, '姓名和身份证号不能为空')
            return render(request, 'edit_resident.html', {
                'resident': resident,
                'families': Family.objects.all()
            })

        try:
            # 更新居民对象
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
            messages.success(request, '居民信息更新成功')
            return redirect('test')
        except Exception as e:
            messages.error(request, f'更新失败: {str(e)}')
            return render(request, 'edit_resident.html', {
                'resident': resident,
                'families': Family.objects.all()
            })

    # GET 请求，显示编辑居民表单
    return render(request, 'edit_resident.html', {
        'resident': resident,
        'families': Family.objects.all()
    })


@login_required
def delete_resident(request, resident_id):
    """View to delete an existing resident"""
    from django.shortcuts import redirect, get_object_or_404
    from django.contrib import messages

    # 获取要删除的居民对象
    resident = get_object_or_404(Resident, id=resident_id)

    try:
        # 删除居民
        resident.delete()
        messages.success(request, '居民删除成功')
    except Exception as e:
        messages.error(request, f'删除失败: {str(e)}')

    # 重定向回居民列表页面
    return redirect('residents')


@login_required
def index(request):
    """Index view that redirects to dashboard"""
    return redirect('dashboard')


@login_required
def dashboard(request):
    """Dashboard view"""
    return render(request, 'dashboard.html')


@login_required
def residents_view(request):
    """Residents view to display resident data with pagination, filtering and search"""
    from django.core.paginator import Paginator
    from django.db.models import Q
    from datetime import datetime

    # 获取前端传来的分页参数，默认为第1页，每页10条
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)

    # 获取前端传来的筛选参数
    political_status = request.GET.get('political_status')
    age_group = request.GET.get('age_group')
    nationality = request.GET.get('nationality')
    education = request.GET.get('education')
    search_query = request.GET.get('search_query')

    # 查询所有居民数据，并按ID排序，确保分页结果一致
    residents_list = Resident.objects.all().order_by('id')

    # 政治面貌筛选
    if political_status:
        residents_list = residents_list.filter(
            political_status=political_status)

    # 年龄段筛选
    if age_group:
        from django.db.models.functions import Substr
        from django.db.models import IntegerField
        from django.db.models import Value

        today = datetime.today()
        current_year = today.year

        # 根据不同的年龄段，计算对应的出生年份范围
        if age_group == '0-14':
            # 14岁以下，出生年份 >= 当前年份 - 14
            min_birth_year = current_year - 14
            # 使用Substr函数截取身份证号的第7-10位作为出生年份，然后转换为整数进行比较
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
            residents_list = residents_list.filter(nationality=nationality)

    # 学历筛选
    if education:
        residents_list = residents_list.filter(education=education)

    # 搜索功能：支持姓名、身份证号、手机号搜索
    if search_query:
        from django.db.models import Q
        residents_list = residents_list.filter(
            Q(name__icontains=search_query)
            | Q(id_card__icontains=search_query)
            | Q(phone__icontains=search_query))

    # 创建分页器实例
    paginator = Paginator(residents_list, page_size)

    # 获取指定页码的数据
    page_obj = paginator.get_page(page_number)

    # 准备筛选选项
    political_status_choices = Resident.POLITICAL_STATUS_CHOICES
    nationality_choices = [(1, "汉族"), (2, "满族"), (3, "蒙古族"), (4, "回族"),
                           ('other', "其他少数民族")]
    age_group_choices = [('0-14', "0-14岁"), ('15-18', "15-18岁"),
                         ('15-64', "15-64岁"), ('65+', "65岁以上"),
                         ('80+', "80岁以上")]
    education_choices = Resident.EDUCATION_CHOICES

    # 添加登录信息、分页数据和筛选数据到上下文
    context = {
        'page_obj': page_obj,
        'residents': page_obj.object_list,  # 当前页的数据列表
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'page_number': page_obj.number,
        'total_pages': paginator.num_pages,
        'total_residents': paginator.count,
        'page_size': page_size,
        # 筛选参数
        'political_status': political_status,
        'age_group': age_group,
        'nationality': nationality,
        'education': education,
        'search_query': search_query,
        # 筛选选项
        'political_status_choices': political_status_choices,
        'nationality_choices': nationality_choices,
        'age_group_choices': age_group_choices,
        'education_choices': education_choices
    }
    return render(request, 'residents.html', context)


@login_required
def families_view(request):
    """Families view"""
    return render(request, 'families.html')


@login_required
def notifications_view(request):
    """Notifications view"""
    return render(request, 'notifications.html')


@login_required
def analytics_view(request):
    """Analytics view"""
    return render(request, 'analytics.html')


@login_required
def addresses_view(request):
    """Addresses view"""
    return render(request, 'addresses.html')


@login_required
def settings_view(request):
    """Settings view"""
    return render(request, 'settings.html')


@login_required
def test_auth(request):
    """Test view to verify authentication is working"""
    from django.middleware.csrf import get_token
    return JsonResponse({
        'authenticated': request.user.is_authenticated,
        'username': request.user.username,
        'csrf_token': get_token(request)
    })

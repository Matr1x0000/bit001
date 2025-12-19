from rest_framework import viewsets, permissions, filters, status
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
    # 添加过滤支持，允许通过estate参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estate']


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 添加过滤支持，允许通过building参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['building']


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 添加过滤支持，允许通过unit参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['unit']


class HutongViewSet(viewsets.ModelViewSet):
    queryset = Hutong.objects.all()
    serializer_class = HutongSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 添加过滤支持，允许通过community参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['community']


class SingleHouseViewSet(viewsets.ModelViewSet):
    queryset = SingleHouse.objects.all()
    serializer_class = SingleHouseSerializer
    permission_classes = [permissions.IsAuthenticated]
    # 添加过滤支持，允许通过hutong参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['hutong']


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
    # 添加过滤支持，允许通过family参数过滤
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['family']


class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    permission_classes = [permissions.IsAuthenticated]
    # 添加搜索支持，允许通过household_number、owner_name、contact_phone搜索
    filter_backends = [filters.SearchFilter]
    search_fields = ['household_number', 'owner_name', 'contact_phone']


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

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

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NotificationReadViewSet(viewsets.ModelViewSet):
    queryset = NotificationRead.objects.all()
    serializer_class = NotificationReadSerializer
    permission_classes = [permissions.IsAuthenticated]


class NotificationAttachmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NotificationAttachment.objects.all()
    serializer_class = NotificationAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['notification']


@login_required
def test_view(request):
    """Test view to render the test template with comprehensive data"""
    import requests
    import json
    from pypinyin import lazy_pinyin
    from django.core.cache import cache
    from django.core.paginator import Paginator
    from django.db.models import Q, Count, Sum
    from django.utils import timezone
    from datetime import timedelta

    # 1. 社区人口与家庭数据展示功能
    def get_community_data():
        # 尝试从缓存获取数据，缓存过期时间为1小时
        cache_key = f'community_data_{request.user.id}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        community_data = {
            'total_population': '-',
            'total_families': '-',
            'data_source': ''
        }

        # 获取用户的department属性
        user_profile = request.user.userprofile
        department = user_profile.get_department_display()

        if department == '社区办':
            # 显示所有社区的总人口数和总家庭数
            total_population = Resident.objects.count()
            total_families = Family.objects.count()

            community_data = {
                'total_population': total_population,
                'total_families': total_families,
                'data_source': '系统数据库'
            }
        elif department == '社区':
            # 根据用户关联的社区工作者所属社区查询
            try:
                # 查找用户关联的社区工作者
                social_worker = SocialWorker.objects.get(
                    user_profile=user_profile)
                community = social_worker.community

                # 查询该社区的总人口数和总家庭数
                # 假设Resident通过family关联到Family，Family通过residential_address关联到社区
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
                pass

        # 缓存数据，过期时间1小时
        cache.set(cache_key, community_data, 3600)
        return community_data

    # 2. 用户未读通知计数功能
    def get_unread_notifications_count():
        # 尝试从缓存获取数据，缓存过期时间为5分钟
        cache_key = f'unread_notifications_{request.user.id}'
        cached_count = cache.get(cache_key)

        if cached_count is not None:
            return cached_count

        # 获取当前用户的通知总数
        total_notifications = Notification.objects.count()

        # 获取当前用户的已读通知数量
        read_notifications = NotificationRead.objects.filter(
            user=request.user).count()

        # 计算未读通知数量
        unread_count = total_notifications - read_notifications

        # 缓存数据，过期时间5分钟
        cache.set(cache_key, unread_count, 300)
        return unread_count

    # 3. 天气预报集成功能
    def get_weather_data():
        # 尝试从缓存获取数据，缓存过期时间为3小时
        cache_key = 'weather_data'
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        weather_data = {'today': {}, 'forecast': []}

        try:
            # 这里使用和风天气API作为示例，实际使用时需要替换为真实的API
            # API Key需要从和风天气官网注册获取
            api_key = 'YOUR_WEATHER_API_KEY'
            city_code = '101010100'  # 北京的城市代码
            weather_url = f'https://devapi.qweather.com/v7/weather/now?location={city_code}&key={api_key}'
            forecast_url = f'https://devapi.qweather.com/v7/weather/7d?location={city_code}&key={api_key}'

            # 获取今日天气
            now_response = requests.get(weather_url, timeout=5)
            now_data = now_response.json()

            if now_data.get('code') == '200':
                weather_data['today'] = {
                    'temp': now_data['now']['temp'],
                    'text': now_data['now']['text'],
                    'humidity': now_data['now']['humidity'],
                    'windSpeed': now_data['now']['windSpeed'],
                    'windDir': now_data['now']['windDir']
                }

            # 获取未来一周天气预报
            forecast_response = requests.get(forecast_url, timeout=5)
            forecast_data = forecast_response.json()

            if forecast_data.get('code') == '200':
                weather_data['forecast'] = []
                for day in forecast_data['daily'][:7]:
                    weather_data['forecast'].append({
                        'date':
                        day['fxDate'],
                        'maxTemp':
                        day['tempMax'],
                        'minTemp':
                        day['tempMin'],
                        'textDay':
                        day['textDay'],
                        'textNight':
                        day['textNight']
                    })
        except Exception as e:
            # 记录错误日志
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'获取天气数据失败: {str(e)}')

        # 缓存数据，过期时间3小时
        cache.set(cache_key, weather_data, 10800)
        return weather_data

    # 4. 通讯录管理功能
    def get_contacts_data(search_query=None,
                          page=1,
                          page_size=20,
                          sort_field='name',
                          sort_order='asc'):
        # 查询所有未离职的社区工作者和干部
        base_query = Q(is_baned=True)

        if search_query:
            # 同时搜索姓名和联系电话
            search_query = Q(name__icontains=search_query) | Q(
                phone__icontains=search_query)
            social_worker_query = base_query & search_query
            cadre_query = base_query & search_query
        else:
            social_worker_query = base_query
            cadre_query = base_query

        # 查询社区工作者，预取社区信息
        social_workers = SocialWorker.objects.filter(
            social_worker_query).select_related('community').order_by('name')

        # 查询干部
        cadres = Cadre.objects.filter(cadre_query).order_by('name')

        # 合并结果
        all_contacts = list(social_workers) + list(cadres)

        # 定义排序函数，使用拼音排序
        def get_sort_key(contact):
            if sort_field == 'name':
                # 按姓名拼音排序
                return ''.join(lazy_pinyin(contact.name))
            elif sort_field == 'department':
                if isinstance(contact, SocialWorker):
                    # 按部门拼音排序
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
                return ''.join(lazy_pinyin(contact.name))

        # 执行排序
        reverse = True if sort_order == 'desc' else False
        all_contacts.sort(key=get_sort_key, reverse=reverse)

        # 分页
        paginator = Paginator(all_contacts, page_size)
        page_obj = paginator.get_page(page)

        # 格式化数据
        formatted_contacts = []
        for contact in page_obj.object_list:
            if isinstance(contact, SocialWorker):
                department = contact.community.name if contact.community else '未分配社区'
                position = '社工'
            else:  # Cadre
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

    # 5. 社区列表展示功能
    def get_community_list(page=1, page_size=10):
        # 查询所有社区
        communities = Community.objects.all().order_by('name')

        # 分页
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
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    search_query = request.GET.get('search_query')
    sort_field = request.GET.get('sort_field', 'name')
    sort_order = request.GET.get('sort_order', 'asc')

    # 获取各功能数据
    community_data = get_community_data()
    unread_count = get_unread_notifications_count()
    weather_data = get_weather_data()
    contacts_data = get_contacts_data(search_query, page, page_size,
                                      sort_field, sort_order)
    community_list_data = get_community_list(page, page_size)

    # 准备上下文数据
    context = {
        # 用户信息
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'user_profile': request.user.userprofile,

        # 1. 社区人口与家庭数据
        'community_data': community_data,

        # 2. 未读通知计数
        'unread_notifications_count': unread_count,

        # 3. 天气预报数据
        'weather_data': weather_data,

        # 4. 通讯录管理
        'contacts': contacts_data['contacts'],
        'contacts_page_obj': contacts_data['page_obj'],
        'total_contacts': contacts_data['total_contacts'],
        'contacts_total_pages': contacts_data['total_pages'],
        'current_contacts_page': contacts_data['current_page'],

        # 5. 社区列表
        'communities': community_list_data['communities'],
        'communities_page_obj': community_list_data['page_obj'],
        'total_communities': community_list_data['total_communities'],
        'communities_total_pages': community_list_data['total_pages'],
        'current_communities_page': community_list_data['current_page'],

        # 搜索参数
        'search_query': search_query,

        # 排序参数
        'sort_field': sort_field,
        'sort_order': sort_order,
    }

    return render(request, 'test.html', context)


@login_required
def add_resident(request):
    """View to add a new resident"""
    from django.shortcuts import redirect
    from django.contrib import messages
    from .models import Family
    from django.http import JsonResponse

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
        job = request.POST.get('job') == 'true'
        is_dead = request.POST.get('is_dead') == 'true'
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
def edit_resident(request, resident_id):
    """View to edit an existing resident"""
    from django.shortcuts import redirect, get_object_or_404
    from django.contrib import messages
    from .models import Family
    from django.http import JsonResponse

    # 获取要编辑的居民对象
    resident = get_object_or_404(Resident, id=resident_id)

    if request.method == 'PUT':
        # 获取表单数据
        import json
        data = json.loads(request.body)
        name = data.get('name')
        gender = data.get('gender')
        nationality = data.get('nationality')
        id_card = data.get('id_card')
        phone = data.get('phone')
        family_id = data.get('family')
        political_status = data.get('political_status')
        marital_status = data.get('marital_status')
        education = data.get('education')
        job = data.get('job') == 'true'
        is_dead = data.get('is_dead') == 'true'
        remark = data.get('remark')

        # 验证必填字段
        if not name or not id_card:
            return JsonResponse({'success': False, 'message': '姓名和身份证号不能为空'})

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
def add_family(request):
    """View to add a new family"""
    from django.shortcuts import redirect, render
    from django.contrib import messages
    from .models import ResidentialAddress, Community

    if request.method == 'POST':
        # 获取表单数据
        household_number = request.POST.get('household_number')
        owner_name = request.POST.get('owner_name')
        contact_phone = request.POST.get('contact_phone')
        remark = request.POST.get('remark')

        # 地址信息
        address_type = request.POST.get('address_type')
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
                # 楼房
                if estate_id and building_id and unit_id and apartment_id:
                    try:
                        # 尝试获取现有的居住地址
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
                        return render(request, 'add_family.html',
                                      {'communities': Community.objects.all()})
            elif address_type == '2':
                # 平房
                if hutong_id and single_house_id:
                    try:
                        # 尝试获取现有的居住地址
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

        # 验证必填字段
        if not household_number or not owner_name:
            messages.error(request, '户号和房主姓名不能为空')
            return render(request, 'add_family.html',
                          {'communities': Community.objects.all()})

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
            return render(request, 'add_family.html',
                          {'communities': Community.objects.all()})

    # GET 请求，显示添加家庭表单
    return render(request, 'add_family.html',
                  {'communities': Community.objects.all()})


@login_required
def edit_family(request, family_id):
    """View to edit an existing family"""
    from django.shortcuts import redirect, render, get_object_or_404
    from django.contrib import messages
    from .models import ResidentialAddress, Community, Family

    # 获取要编辑的家庭对象
    family = get_object_or_404(Family, id=family_id)

    if request.method == 'POST':
        # 获取表单数据
        household_number = request.POST.get('household_number')
        owner_name = request.POST.get('owner_name')
        contact_phone = request.POST.get('contact_phone')
        remark = request.POST.get('remark')

        # 地址信息
        address_type = request.POST.get('address_type')
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
                # 楼房
                if estate_id and building_id and unit_id and apartment_id:
                    try:
                        # 尝试获取现有的居住地址
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
                # 平房
                if hutong_id and single_house_id:
                    try:
                        # 尝试获取现有的居住地址
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
                                'family': family,
                                'communities': Community.objects.all()
                            })

        # 验证必填字段
        if not household_number or not owner_name:
            messages.error(request, '户号和房主姓名不能为空')
            return render(request, 'edit_family.html', {
                'family': family,
                'communities': Community.objects.all()
            })

        try:
            # 更新家庭对象
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
            return render(request, 'edit_family.html', {
                'family': family,
                'communities': Community.objects.all()
            })

    # GET 请求，显示编辑家庭表单
    return render(request, 'edit_family.html', {
        'family': family,
        'communities': Community.objects.all()
    })


@login_required
def index(request):
    """Index view that redirects to dashboard"""
    return redirect('dashboard')


@login_required
def dashboard(request):
    """Dashboard view"""
    import requests
    import json
    from pypinyin import lazy_pinyin
    from django.core.cache import cache
    from django.core.paginator import Paginator
    from django.db.models import Q, Count, Sum
    from django.utils import timezone
    from datetime import timedelta

    # 社区人口与家庭数据展示功能
    def get_community_data():
        # 每次刷新页面都重新计算数据，不使用缓存
        community_data = {
            'total_population': '-',
            'total_families': '-',
            'data_source': ''
        }

        # 获取用户的department属性
        user_profile = request.user.userprofile
        department = user_profile.get_department_display()

        if department == '社区办':
            # 显示所有社区的总人口数和总家庭数
            total_population = Resident.objects.count()
            total_families = Family.objects.count()

            community_data = {
                'total_population': total_population,
                'total_families': total_families,
                'data_source': '系统数据库'
            }
        elif department == '社区':
            # 根据用户关联的社区工作者所属社区查询
            try:
                # 查找用户关联的社区工作者
                social_worker = SocialWorker.objects.get(
                    user_profile=user_profile)
                community = social_worker.community

                # 查询该社区的总人口数和总家庭数
                # 假设Resident通过family关联到Family，Family通过residential_address关联到社区
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
                pass

        return community_data

    # 通讯录管理功能
    def get_contacts_data(search_query=None,
                          page=1,
                          page_size=20,
                          sort_field='name',
                          sort_order='asc'):
        # 查询所有未离职的社区工作者和干部
        social_worker_query = Q(is_baned=True)
        cadre_query = Q(is_baned=True)

        if search_query:
            social_worker_query &= (Q(name__icontains=search_query)
                                    | Q(phone__icontains=search_query))
            cadre_query &= (Q(name__icontains=search_query)
                            | Q(phone__icontains=search_query))

        # 查询社区工作者，预取社区信息
        social_workers = SocialWorker.objects.filter(
            social_worker_query).select_related('community').order_by('name')

        # 查询干部
        cadres = Cadre.objects.filter(cadre_query).order_by('name')

        # 合并结果
        all_contacts = list(social_workers) + list(cadres)

        # 定义排序函数
        def get_sort_key(contact):
            if sort_field == 'name':
                # 按姓名拼音排序
                return ''.join(lazy_pinyin(contact.name))
            elif sort_field == 'department':
                if isinstance(contact, SocialWorker):
                    # 按部门拼音排序
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
                return ''.join(lazy_pinyin(contact.name))

        # 执行排序
        reverse = True if sort_order == 'desc' else False
        all_contacts.sort(key=get_sort_key, reverse=reverse)

        # 分页
        paginator = Paginator(all_contacts, page_size)
        page_obj = paginator.get_page(page)

        # 格式化数据
        formatted_contacts = []
        for contact in page_obj.object_list:
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
        # 每次刷新页面都重新计算未读通知数量，不使用缓存
        # 获取当前用户的通知总数
        total_notifications = Notification.objects.count()

        # 获取当前用户的已读通知数量
        read_notifications = NotificationRead.objects.filter(
            user=request.user).count()

        # 计算未读通知数量
        unread_count = total_notifications - read_notifications

        return unread_count

    # 社区列表展示功能
    def get_community_list(page=1, page_size=10):
        # 查询所有社区
        communities = Community.objects.all().order_by('name')

        # 分页
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

    # 获取各功能数据
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

        # 搜索参数
        'search_query': search_query,

        # 排序参数
        'sort_field': sort_field,
        'sort_order': sort_order,
    }

    return render(request, 'dashboard.html', context)


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
    family_id = request.GET.get('family_id')
    household_number = request.GET.get('household_number')

    # 查询所有居民数据，并按ID排序，确保分页结果一致
    residents_list = Resident.objects.all().order_by('id')

    # 政治面貌筛选
    if political_status:
        try:
            political_status = int(political_status)
            residents_list = residents_list.filter(political_status=political_status)
        except ValueError:
            pass

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
            try:
                nationality = int(nationality)
                residents_list = residents_list.filter(nationality=nationality)
            except ValueError:
                pass

    # 学历筛选
    if education:
        try:
            education = int(education)
            residents_list = residents_list.filter(education=education)
        except ValueError:
            pass

    # 搜索功能：支持姓名、身份证号、手机号搜索
    if search_query:
        from django.db.models import Q
        residents_list = residents_list.filter(
            Q(name__icontains=search_query)
            | Q(id_card__icontains=search_query)
            | Q(phone__icontains=search_query))

    # 家庭ID筛选
    if family_id:
        residents_list = residents_list.filter(family_id=family_id)

    # 户号筛选
    if household_number:
        residents_list = residents_list.filter(
            family__household_number__icontains=household_number)

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
    """Families view to display family data with pagination, filtering and search"""
    from django.core.paginator import Paginator
    from django.db.models import Q

    # 获取前端传来的分页参数，默认为第1页，每页10条
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)

    # 获取筛选参数
    community_id = request.GET.get('community')
    estate_id = request.GET.get('estate')
    hutong_id = request.GET.get('hutong')
    search_query = request.GET.get('search_query')

    # 获取所有社区数据
    communities = Community.objects.all().order_by('name')

    # 根据选择的社区，获取对应的小区数据
    if community_id:
        estates = HousingEstate.objects.filter(
            community_id=community_id).order_by('name')
        # 根据选择的社区，获取对应的胡同数据
        hutongs = Hutong.objects.filter(
            community_id=community_id).order_by('name')
    else:
        estates = HousingEstate.objects.all().order_by('name')
        hutongs = Hutong.objects.all().order_by('name')

    # 构建查询条件
    query = Q()

    # 根据社区筛选
    if community_id:
        # 同时筛选属于该社区的小区和胡同的家庭
        query &= Q(
            Q(residential_address__estate__community_id=community_id)
            | Q(residential_address__hutong__community_id=community_id))

    # 根据小区筛选
    if estate_id:
        query &= Q(residential_address__estate_id=estate_id)

    # 根据胡同筛选
    if hutong_id:
        query &= Q(residential_address__hutong_id=hutong_id)

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
        'hutongs': hutongs,
        'selected_community': community_id,
        'selected_estate': estate_id,
        'selected_hutong': hutong_id,
        'search_query': search_query
    }

    return render(request, 'families.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def notification_read_status(request, notification_id):
    """API endpoint to check or update notification read status"""
    from django.http import JsonResponse
    from api.models import Notification, NotificationRead

    try:
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
                # 标记为已读
                notification_read, created = NotificationRead.objects.get_or_create(
                    user=request.user, notification=notification)
                # 如果是新创建的记录，更新阅读时间和通知的阅读次数
                if created:
                    from django.utils import timezone
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
    """Notifications view to display notification data with pagination, filtering and search"""
    from django.core.paginator import Paginator
    from django.db.models import Q

    # 获取前端传来的分页参数，默认为第1页，每页10条
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)

    # 获取筛选参数
    search_query = request.GET.get('search_query')
    notification_type = request.GET.get('notification_type')
    is_expired = request.GET.get('is_expired')

    # 构建查询条件
    query = Q()

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
        'user_read_notifications': user_read_notifications
    }

    return render(request, 'notifications.html', context)


@login_required
def analytics_view(request):
    """Analytics view"""
    return render(request, 'analytics.html')


@login_required
def addresses_view(request):
    """Addresses view to display address data with pagination, filtering and search"""
    from django.core.paginator import Paginator
    from django.db.models import Q

    # 获取前端传来的分页参数，默认为第1页，每页10条
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)

    # 获取筛选参数
    community_id = request.GET.get('community')
    estate_id = request.GET.get('estate')
    hutong_id = request.GET.get('hutong')
    address_type = request.GET.get('address_type')
    is_resident = request.GET.get('is_resident')
    search_query = request.GET.get('search_query')

    # 获取所有社区数据
    communities = Community.objects.all().order_by('name')

    # 根据选择的社区，获取对应的小区数据
    if community_id:
        estates = HousingEstate.objects.filter(
            community_id=community_id).order_by('name')
        # 根据选择的社区，获取对应的胡同数据
        hutongs = Hutong.objects.filter(
            community_id=community_id).order_by('name')
    else:
        estates = HousingEstate.objects.all().order_by('name')
        hutongs = Hutong.objects.all().order_by('name')

    # 构建查询条件
    query = Q()

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

import pandas as pd
import os
import sys
import django
from datetime import datetime

# 设置Django环境


def setup_django():
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'community_management.settings')
    django.setup()

# 辅助函数：将字符串转换为datetime对象


def parse_datetime(dt_str):
    if isinstance(dt_str, pd.Timestamp):
        return dt_str.to_pydatetime()
    elif isinstance(dt_str, str):
        try:
            return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                return datetime.strptime(dt_str, '%Y-%m-%d')
    return dt_str

# 主函数


def main():
    # 设置Django环境
    setup_django()

    # 导入所有模型
    from api.models import (
        Community, SocialWorker, HousingEstate, Building, Unit,
        Apartment, Hutong, SingleHouse, ResidentialAddress, UserProfile,
        Resident, Family, Notification, NotificationRead
    )

    # 数据文件路径
    data_dir = 'testdata'

    # 数据上传顺序，按照外键依赖关系排序
    upload_order = [
        {'model': Community, 'file_name': '社区数据.xlsx', 'model_name': '社区'},
        {'model': Hutong, 'file_name': '胡同数据.xlsx', 'model_name': '胡同'},
        {'model': HousingEstate, 'file_name': '小区数据.xlsx', 'model_name': '小区'},
        {'model': Building, 'file_name': '栋楼数据.xlsx', 'model_name': '栋楼'},
        {'model': Unit, 'file_name': '单元数据.xlsx', 'model_name': '单元'},
        {'model': Apartment, 'file_name': '楼房房号数据.xlsx', 'model_name': '楼房房号'},
        {'model': SingleHouse, 'file_name': '平房房号数据.xlsx', 'model_name': '平房房号'},
        {'model': ResidentialAddress, 'file_name': '居住地址数据.xlsx', 'model_name': '居住地址'},
        {'model': Family, 'file_name': '家庭数据.xlsx', 'model_name': '家庭'},
        {'model': SocialWorker, 'file_name': '社区工作者数据.xlsx', 'model_name': '社区工作者'},
        {'model': Notification, 'file_name': '通知数据.xlsx', 'model_name': '通知'},
        {'model': Resident, 'file_name': '居民数据.xlsx', 'model_name': '居民'},
        {'model': NotificationRead, 'file_name': '通知状态数据.xlsx', 'model_name': '通知状态'}
    ]

    print("开始上传数据到数据库...")
    print("=" * 50)

    for item in upload_order:
        model = item['model']
        file_name = item['file_name']
        model_name = item['model_name']

        file_path = os.path.join(data_dir, file_name)

        print(f"\n正在上传 {model_name} 数据...")
        print(f"文件路径: {file_path}")

        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)

            # 清除现有数据，使用更适合SQLite的方式
            print(f"正在清除现有 {model_name} 数据...")
            # 对于SQLite，我们使用一种更简单的方式：直接删除所有记录，不使用WHERE子句
            from django.db import connection
            with connection.cursor() as cursor:
                # 使用SQL直接删除表中的所有记录，不使用WHERE子句
                table_name = model._meta.db_table
                cursor.execute(f"DELETE FROM {table_name};")
                print(f"已清除现有 {model_name} 数据")

            # 准备数据
            records = []
            # 跟踪批次内已使用的唯一字段
            used_unique_fields = {
                'household_number': set(),
                'id_card': set(),
                'housing_estate_name_community': set()
            }

            # 分批次处理和插入数据
            batch_size = 500  # 减小批次大小，避免SQLite参数数量限制
            total_records = 0

            for _, row in df.iterrows():
                # 转换日期时间字段
                for col in row.index:
                    if 'created_at' in col or 'updated_at' in col or 'birth_date' in col or 'publish_time' in col or 'valid_until' in col or 'read_time' in col:
                        row[col] = parse_datetime(row[col])

                # 转换数据类型
                row_dict = row.to_dict()

                # 处理nan值
                for key, value in list(row_dict.items()):
                    if pd.isna(value):
                        # 跳过nan值
                        del row_dict[key]
                        continue
                    # 确保id字段是整数
                    if key == 'id':
                        row_dict[key] = int(value)
                    # 确保其他数值字段是正确类型
                    elif isinstance(value, float):
                        if key.endswith('_id') or key in ['gender', 'building_type', 'total_floors', 'units_per_floor', 'address_type', 'notification_type', 'house_type', 'political_status', 'marital_status', 'education', 'job', 'is_secretary', 'is_baned', 'is_read', 'view_count', 'nationality']:
                            row_dict[key] = int(value)

                # 处理家庭数据的重复户号问题
                if model == Family and 'household_number' in row_dict:
                    # 确保户号唯一，考虑到整个数据集可能存在重复
                    original_hh_number = row_dict['household_number']
                    household_number = original_hh_number
                    counter = 0

                    # 检查批次内是否已使用该户号
                    while True:
                        # 首先检查批次内是否已使用
                        if household_number in used_unique_fields['household_number']:
                            counter += 1
                            household_number = f"{original_hh_number}_{counter}"
                        else:
                            # 然后检查数据库中是否已存在
                            try:
                                Family.objects.get(
                                    household_number=household_number)
                                # 如果存在，继续生成新的户号
                                counter += 1
                                household_number = f"{original_hh_number}_{counter}"
                            except Family.DoesNotExist:
                                # 如果不存在，使用这个户号
                                break

                    # 更新户号
                    row_dict['household_number'] = household_number
                    used_unique_fields['household_number'].add(
                        household_number)

                # 处理居民数据的重复身份证号问题
                if model == Resident and 'id_card' in row_dict:
                    # 确保身份证号唯一，考虑到整个数据集可能存在重复
                    original_id_card = row_dict['id_card']
                    id_card = original_id_card
                    counter = 0

                    # 检查批次内和数据库中是否已使用该身份证号
                    while True:
                        # 首先检查批次内是否已使用
                        if id_card in used_unique_fields['id_card']:
                            counter += 1
                            # 生成新的身份证号（在原有基础上修改最后一位）
                            id_card = f"{original_id_card[:17]}{chr(ord(original_id_card[17]) + counter % 10)}"
                        else:
                            # 然后检查数据库中是否已存在
                            try:
                                Resident.objects.get(id_card=id_card)
                                # 如果存在，继续生成新的身份证号
                                counter += 1
                                id_card = f"{original_id_card[:17]}{chr(ord(original_id_card[17]) + counter % 10)}"
                            except Resident.DoesNotExist:
                                # 如果不存在，使用这个身份证号
                                break

                    # 更新身份证号
                    row_dict['id_card'] = id_card
                    used_unique_fields['id_card'].add(id_card)
                
                # 处理小区数据的重复名称和社区组合问题
                if model == HousingEstate and 'name' in row_dict and 'community_id' in row_dict:
                    # 确保小区名称和社区组合唯一
                    original_name = row_dict['name']
                    community_id = row_dict['community_id']
                    name = original_name
                    counter = 0
                    
                    # 检查批次内和数据库中是否已使用该名称和社区组合
                    while True:
                        # 生成唯一键
                        unique_key = (name, community_id)
                        # 首先检查批次内是否已使用
                        if unique_key in used_unique_fields['housing_estate_name_community']:
                            counter += 1
                            name = f"{original_name}_{counter}"
                        else:
                            # 然后检查数据库中是否已存在
                            try:
                                HousingEstate.objects.get(name=name, community_id=community_id)
                                # 如果存在，继续生成新的名称
                                counter += 1
                                name = f"{original_name}_{counter}"
                            except HousingEstate.DoesNotExist:
                                # 如果不存在，使用这个名称
                                break
                    
                    # 更新小区名称
                    row_dict['name'] = name
                    # 添加到已使用的唯一字段集合
                    used_unique_fields['housing_estate_name_community'].add((name, community_id))

                # 处理外键字段，将_id后缀的字段转换为模型实例
                for key, value in list(row_dict.items()):
                    if key.endswith('_id'):
                        # 移除_id后缀，获取字段名
                        field_name = key[:-3]
                        # 获取模型的字段映射
                        fields_map = {
                            field.name: field for field in model._meta.fields}
                        if field_name in fields_map:
                            # 获取外键字段的关联模型
                            related_model = fields_map[field_name].remote_field.model
                            try:
                                # 获取关联实例
                                related_instance = related_model.objects.get(
                                    id=value)
                                # 替换_id字段为关联实例
                                row_dict[field_name] = related_instance
                                # 删除_id字段
                                del row_dict[key]
                            except related_model.DoesNotExist:
                                print(
                                    f"警告：{model_name} 外键 {field_name} 关联的 {related_model.__name__} 实例不存在，ID: {value}")
                                # 如果外键不存在，跳过这条记录
                                row_dict = None
                                break

                if row_dict:
                    # 创建模型实例
                    instance = model(**row_dict)
                    records.append(instance)

                    # 当达到批次大小时，批量插入数据
                    if len(records) >= batch_size:
                        model.objects.bulk_create(
                            records, batch_size=batch_size)
                        total_records += len(records)
                        print(f"已上传 {total_records} 条 {model_name} 数据")
                        records = []
                        # 重置唯一字段跟踪，避免内存占用过大
                        used_unique_fields = {
                            'household_number': set(),
                            'id_card': set(),
                            'housing_estate_name_community': set()
                        }

            # 插入剩余的数据
            if records:
                model.objects.bulk_create(records, batch_size=len(records))
                total_records += len(records)

            print(f"成功上传 {total_records} 条 {model_name} 数据")

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"上传 {model_name} 数据失败: {str(e)}")
            print(f"数据文件: {file_path}")
            print(f"错误类型: {type(e).__name__}")
            print("正在回滚所有数据...")
            # 回滚已上传的数据，使用更安全的方式删除数据
            for item_rolled in upload_order[:upload_order.index(item)]:
                try:
                    # 使用分批次删除或直接截断表
                    # 对于SQLite，直接删除所有记录可能会遇到参数数量限制
                    # 我们可以使用更简单的方式：先删除外键关联，再删除主表数据
                    model_rolled = item_rolled['model']
                    print(f"正在回滚 {item_rolled['model_name']} 数据...")
                    # 使用直接删除，避免参数数量限制
                    model_rolled.objects.all().delete()
                except Exception as rollback_e:
                    print(
                        f"回滚 {item_rolled['model_name']} 数据失败: {str(rollback_e)}")
                    # 继续回滚其他数据，不中断
                    continue
            print("数据回滚完成，上传失败")
            return False

    print("\n" + "=" * 50)
    print("所有数据上传完成！")

    # 验证数据完整性
    print("\n开始验证数据完整性...")
    print("=" * 50)

    total_errors = 0

    for item in upload_order:
        model = item['model']
        model_name = item['model_name']

        # 检查记录数量
        count = model.objects.count()
        print(f"{model_name} 记录数量: {count}")

        # 检查外键完整性
        for field in model._meta.fields:
            if field.is_relation and not field.primary_key:
                # 检查外键字段
                field_name = field.name
                related_model = field.remote_field.model

                # 获取所有非空的外键值
                foreign_key_values = model.objects.filter(
                    **{f"{field_name}__isnull": False}).values_list(f"{field_name}_id", flat=True)
                related_ids = set(
                    related_model.objects.values_list('id', flat=True))

                # 检查缺失的外键
                missing_ids = set(foreign_key_values) - related_ids
                if missing_ids:
                    total_errors += len(missing_ids)
                    print(
                        f"  错误：{model_name} 的 {field_name} 字段引用了不存在的 {related_model.__name__} 实例，缺失ID: {missing_ids}")

    if total_errors == 0:
        print("\n所有数据验证通过！")
        print(f"数据完整性验证结果：成功")
    else:
        print(f"\n数据完整性验证结果：失败，共发现 {total_errors} 个错误")

    print("=" * 50)
    return total_errors == 0


if __name__ == "__main__":
    main()

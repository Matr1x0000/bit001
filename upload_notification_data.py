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

    # 导入通知相关模型
    from api.models import (Notification, NotificationRead, User)

    # 数据文件路径
    data_dir = 'testdata'

    # 只导入通知相关的数据
    upload_order = [{
        'model': Notification,
        'file_name': '通知数据.xlsx',
        'model_name': '通知'
    }, {
        'model': NotificationRead,
        'file_name': '通知状态数据.xlsx',
        'model_name': '通知状态'
    }]

    print("开始上传通知相关数据到数据库...")
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

            # 清除现有数据
            print(f"正在清除现有 {model_name} 数据...")
            model.objects.all().delete()
            print(f"已清除现有 {model_name} 数据")

            # 准备数据
            records = []

            # 分批次处理和插入数据
            batch_size = 500
            total_records = 0

            for _, row in df.iterrows():
                # 转换日期时间字段
                for col in row.index:
                    if 'created_at' in col or 'updated_at' in col or 'publish_time' in col or 'valid_until' in col or 'read_time' in col:
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
                        if key.endswith('_id') or key in [
                                'notification_type', 'is_read', 'view_count'
                        ]:
                            row_dict[key] = int(value)

                # 处理外键字段，将_id后缀的字段转换为模型实例
                for key, value in list(row_dict.items()):
                    if key.endswith('_id'):
                        # 移除_id后缀，获取字段名
                        field_name = key[:-3]
                        # 获取模型的字段映射
                        fields_map = {
                            field.name: field
                            for field in model._meta.fields
                        }
                        if field_name in fields_map:
                            # 获取外键字段的关联模型
                            related_model = fields_map[
                                field_name].remote_field.model
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
                                    f"警告：{model_name} 外键 {field_name} 关联的 {related_model.__name__} 实例不存在，ID: {value}"
                                )
                                # 如果外键不存在，跳过这条记录
                                row_dict = None
                                break

                if row_dict:
                    # 创建模型实例
                    instance = model(**row_dict)
                    records.append(instance)

                    # 当达到批次大小时，批量插入数据
                    if len(records) >= batch_size:
                        model.objects.bulk_create(records,
                                                  batch_size=batch_size)
                        total_records += len(records)
                        print(f"已上传 {total_records} 条 {model_name} 数据")
                        records = []

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
            print("数据上传失败")
            return False

    print("\n" + "=" * 50)
    print("所有通知相关数据上传完成！")

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
                    **{
                        f"{field_name}__isnull": False
                    }).values_list(f"{field_name}_id", flat=True)
                related_ids = set(
                    related_model.objects.values_list('id', flat=True))

                # 检查缺失的外键
                missing_ids = set(foreign_key_values) - related_ids
                if missing_ids:
                    total_errors += len(missing_ids)
                    print(
                        f"  错误：{model_name} 的 {field_name} 字段引用了不存在的 {related_model.__name__} 实例，缺失ID: {missing_ids}"
                    )

    if total_errors == 0:
        print("\n所有数据验证通过！")
        print(f"数据完整性验证结果：成功")
    else:
        print(f"\n数据完整性验证结果：失败，共发现 {total_errors} 个错误")

    print("=" * 50)
    return total_errors == 0


if __name__ == "__main__":
    main()

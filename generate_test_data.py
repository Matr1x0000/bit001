#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成模拟数据脚本
"""

import os
import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import numpy as np

# 初始化Faker实例，设置为中文
fake = Faker('zh_CN')

# 设置随机种子，确保结果可复现
random.seed(42)
np.random.seed(42)

# 创建输出目录
output_dir = 'f:/lswcode/bit002/testdata'
os.makedirs(output_dir, exist_ok=True)

# 1. 生成社区数据
print("正在生成社区数据...")
community_names = [
    "阳光社区", "春风社区", "幸福社区", "和谐社区", "绿苑社区",
    "新华社区", "文化社区", "平安社区", "健康社区", "未来社区"
]

communities = []
for i in range(10):
    community = {
        "id": i+1,
        "name": community_names[i],
        "office_address": fake.street_address(),
        "office_phone": fake.phone_number(),
        "created_at": fake.date_time_between(start_date="-2y", end_date="now"),
        "remark": fake.sentence()
    }
    communities.append(community)

# 保存社区数据到Excel
pd.DataFrame(communities).to_excel(os.path.join(output_dir, "社区数据.xlsx"), index=False)
print(f"已生成社区数据，共{len(communities)}条")

# 2. 生成社区工作者数据
print("正在生成社区工作者数据...")
social_workers = []
for i in range(100):
    community_id = random.randint(1, 10)
    social_worker = {
        "id": i+1,
        "community_id": community_id,
        "name": fake.name(),
        "gender": random.randint(1, 2),
        "phone": fake.phone_number(),
        "birth_date": fake.date_of_birth(minimum_age=20, maximum_age=65),
        "is_secretary": random.random() < 0.1,  # 10%概率为书记
        "is_baned": random.random() > 0.05,  # 5%概率离职
        "created_at": fake.date_time_between(start_date="-2y", end_date="now"),
        "remark": fake.sentence()
    }
    social_workers.append(social_worker)

# 保存社区工作者数据到Excel
pd.DataFrame(social_workers).to_excel(os.path.join(output_dir, "社区工作者数据.xlsx"), index=False)
print(f"已生成社区工作者数据，共{len(social_workers)}条")

# 3. 生成小区数据
print("正在生成小区数据...")
housing_estates = []
estate_id = 1
for community in communities:
    # 每个社区生成4-6个小区
    num_estates = random.randint(4, 6)
    for _ in range(num_estates):
        # 小区名称使用常见的命名元素
        estate_name = f"{community['name']}{random.choice(['花园', '家园', '小区', '苑', '里', '居'])}"
        housing_estate = {
            "id": estate_id,
            "community_id": community["id"],
            "name": estate_name,
            "address": fake.street_address(),
            "property_company": fake.company(),
            "property_phone": fake.phone_number(),
            "created_at": fake.date_time_between(start_date="-3y", end_date="now"),
            "remark": fake.sentence()
        }
        housing_estates.append(housing_estate)
        estate_id += 1

# 保存小区数据到Excel
pd.DataFrame(housing_estates).to_excel(os.path.join(output_dir, "小区数据.xlsx"), index=False)
print(f"已生成小区数据，共{len(housing_estates)}条")

# 4. 生成栋楼数据
print("正在生成栋楼数据...")
buildings = []
building_id = 1
for estate in housing_estates:
    # 每个小区生成6-12栋楼
    num_buildings = random.randint(6, 12)
    for i in range(num_buildings):
        building = {
            "id": building_id,
            "estate_id": estate["id"],
            "name": f"{i+1}栋",
            "building_type": random.randint(1, 2),  # 1=多层, 2=高层
            "total_floors": random.randint(6, 22),  # 多层6-22层
            "units_per_floor": random.randint(2, 4),  # 每层2-4户
            "created_at": fake.date_time_between(start_date="-5y", end_date="now"),
            "remark": fake.sentence()
        }
        buildings.append(building)
        building_id += 1

# 保存栋楼数据到Excel
pd.DataFrame(buildings).to_excel(os.path.join(output_dir, "栋楼数据.xlsx"), index=False)
print(f"已生成栋楼数据，共{len(buildings)}条")

# 5. 生成单元数据
print("正在生成单元数据...")
units = []
unit_id = 1
for building in buildings:
    # 每栋楼生成1-5个单元
    num_units = random.randint(1, 5)
    for i in range(num_units):
        unit = {
            "id": unit_id,
            "building_id": building["id"],
            "name": f"{i+1}单元",
            "created_at": fake.date_time_between(start_date="-5y", end_date="now"),
            "remark": fake.sentence()
        }
        units.append(unit)
        unit_id += 1

# 保存单元数据到Excel
pd.DataFrame(units).to_excel(os.path.join(output_dir, "单元数据.xlsx"), index=False)
print(f"已生成单元数据，共{len(units)}条")

# 6. 生成房号数据（楼房）
print("正在生成楼房房号数据...")
apartments = []
apartment_id = 1
for unit in units:
    # 每个单元生成12-44个偶数房号
    num_apartments = random.randint(12, 44)
    # 生成偶数房号，如201, 202等，注意：房号是偶数，所以需要生成奇数层和偶数层的偶数房间
    for i in range(num_apartments):
        # 生成楼层号
        floor = i // 4 + 1
        # 生成房间号（偶数）
        room = (i % 4) * 2 + 1 if i % 2 == 0 else (i % 4) * 2 + 2
        house_number = f"{floor:02d}{room:02d}"
        apartment = {
            "id": apartment_id,
            "unit_id": unit["id"],
            "house_number": house_number,
            "created_at": fake.date_time_between(start_date="-5y", end_date="now"),
            "remark": fake.sentence()
        }
        apartments.append(apartment)
        apartment_id += 1

# 保存楼房房号数据到Excel
pd.DataFrame(apartments).to_excel(os.path.join(output_dir, "楼房房号数据.xlsx"), index=False)
print(f"已生成楼房房号数据，共{len(apartments)}条")

# 7. 生成胡同数据
print("正在生成胡同数据...")
hutongs = []
hutong_id = 1
for i in range(20):
    community_id = random.randint(1, 10)
    hutong = {
        "id": hutong_id,
        "community_id": community_id,
        "name": f"{fake.street_name()}胡同",
        "created_at": fake.date_time_between(start_date="-10y", end_date="now"),
        "remark": fake.sentence()
    }
    hutongs.append(hutong)
    hutong_id += 1

# 保存胡同数据到Excel
pd.DataFrame(hutongs).to_excel(os.path.join(output_dir, "胡同数据.xlsx"), index=False)
print(f"已生成胡同数据，共{len(hutongs)}条")

# 8. 生成房号数据（平房）
print("正在生成平房房号数据...")
single_houses = []
single_house_id = 1
for hutong in hutongs:
    # 每个胡同生成35-50个平房房号
    num_houses = random.randint(35, 50)
    for i in range(num_houses):
        house_number = f"{i+1}号"
        single_house = {
            "id": single_house_id,
            "hutong_id": hutong["id"],
            "house_number": house_number,
            "created_at": fake.date_time_between(start_date="-10y", end_date="now"),
            "remark": fake.sentence()
        }
        single_houses.append(single_house)
        single_house_id += 1

# 保存平房房号数据到Excel
pd.DataFrame(single_houses).to_excel(os.path.join(output_dir, "平房房号数据.xlsx"), index=False)
print(f"已生成平房房号数据，共{len(single_houses)}条")

# 9. 生成居住地址数据
print("正在生成居住地址数据...")
residential_addresses = []
address_id = 1

# 生成楼房居住地址
for apartment in apartments:
    # 找到对应的单元、楼栋、小区
    unit = next(u for u in units if u["id"] == apartment["unit_id"])
    building = next(b for b in buildings if b["id"] == unit["building_id"])
    estate = next(e for e in housing_estates if e["id"] == building["estate_id"])
    
    address = {
        "id": address_id,
        "address_type": 1,  # 1=楼房
        "estate_id": estate["id"],
        "building_id": building["id"],
        "unit_id": unit["id"],
        "apartment_id": apartment["id"],
        "hutong_id": None,
        "single_house_id": None,
        "is_resident": random.randint(1, 3),  # 1=自住, 2=租住, 3=空房
        "created_at": fake.date_time_between(start_date="-5y", end_date="now"),
        "remark": fake.sentence()
    }
    residential_addresses.append(address)
    address_id += 1

# 生成平房居住地址
for single_house in single_houses:
    # 找到对应的胡同
    hutong = next(h for h in hutongs if h["id"] == single_house["hutong_id"])
    
    address = {
        "id": address_id,
        "address_type": 2,  # 2=平房
        "estate_id": None,
        "building_id": None,
        "unit_id": None,
        "apartment_id": None,
        "hutong_id": hutong["id"],
        "single_house_id": single_house["id"],
        "is_resident": random.randint(1, 3),  # 1=自住, 2=租住, 3=空房
        "created_at": fake.date_time_between(start_date="-10y", end_date="now"),
        "remark": fake.sentence()
    }
    residential_addresses.append(address)
    address_id += 1

# 保存居住地址数据到Excel
pd.DataFrame(residential_addresses).to_excel(os.path.join(output_dir, "居住地址数据.xlsx"), index=False)
print(f"已生成居住地址数据，共{len(residential_addresses)}条")

# 10. 生成家庭数据
print("正在生成家庭数据...")
families = []
family_id = 1
# 生成5000个家庭
for _ in range(5000):
    # 随机选择一个居住地址
    address = random.choice(residential_addresses)
    family = {
        "id": family_id,
        "household_number": f"F{family_id:06d}",
        "owner_name": fake.name(),
        "residential_address_id": address["id"],
        "contact_phone": fake.phone_number(),
        "created_at": fake.date_time_between(start_date="-10y", end_date="now"),
        "remark": fake.sentence()
    }
    families.append(family)
    family_id += 1

# 保存家庭数据到Excel
pd.DataFrame(families).to_excel(os.path.join(output_dir, "家庭数据.xlsx"), index=False)
print(f"已生成家庭数据，共{len(families)}条")

# 11. 生成通知数据
print("正在生成通知数据...")
notifications = []
notification_id = 1
# 通知标题和内容模板
notification_templates = [
    ("社区消防演练通知", "为增强居民消防安全意识，社区将于{date}上午9:00在{location}举行消防演练，请居民积极参与。"),
    ("垃圾分类宣传活动", "社区将于{date}开展垃圾分类宣传活动，现场将发放分类垃圾桶和宣传资料，欢迎居民参加。"),
    ("社区疫苗接种通知", "{date}将在社区卫生服务中心开展疫苗接种工作，请符合条件的居民携带身份证前往接种。"),
    ("社区老年人健康体检", "社区将于{date}为65岁以上老年人开展免费健康体检，请携带身份证和医保卡参加。"),
    ("社区文化节活动", "社区文化节将于{date}在社区广场举行，包括文艺演出、手工制作等活动，欢迎居民参加。"),
    ("社区安全隐患排查", "近期将开展社区安全隐患排查工作，请居民配合社区工作人员检查，确保居住安全。"),
    ("社区志愿者招募", "社区招募志愿者，参与社区服务工作，有意者请前往社区居委会报名。"),
    ("社区水电费缴纳通知", "请居民及时缴纳水电费，避免影响正常使用。"),
    ("社区停车位管理通知", "为规范社区停车秩序，将对社区停车位进行统一管理，请居民配合。"),
    ("社区环境整治通知", "将开展社区环境整治工作，清理小区内的杂物和垃圾，请居民自觉维护小区环境。")
]

for i in range(20):
    # 随机选择一个模板
    title, content_template = random.choice(notification_templates)
    # 生成未来1-30天内的随机日期
    future_date = datetime.now() + timedelta(days=random.randint(1, 30))
    # 填充模板内容
    content = content_template.format(
        date=future_date.strftime("%Y年%m月%d日"),
        location=fake.street_address(),
        time=fake.time()
    )
    notification = {
        "id": notification_id,
        "title": title,
        "content": content,
        "notification_type": random.randint(1, 3),  # 1=紧急, 2=普通, 3=活动
        "publisher_id": 1,  # 假设用户ID为1的是管理员
        "publish_time": datetime.now(),
        "valid_until": future_date + timedelta(days=7),  # 有效期7天
        "view_count": 0,
        "created_at": datetime.now(),
        "remark": fake.sentence()
    }
    notifications.append(notification)
    notification_id += 1

# 保存通知数据到Excel
pd.DataFrame(notifications).to_excel(os.path.join(output_dir, "通知数据.xlsx"), index=False)
print(f"已生成通知数据，共{len(notifications)}条")

# 12. 生成通知状态数据
print("正在生成通知状态数据...")
notification_reads = []
notification_read_id = 1
# 生成500条通知状态记录
for _ in range(500):
    # 随机选择一个通知
    notification = random.choice(notifications)
    # 随机选择一个家庭
    family = random.choice(families)
    # 随机生成阅读状态
    is_read = random.random() < 0.7  # 70%概率已读
    read_time = datetime.now() if is_read else None
    notification_read = {
        "id": notification_read_id,
        "notification_id": notification["id"],
        "user_id": 1,  # 假设用户ID为1的是管理员
        "is_read": is_read,
        "read_time": read_time,
        "created_at": datetime.now(),
        "remark": fake.sentence()
    }
    notification_reads.append(notification_read)
    notification_read_id += 1

# 保存通知状态数据到Excel
pd.DataFrame(notification_reads).to_excel(os.path.join(output_dir, "通知状态数据.xlsx"), index=False)
print(f"已生成通知状态数据，共{len(notification_reads)}条")

# 13. 生成居民数据
print("正在生成居民数据...")
residents = []
resident_id = 1
# 地区代码：20个北京地区、10个天津地区、5个上海地区、其余承德地区
area_codes = [
    # 北京地区
    "110101", "110102", "110105", "110106", "110107", "110108", "110109", "110111", "110112", "110113",
    "110114", "110115", "110116", "110117", "110228", "110229", "110230", "110231", "110232", "110233",
    # 天津地区
    "120101", "120102", "120103", "120104", "120105", "120106", "120110", "120111", "120112", "120113",
    # 上海地区
    "310101", "310103", "310104", "310105", "310106",
    # 承德地区
    "130802", "130803", "130821", "130822", "130823", "130824", "130825", "130826", "130827", "130828",
    "130829", "130830", "130831", "130832", "130833", "130834", "130835", "130836", "130837", "130838"
]

# 生成符合国家标准的身份证号
def generate_id_card():
    # 随机选择地区代码
    area_code = random.choice(area_codes)
    # 生成随机出生日期
    birth_date = fake.date_of_birth(minimum_age=0, maximum_age=100)
    birth_str = birth_date.strftime("%Y%m%d")
    # 生成随机顺序码
    sequence = f"{random.randint(0, 999):03d}"
    # 计算校验码
    id_card_no = area_code + birth_str + sequence
    # 简单的校验码计算（真实校验码算法较复杂，这里使用随机数模拟）
    check_code = random.choice("0123456789Xx")
    return f"{id_card_no}{check_code}"

# 为每个家庭生成1-5位居民
for family in families:
    # 每个家庭1-5位居民
    num_residents = random.randint(1, 5)
    for i in range(num_residents):
        # 生成身份证号
        id_card = generate_id_card()
        # 生成居民信息
        resident = {
            "id": resident_id,
            "name": fake.name(),
            "gender": random.randint(1, 2),
            "nationality": random.randint(1, 57),  # 57个民族
            "id_card": id_card,
            "phone": fake.phone_number(),
            "family_id": family["id"],
            "political_status": random.randint(1, 13),  # 13种政治面貌
            "marital_status": random.randint(1, 4),  # 4种婚姻状态
            "education": random.randint(1, 9),  # 9种学历
            "job": random.random() < 0.7,  # 70%概率有工作
            "is_dead": random.random() < 0.01,  # 1%概率死亡
            "created_at": fake.date_time_between(start_date="-10y", end_date="now"),
            "remark": fake.sentence()
        }
        residents.append(resident)
        resident_id += 1

# 保存居民数据到Excel
pd.DataFrame(residents).to_excel(os.path.join(output_dir, "居民数据.xlsx"), index=False)
print(f"已生成居民数据，共{len(residents)}条")

print("所有数据生成完成！")
print(f"数据已保存到目录：{output_dir}")

#!/usr/bin/env python
"""
生成模拟数据的Excel文件，包括20条社区工作者数据和10条干部数据
"""

import os
import sys
import random
from datetime import datetime, date, timedelta
from openpyxl import Workbook

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 社区名称列表
COMMUNITIES = [
    "胜利社区", "和平社区", "民主社区", "团结社区", "建国社区", "解放社区", "幸福社区", "光明社区", "前进社区",
    "先锋社区"
]

# 干部职务列表
CADRE_POSITIONS = [
    "主任", "副主任", "科长", "副科长", "科员", "办事员", "调研员", "助理调研员", "主任科员", "副主任科员"
]


# 生成随机姓名
def generate_name():
    first_names = ["王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴"]
    male_names = ["明", "强", "军", "伟", "磊", "刚", "勇", "杰", "涛", "超"]
    female_names = ["芳", "娜", "秀英", "敏", "静", "丽", "娟", "艳", "玲", "燕"]

    first = random.choice(first_names)
    if random.random() < 0.5:
        last = random.choice(male_names)
    else:
        last = random.choice(female_names)

    return first + last


# 生成随机性别
def generate_gender():
    return random.randint(1, 2)  # 1男，2女


# 生成随机手机号
def generate_phone():
    prefixes = [
        "130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
        "150", "151", "152", "153", "155", "156", "157", "158", "159", "180",
        "181", "182", "183", "184", "185", "186", "187", "188", "189"
    ]
    prefix = random.choice(prefixes)
    suffix = ''.join(random.choices('0123456789', k=8))
    return prefix + suffix


# 生成随机出生年月
def generate_birth_date():
    start = date(1970, 1, 1)
    end = date(2000, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)


# 生成社区工作者数据
def generate_social_worker_data(count=20):
    data = []
    for i in range(count):
        name = generate_name()
        gender = generate_gender()
        phone = generate_phone()
        birth_date = generate_birth_date()
        community = random.choice(COMMUNITIES)
        is_secretary = random.random() < 0.2  # 20%的概率是书记
        is_baned = random.random() < 0.9  # 90%的概率在职
        remark = f"社区工作者{i+1}"

        data.append({
            "序号": i + 1,
            "姓名": name,
            "性别": "男" if gender == 1 else "女",
            "联系电话": phone,
            "出生年月": birth_date.strftime("%Y-%m-%d"),
            "所属社区": community,
            "是否为书记": "是" if is_secretary else "否",
            "是否在职": "在职" if is_baned else "离职",
            "备注": remark
        })
    return data


# 生成干部数据
def generate_cadre_data(count=10):
    data = []
    for i in range(count):
        name = generate_name()
        gender = generate_gender()
        phone = generate_phone()
        birth_date = generate_birth_date()
        position = random.choice(CADRE_POSITIONS)
        is_baned = random.random() < 0.95  # 95%的概率在职
        remark = f"干部{i+1}"

        data.append({
            "序号": i + 1,
            "姓名": name,
            "性别": "男" if gender == 1 else "女",
            "联系电话": phone,
            "出生年月": birth_date.strftime("%Y-%m-%d"),
            "职务": position,
            "是否在职": "在职" if is_baned else "离职",
            "备注": remark
        })
    return data


# 生成Excel文件
def generate_excel_file():
    # 创建工作簿
    wb = Workbook()

    # 生成社区工作者数据
    social_worker_data = generate_social_worker_data(20)
    # 创建社区工作者工作表
    sw_sheet = wb.active
    sw_sheet.title = "社区工作者"

    # 写入社区工作者表头
    sw_headers = [
        "序号", "姓名", "性别", "联系电话", "出生年月", "所属社区", "是否为书记", "是否在职", "备注"
    ]
    sw_sheet.append(sw_headers)

    # 写入社区工作者数据
    for row in social_worker_data:
        sw_sheet.append([row[header] for header in sw_headers])

    # 生成干部数据
    cadre_data = generate_cadre_data(10)
    # 创建干部工作表
    cad_sheet = wb.create_sheet(title="干部")

    # 写入干部表头
    cad_headers = ["序号", "姓名", "性别", "联系电话", "出生年月", "职务", "是否在职", "备注"]
    cad_sheet.append(cad_headers)

    # 写入干部数据
    for row in cadre_data:
        cad_sheet.append([row[header] for header in cad_headers])

    # 保存Excel文件
    excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "testdata", "模拟数据.xlsx")
    wb.save(excel_path)

    print(f"✅ 模拟数据已生成，保存路径：{excel_path}")
    print(f"📊 社区工作者数据：{len(social_worker_data)}条")
    print(f"📊 干部数据：{len(cadre_data)}条")


if __name__ == "__main__":
    generate_excel_file()

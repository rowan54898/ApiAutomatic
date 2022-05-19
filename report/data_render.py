#  -*-  coding:utf-8 -*-
import os
from datetime import datetime

import jinja2

from utils.testcase_handler import *


def data_render_html():
    """获取测试用例信息"""
    excel_data_list = get_testcase()
    # print(excel_data_list)

    root_dir = os.path.dirname(os.path.abspath(__file__))  # 获取系统当前绝对路径
    # print(ROOT_DIR)

    """指定使用模板文件"""
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(root_dir))
    temp = env.get_template('template.html')

    """测试报告页面数据"""
    # 统计测试用例条数
    testcase_num = len(excel_data_list)
    # print(testcase_num)

    # 统计测试用例为TRUE数量
    x = 0  # true
    y = 0  # false
    z = 0  # 耗时，单位：s（秒）
    api_list = []

    for case_info in excel_data_list:
        # 计数true和false的测试用例各多少
        if case_info[15] is True:
            x += 1
        else:
            y += 1

        # 找到所有不同的接口添加进空列表
        if case_info[16] not in api_list:
            api_list.append(case_info[16])
        else:
            pass

        # 找到所有接口耗时，并累计总耗时
        z += eval(str(case_info[18]))

    # 精度俩位小数
    request_time = "%.2f" % z
    # print(x, y, request_time)

    # 统计接口数量
    api_num = len(api_list)
    # print(api_num)

    # 统计成功率
    a = '%'
    success_rate = (x / (x + y)) * 100
    success_rate_new = str(success_rate) + a
    # print(success_rate_new)

    """渲染页面信息context，必须json格式"""
    context = {'excel_data_list': excel_data_list,
               'testcase_num': testcase_num,
               'api_num': api_num,
               'success_num': x,
               'fail_num': y,
               'success_rate': success_rate_new,
               'request_time': request_time
               }
    temp_out = temp.render(context)

    """指定生成html文件的名字+路径"""
    time = datetime.now()
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    report_path = '测试报告' + now + '.html'
    with open(os.path.join(root_dir, report_path), 'w', encoding='utf-8') as f:
        f.writelines(temp_out)
        f.close()


# data_render_html()

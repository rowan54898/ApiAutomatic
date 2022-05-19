# -*- coding:utf-8 -*-
import json

from biz import login
from report import data_render
from utils import request_process, data_process
from utils.conftest import args
from utils.keyword_parsing import *


def excute_testcase(path):
    # path = './config/ksb_login_info.yaml'
    auth_token = login.get_token(path=path)
    print(auth_token)
    for mylist in testcase_handler.get_testcase():
        """获取基本信息"""
        case_no = str(mylist[0])
        print(case_no)
        line_no = testcase_handler.get_testcase_line_no(case_no=case_no)

        # 获取解析后的api，并写入Excel
        api = keyword_parsing_api(case_no=case_no)
        testcase_handler.write_result(line_no=line_no, column=17, excute_result=api)

        url = login.read_yaml(path=path)['login_page_url'] + api
        print(url)
        method = mylist[10]
        header = {"Content-Type": "application/json", "Authorization": auth_token}

        # 获取解析后的request参数，并写入Excel
        request = keyword_parsing_request(case_no=case_no)
        testcase_handler.write_result(line_no=line_no, column=18, excute_result=str(request))
        print(request)

        """获取基本信息后，执行接口，获取返回值，并写入Excel"""
        res = request_process.request_process(url=url, request_method=method, request_header=header,
                                              request_content=request)
        resjson = json.loads(res.content)
        print(resjson)
        testcase_handler.write_result(line_no=line_no, column=14, excute_result=str(resjson))

        """获取接口执行耗时,并写入Excel"""
        request_time = res.elapsed.total_seconds()
        print(request_time)
        testcase_handler.write_result(line_no=line_no, column=19, excute_result=str(request_time))

        """获取断言结果，并写入Excel"""
        asser_result = data_process.assert_result(line_no=line_no)
        print(asser_result)
        testcase_handler.write_result(line_no=line_no, column=16, excute_result=asser_result)

    """生成测试报告"""
    data_render.data_render_html()


if __name__ == '__main__':
    """引入命令行传参path，如果命令行没有指定值，则按照默认值，详情按照 python3 run.py -h 查看"""
    excute_testcase(args.path)

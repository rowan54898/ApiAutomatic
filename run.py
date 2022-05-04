# -*- coding:utf-8 -*-
import argparse
import json

from biz import login
from utils import request_process, data_process
from utils.keyword_parsing import *

"""
引入注册参数，在命令行传参,便于以后可以和headless无界面Chrome浏览器启动一起，集成Git、Jenkins，在linux上执行。
命令：(python3 run.py -p xxxx -c xxxx)
如：python3 run.py -p ./config/ksb_login_info.yaml -c ./testcase/接口自动化测试用例模板.xlsx
"""
parser = argparse.ArgumentParser(description='启动测试用例的ip地址')
parser.add_argument('-p', '--path', default='./config/ksb_login_info.yaml', help='path')
parser.add_argument('-c', '--case', default='./testcase/接口自动化测试用例模板.xlsx', help='caseName')
args = parser.parse_args()


def excute_testcase(path):
    # path = './config/ksb_login_info.yaml'
    auth_token = login.get_token(path=path)
    print(auth_token)
    for mylist in testcase_handler.get_testcase():
        """获取基本信息"""
        case_no = str(mylist[0])
        print(case_no)
        line_no = testcase_handler.get_testcase_line_no(case_no=case_no)
        # url = mylist[8] + keyword_parsing_api(case_no=case_no)
        url = login.read_yaml(path=path)['login_page_url'] + keyword_parsing_api(case_no=case_no)
        print(url)
        testcase_handler.write_result(line_no=line_no, column=17, excute_result=url)
        method = mylist[10]
        header = {"Content-Type": "application/json", "Authorization": auth_token}
        # request = eval(str(mylist[12]))
        request = keyword_parsing_request(case_no=case_no)
        testcase_handler.write_result(line_no=line_no, column=18, excute_result=str(request))
        print(request)

        """获取基本信息后，执行接口，获取返回值"""
        res = request_process.request_process(url=url, request_method=method, request_header=header,
                                              request_content=request)
        resjson = json.loads(res.content)
        print(resjson)

        """写入执行结果"""
        testcase_handler.write_result(line_no=line_no, column=14, excute_result=str(resjson))
        asser_result = data_process.assert_result(line_no=line_no)
        print(asser_result)

        """写入断言结果"""
        testcase_handler.write_result(line_no=line_no, column=16, excute_result=asser_result)


if __name__ == '__main__':
    """引入命令行传参path，如果命令行没有指定值，则按照默认值，详情按照 python3 run.py -h 查看"""
    excute_testcase(args.path)

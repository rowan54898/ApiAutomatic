# -*- coding:utf-8 -*-
import json
import unittest
from time import sleep

import jsonpath
import openpyxl
import requests
import yaml
from biz import login
from utils import request_process, data_process, testcase_handler
from utils.keyword_parsing import *

path = './config/ksb_login_info.yaml'
auth_token = login.get_token(path=path)
print(auth_token)


def excute_testcase():
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
    excute_testcase()

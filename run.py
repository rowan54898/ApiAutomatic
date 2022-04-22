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

token = login.get_token()
print(token)


def excute_testcase():
    for mylist in testcase_handler.get_testcase():
        case_no = str(mylist[0])
        print(case_no)
        line_no = testcase_handler.get_testcase_line_no(case_no=case_no)
        url = mylist[8] + keyword_parsing_api(case_no=case_no)
        print(url)
        method = mylist[10]
        header = {"Content-Type": "application/json", "Authorization": token}
        # request = eval(str(mylist[12]))
        request = keyword_parsing_response(case_no=case_no)
        print(request)
        res = request_process.request_process(url=url, request_method=method, request_header=header,
                                              request_content=request)
        resjson = json.loads(res.content)
        print(resjson)
        testcase_handler.write_result(line_no=line_no, column=14, excute_result=str(resjson))
        asser_result = data_process.assert_result(line_no=line_no)
        print(asser_result)
        testcase_handler.write_result(line_no=line_no, column=16, excute_result=asser_result)
        sleep(10)

if __name__ == '__main__':
    excute_testcase()

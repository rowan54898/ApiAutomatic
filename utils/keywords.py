#  -*-  coding:utf-8 -*-
import ast
import inspect
import json

from utils import testcase_handler


# @ResponseDependMulti('A-002','industryNo','data')
# @PayloadDepend('A-001','industryNam')


def ResponseDependMulti(case_no, keyword, DTO):
    caseinfo = testcase_handler.get_case_info(case_no=case_no)  # 获取当前case_no完整信息
    responsebody = eval(str(caseinfo[13]))
    for data in responsebody[DTO]:
        return data[str(keyword)]


# def ResponseDepend(case_no, keyword):
#     pass


def PayloadDepend(case_no, keyword):
    caseinfo = testcase_handler.get_case_info(case_no=case_no)  # 获取当前case_no完整信息
    requestbody = eval(str(caseinfo[12]))
    return requestbody[keyword]

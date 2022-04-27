#  -*-  coding:utf-8 -*-

import re
import random

from utils import testcase_handler


# @ResponseDependMulti('A-002','industryNo','data')
# @PayloadDepend('A-001','industryNam')


def ResponseDependMulti(case_no, keyword, DTO):
    caseinfo = testcase_handler.get_case_info(case_no=case_no)  # 获取当前case_no完整信息
    responsebody = eval(str(caseinfo[13]))
    if '#' not in DTO:
        for data in responsebody[DTO]:
            return data[str(keyword)]
    elif '#' in DTO:
        jsonpath = re.split('#', DTO)
        print(jsonpath)
        for i in range(len(jsonpath)):
            print(responsebody)
            if type(responsebody) == list:
                responsebody = responsebody[0][jsonpath[i]]
            else:
                responsebody = responsebody[jsonpath[i]]
        # print(responsebody[str(keyword)])
        # print(responsebody)
        if type(responsebody) == list:
            responsebody = responsebody[0][keyword]
            print(responsebody)
            return responsebody
        else:
            return responsebody[keyword]
    else:
        pass


def PayloadDepend(case_no, keyword):
    caseinfo = testcase_handler.get_case_info(case_no=case_no)  # 获取当前case_no完整信息
    requestbody = eval(str(caseinfo[17]))
    return requestbody[keyword]


# @RString('u','10')
# re.search('@(.+?)\(', str("@RString('u','10')")).group(1)
# print(re.search('@(.+?)\(', str("@RString('u','10')")).group(1))
def RString(flag, length):
    u_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZ'
    l_str = 'abcdefghigklmnopqrstuvwxyz'
    m_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz'
    if flag == 'u':
        """获取指定长度的大写字母"""
        random_str = ''
        for i in range(int(length)):
            random_str += u_str[random.randint(0, len(u_str) - 1)]
        # print(random_str)
        return random_str
    elif flag == 'l':
        """获取指定长度的小写字母"""
        random_str = ''
        for i in range(int(length)):
            random_str += l_str[random.randint(0, len(l_str) - 1)]
        # print(random_str)
        return random_str
    elif flag == 'm':
        """获取指定长度的大小写混合字母"""
        random_str = ''
        for i in range(int(length)):
            random_str += m_str[random.randint(0, len(m_str) - 1)]
        # print(random_str)
        return random_str


def RNum(length):
    randstart = 10 ** (length - 1)
    randend = (10 ** length) - 1
    return random.randint(randstart, randend)
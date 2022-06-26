#  -*-  coding:utf-8 -*-
import json
import re

from utils import testcase_handler, keywords
from utils.data_format import data_format


def keywords_list():
    """
    关键字列表
    通过一行行读取py文件的方式，获取所有关键字
    """
    path = './utils/keywords.py'
    func_list = []
    func_list_noparam = []
    with open(path, 'r', encoding='utf-8') as f:
        line = f.readline()
        # print(line)
        while line:
            if ('def' and ':') in line:
                k1, v1 = line.split(':', 1)
                func_i = k1[4:]
                func_list.append(func_i)
                klist = func_i.split('(')
                k2 = klist[0]
                func_list_noparam.append(k2)
            line = f.readline()
    # print(func_list_noparam)
    return func_list_noparam


def dict_flatlist(d):
    """递归方法，将所有k对应的v替换成关键字解析后的真实值"""
    # print(d)
    if d is not None:  # and (':' in d)
        for k, v in d.items():
            if type(v) == dict:
                dict_flatlist(v)
            elif type(v) == list:
                for i in range(len(v)):
                    if type(v) == dict:
                        dict_flatlist(v[i])
                    else:
                        pass
            elif type(v) == int or v is None:
                d[k] = d[k]
            else:
                if re.search('@(.+?)\(', str(v)) is None:
                    d[k] = d[k]
                else:

                    if v.startswith('{'):
                        a = data_format(value=v)
                        dict_flatlist(a)
                        d[k] = str(a)
                    elif v.startswith('['):
                        a = data_format(value=v)
                        for i in range(len(a)):
                            dict_flatlist(a[i])
                        # print(a)
                        a = json.dumps(a)
                        # print(a)
                        d[k] = str(a)
                    else:
                        d[k] = keyword_handler(value=v)
        else:
            pass


def keyword_parsing_request(case_no):
    """
    解析关键字--请求入参
    """
    caseinfo = testcase_handler.get_case_info(case_no=case_no)  # 获取当前case_no完整信息
    request = str(caseinfo[12])
    print(request)
    a = request
    if (type(a) is str) and a.startswith('{'):
        request_new = data_format(request)
        dict_flatlist(d=request_new)
    elif (type(a) is str) and a.startswith('['):
        request_new = data_format(request)
        # print(request_new)
        request_list = []
        for i in range(len(request_new)):
            request_i = request_new[i]
            # print(type(request_i))
            dict_flatlist(d=request_i)
            # request_i = json.dumps(request_i)
            request_list.append(request_i)
            # print(request_new)
        request_new = request_list

    elif type(a) is str and (len(a) > 0):
        request_keywords = re.split('\"', request)
        request_new = ''
        for i in range(len(request_keywords)):
            """将入参重新拼装"""
            if '@' in request_keywords[i]:
                request_new += keyword_handler(value=request_keywords[i])
            else:
                request_new += request_keywords[i]
    else:
        request_new = None
    # print(request_new)
    return request_new


def keyword_parsing_api(case_no):
    """
    解析关键字--请求接口
    """

    caseinfo = testcase_handler.get_case_info(case_no=case_no)  # 获取当前case_no完整信息
    url = caseinfo[9]  # 获取api
    print(url)
    url_keywords = re.split('\"', url)
    url_new = ''
    for i in range(len(url_keywords)):
        """将api重新拼装"""
        if '@' in url_keywords[i]:
            url_new += keyword_handler(value=url_keywords[i])
        else:
            url_new += url_keywords[i]
    # print(url_new)
    return url_new


def keyword_handler(value):
    """
    关键字处理方法，将关键字换成对应值并返回
    ps：支持一个value中有多个关键字，并且拼接上
    """

    new_value = ''
    if '@' in value:
        keyword_handler_list = re.split('@', value)
        # print(keyword_handler_list)
        for v in keyword_handler_list:
            if re.search('(.+?)\(', str(v)) is None:
                new_value += v
            elif re.search('(.+?)\(', str(v)).group(1) in keywords_list():
                # re.search('((.+?)\)', str(v)).group(1)
                case_no_find = re.split('\'', v)[1]
                # print(case_no_find)
                keyword = re.split('\'', v)[3]
                if str(re.search('(.+?)\(', str(v)).group(1)) == 'ResponseDependMulti':
                    dto = re.split('\'', v)[5]
                    # print(DTO)
                    new_value += keywords.ResponseDependMulti(case_no=case_no_find, keyword=keyword, dto=dto)
                    # print(d[k])
                elif str(re.search('(.+?)\(', str(v)).group(1)) == 'PayloadDepend':
                    new_value += keywords.PayloadDepend(case_no=case_no_find, keyword=keyword)
                elif str(re.search('(.+?)\(', str(v)).group(1)) == 'RString':
                    new_value += keywords.RString(flag=case_no_find, length=keyword)

            else:
                pass
    else:
        new_value += value
    return new_value


def keyword_header(case_no, auth_token):
    """
    请求头content_type的格式处理
    """
    mylist = testcase_handler.get_case_info(case_no=case_no)
    content_type = mylist[11]
    if len(content_type) > 0:
        header = {"Content-Type": content_type, "Authorization": auth_token}
    else:
        header = {"Content-Type": "application/json", "Authorization": auth_token}

    return header


def keyword_judge_header(header, request, res):
    """判断是不同格式的请求头返回不一样的数据"""
    if 'x' not in header:
        if isinstance(request, list):
            resjson = res.text
        else:
            resjson = json.loads(res.content)
    else:
        resjson = res.text
    return resjson

# case_no = 'A-049'
# # keyword_parsing_api(case_no=case_no)
# keyword_parsing_request(case_no=case_no)

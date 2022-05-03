#  -*-  coding:utf-8 -*-
import re

from utils import testcase_handler, keywords


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
                    if type(i) == dict:
                        dict_flatlist(v[i])
                    else:
                        pass
            elif type(v) == int or v is None:
                d[k] = d[k]
            else:
                if re.search('@(.+?)\(', str(v)) is None:
                    d[k] = d[k]
                else:
                    d[k] = keyword_handler(value=v)
        else:
            pass


def keyword_parsing_request(case_no):
    """
    解析关键字--请求入参
    """
    caseinfo = testcase_handler.get_case_info(case_no=case_no)  # 获取当前case_no完整信息
    request = eval(str(caseinfo[12]))
    print(request)
    dict_flatlist(d=request)
    # print(request)
    return request


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

    return new_value

# case_no = 'A-004'
# keyword_parsing_api(case_no=case_no)
# keyword_parsing_response(case_no=case_no)

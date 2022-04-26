#  -*-  coding:utf-8 -*-
import re

from utils import testcase_handler, keywords


def keywords_list():
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
    # print(d)
    if (d is not None):  # and (':' in d)
        for k, v in d.items():
            if type(v) == dict:
                dict_flatlist(v)
            elif type(v) == list:
                for i in range(len(v)):
                    if type(i) == dict:
                        dict_flatlist(v[i])
                    else:
                        pass
            elif type(v) == int or v == None:
                d[k] = d[k]
            else:
                if re.search('@(.+?)\(', str(v)) == None:
                    d[k] = d[k]
                elif re.search('@(.+?)\(', str(v)).group(1) in keywords_list():
                    # re.search('((.+?)\)', str(v)).group(1)
                    case_no_find = re.split('\'', v)[1]
                    print(case_no_find)
                    keyword = re.split('\'', v)[3]
                    if str(re.search('@(.+?)\(', str(v)).group(1)) == 'ResponseDependMulti':
                        DTO = re.split('\'', v)[5]
                        print(DTO)
                        d[k] = keywords.ResponseDependMulti(case_no=case_no_find, keyword=keyword, DTO=DTO)
                        print(d[k])
                    elif str(re.search('@(.+?)\(', str(v)).group(1)) == 'PayloadDepend':
                        d[k] = keywords.PayloadDepend(case_no=case_no_find, keyword=keyword)
                    elif str(re.search('@(.+?)\(', str(v)).group(1)) == 'RString':
                        d[k] = keywords.RString(flag=case_no_find, length=keyword)

                else:
                    pass
        else:
            pass


def keyword_parsing_response(case_no):
    caseinfo = testcase_handler.get_case_info(case_no=case_no)  # 获取当前case_no完整信息
    request = eval(str(caseinfo[12]))
    print(request)
    dict_flatlist(d=request)
    return request


# case_no = 'A-001'
# keyword_parsing_response(case_no=case_no)


def keyword_parsing_api(case_no):
    caseinfo = testcase_handler.get_case_info(case_no=case_no)  # 获取当前case_no完整信息
    url = caseinfo[9]
    print(url)
    url_keywords = re.split('\"', url)
    url_new = ''
    for i in range(len(url_keywords)):
        if '@' in url_keywords[i]:
            url_keywords_i = re.search('@(.+?)\(', url_keywords[i]).group(1)
            case_no_find = re.split('\'', url_keywords[i])[1]
            keyword = re.split('\'', url_keywords[i])[3]
            if url_keywords_i == 'PayloadDepend':
                url_keywords[i] = keywords.PayloadDepend(case_no=case_no_find, keyword=keyword)
                url_new += url_keywords[i]
            elif url_keywords_i == 'ResponseDependMulti':
                DTO = re.split('\'', url_keywords[i])[5]
                url_keywords[i] = keywords.ResponseDependMulti(case_no=case_no_find, keyword=keyword, DTO=DTO)
                url_new += url_keywords[i]
        else:
            url_new += url_keywords[i]
    # print(url_new)
    return url_new

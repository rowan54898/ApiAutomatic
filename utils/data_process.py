# -*- coding:utf-8 -*-
import json
import re

from utils import testcase_handler

splitList = ['==', '!=', '>', '>=', '<', '<=', '!!']


def assert_handler(line_no):
    mylist = testcase_handler.get_line_no_testcase(line_no=line_no)
    print(mylist)
    checkpoint = mylist[14].split('\n')
    responsebody = eval(str(mylist[13]))
    # print(responsebody)
    newlist = []
    for check in checkpoint:
        for split in splitList:
            if split in check:
                arr = re.split(split, check)
                new_check = str(responsebody[arr[0]]) + str(split) + arr[1]
                newlist.append(new_check)
    # print(newlist)
    return newlist


def assert_result(line_no):
    check_point = assert_handler(line_no=line_no)
    print(check_point)
    try:
        flag = []
        for option in check_point:
            # exceptList = re.split('==|!=|>|>=|<|<=|!!', option)
            if '==' in option:
                exceptList = re.split('==', option)
                if exceptList[0] == exceptList[1]:
                    flag.append('True')
                else:
                    flag.append('False')
            elif '!=' in option:
                exceptList = re.split('!=', option)
                if exceptList[0] != exceptList[1]:
                    flag.append('True')
                else:
                    flag.append('False')
            elif '>' in option:
                exceptList = re.split('>', option)
                if exceptList[0] > exceptList[1]:
                    flag.append('True')
                else:
                    flag.append('False')
                    return flag
            elif '>=' in option:
                exceptList = re.split('>=', option)
                if exceptList[0] >= exceptList[1]:
                    flag.append('True')
                else:
                    flag.append('False')
            elif '<' in option:
                exceptList = re.split('<', option)
                if exceptList[0] < exceptList[1]:
                    flag.append('True')
                else:
                    flag.append('False')
            elif '<=' in option:
                exceptList = re.split('<=', option)
                if exceptList[0] <= exceptList[1]:
                    flag.append('True')
                else:
                    flag.append('False')
            elif '!!' in option:
                exceptList = re.split('!!', option)
                if exceptList[0] is not None:
                    flag.append('True')
                else:
                    flag.append('False')
            else:
                flag.append('False')
        if 'False' in flag:
            return False
        else:
            return True
    except Exception as e:
        raise e



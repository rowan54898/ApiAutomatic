# -*- coding:utf-8 -*-
import json

import requests


def request_process(url, request_method, request_header, request_content):
    """
    封装请求方法
    :param url: 请求接口
    :param request_method: post/get
    :param request_header: 一般是{"Content-Type": "application/json", "Authorization": token}
    :param request_content: 请求体
    :return: 返回执行结果或者异常
    """
    if request_method == 'get':
        try:
            r = requests.get(url, params=request_content, headers=request_header)
        except Exception as e:
            r = None
        return r
    elif request_method == 'post':
        try:
            if isinstance(request_content, dict):
                r = requests.post(url, data=json.dumps(request_content), headers=request_header)
            elif isinstance(request_content, str):
                r = requests.post(url, data=request_content, headers=request_header)
            elif isinstance(request_content, list):
                r = requests.post(url, data=json.dumps(request_content), headers=request_header)
            else:
                raise ValueError
        except ValueError as e:
            r = None
        except Exception as e:
            r = None
        return r
    elif request_method == 'delete':
        try:
            r = requests.delete(url, headers=request_header)
        except Exception as e:
            r = None
        return r

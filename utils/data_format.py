# -*- coding:utf-8 -*-
import json


def data_format(value):
    """格式化数据，全部把value数据，搞成json对象"""
    if type(value) is str:
        if value.startswith('{'):
            if 'null' in value or 'false' in value or 'true' in value:
                new_value = json.loads(value)
            else:
                new_value = eval(value)
        elif value.startswith('['):
            if 'null' in value or 'false' in value or 'true' in value:
                new_value = json.loads(value)
            else:
                new_value = eval(value)
        elif len(value) > 0:
            new_value = value
        else:
            new_value = None
    else:
        new_value = None
    return new_value

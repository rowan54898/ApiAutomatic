#  -*-  coding:utf-8 -*-


"""
引入注册参数，在命令行传参,便于以后可以和headless无界面Chrome浏览器启动一起，集成Git、Jenkins，在linux上执行。
mac 上执行命令：(python run.py -p xxxx -c xxxx)
如：python run.py -p ./config/ksb_login_info.yaml -c ./testcase/接口自动化测试用例模板.xlsx

windows上执行命令为：.\run.py -p .\config\product_login_info.yaml -c .\testcase\自动化测试用例yuruifang.xlsx
"""
import argparse

parser = argparse.ArgumentParser(description='启动测试用例的ip地址和Excel')
parser.add_argument('-p', '--path', default='./config/ksb_login_info.yaml', help='path')
parser.add_argument('-c', '--case', default='./testcase/接口自动化测试用例模板.xlsx', help='caseName')
args = parser.parse_args()
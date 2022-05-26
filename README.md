# Sushine—Automatic-Test整体介绍

## 一、环境&目录规划

### 启动参数

#### 在run.py中parser变量中添加启动参数

"""

--path 登陆路径，默认：‘./config/jituan_login_info.yaml’

--case 测试用例，默认：‘./testcase/接口自动化测试用例模板.xlsx’

"""

biz.login.get_token 根据 --path 参数获取config.{}.yaml

untils.testcase_handler.workbook 根据 --case 参数获取testcase.{}.xlsx

### 目录规划

“”“

biz --业务包

config --配置文件目录

learn --官方文档学习

log --日志

report --测试报告

testcase --测试用例

untils --公共组件，封装方法等

run.py --执行文件

“”“

## 二、case相关

### 测试用例模板

**1、模板基本信息**

’‘’ 用例编号不要重复，类似 A-001这种写法即可

URI无需填写，已经从config/{}.yaml文件中获取

Header无需填写，目前写死格式为Application/json格式，token从biz/login.py中get_token获取 ‘’‘

**2、assert写法：**

‘’‘ 左 符号 右 左：实际返回值中取得值 右：预期 ’‘’

**3、断言符号：**

‘’‘
'==', '!=', '>', '>=', '<', '<=', '!!'   
目前仅支持多条件判断，多层结构还不支持。未来引入关键字，更加方便使用 ’‘’

**4、关键字引用：**

‘’‘ 在API和request中使用（未来会支持在断言中使用），详细关键字见utils.keywords.py文件中，后续会出一份关键字使用文档 基本格式为：@ResponseDependMulti('A-002','
industryNo','data') @PayloadDepend('A-001','industryNam')
（）内第一标记位是用例编号，第二标记位是key，第三标记位是condition条件 ‘’‘

## 三、封装

1、excel数据读写 utils/testcase_handler.py 2、关键字库 utils/keywords.py 3、关键字解析 utils/keyword_parsing.py 4、请求方法post、get封装
utils/request_process.py 5、断言处理 utils/data_process.py

## 各种命令

命令行启动 python run.py -p xxx -c xxxx eg：python run.py -p .\config\jituan_login_info.yaml -c .\testcase\接口自动化测试用例模板.xlsx
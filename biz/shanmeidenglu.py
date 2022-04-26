# -*- coding:utf-8 -*-
import json
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains


def get_track(distance):
    """位移轨迹封装
    目的：登陆滑块滑动放平缓
    通过 加速度计算公式算出为移动距离，再添加进入轨迹列表track里
    :param distance 滑块横向移动距离一般150px就够了，在调用该函数时，xxxx.get_track(150)
    """
    track = []
    current = 0
    mid = distance * 3 / 5
    t = 2
    v = 0
    while current < distance:
        if current < mid:  # 这里用mid将全程位移分成俩段，滑动太快，登陆接口容易校验不通过，所以在后半程需要放缓慢
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(move)
    return track


def get_token():
    """
    通过ui自动化获取页面接口全量信息，并且拿到接口的token
    :return:token 接口请求头中Authorization的值
    """

    caps = {
        'browserName': 'chrome',
        'loggingPrefs': {
            'browser': 'ALL',
            'driver': 'ALL',
            'performance': 'ALL',
        },
        'goog:chromeOptions': {
            'perfLoggingPrefs': {
                'enableNetwork': True,
            },
            'w3c': False,
        },
    }

    driver = webdriver.Chrome(desired_capabilities=caps)
    driver.get('http://168.168.10.106:81/userlogin.html')
    driver.find_element_by_xpath('//*[@id="App"]/div[1]/div[2]/div[1]/div[2]/div/input').send_keys('ADMIN')
    driver.find_element_by_xpath('//*[@id="App"]/div[1]/div[2]/div[1]/div[3]/div/input').send_keys('abcd@1234')
    element = driver.find_element('xpath', '//*[@id="slider"]/div/div[2]')
    ActionChains(driver).click_and_hold(on_element=element).perform()
    sleep(0.5)
    ActionChains(driver).move_to_element_with_offset(element, 200, 0).perform()
    tracks = get_track(150)
    for track in tracks:
        ActionChains(driver).move_by_offset(track, 0).perform()
    sleep(0.2)
    ActionChains(driver).release().perform()
    sleep(0.5)
    driver.find_element_by_xpath('//*[@id="App"]/div[1]/div[2]/button').click()
    sleep(2)
    request_log = driver.get_log('performance')

    token = ""
    for i in range(len(request_log)):
        message = json.loads(request_log[i]['message'])
        message = message['message']['params']
        # .get() 方式获取是了避免字段不存在时报错
        request = message.get('request')
        if request is None:
            continue

        url = request.get('url')
        if (url == "http://168.168.10.106:81/rest/system/menu/listIndexForMk"):
            # 得到requestId
            token += message['request']['headers']['Authorization']
            print(token)
            break
    sleep(3)
    driver.quit()
    return token


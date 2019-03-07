# /usr/bin/python
# encoding: utf-8

import time
from selenium import webdriver


def login(username, password):
    # url = 'https://passport.cnblogs.com/user/signin'  # 使用这个url登录成功后定位到园子
    url = 'http://192.168.1.68/dvwa/login.php'  # url中指明定位到博客园首页

    driver = webdriver.Firefox(executable_path='C:\Program Files (x86)\Mozilla Firefox\\firefox.exe')
    driver.get(url)
    # print driver.title
    name_input = driver.find_element_by_id('username')  # 找到用户名的框框
    pass_input = driver.find_element_by_id('password')  # 找到输入密码的框框
    login_button = driver.find_element_by_id('Login')  # 找到登录按钮

    name_input.clear()
    name_input.send_keys(username)  # 填写用户名
    time.sleep(0.2)
    pass_input.clear()
    pass_input.send_keys(password)  # 填写密码
    time.sleep(0.2)
    login_button.click()            # 点击登录

    time.sleep(0.2)
    print(driver.get_cookies())

    time.sleep(2)
    print(driver.title)

    driver.close()

if __name__ == "__main__":
    user = "admin"
    pw = "password"
    login(user, pw)
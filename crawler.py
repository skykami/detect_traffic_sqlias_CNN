# -*- coding:utf-8 -*-

import subprocess
import sqlite3
import win32crypt

import requests
from bs4 import BeautifulSoup

from random import choice
import random
import time

SOUR_COOKIE_FILENAME = r'C:\Users\la\AppData\Local\Google\Chrome\User Data\Default\Cookies'
DIST_COOKIE_FILENAME = '.\python-chrome-cookies'
server = 'http://192.168.1.68/dvwa/'
urls = []

def get_chrome_cookies(url):
    subprocess.call(['copy', SOUR_COOKIE_FILENAME, DIST_COOKIE_FILENAME], shell=True)
    conn = sqlite3.connect(".\python-chrome-cookies")
    ret_dict = {}
    for row in conn.execute("SELECT host_key, name, path, value, encrypted_value FROM cookies"):
        # if row[0] not in url:
        if row[0] != url:
            continue
        #print(row[0])
        ret = win32crypt.CryptUnprotectData(row[4], None, None, None, 0)
        ret_dict[row[1]] = ret[1].decode()
    conn.close()
    subprocess.call(['del', '.\python-chrome-cookies'], shell=True)
    return ret_dict

DOMAIN_NAME = '192.168.1.68'
get_url = r'http://192.168.1.68/dvwa/index.php'

cookie = get_chrome_cookies(DOMAIN_NAME)

response = requests.get(get_url, cookies=cookie)
html = response.text
div_bf = BeautifulSoup(html,'lxml')
div = div_bf.find_all('div', id = 'main_menu_padded')
a_bf = BeautifulSoup(str(div[0]),'lxml')
a = a_bf.find_all('a')
for each in a:
    new_arl = server + each.get('href')
    if (new_arl not in urls):
        urls.append(new_arl)

urls.append("http://192.168.1.68/dvwa/instructions.php?doc=readme")
urls.append("http://192.168.1.68/dvwa/instructions.php?doc=PDF")
urls.append("http://192.168.1.68/dvwa/instructions.php?doc=changelog")
urls.append("http://192.168.1.68/dvwa/instructions.php?doc=copying")
urls.append("http://192.168.1.68/dvwa/instructions.php?doc=PHPIDS-license")
urls.append("http://192.168.1.68/dvwa/vulnerabilities/fi/?page=file1.php")
urls.append("http://192.168.1.68/dvwa/vulnerabilities/fi/?page=file2.php")
urls.append("http://192.168.1.68/dvwa/vulnerabilities/fi/?page=file3.php")




count = 1
while count < 10000:
    count = count + 1
    random_url = choice(urls)
    req = requests.get(url=random_url, cookies=cookie)
    time.sleep(random.uniform(0.0,0.5))
    print(count)


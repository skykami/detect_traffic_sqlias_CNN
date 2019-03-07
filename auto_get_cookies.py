# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup


url = r'http://192.168.1.68/dvwa/login.php'
get_url = r'http://192.168.1.68/dvwa/index.php'
headers={"Accept-Encoding" :  "gzip, deflate"
,"Accept-Language" : "en-US,en;q=0.5"
,"Connection" : "keep-alive"
,"Content-Length" : "88"
,"Content-Type" : "application/x-www-form-urlencoded"
,"Host" : "192.168.1.68"
,"Referer" : "http://192.168.1.68/dvwa/login.php?Login=Login&username=admin&password=password"
,"Upgrade-Insecure-Requests" : "1"}
# Cookie
# security=impossible; PHPSESSID…0f3b86723971ab031088c13015f19
response = requests.get(get_url,data = {"username":"admin","password":"password","Login":"Login"})
html = response.text
div_bf = BeautifulSoup(html,'lxml')
print(div_bf)




#
# s = requests.Session()
# # a='http://192.168.1.68/dvwa/login.php?Login=Login&username=admin&password=password'
# # b='http://192.168.1.68/dvwa/login.php?Login=Login&username=admin&password=password'
# login_page=s.post(url,headers=headers)
# print(login_page.text)
# html = s.get(get_url)
#print(html.text)
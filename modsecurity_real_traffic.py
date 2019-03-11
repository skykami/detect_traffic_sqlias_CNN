# encoding: utf-8
#
import requests

FILE_PATH="./data/real_normal.txt"

data_sum = 0
sensitive_data_sum = 0


with open(FILE_PATH) as f:
    str = f.readlines()
    for payload in str:
        data_sum += 1
        post_data = {'username': payload, 'password': '', 'login': 'Login'}

        r = requests.post("http://192.168.1.68/login.php", data=post_data)

        if "Forbidden" in r.text:
            sensitive_data_sum += 1
        # else:
            print(data_sum)
            print(payload)

print("data_sum is ", data_sum)
print("sensitive_data_sum is ", sensitive_data_sum)
print(float(sensitive_data_sum)/float(data_sum))
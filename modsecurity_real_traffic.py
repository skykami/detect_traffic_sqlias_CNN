# encoding: utf-8
#
import requests

SQL_FILE_PATH="/home/kami/CNN-SQL-master/data/test_xss.txt"
XSS_FILE_PATH="/home/kami/CNN-SQL-master/data/wordlist-huge.txt"
NORMAL_FILE_PATH="/home/kami/CNN-SQL-master/data/test_normal.txt"

sql_data_sum = 0
sql_sensitive_data_sum = 0
normal_data_sum = 0
normal_sensitive_data_sum = 0


with open(XSS_FILE_PATH) as f:
    str = f.readlines()
    for payload in str:
        sql_data_sum += 1
        post_data = {'username': payload, 'password': '', 'login': 'Login'}

        r = requests.post("http://192.168.1.68/login.php", data=post_data)

        if "Forbidden" in r.text:
            sql_sensitive_data_sum += 1
        else:
            print(sql_data_sum)
            print(payload)

# with open(NORMAL_FILE_PATH) as f:
#     str = f.readlines()
#     for payload in str:
#         normal_data_sum += 1
#         post_data = {'username': payload, 'password': '', 'login': 'Login'}
#
#         r = requests.post("http://192.168.1.68/login.php", data=post_data)
#
#         if "Forbidden" in r.text:
#             normal_sensitive_data_sum += 1

print("sql_data_sum is ", sql_data_sum)
print("sql_sensitive_data_sum is ", sql_sensitive_data_sum)
print("检测率为：", float(sql_sensitive_data_sum)/float(sql_data_sum))

# print("normal_data_sum is ", normal_data_sum)
# print("sensitive_data_sum is ", normal_sensitive_data_sum)
# print("误报率为：", float(normal_sensitive_data_sum)/float(normal_data_sum))
#
# print("acc 为：", float(sql_sensitive_data_sum + normal_data_sum - normal_sensitive_data_sum)/float(sql_data_sum + normal_data_sum))
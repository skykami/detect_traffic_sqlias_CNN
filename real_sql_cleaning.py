#encoding:utf-8

import os

FILE_PATH="./data/real_sql.txt"

str_new = ""

with open(FILE_PATH) as f:
    str = f.readlines()
    for i in str:
        if i != '/dvwa/login.php\n':
            str_new = str_new + i

with open(FILE_PATH, 'w') as f:
    f.write(str_new)

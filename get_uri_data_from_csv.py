#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv
import ipaddress


#init_length = 49
current_row = 0

path = './bro_logs/http.csv'

sql_file = './data/real_sql.txt'
normal_file = './data/real_normal.txt'


#逐行写入数据（特征+标记）
def save_data(text,filename):
    with open(filename,'a') as f:
      f.write(text+"\n")


with open(path) as f:
  f_csv = csv.reader(f)
  for row in f_csv:
    current_row = current_row + 1
    #add pcap panel according to the time_stamp
    if row[2] == '192.168.1.82' and row[9] != '/dvwa/login.php':
      save_data(row[9],sql_file)
    else:
      save_data(row[9], normal_file)


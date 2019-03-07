#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv

CSV_FILE_PATH = './bro_logs/http.csv'

str_new = ""

with open(CSV_FILE_PATH) as f:
    str=f.readlines()
    for i in str:
        if i!='\n':
            str_new=str_new+i


with open(CSV_FILE_PATH,'w') as f:
    f.write(str_new)
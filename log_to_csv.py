#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv

LOG_FILE_PATH = './bro_logs/http.log'
CSV_FILE_PATH = './bro_logs/http.csv'

rows = []

with open(LOG_FILE_PATH) as log_file:
    log_file_content = csv.reader(log_file, delimiter='\x09')
    for row in log_file_content:
        rows.append(row)

    with open(CSV_FILE_PATH, mode='w') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(rows)


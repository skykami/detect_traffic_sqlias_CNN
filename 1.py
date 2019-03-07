#coding=utf-8
import sys

if __name__ == '__main__':
    n = input()
    result = 0
    list_n = []
    for i in n:
        if i not in list_n:
            result = result +1
        list_n.append(i)

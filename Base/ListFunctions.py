# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


'''
count different time intervals of data that is in list format
'''
def Counter(lis):
    dic_cnt = {}
    for element in lis:
        int_element = int(element)
        if int_element in dic_cnt:
            dic_cnt[int_element] += 1
        else:
            dic_cnt[int_element] = 1
    return dic_cnt
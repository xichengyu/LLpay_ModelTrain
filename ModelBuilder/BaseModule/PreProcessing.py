# coding=utf-8

import sys
from pandas import Series, DataFrame
import pandas
import math
import numpy as np
import hashlib
import binascii
import time
from scipy.stats import pearsonr


def delete_sample(X, threshold=0.5):
    temp = []
    try:
        for idx in range(X.shape[0]):
            row = X[idx, :]
            percentile = 1 - sum(np.isnan(row)) / float(len(row))
            if percentile >= threshold:
                temp.append(row)
    except ValueError:
        pass
    return np.array(temp)


'''transform unixtime to hour, both 'ms' and 's' '''


def Unixtime2Hour(lis):
    return [time.strftime('%H', time.localtime(int(x))) if len(x) == 10
            else time.strftime('%H', time.localtime((int(x) + 500) / 1000)) for x in lis]


'''split area to detailed province and city'''


def SplitArea(lis, delim=','):
    l = len(lis)
    prov, city = [], []
    for i in range(l):
        tmp = lis[i].split(delim)
        if len(tmp) == 2:
            prov.append(tmp[0])
            city.append(tmp[1])
        elif len(tmp) == 1:
            prov.append(tmp[0])
            city.append('')
        else:
            prov.append('')
            city.append('')
    return prov, city


'''transform digital str to int'''


def Str2Int(lis):  # transform digital str to int
    def func(x):
        if x == "" or x == "null":
            return
        else:
            return float(x)
    return map(func, lis)
    # return [int(x) for x in lis]


'''transform str to int using hashlib.md5'''


def Str2Md5(lis):  # tansform str to int
    '''
    for i in range(len(lis)):
        try:
            lis[i] = int(binascii.hexlify(hashlib.md5(lis[i]).hexdigest())) % int(10e6)
        except:
            print lis[i]
            raise IOError
    return lis
    '''
    return [int(binascii.hexlify(hashlib.md5(x).hexdigest())) % int(10e6) for x in lis]


'''max_min normalization method'''


def max_min(nparray_data):  # normalization: max_min method
    lower_upper_list = []
    for idx in range(nparray_data.shape[-1]):
        tmp = nparray_data[:, idx]
        upper = max(tmp)
        lower = min(tmp)
        if upper != lower:
            tmp = (tmp - lower) / (upper - lower)
        elif upper != 0:
            tmp /= upper
        nparray_data[:, idx] = tmp
        lower_upper_list.append((lower, upper))
    return nparray_data, lower_upper_list


'''dummy coding'''


def DummyCoding(dic, dum_coding_fields):
    keys = dic.keys()
    for key in keys:
        if key in dum_coding_fields:
            tmp = set(dic[key])
            index = 0
            for ele in tmp:
                index += 1
                if index == len(tmp):
                    continue
                new_key = key + "_" + str(ele)
                dic[new_key] = []
                for val in dic[key]:
                    if val == ele:
                        dic[new_key].append('1')
                    else:
                        dic[new_key].append('0')
            dic.pop(key)
    return dic


def __dumcoding(dic, dum_coding_fields):
    keys = dic.keys()
    for key in keys:
        if key in dum_coding_fields:
            tmp = set(dic[key])
            # index=0
            for ele in tmp:
                # index += 1
                # if index==len(tmp):
                #    continue
                new_key = key + "_" + ele
                dic[new_key] = []
                for val in dic[key]:
                    if val == ele:
                        dic[new_key].append('1')
                    else:
                        dic[new_key].append('0')
            dic.pop(key)
    return dic
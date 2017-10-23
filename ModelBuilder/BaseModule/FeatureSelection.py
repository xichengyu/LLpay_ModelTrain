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
reload(sys)
sys.setdefaultencoding('utf-8')


'''merge factors'''


def __mergefeature(dataframe):
    columns = dataframe.columns
    init = len(columns)
    dic = {}
    for i in xrange(init):
        if columns[i] == "clicked":
            continue
        dic[columns[i]] = [min(dataframe[columns[i]]), max(dataframe[columns[i]])]
        for j in xrange(i + 1, init):
            if columns[j] == "clicked":
                continue
            new_key = columns[i] + "_" + columns[j]
            dataframe[new_key] = dataframe[columns[i]] + dataframe[columns[j]]
            Max = max(dataframe[new_key])
            Min = min(dataframe[new_key])
            dic[new_key] = [Min, Max]
            dataframe[new_key] = (dataframe[new_key] - Min) / (Max - Min) if Max != Min else dataframe[new_key] / Max
    return dataframe, dic


def MergeFeature(dataframe):
    init = len(dataframe.columns)
    for i in xrange(init):
        for j in xrange(i + 1, init):
            new_key = dataframe.columns[i] + "_" + dataframe.columns[j]
            dataframe[new_key] = dataframe[dataframe.columns[i]] + dataframe[dataframe.columns[j]]
    return dataframe


'''select factor'''


def __selectfeature(dataframe):
    # var selection
    data = dataframe.apply(np.var, axis=0)
    for ind in data.index:
        if data[ind] == 0:
            dataframe = dataframe.drop(ind, axis=1)
    # pearsonr selection
    keys = dataframe.columns
    for s in keys:
        args = pearsonr(dataframe[s], dataframe['clicked'])
        # print "Pearson test: ", s, args
        if args[1] > 0.5:
            dataframe = dataframe.drop(s, axis=1)
    return dataframe


'''variance selection'''


def VarSelection(dataframe):
    data = dataframe.apply(np.var, axis=0)
    for ind in data.index:
        if data[ind] == 0:
            # print ('\033[1;35;40m')
            # print "Droped factor: %s"%(ind)
            # print ('\033[0m')
            dataframe = dataframe.drop(ind, axis=1)
    return dataframe


'''pearsonr selection'''


def PearsonrSelection(dataframe, dependent_variale, t=0.5):
    keys = dataframe.columns
    for s in keys:
        args = pearsonr(dataframe[s], dependent_variale)
        if args[1] > t:
            dataframe = dataframe.drop(s, axis=1)
    return dataframe


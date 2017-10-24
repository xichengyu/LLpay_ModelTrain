# coding=utf-8

import os
import numpy as np
# import traceback
from sklearn.externals import joblib
import sys
sys.path.append("../")
from read_cnf import get_conf_info
from print_switch import prints

def read_local_data(localpath, default=-1.0):
    """
    read data from local place
    :param default: default value used to replace non_type value
    :param localpath: the path of data
    :return: the new numpy array in which None_type values are replaced with -1.0
    """
    files = os.listdir(localpath)
    res = []
    for file in files:
        temp = open(localpath + "/%s" % file).readlines()
        prints(type(temp))
        prints(temp[0].split(), len(temp[0].split()))
        for line in temp:
            res.append(line.split())
    prints("total data: ", len(res))
    res = np.array(res)

    for idx in range(res.shape[-1]):        # replace non_type value with -1.0
        res[:, idx][np.where(res[:, idx] == '\\N')[0]] = default
    prints(res[0])
    return res


def load_local_data(localpath, default=-1.0):
    """
    load joblib format data from loacal place
    :param localpath:
    :param default:
    :return:
    """
    res = np.array(joblib.load(localpath))
    for idx in range(res.shape[-1]):        # replace non_type value with -1.0
        res[:, idx][np.where((res[:, idx] == '') | (res[:, idx] == None))[0]] = default
    prints(res[0])
    return res


if __name__ == "__main__":
    localpath = "../../data/raw_data.dt"
    res = read_local_data(localpath)

    prints(res.shape, res[0])

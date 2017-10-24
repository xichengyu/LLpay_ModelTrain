# coding=utf-8

import os
import numpy as np
# import traceback
from sklearn.externals import joblib
import sys
sys.path.append("../")
from read_cnf import get_conf_info


def print_info(*args, if_print=False):
    """
    determine if log info printed
    :param string:
    :param if_print: control switch
    :return:
    """
    if if_print:
        print(*args)


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
        print_info(type(temp))
        print_info(temp[0].split(), len(temp[0].split()))
        for line in temp:
            res.append(line.split())
    print_info("total data: ", len(res))
    res = np.array(res)

    for idx in range(res.shape[-1]):        # replace non_type value with -1.0
        res[:, idx][np.where(res[:, idx] == '\\N')[0]] = default
    print_info(res[0])
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
    print_info(res[0])
    return res


def delete_str_column(nparray):
    """
    delete columns whose type is string
    :param nparray:
    :return: the new numpy array
    """
    columns = [x.strip() for x in open("%s" % get_conf_info()["column_name"]).readlines()]
    fnew = open("new_column_name.txt", "w")
    fdrop = open("dropped_column_name.txt", "w")
    new_nparray = np.array([[]]*nparray.shape[0])
    for idx in range(nparray.shape[-1]):
        try:
            new_nparray = np.column_stack((new_nparray, nparray[:, idx].astype(float)))
            if idx < nparray.shape[-1]-1:       # nparray has one more column named "label"
                fnew.write(columns[idx] + "\n")
        except ValueError:
            print_info(columns[idx], nparray[:, idx])
            fdrop.write(columns[idx] + "\n")
            # traceback.print_exc()
            continue
    fnew.close()
    fdrop.close()
    return new_nparray


if __name__ == "__main__":
    localpath = "../data_lianlian"
    res = read_local_data(localpath)
    new_nparray = delete_str_column(res)

    print_info(new_nparray.shape, new_nparray[0])

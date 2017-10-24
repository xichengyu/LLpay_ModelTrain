# coding=utf-8

from __future__ import absolute_import, division, print_function

# import itertools
import logging
import sys
# import random
# import re
# import functools
# from string import Template
import numpy as np
# import pandas as pd
from sklearn.externals import joblib
sys.path.append("../")
from read_cnf import get_conf_info
from print_switch import prints


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='[%Y-%m-%d %H:%M:%S]', filename='../hive.log', filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def fetch_from_hive(sql):
    """
    fetch data from hive
    :param sql:
    :return: nparray data
    """
    if not isinstance(sql, str):
        raise TypeError('sql must be type str, got %s' % type(sql))
    from pyhive import hive
    from TCLIService.ttypes import TOperationState
    cursor = hive.connect('HZ2-BG-1601-P018').cursor()
    cursor.execute(sql, async=True)
    status = cursor.poll().operationState
    while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):
        logs = cursor.fetch_logs()
        for message in logs:
            logging.info(message)
        status = cursor.poll().operationState
    return cursor.fetchall()


def detect_str_column(nparray):
    """
    detect columns whose type is string
    :param nparray:
    :return: the new numpy array
    """
    columns = [x.strip() for x in open("%s" % get_conf_info()["column_name"]).readlines()]
    fnew = open("../../conf/new_column_name.txt", "w")
    fdrop = open("../../conf/dropped_column_name.txt", "w")
    new_nparray = np.array([[]]*nparray.shape[0])
    for idx in range(nparray.shape[-1]):
        try:
            new_nparray = np.column_stack((new_nparray, nparray[:, idx].astype(float)))
        except ValueError:
            prints(columns[idx], nparray[:, idx])
            fdrop.write(columns[idx] + "\n")
            # traceback.print_exc()
            continue
    fnew.close()
    fdrop.close()
    return new_nparray


if __name__ == "__main__":

    test_sql = "select * from %s" % get_conf_info()["table"]

    data_zz_iv = detect_str_column(fetch_from_hive(test_sql))

    joblib.dump(data_zz_iv, "%s" % get_conf_info()["raw_data"])
    print(np.array(data_zz_iv).shape)

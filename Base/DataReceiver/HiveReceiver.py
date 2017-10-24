# coding=utf-8

from __future__ import absolute_import, division, print_function

# import itertools
import logging
# import os
# import random
# import re
# import functools
# from string import Template
import numpy as np
# import pandas as pd
from sklearn.externals import joblib


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='[%Y-%m-%d %H:%M:%S]', filename='hive.log', filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def fetch_from_hive(sql):
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


if __name__ == "__main__":

    test_sql = "select * from dbmodel.data_xicy_fullstep_sample"

    data_zz_iv = fetch_from_hive(test_sql)

    joblib.dump(data_zz_iv, "raw_data.dt")
    print(np.array(data_zz_iv).shape)

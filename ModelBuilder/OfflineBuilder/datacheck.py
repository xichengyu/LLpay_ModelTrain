# coding=utf-8

import sys
from pandas import DataFrame
sys.path.append('../BaseModule')
sys.path.append("../../Base/DataReceiver")
sys.path.append("../../Base")
# import PreProcessing as pp
import LocalReceiver as lr
# import DataSampling as ds
# import traceback
from read_cnf import get_conf_info
from pandas import DataFrame
import numpy as np
from collections import Counter

if __name__ == '__main__':

    conf_info = get_conf_info()
    raw_data = lr.load_local_data(conf_info["raw_data"])  # get original data
    print(DataFrame(raw_data))

    percentile = []
    for idx in range(raw_data.shape[0]):
        column = raw_data[idx, :]
        percentile.append(1-sum(np.isnan(column))/float(len(column)))

    print(percentile)

    cnt_dict = {}
    for item in percentile:
        for threshold in [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]:
            if item <= threshold:
                cnt_dict[threshold] = cnt_dict.get(threshold, 0) + 1

    print(cnt_dict)

# coding=utf-8

import sys
from pandas import DataFrame
sys.path.append('../BaseModule')
sys.path.append("../../DataReceiver")
sys.path.append("../../Base")
import PreProcessing as pp
import LocalReceiver as lr
import MongoReceiver
import DataSampling as ds
import traceback
from read_cnf import get_conf_info
from pandas import DataFrame


if __name__ == '__main__':

    conf_info = get_conf_info()
    raw_data = lr.load_local_data(conf_info["raw_data"])  # get original data
    print(DataFrame(raw_data))

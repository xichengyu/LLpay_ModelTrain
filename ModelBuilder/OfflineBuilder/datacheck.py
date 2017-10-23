# coding=utf-8

import sys
from pandas import DataFrame
sys.path.append('../BaseModule')
sys.path.append("../../DataReceiver")
import PreProcessing as pp
import LocalReceiver as lr
import MongoReceiver
import DataSampling as ds
reload(sys)
sys.setdefaultencoding('utf-8')
import traceback


data_src = 'local'
data_path = "../../data/fangdichan.csv"

delim = ";"
target_fields = ['wcType', 'unixTime', 'networkMode', 'area', 'adxCode', 'gender', 'price', 'appName', 'mobileOs', 'ip',
                 'wcAcId', 'wcOrgBidPrice', 'appMediaCat', 'clicked']
dum_coding_fields = ["unixTime", "networkMode", "mobileOs", "appMediaCat"]


def get_origin_data(data_src, data_path, delim, target_fields):
    train_data = {}
    test_data = []
    threshold = 1
    try:
        if data_src == "local":

            # dic_exp, dic_clc = lr.GetOriginData2(data_path, delim, target_fields)  # get original data
            dic_exp, dic_clc = lr.GetOriginData2(data_path, delim)  # get original data

            dic_exp['unixTime'] = pp.Unixtime2Hour(dic_exp['unixTime'])
            dic_clc['unixTime'] = pp.Unixtime2Hour(dic_clc['unixTime'])

            print 'exposure: ', len(dic_exp['unixTime']), '*'*30
            for k, v in dic_exp.items():
                if len(set(v)) > threshold:
                    print '%s: ' % k, len(set(v))

            print 'click: ', len(dic_clc['unixTime']), '*'*30
            for k, v in dic_clc.items():
                if len(set(v)) > threshold:
                    print '%s: ' % k, len(set(v))

            dic_merge = ds.merge_data(dic_exp, dic_clc, 'up')
            print 'merged: ', len(dic_merge['unixTime']), '*'*30
            for k, v in dic_merge.items():
                if len(set(v)) > threshold:
                    print '%s: ' % k, len(set(v))

        elif data_src == "mongo":
            mr = MongoReceiver.Receiver(10001)
            train_data = mr.receiver('pCTR', 'wuhu', target_fields)
    except:
        traceback.print_exc()
        pass
    return train_data, test_data


if __name__ == '__main__':

    train_data, test_data_list = get_origin_data('local', data_path, delim, target_fields)
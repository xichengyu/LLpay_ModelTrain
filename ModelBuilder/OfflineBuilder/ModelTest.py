# coding=utf-8

import sys
from pandas import DataFrame
sys.path.append('../BaseModule')
sys.path.append("../../Base/DataReceiver")
sys.path.append("../../Base/")
from print_switch import prints
import PreProcessing as pp
import FeatureSelection as fs
import DataSampling as ds
import ModelEvaluationTool as met
from sklearn.externals import joblib
from sklearn.metrics import auc
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import json
import traceback
import ModelTrain
# from matplotlib import pylab as plb
import numpy as np
from LocalReceiver import load_local_data


data_src = 'local'
delim = ";"
# target_fields = ['wcType', 'unixTime', 'networkMode', 'area', 'adxCode', 'gender', 'price', 'appName', 'mobileOs',
#                  'ip', 'wcAcId', 'wcOrgBidPrice', 'appMediaCat', 'clicked']
target_fields = ['unixTime', 'networkMode', 'area', 'adxCode', 'price', 'mobileOs',
                 'wcAcId', 'wcOrgBidPrice', 'appMediaCat', 'clicked', 'wcAeId', 'wcAdId', 'wcBidPrice']
# dum_coding_fields = ["unixTime", "networkMode", "mobileOs", "appMediaCat"]
dum_coding_fields = ["unixTime", "networkMode", "mobileOs"]


def normalize_input_data(json_fmt, keys, bounds, merge_bounds, dum_coding_fields):
    # print "input_json:\n", json_fmt
    dic = {}
    try:
        if json_fmt == "":
            return "Empty Input!!"
        '''load json'''
        origin_keys = json.loads(json_fmt, encoding="utf-8")
        print("origin_keys:\n", len(origin_keys), len(origin_keys['unixTime']))

        '''verify data format'''
        if not isinstance(origin_keys['unixTime'], list):  # verify data format
            return "Wrong Data Format!!"

        origin_len = len(origin_keys['unixTime'])

        '''unixtime to hour'''
        origin_keys['unixTime'] = pp.Unixtime2Hour(origin_keys['unixTime'])
        print("unixtime to hour:\n", len(origin_keys), len(origin_keys['unixTime']))

        '''dummy coding
        if origin_len == 1:
            tmp_keys = origin_keys.keys()
            for key in tmp_keys:
                if key in dum_coding_fields:
                    new_key = key + "_" + str(origin_keys[key][0])
                    origin_keys[new_key] = "1"
        else:
            origin_keys = pp.__dumcoding(origin_keys, dum_coding_fields)
        print "dummy coding:\n", len(origin_keys), len(origin_keys['unixTime'])
        '''
        '''string to md5 & int'''
        for k in origin_keys:
            try:
                float(origin_keys[k][0])
                origin_keys[k] = pp.Str2Int(origin_keys[k])
            except:
                origin_keys[k] = pp.Str2Md5(origin_keys[k])
                continue
        print("string to md5 & int:\n", len(origin_keys), len(origin_keys['unixTime']))

        '''max_min input data'''
        for key in origin_keys:
            if key in bounds:
                origin_keys[key] = [abs(x - bounds[key][0]) / (bounds[key][1] - bounds[key][0]) for x in origin_keys[key]]
        print("max_min:\n", len(origin_keys), len(origin_keys['unixTime']))

        '''merge features'''
        origin_keys = DataFrame(origin_keys).sort_index(axis=1, ascending=True)
        origin_keys = fs.MergeFeature(origin_keys)
        print("merge:\n", len(origin_keys.columns), len(origin_keys['unixTime']))

        '''return final dict'''
        for key in keys:
            dic[key] = [0] * origin_len
            if key in origin_keys.columns:
                dic[key] = abs(origin_keys[key] - merge_bounds[key][0]) / (merge_bounds[key][1] - merge_bounds[key][0])
        # print DataFrame(dic)
    except:
        traceback.print_exc()
        pass
    return DataFrame(dic)


def get_train_test_data(data_src, data_path, delim, target_fields):
    train_data = []
    test_data = []
    try:
        if data_src == "local":
            print("getting Original data...")

            raw_data = load_local_data(data_path)  # get original data

            print(DataFrame(raw_data))

            '''create train_data, test_data'''
            randsamp = ds.RandSamp()
            randsamp.MULTIPLE = 1
            randsamp.TRAIN_PERCENTILE = 0.7
            train_data, test_data = randsamp.random_sampling(raw_data)

        elif data_src == "hive":
            pass

    except:
        traceback.print_exc()
        pass
    return train_data, test_data


if __name__ == '__main__':

    preprocessing_flag = False

    data_path = "../../data/raw_data.dt"

    algorithm = "RF"      # RF, GBDT, LR

    total_partition_n = [1]
    train_partition_n = [1]

    # total_partition_n = [x * 1.0 for x in range(2, 21)]
    # train_partition_n = [x - 1.0 for x in total_partition_n]

    # total_partition_n = [10.0]*9 + [x * 1.0 for x in range(2, 21)]
    # train_partition_n = [x*1.0 for x in range(1, 10)] + [x - 1.0 for x in [x * 1.0 for x in range(2, 21)]]
    '''
    train_data_list, test_data_list = get_train_test_data(data_src=data_src, data_path=data_path, delim=delim,
                                                          target_fields=target_fields, sampling_process='up',
                                                          percentage=0.7, train_partition_n=5, test_partition_n=1)

    print(len(train_data_list), len(test_data_list))
    for line in train_data_list:
        print(line.shape)

    '''
    try:
        for k, v in dict(zip(train_partition_n, total_partition_n)).items():

            train_data_list, test_data_list = get_train_test_data(data_src='local', data_path=data_path, delim=delim,
                                                                  target_fields=target_fields)

            sum_auc = 0.0
            for train_data in train_data_list:

                if 1:
                    ModelTrain.train_model(train_data, dum_coding_fields, algorithm, preprocessing_flag)

                ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                '''
                keys = joblib.load("../../conf/keys.cf")
                bounds = joblib.load("../../conf/feature_value_bounds.cf")
                merge_bounds = joblib.load("../../conf/merge_value_bounds.cf")
                dum_coding_fields = joblib.load('../../conf/dum_coding_fields.cf')
                dr_model = joblib.load('../../conf/dr_model.cf')
                input_test_features = [x for x in keys if x.find('_') == -1]
                print(input_test_features)
                '''
                model = joblib.load("../../conf/%s_model.jm" % algorithm.lower())

                target = []

                if 0:
                    '''
                    test_data = joblib.load("../../conf/test_data.dt")
                    target = [float(x) for x in joblib.load("../../conf/target.dt")]

                    test_keys = test_data.keys()
                    for k in test_keys:
                        test_data.pop(k) if k not in input_test_features else test_data
                    test_json = json.JSONEncoder().encode(test_data)
                    test_data = normalize_input_data(test_json, keys, bounds, merge_bounds, dum_coding_fields)
                    predict_y = model.predict(test_data)

                    met.ROC(algorithm, predict_y, target)
                    fpr, tpr, thresholds = roc_curve(target, predict_y)
                    print(fpr, tpr, thresholds)
                    print(roc_auc_score(target, predict_y))
                    '''
                    pass
                else:
                    for test_data in test_data_list:
                        target = test_data[:, 0]
                        test_data = np.delete(test_data, 0, axis=1)
                        '''
                        for k in test_keys:
                            test_data.pop(k) if k not in input_test_features else test_data

                        test_json = json.JSONEncoder().encode(test_data)
                        test_data = normalize_input_data(test_json, keys, bounds, merge_bounds, dum_coding_fields)
                        # test_data = dr_model.transform(np.array(test_data))
                        '''
                        predict_y = model.predict(test_data)

                        met.ROC(algorithm, predict_y, target)
                        fpr, tpr, thresholds = roc_curve(target, predict_y)
                        # plb.plot(fpr, tpr)
                        # print fpr, tpr, thresholds
                        print('roc_auc_score: ', roc_auc_score(target, predict_y))
                        print ('auc: ', auc(fpr, tpr))
                        sum_auc += auc(fpr, tpr)
                    # plb.savefig('%s' % algorithm)


    except:
        traceback.print_exc()
        pass


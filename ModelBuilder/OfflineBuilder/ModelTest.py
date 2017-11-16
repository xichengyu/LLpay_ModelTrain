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
import MissingValueStrategy as mvs
from sklearn.externals import joblib
from sklearn.metrics import auc
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import json
import traceback
import ModelTrain
# from matplotlib import pylab as plb
import numpy as np
import LocalReceiver as lr
from read_cnf import get_conf_info
from sklearn.ensemble import RandomForestRegressor


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


def get_train_test_data(data, target_fields):
    train_data = []
    test_data = []
    try:
        '''create train_data, test_data'''
        randsamp = ds.RandSamp()
        randsamp.MULTIPLE = 1
        randsamp.TRAIN_PERCENTILE = 0.8
        train_data, test_data = randsamp.random_sampling(data)

    except:
        traceback.print_exc()
        pass
    return train_data, test_data


if __name__ == '__main__':

    conf_info = get_conf_info()
    preprocessing_flag = True
    algorithm = "RF"      # RF, GBDT, LR
    strategies = ["mean", "median", "most_frequent"]    # different strategies for dealing with missing value
    # strategies = ["median"]
    run_times = 10
    y_idx = 0
    # tree_n = [60, 70, 80, 90, 100, 110, 120, 130, 140]
    tree_n = [60]
    # depth_n = [12, 13, 14, 15]
    depth_n = [10]
    job_n = 35

    train_partition_n = [1]
    test_partition_n = [1]

    prints("Getting Raw Data...")
    raw_data = lr.load_local_data(conf_info["raw_data"])  # get original data

    # prints("deleting Sample...")
    # raw_data = pp.delete_sample(raw_data)
    # prints(raw_data.shape)

    try:
        prints("Dealing Missing Value...")
        for strategy in strategies:
            # raw_data[np.isnan(raw_data)] = -1
            # new_data = raw_data
            new_data = mvs.fill_strategy(raw_data, strategy)
            prints(DataFrame(new_data))

            sum_auc = {}
            sum_ks = {}
            for i in range(run_times):

                prints("Generating Train Data & Test Data...")
                train_data_list, test_data_list = get_train_test_data(data=new_data, target_fields=target_fields)

                for train_data in train_data_list:

                    train_target = train_data[:, y_idx]
                    train_data = np.delete(train_data, y_idx, axis=1)

                    if 0:
                        ModelTrain.train_model(train_data, train_target, dum_coding_fields, algorithm, preprocessing_flag)

                    for tree in tree_n:
                        for depth in depth_n:

                            prints("Training Model...")
                            rf = RandomForestRegressor(n_estimators=tree, max_depth=depth, n_jobs=job_n)
                            rf.fit(train_data, train_target)
                            model = rf

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
                            # model = joblib.load("../../conf/%s_model.jm" % algorithm.lower())

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
                                prints("Testing Model...")
                                for test_data in test_data_list:
                                    test_target = test_data[:, 0]
                                    test_data = np.delete(test_data, 0, axis=1)

                                    if 0:
                                        prints(test_data.shape)
                                        ivs = joblib.load("../../conf/iv.cnf")
                                        temp = []
                                        for idx, iv in enumerate(ivs):
                                            if iv > 0.02:
                                                temp.append(test_data[:, idx])
                                        test_data = np.array(temp).T
                                        prints(test_data.shape)

                                    '''
                                    for k in test_keys:
                                        test_data.pop(k) if k not in input_test_features else test_data
            
                                    test_json = json.JSONEncoder().encode(test_data)
                                    test_data = normalize_input_data(test_json, keys, bounds, merge_bounds, dum_coding_fields)
                                    # test_data = dr_model.transform(np.array(test_data))
                                    '''
                                    predict_y = model.predict(test_data)

                                    thresholds = [x/100 for x in range(100)]

                                    ks_max = met.ROC(algorithm, strategy, predict_y, test_target,
                                                     conf_info["log_path"], tree, depth,thresholds=thresholds)
                                    fpr, tpr, thresholds = roc_curve(test_target, predict_y)
                                    # plb.plot(fpr, tpr)
                                    # print fpr, tpr, thresholds
                                    prints('roc_auc_score: ', roc_auc_score(test_target, predict_y))
                                    prints('auc: ', auc(fpr, tpr))

                                    sum_auc[(tree, depth)] = sum_auc.get((tree, depth), 0)+auc(fpr, tpr)
                                    sum_ks[(tree, depth)] = sum_ks.get((tree, depth), 0) + ks_max

                                    # plb.savefig('%s' % algorithm)

            for tree_depth, aucs in sum_auc.items():
                sum_auc[tree_depth] = aucs/run_times

            for tree_depth, kses in sum_ks.items():
                sum_ks[tree_depth] = kses/run_times

            fout = open(conf_info["log_path"], "a")
            fout.write(strategy+" avg_auc: "+str(sum_auc)+"\n")
            fout.write(strategy+" avg_ks: "+str(sum_ks)+"\n")
            fout.close()
            prints("avg_auc: ", sum_auc)
            prints("avg_ks: ", sum_ks)


    except:
        traceback.print_exc()
        pass


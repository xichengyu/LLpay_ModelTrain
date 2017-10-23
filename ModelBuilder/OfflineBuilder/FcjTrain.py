# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
reload(sys)
sys.path.append("../BaseModule")
sys.path.append("../../DataReceiver")
from pandas import DataFrame
# import numpy as np
# from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.externals import joblib
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.decomposition import PCA
# from matplotlib import pyplot as plt
# import json
import traceback
import LocalReceiver as lr
import MongoReceiver
import PreProcessing as pp
import FeatureSelection as fs
import ModelEvaluationTool as met
import DataSampling as ds
import time
import numpy as np


data_path = "../../data/126.csv"
target_fields = ['wcType', 'timestamp', 'networkMode', 'area', 'adxCode', 'gender', 'price', 'appName', 'mobileOs', 'ip',
          'wcAcId', 'wcOrgBidPrice', 'appMediaCat', 'clicked']

dum_coding_fields = ['mediasi', 'fcsid', 'timestamp', 'network', 'co', 'os', 'model', 'text_id']
delim = ";"
area_delim = ","

'''['appMediaCat', 'appName', 'ip', 'networkMode', 'price', 'timestamp', 'wcAcId']'''

''''normalize dict data'''


def norm_data(dic):
    try:
        dic_lu = {}
        for k, v in dic.items():
            if k == "timestamp":
                res = pp.MaxMin(pp.Str2Int(dic[k]))
                dic[k] = res[0]
                dic_lu[k] = res[1]
            elif k == "area":  # areacode transform to real area name?
                tmp = pp.SplitArea(dic[k], area_delim)
                res = pp.MaxMin(pp.Str2Int(tmp[0]))
                dic['area_prov'] = res[0]
                dic_lu['area_prov'] = res[1]
                res = pp.MaxMin(pp.Str2Int(tmp[1]))
                dic['area_city'] = res[0]
                dic_lu['area_city'] = res[1]
                res = pp.MaxMin(pp.Str2Md5(dic['area']))
                dic['area'] = res[0]
                dic_lu['area'] = res[1]
            else:
                try:
                    float(dic[k][0])
                    res = pp.MaxMin(pp.Str2Int(dic[k]))
                    dic[k] = res[0]
                    dic_lu[k] = res[1]
                except:
                    res = pp.MaxMin(pp.Str2Md5(dic[k]))
                    dic[k] = res[0]
                    dic_lu[k] = res[1]
                    continue
        return dic, dic_lu
    except:
        raise ValueError


def train_model(train_data, dum_coding_fields, algorithm, if_preprocessing=True):
    try:
        dic = train_data

        joblib.dump(dic['clicked'], "../../conf/target.dt")
        test_dic=dic.copy()
        test_dic.pop('clicked')
        joblib.dump(test_dic, "../../conf/test_data.dt")

        '''unixtime to hour'''
        dic['timestamp'] = pp.Unixtime2Hour(dic['timestamp'])

        print DataFrame(dic)

        if if_preprocessing:
            '''dummy coding & normalization'''
            st_time = time.time()
            print ('\033[1;35;40m')
            print "Normalizing data..."
            print ('\033[0m')
            # dic = pp.DummyCoding(dic, dum_coding_fields)
            dic = pp.__dumcoding(dic, dum_coding_fields)
            joblib.dump(dum_coding_fields, "../../conf/dum_coding_fields.cf")
            dic_norm = norm_data(dic)
            joblib.dump(dic_norm[1], "../../conf/feature_value_bounds.cf")
            data = DataFrame(dic_norm[0])
            print data
            norm_time = time.time()

            '''merge features'''
            print ('\033[1;35;40m')
            print "Merging DataFrame..."
            print ('\033[0m')
            data = fs.VarSelection(data)
            '''
            data = data.sort_index(axis=1, ascending=True)
            merge_res = fs.__mergefeature(data)
            data = merge_res[0]  # merge factors
            joblib.dump(merge_res[1], "../../conf/merge_value_bounds.cf")
            print data
            '''
            merge_time = time.time()

            '''select features'''
            print ('\033[1;35;40m')
            print "selecting Features..."
            print ('\033[0m')
            data = fs.__selectfeature(data)
            print data
            select_time = time.time()

        else:
            '''dummy coding & normalization'''
            print ('\033[1;35;40m')
            print "Normalizing data..."
            print ('\033[0m')
            dic_norm = norm_data(dic)
            joblib.dump(dic_norm[1], "../../conf/feature_value_bounds.cf")
            data = DataFrame(dic_norm[0])

        target = data['clicked']
        data = data.drop('clicked', axis=1)

        # data=DataFrame(SelectFromModel(LogisticRegression(penalty="l1", C=0.1)).fit_transform(data, target))
        # data=DataFrame(SelectFromModel(LinearRegression()).fit_transform(data, target))

        '''sort data in ascending order'''
        print ('\033[1;35;40m')
        print "Sort data..."
        print ('\033[0m')
        data = data.sort_index(axis=1, ascending=True)
        print data
        joblib.dump(data.columns, "../../conf/keys.cf")
        sort_time = time.time()

        '''Dimensionality Reduction
        print ('\033[1;35;40m')
        print "Dimensionality reduction..."
        print ('\033[0m')
        data = np.array(data)
        # print "Before: ", data
        # dr_model = PCA(n_components='mle').fit(data)
        dr_model = LDA(n_components=10).fit(data, target)
        joblib.dump(dr_model, "../../conf/dr_model.cf")
        data = dr_model.transform(data)
        # print "After: ", data
        '''
        if algorithm == "LR":
            # LinearRegression
            # lr = LogisticRegression(penalty='l1', C=0.1)
            # lr = LogisticRegression(penalty='l2', C=0.02)
            # C = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.2, 0.3, 0.4, 0.5]
            C = [0.5]
            # Penalty = ['l1', 'l2']
            Penalty = ['l1']

            for c in C:
                for p in Penalty:
                    lr = LogisticRegression(penalty=p, C=c)
                    # lr = LinearRegression()
                    lr.fit(data, target)
                    train_time = time.time()
                    predict_y=lr.predict(data)
                    # print set(predict_y)
                    met.ROC("LR", predict_y, target, c, p)
                    joblib.dump(lr, "../../conf/lr_model.jm")

        elif algorithm == "GBDT":
            # GBDT
            gbdt = GradientBoostingRegressor()
            # gbdt = GradientBoostingClassifier()
            gbdt.fit(data, target)
            train_time = time.time()
            predict_y=gbdt.predict(data)
            # print set(predict_y)
            met.ROC("GBDT", predict_y, target)
            joblib.dump(gbdt, "../../conf/gbdt_model.jm")

        elif algorithm == "RF":
            # RandomForest
            rf=RandomForestRegressor(n_estimators=100)
            # rf = RandomForestClassifier(n_estimators=100)
            rf.fit(data, target)
            train_time = time.time()
            predict_y = rf.predict(data)
            # print set(predict_y)
            met.ROC("RF", predict_y, target)
            joblib.dump(rf, "../../conf/rf_model.jm")

        print 'norm_cost: ', norm_time - st_time
        print 'merge_cost: ', merge_time - norm_time
        print 'select_cost: ', select_time - merge_time
        print 'sort_cost: ', sort_time - select_time
        print 'train_cost: ', train_time - sort_time
        print 'total_cost: ', train_time - st_time

    except:
        traceback.print_exc()
        pass



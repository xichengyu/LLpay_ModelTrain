# coding=utf-8

import sys
sys.path.append("../BaseModule")
sys.path.append("../../Base/DataReceiver")
sys.path.append("../../Base/")
from print_switch import prints
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
import PreProcessing as pp
import FeatureSelection as fs
import ModelEvaluationTool as met
import DataSampling as ds
import time
import numpy as np


data_path = "../../data/126.csv"
target_fields = ['wcType', 'unixTime', 'networkMode', 'area', 'adxCode', 'gender', 'price', 'appName', 'mobileOs', 'ip',
          'wcAcId', 'wcOrgBidPrice', 'appMediaCat', 'clicked']
dum_coding_fields = ["unixTime", "networkMode", "mobileOs", "appMediaCat"]
delim = ";"
area_delim = ","


def train_model(train_data, dum_coding_fields, algorithm, if_preprocessing=True, y_idx=0):
    try:
        joblib.dump(train_data[:, y_idx], "../../data/target.dt")

        train_data = np.delete(train_data, y_idx, axis=1)

        joblib.dump(train_data, "../../data/train_data.dt")

        '''unixtime to hour'''

        if if_preprocessing:
            '''dummy coding & normalization'''
            st_time = time.time()
            print('\033[1;35;40m')
            print("Normalizing data...")
            print('\033[0m')
            train_data, lower_upper = pp.max_min(train_data)
            prints(DataFrame(train_data))
            # dic = pp.DummyCoding(dic, dum_coding_fields)
            # joblib.dump(dum_coding_fields, "../../conf/dum_coding_fields.cf")

            '''
            # merge features
            print ('\033[1;35;40m')
            print("Merging DataFrame...")
            print ('\033[0m')
            data = fs.VarSelection(train_data)
            data = data.sort_index(axis=1, ascending=True)
            merge_res = fs.__mergefeature(data)
            data = merge_res[0]  # merge factors
            joblib.dump(merge_res[1], "../../conf/merge_value_bounds.cf")
            # print data
            merge_time = time.time()

            # select features
            print ('\033[1;35;40m')
            print("selecting Features...")
            print ('\033[0m')
            data = fs.__selectfeature(data)
            # print data
            select_time = time.time()
            '''

        else:
            pass

        target = joblib.load("../../data/target.dt")

        # data=DataFrame(SelectFromModel(LogisticRegression(penalty="l1", C=0.1)).fit_transform(data, target))
        # data=DataFrame(SelectFromModel(LinearRegression()).fit_transform(data, target))

        '''sort data in ascending order
        print ('\033[1;35;40m')
        print("Sort data...")
        print ('\033[0m')
        data = data.sort_index(axis=1, ascending=True)
        # print data
        joblib.dump(data.columns, "../../conf/keys.cf")
        sort_time = time.time()
        '''
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

        prints(train_data.shape, target.shape)

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
                    # met.ROC("LR", predict_y, target, c, p)
                    joblib.dump(lr, "../../conf/lr_model.jm")

        elif algorithm == "GBDT":
            # GBDT
            gbdt = GradientBoostingRegressor()
            # gbdt = GradientBoostingClassifier()
            gbdt.fit(train_data, target)
            train_time = time.time()
            predict_y=gbdt.predict(train_data)
            # print set(predict_y)
            # met.ROC("GBDT", predict_y, target)
            joblib.dump(gbdt, "../../conf/gbdt_model.jm")

        elif algorithm == "RF":
            # RandomForest
            rf=RandomForestRegressor(n_estimators=60, max_depth=10)
            # rf = RandomForestClassifier(n_estimators=100)
            rf.fit(train_data, target)
            train_time = time.time()
            predict_y = rf.predict(train_data)
            # print set(predict_y)
            # met.ROC("RF", predict_y, target)
            joblib.dump(rf, "../../conf/rf_model.jm")

    except:
        traceback.print_exc()
        pass



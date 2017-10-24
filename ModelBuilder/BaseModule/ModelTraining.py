# coding=utf-8

import sys
from sklearn.externals import joblib
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression

'''LinearRegression'''


def LR(data, target):
    # lr = LogisticRegression(penalty='l1', C=0.1)
    # lr = LogisticRegression(penalty='l2', C=0.02)
    C = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.2, 0.3, 0.4, 0.5]
    Penalty = ['l1', 'l2']
    for c in C:
        for p in Penalty:
            lr = LogisticRegression(penalty=p, C=c)
            lr.fit(data, target)
            # predict_y = lr.predict(data)
            # ROC("LR", predict_y, target, c, p)


'''GBDT'''


def GBDT(data, target):
    # gbdt=GradientBoostingRegressor()
    gbdt = GradientBoostingClassifier()
    gbdt.fit(data, target)
    # predict_y=gbdt.predict(data)
    # ROC("GBDT", predict_y, target)
    joblib.dump(gbdt, "conf/gbdt_model.jm")

'''RandomForest'''


def RF(data, target):
    # rf=RandomForestRegressor()
    rf = RandomForestClassifier()
    rf.fit(data, target)
    # predict_y = rf.predict(data)
    # ROC("RF", predict_y, target)
    joblib.dump(rf, "conf/rf_model.jm")

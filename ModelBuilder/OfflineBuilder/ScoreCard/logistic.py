# coding=utf-8

import sys
from pandas import DataFrame

sys.path.append('../../BaseModule')
sys.path.append("../../../Base/DataReceiver")
sys.path.append("../../../Base/")
from sklearn.linear_model import LogisticRegression


def get_priority(X, y):
    model = LogisticRegression()
    model.fit(X, y)
    coef = model.coef_
    # coef.sort()
    return coef[0]

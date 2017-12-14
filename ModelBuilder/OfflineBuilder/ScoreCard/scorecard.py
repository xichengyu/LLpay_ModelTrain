# coding=utf-8

import sys
import math
import numpy as np
import traceback
sys.path.append('../../BaseModule')
sys.path.append("../../../Base/DataReceiver")
sys.path.append("../../../Base/")
from print_switch import prints
from read_cnf import get_conf_info as cnf
from InformationValue import WOE
from sklearn.externals import joblib
from logistic import get_priority
import DataSampling as ds


def get_scale_location(base_score=600.0, gap=20.0, odds=10.0):
    """
    score = ln(odds)*scale + location
    :param base_score:
    :param gap:
    :param odds: the ratio of good/bad
    :return: scale, location
    """
    if isinstance(base_score, float) and isinstance(gap, float):
        scale = gap/(math.log(2*odds)-math.log(odds))
        location = base_score - math.log(odds)*scale
        return scale, location
    else:
        return "Param type error, float is needed!"


def get_raw_data(default=-1):
    """
    load joblib format data from local place
    :param default:
    :return:
    """
    data = np.array(joblib.load("../../../data/scorecard_202.dt"))
    for idx in range(data.shape[-1]):        # replace non_type value with -1.0
        data[:, idx][np.where((data[:, idx] == '') | (data[:, idx] == None) | (data[:, idx] == "NULL"))[0]] = default
    data = data.astype(float)
    train_X = data[:, 1:]
    train_y = data[:, 0]
    data = np.column_stack((train_X, train_y))
    return data


def get_train_test_data(data, target_fields=None):
    if not target_fields:
        target_fields = []
    train_data = []
    test_data = []
    try:
        '''create train_data, test_data'''
        randsamp = ds.RandSamp()
        randsamp.MULTIPLE = 1
        randsamp.Y_IDX = -1
        randsamp.TRAIN_PERCENTILE = 0.8
        train_data, test_data = randsamp.random_sampling(data)

    except:
        traceback.print_exc()
        pass
    return train_data, test_data


if __name__ == '__main__':

    conf_info = cnf("./conf/cnf.txt")
    prints(conf_info)
    scale, location = get_scale_location(float(conf_info["base_score"]), float(conf_info["gap"]), float(conf_info["odds"]))
    prints(scale, location)

    data = get_raw_data()
    train_data_list, test_data_list = get_train_test_data(data=data)
    train_X = train_data_list[0][:, :-1]
    train_y = train_data_list[0][:, -1]
    test_X = test_data_list[0][:, :-1]
    test_y = test_data_list[0][:, -1]
    joblib.dump(train_y, "./conf/train_y.nparray")
    joblib.dump(test_y, "./conf/test_y.nparray")

    cal_woe = WOE()
    # cal_woe.WOE_MAX = 1
    # cal_woe.WOE_MIN = -1
    cal_woe.WOE_N = 10
    cal_woe.DISCRETION = "interval_discrete"  # rf_discrete, percentile_discrete, interval_discrete
    X_discretion, woe, iv = cal_woe.woe(train_X, train_y)
    joblib.dump(X_discretion, "./conf/X_discretion.nparray")
    joblib.dump(woe, "./conf/woe.nparray")
    joblib.dump(iv, "./conf/iv.nparray")

    iv.sort()
    prints(iv)

    X_woe_replace, X_interval = cal_woe.woe_replace(X_discretion, woe)
    prints(X_woe_replace)
    for i, interval in enumerate(X_interval):
        prints(i, interval)
    joblib.dump(X_woe_replace, "./conf/X_woe_replace.nparray")
    joblib.dump(X_interval, "./conf/X_interval.nparray")

    test_X_discretion = []
    if cal_woe.DISCRETION == "percentile_discrete":
        test_X_discretion = cal_woe.test_percentile_discrete(test_X)
    elif cal_woe.DISCRETION == "interval_discrete":
        test_X_discretion = cal_woe.test_interval_discrete(test_X)
        prints(test_X_discretion.shape)

    test_X_woe_replace, test_X_interval = cal_woe.woe_replace(test_X_discretion, woe)

    coef = get_priority(X_woe_replace, train_y)
    joblib.dump(coef, "./conf/LR.coef")

    for idx in range(test_X_woe_replace.shape[-1]):
        test_X_woe_replace[:, idx] = test_X_woe_replace[:, idx]*scale*coef[idx]

    for idx in range(woe.shape[0]):
        for key in woe[idx].keys():
            woe[idx][key] = woe[idx][key]*scale*coef[idx]
    joblib.dump(woe, "./conf/woe_score.nparray")

    score = []
    for idx in range(test_X_woe_replace.shape[0]):
        score.append(location+sum(test_X_woe_replace[idx, :]))
    joblib.dump(score, "./conf/score.nparray")






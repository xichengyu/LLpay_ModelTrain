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


def get_raw_data(data_dir, default=-1, y_idx=0):
    """
    load joblib format data from local place
    :param data_dir: data directory
    :param default:
    :param y_idx: the index of y
    :return:
    """
    data = np.array(joblib.load(data_dir))
    for idx in range(data.shape[-1]):        # replace non_type value with -1.0
        data[:, idx][np.where((data[:, idx] == '') | (data[:, idx] == None) | (data[:, idx] == "NULL"))[0]] = default
    data = data.astype(float)
    if y_idx == 0:
        train_X = data[:, 1:]
        train_y = data[:, 0]
    else:
        train_X = data[:, :-1]
        train_y = data[:, -1]
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

    # 计算scale，location
    conf_info = cnf("./conf/cnf.txt")
    prints(conf_info)
    scale, location = get_scale_location(float(conf_info["base_score"]), float(conf_info["gap"]), float(conf_info["odds"]))

    # 获取训练集和测试集
    data = get_raw_data(data_dir=conf_info["data"], y_idx=int(conf_info["y_idx"]))
    train_data_list, test_data_list = get_train_test_data(data=data)
    train_X = train_data_list[0][:, :-1]
    train_y = train_data_list[0][:, -1]
    test_X = test_data_list[0][:, :-1]
    test_y = test_data_list[0][:, -1]

    # train_y, test_y = 1-train_y, 1-test_y

    joblib.dump(train_X, "./conf/train_X.nparray")
    joblib.dump(train_y, "./conf/train_y.nparray")
    joblib.dump(test_X, "./conf/test_X.nparray")
    joblib.dump(test_y, "./conf/test_y.nparray")

    # 计算woe
    cal_woe = WOE()
    cal_woe.WOE_MAX = 1
    cal_woe.WOE_MIN = -1
    cal_woe.WOE_N = 10
    cal_woe.DISCRETION = "interval_discrete"  # rf_discrete, percentile_discrete, interval_discrete
    X_discretion, woe, iv = cal_woe.woe(train_X, train_y)
    joblib.dump(X_discretion, "./conf/X_discretion.nparray")
    joblib.dump(woe, "./conf/woe.nparray")
    joblib.dump(iv, "./conf/iv.nparray")
    iv.sort()
    prints(iv)

    # 生成woe DataFrame
    X_woe_replace, X_interval = cal_woe.woe_replace(X_discretion, woe)
    prints(X_woe_replace)
    for i, interval in enumerate(X_interval):
        prints(i, interval)
    joblib.dump(X_woe_replace, "./conf/X_woe_replace.nparray")
    joblib.dump(X_interval, "./conf/X_interval.nparray")

    # 测试集分箱
    test_X_discretion = []
    if cal_woe.DISCRETION == "percentile_discrete":
        test_X_discretion = cal_woe.test_percentile_discrete(test_X)
    elif cal_woe.DISCRETION == "interval_discrete":
        test_X_discretion = cal_woe.test_interval_discrete(test_X)

    prints(test_X_discretion.shape)
    joblib.dump(test_X_discretion, "./conf/test_X_discretion.nparray")

    test_X_woe_replace, test_X_interval = cal_woe.woe_replace(test_X_discretion, woe)
    joblib.dump(test_X_woe_replace, "./conf/test_X_woe_replace.nparray")

    # 获取指标权重
    coef = get_priority(X_woe_replace, train_y)
    prints(coef)
    joblib.dump(coef, "./conf/LR.coef")

    # 计算测试集woe score
    for idx in range(test_X_woe_replace.shape[-1]):
        test_X_woe_replace[:, idx] = test_X_woe_replace[:, idx]*scale*coef[idx]
    joblib.dump(test_X_woe_replace, "./conf/test_X_woe_score.nparray")

    for idx in range(woe.shape[0]):
        for key in woe[idx].keys():
            woe[idx][key] = woe[idx][key]*scale*coef[idx]
    joblib.dump(woe, "./conf/woe_score.nparray")

    # 计算各用户score
    score = []
    for idx in range(test_X_woe_replace.shape[0]):
        score.append(location+sum(test_X_woe_replace[idx, :]))
    joblib.dump(score, "./conf/score.nparray")

    prints(scale, location)


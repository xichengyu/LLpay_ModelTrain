# coding=utf-8

import sys
import random
import traceback
import numpy as np
sys.path.append("../../Base/")
from print_switch import prints


def create_traindata(train_matrix, partition_n, sampling_process="up", multiple=None):
    shape_matrix = train_matrix.shape
    train_data = []
    try:
        for i in range(partition_n):
            tmp_data = train_matrix[shape_matrix[0]/partition_n * i:shape_matrix[0]/partition_n * (i+1), :]
            if sampling_process == "up":
                if multiple is None:
                    remain_click = 1
                else:
                    remain_click = len_exp / (multiple * len_clc)
                for i in range(remain_click):
                    for k in tmp_exp:
                        tmp_exp[k] += tmp_clc[k]
            elif sampling_process == "down":
                pass
            elif sampling_process is None:
                pass

            train_data.append(tmp_exp)
    except:
        traceback.print_exc()
        pass
    return train_data


def create_testdata(dic_exp, dic_clc, num=10000, partition_n=None):
    test_data = []
    try:
        exp_len = len(dic_exp['timestamp']) if 'timestamp' in dic_exp else len(dic_exp['unixTime'])
        clc_len = len(dic_clc['timestamp']) if 'timestamp' in dic_clc else len(dic_clc['unixTime'])
        if partition_n is None:
            partition_n = exp_len/num
        else:
            num = exp_len / partition_n
        exp_shuffled_index = range(exp_len)
        clc_shuffled_index = range(clc_len)
        random.shuffle(exp_shuffled_index)
        random.shuffle(clc_shuffled_index)

        for i in range(partition_n):
            dic_both = {}
            for k, v in dic_exp.items():
                dic_both[k] = []
                for index in exp_shuffled_index[i*num:(i+1)*num]:
                    dic_both[k].append(v[index])
            for k, v in dic_clc.items():
                for index in clc_shuffled_index[i*clc_len/partition_n:(i+1)*clc_len/partition_n]:
                    dic_both[k].append(v[index])

            test_data.append(dic_both)
    except:
        traceback.print_exc()
        pass
    return test_data


def random_sampling(data_matrix, sampling_process, train_partition_n, test_partition_n, num=100000, train_percentile=None):
    shape_tuple = data_matrix.shape
    train_data = np.array([[]]*shape_tuple[-1]).T
    test_data = np.array([[]]*shape_tuple[-1]).T
    prints(shape_tuple, train_data.shape, test_data.shape)
    try:
        selected_index = set(random.sample(range(shape_tuple[0]), num if train_percentile is None else int(shape_tuple[0] * train_percentile)))

        for idx in range(shape_tuple[0]):
            prints(data_matrix[idx, :].shape)
            if idx in selected_index:
                train_data = np.stack((train_data, data_matrix[idx, :]))
            else:
                test_data = np.stack((test_data, data_matrix[idx, :]))

        prints(train_data.shape, test_data.shape)

        train_data = create_traindata(train_data, partition_n=train_partition_n, sampling_process=sampling_process, multiple=5)
        test_data = create_testdata(new_dic_exp, new_dic_clc, num=10000, partition_n=test_partition_n)
    except:
        traceback.print_exc()
        pass
    return train_data, test_data


# def

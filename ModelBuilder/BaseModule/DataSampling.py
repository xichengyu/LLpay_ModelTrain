# coding=utf-8

import sys
import random
import traceback
import numpy as np
sys.path.append("../../Base/")
from print_switch import prints


def create_traindata(train_matrix, partition_n=1, sampling_process="up", multiple=None):
    shape_matrix = train_matrix.shape
    train_data = []
    try:
        for i in range(partition_n):
            tmp_data = train_matrix[int(shape_matrix[0]/partition_n * i):int(shape_matrix[0]/partition_n * (i+1)), :]

            good_sample = tmp_data[tmp_data[:, 0] == 0]
            bad_sample = tmp_data[tmp_data[:, 0] == 1]

            if sampling_process == "up":
                if multiple is None:
                    remain_bad = 0
                else:
                    remain_bad = int(float(good_sample.shape[0]) / (multiple * bad_sample.shape[0]) + 0.5) - 1
                for j in range(remain_bad):
                    prints(tmp_data.shape, bad_sample.shape)
                    tmp_data = np.stack((tmp_data, bad_sample))
            elif sampling_process == "down":
                pass
            elif sampling_process is None:
                pass

            train_data.append(tmp_data)
    except:
        traceback.print_exc()
        pass
    return train_data


def create_testdata(test_matrix, partition_n=1):
    shape_matrix = test_matrix.shape
    test_data = []
    try:
        for i in range(partition_n):
            tmp_data = test_matrix[int(shape_matrix[0]/partition_n * i):int(shape_matrix[0]/partition_n * (i+1)), :]

            test_data.append(tmp_data)
    except:
        traceback.print_exc()
        pass
    return test_data


def random_sampling(data_matrix, sampling_process, train_partition_n, test_partition_n, multiple=5,num=100000, train_percentile=None):
    shape_tuple = data_matrix.shape
    train_data = []
    test_data = []
    try:
        np.random.shuffle(data_matrix)
        train_data_tmp = data_matrix[:num if train_percentile is None else int(shape_tuple[0] * train_percentile), :]
        test_data_tmp = data_matrix[num if train_percentile is None else int(shape_tuple[0] * train_percentile):, :]

        prints(train_data_tmp.shape, test_data_tmp.shape)

        train_data = create_traindata(train_data_tmp, partition_n=train_partition_n, sampling_process=sampling_process, multiple=multiple)
        test_data = create_testdata(test_data_tmp, partition_n=test_partition_n)
    except:
        traceback.print_exc()
        pass
    return train_data, test_data


# def

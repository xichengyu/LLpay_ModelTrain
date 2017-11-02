# coding=utf-8

import sys
import random
import traceback
import numpy as np
sys.path.append("../../Base/")
from print_switch import prints


def create_traindata(train_matrix, y_idx, partition_n=1, sampling_process="up", multiple=None):
    shape_matrix = train_matrix.shape
    train_data = []
    try:
        for i in range(partition_n):
            tmp_data = train_matrix[int(shape_matrix[0]/partition_n * i):int(shape_matrix[0]/partition_n * (i+1)), :]

            good_sample = tmp_data[tmp_data[:, y_idx] == 0]
            bad_sample = tmp_data[tmp_data[:, y_idx] == 1]

            if sampling_process == "up":
                if multiple is None:
                    remain_bad = 0
                else:
                    remain_bad = int(float(good_sample.shape[0]) / (multiple * bad_sample.shape[0]) + 0.5) - 1
                for j in range(remain_bad):
                    tmp_data = np.row_stack((tmp_data, bad_sample))
            elif sampling_process == "down":
                pass
            elif sampling_process is None:
                pass
            prints(tmp_data.shape, bad_sample.shape)
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


class RandSamp(object):
    def __init__(self):
        self._SAMPLING_PROCESS = "up"
        self._TRAIN_PARTITION_N = 1
        self._TEST_PARTITION_N = 1
        self._MULTIPLE = 5
        self._NUM = 100000
        self._TRAIN_PERCENTILE = 0.9
        self._Y_IDX = 0

    def random_sampling(self, data_matrix):
        shape_tuple = data_matrix.shape
        train_data = []
        test_data = []
        try:
            np.random.shuffle(data_matrix)
            train_data_tmp = data_matrix[:self._NUM if self._TRAIN_PERCENTILE is None else int(shape_tuple[0] * self._TRAIN_PERCENTILE), :]
            test_data_tmp = data_matrix[self._NUM if self._TRAIN_PERCENTILE is None else int(shape_tuple[0] * self._TRAIN_PERCENTILE):, :]

            prints(train_data_tmp.shape, test_data_tmp.shape)

            train_data = create_traindata(train_data_tmp, self._Y_IDX, partition_n=self._TRAIN_PARTITION_N,
                                          sampling_process=self._SAMPLING_PROCESS, multiple=self._MULTIPLE)
            test_data = create_testdata(test_data_tmp, partition_n=self._TEST_PARTITION_N)
        except:
            traceback.print_exc()
            pass
        return train_data, test_data

    @property
    def SAMPLING_PROCESS(self):
        return self._SAMPLING_PROCESS

    @SAMPLING_PROCESS.setter
    def SAMPLING_PROCESS(self, sampling_process):
        self._SAMPLING_PROCESS = sampling_process

    @property
    def TRAIN_PARTITION_N(self):
        return self._TRAIN_PARTITION_N

    @TRAIN_PARTITION_N.setter
    def TRAIN_PARTITION_N(self, train_partition_n):
        self._TRAIN_PARTITION_N = train_partition_n

    @property
    def TEST_PARTITION_N(self):
        return self._TEST_PARTITION_N

    @TEST_PARTITION_N.setter
    def TEST_PARTITION_N(self, test_partition_n):
        self._TEST_PARTITION_N = test_partition_n

    @property
    def MULTIPLE(self):
        return self._MULTIPLE

    @MULTIPLE.setter
    def MULTIPLE(self, multiple):
        self._MULTIPLE = multiple

    @property
    def NUM(self):
        return self._NUM

    @NUM.setter
    def NUM(self, num):
        self._NUM = num

    @property
    def TRAIN_PERCENTILE(self):
        return self._TRAIN_PERCENTILE

    @TRAIN_PERCENTILE.setter
    def TRAIN_PERCENTILE(self, train_percentile):
        self._TRAIN_PERCENTILE = train_percentile

    @property
    def Y_IDX(self):
        return self._Y_IDX

    @Y_IDX.setter
    def Y_IDX(self, y_idx):
        self._Y_IDX = y_idx


# def

# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import random
import traceback


def create_traindata(dic_exposure, dic_click, partition_n, sample_type=None, multiple=None):
    train_data = []
    try:
        len_exp = len(dic_exposure["clicked"])
        len_clc = len(dic_click["clicked"])

        for i in range(partition_n):
            tmp_exp, tmp_clc = {}, {}
            for k, values in dic_exposure.items():
                tmp_exp[k] = tmp_exp.get(k, []) + values[len_exp/partition_n * i:len_exp/partition_n * (i+1)]
            for k, values in dic_click.items():
                tmp_clc[k] = tmp_clc.get(k, []) + values[len_clc/partition_n * i:len_clc/partition_n * (i+1)]

            if sample_type == "up":
                if multiple is None:
                    remain_click = 1
                else:
                    remain_click = len_exp / (multiple * len_clc)
                for i in range(remain_click):
                    for k in tmp_exp:
                        tmp_exp[k] += tmp_clc[k]
            elif sample_type == "down":
                pass
            elif sample_type is None:
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


def random_sampling(dic_exp, dic_clc, sample_type, train_partition_n, test_partition_n, num=10000, percentage=None):
    train_data = []
    test_data = []
    try:
        exp_len = len(dic_exp['timestamp']) if 'timestamp' in dic_exp else len(dic_exp['unixTime'])
        clc_len = len(dic_clc['timestamp']) if 'timestamp' in dic_clc else len(dic_clc['unixTime'])
        exp_selected_index = set(random.sample(range(exp_len), num if percentage is None else int(exp_len * percentage)))
        clc_selected_index = set(random.sample(range(clc_len), num if percentage is None else int(clc_len * percentage)))

        dic_exposure = {}
        dic_click = {}
        new_dic_exp = {}
        new_dic_clc = {}
        for k, values in dic_exp.items():
            for i, value in enumerate(values):
                if i in exp_selected_index:
                    dic_exposure.setdefault(k, dic_exposure.get(k, [])).append(value)
                else:
                    new_dic_exp.setdefault(k, new_dic_exp.get(k, [])).append(value)
        for k, values in dic_clc.items():
            for i, value in enumerate(values):
                if i in clc_selected_index:
                    dic_click.setdefault(k, dic_click.get(k, [])).append(value)
                else:
                    new_dic_clc.setdefault(k, new_dic_clc.get(k, [])).append(value)

        train_data = create_traindata(dic_exposure, dic_click, partition_n=train_partition_n, sample_type=sample_type, multiple=5)
        test_data = create_testdata(new_dic_exp, new_dic_clc, num=10000, partition_n=test_partition_n)
    except:
        traceback.print_exc()
        pass
    return train_data, test_data


# def

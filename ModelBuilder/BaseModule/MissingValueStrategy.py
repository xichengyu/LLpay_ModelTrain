# coding=utf-8

from sklearn.preprocessing import Imputer


def fill_strategy(raw_data, strategy_list):
    res = []
    for strategy in strategy_list:
        if isinstance(strategy, str):
            impute = Imputer(strategy=strategy)
        else:
            impute = Imputer(missing_values=strategy)
        res.append(impute.fit_transform(raw_data))

    return res

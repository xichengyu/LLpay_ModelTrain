# coding=utf-8

from sklearn.preprocessing import Imputer
import traceback


def fill_strategy(raw_data, strategy):
    print(raw_data.shape)
    try:
        if isinstance(strategy, str):
            impute = Imputer(strategy=strategy)
        else:
            impute = Imputer(missing_values=strategy)
        new_data = impute.fit_transform(raw_data)
    except ValueError:
        traceback.print_exc()
        raise ValueError
    print(new_data.shape)
    return new_data

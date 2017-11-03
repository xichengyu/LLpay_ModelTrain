# coding=utf-8

from sklearn.preprocessing import Imputer
import traceback


def fill_strategy(raw_data, strategy, missing_values="NaN"):
    try:
        impute = Imputer(strategy=strategy, missing_values=missing_values)
        new_data = impute.fit_transform(raw_data)
    except ValueError:
        traceback.print_exc()
        raise ValueError
    return new_data

# coding=utf-8

import sys
sys.path.append("../../BaseModule")
# from datetime import datetime
# import pandas as pd
import numpy as np
from sklearn.externals import joblib
import MissingValueStrategy as mvs


if __name__ == "__main__":
    data = joblib.load("../../../data/data_xicy_fullstep_202.dt")
    data = np.array(data)
    print(data.shape)

    data[np.isnan(data)] = -1.0

    strategies = ["mean", "median", "most_frequent"]  # different strategies for dealing with missing value

    new_data = mvs.fill_strategy(data, strategy="median", missing_values=-1.0)

    print(new_data.shape)
    joblib.dump(new_data, "../../../data/data_xicy_fullstep_202_fill.dt")

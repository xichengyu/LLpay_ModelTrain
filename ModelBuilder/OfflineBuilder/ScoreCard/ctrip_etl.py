# coding=utf-8

import sys
sys.path.append("../../BaseModule")
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.externals import joblib
import MissingValueStrategy as mvs



data = pd.read_excel("../../../data/ctrip_sample.xlsx")
# print(data.shape)
data = np.array(data)

for idx in range(data[:, 3].shape[0]):
    data[idx, 3] = 0 if data[idx, 4] == "0-30" else data[idx, 3]

delete_column = [0, 1, 2, 4, 6, 32]

data = np.delete(data, delete_column, axis=1)

# 转换生日为年龄
for idx in range(data[:, 1].shape[0]):
    try:
        data[idx, 1] = datetime.now().year - data[idx, 1].year if isinstance(data[idx, 1], datetime) else -1
    except ValueError:
        raise ValueError

# 识别非数值类型数据
list_idx = []
list_array = []
for idx in range(data.shape[-1]):
    try:
        data[:, idx] = data[:, idx].astype(float)
    except ValueError:
        list_idx.append(idx)
        list_array.append(data[:, idx])
        print(idx)
        continue
list_array = np.array(list_array).T

print(list_array.shape)

data = np.delete(data, list_idx, axis=1)
print(data.shape)

# 分解list类型数据
for idx in range(list_array.shape[-1]):
    temp = []
    for item in list_array[:, idx]:
        try:
            temp.append(item.split(","))
        except:
            temp.append([np.nan])
            continue

    max_len = 1
    for item in temp:
        if len(item) > 1:
            max_len = len(item)
            break

    for i, item in enumerate(temp):
        if len(item) == 1:
            temp[i] = temp[i]*max_len

    temp = np.array(temp).astype(float)
    data = np.column_stack((data, temp))

# 填充缺失值为-1
data = data.astype(float)
for idx in range(data.shape[-1]):
    try:
        data[:, idx][np.isnan(data[:, idx])] = -1.0
    except ValueError:
        print(data[:, idx])
        continue

# 缺失值填充策略
strategies = ["mean", "median", "most_frequent"]    # different strategies for dealing with missing value

new_data = mvs.fill_strategy(data, strategy="median", missing_values=-1.0)


print(new_data.shape)
joblib.dump(new_data, "../../../data/ctrip_sample.dt")

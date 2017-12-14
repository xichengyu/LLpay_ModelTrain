# coding=utf-8

import sys
sys.path.append('../../BaseModule')
from sklearn.externals import joblib
import numpy as np
import ModelEvaluationTool as met

score = joblib.load("./conf/score.nparray")
y = joblib.load("./conf/test_y.nparray")

print(y.shape, sum(y))

n = 400
n = n+1
max_score = max(score)
min_score = min(score)
gap = (max_score-min_score)/n

x_label = [min_score+i*gap for i in range(n)]
x_label[-1] = max_score

cnt_dict = {}
cnt_dict_1 = {}
for j, item in enumerate(score):
    for i in range(n-1):
        if item <= x_label[i]:
            cnt_dict[i] = cnt_dict.get(i, 0)+1
            cnt_dict_1[i] = cnt_dict_1.get(i, 0)+(1 if y[j] == 1 else 0)
            break
for i in range(n-1):
    if i in cnt_dict:
        print((x_label[i], x_label[i+1]), cnt_dict[i], cnt_dict_1[i], cnt_dict_1[i]/cnt_dict[i])

ks_max = met.ROC("lr", "None", score, y,
                 "conf/ks.log", 0, 0, thresholds=x_label)


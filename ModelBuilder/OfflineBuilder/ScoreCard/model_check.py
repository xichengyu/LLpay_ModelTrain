# coding=utf-8

import sys
sys.path.append('../../BaseModule')
sys.path.append("../../../Base/")
sys.path.append("../../../DataAnalyzer/BaseModule")
from sklearn.externals import joblib
import numpy as np
import ModelEvaluationTool as met
from sklearn.metrics import roc_auc_score
from scorecard import get_scale_location
from read_cnf import get_conf_info as cnf
from DataVisualization import BarChart

# 参数设定
n = 400
positive_y = 1
credit_score_upper = 1000
credit_score_lower = 0

# 加载数据
# y = joblib.load("./conf/test_y.nparray")
y = joblib.load("./conf/y.nparray")
score = joblib.load("./conf/score.nparray")
woe_score = joblib.load("./conf/woe_score.nparray")
print("total: ", y.shape, "bad_total: ", sum(y))

# 统计原始score的极值与KS值
max_score = max(score)
min_score = min(score)
gap = (max_score-min_score)/n
x_label = [min_score+i*gap for i in range(n+1)]
x_label[-1] = max_score
ks_max = met.ROC("lr", "None", score, y,
                 "conf/ks.log", 0, 0, thresholds=x_label)

# 计算scale，location
conf_info = cnf("./conf/cnf.txt")
scale, location = get_scale_location(float(conf_info["base_score"]), float(conf_info["gap"]), float(conf_info["odds"]))

# 计算可能出现的score的极值，根据woe_score
sum_max_woe_score, sum_min_woe_score = location, location
for score_dict in woe_score:
    sum_max_woe_score += max(score_dict.values())
    sum_min_woe_score += min(score_dict.values())

# 计算原始score到credit_score的映射参数
a = (sum_min_woe_score-sum_max_woe_score)/(credit_score_upper-credit_score_lower)
b = sum_min_woe_score-a*credit_score_upper

print("a: ", a, "b: ", b)
print("sum_max_woe_score: ", sum_max_woe_score, "sum_min_woe_score: ", sum_min_woe_score)
print("max_score: ", max_score, "min_score: ", min_score, "gap: ", gap)
print("auc: ", roc_auc_score(y, score))

# 计算原始score对应的credit_score
score = (score-b)/a
max_score = max(score)
min_score = min(score)
gap = (max_score-min_score)/n
print("max_credit_score: ", max_score, "min_credit_score: ", min_score, "gap: ", gap)

x_label = [min_score+i*gap for i in range(n+1)]
x_label[-1] = max_score

cnt_dict = {}
cnt_dict_1 = {}
for j, item in enumerate(score):
    for i in range(n):
        if item <= x_label[i+1]:
            cnt_dict[i] = cnt_dict.get(i, 0)+1
            cnt_dict_1[i] = cnt_dict_1.get(i, 0)+(1 if y[j] == positive_y else 0)
            break

for i in range(n):
    if i in cnt_dict:
        print("interval: ", (x_label[i], x_label[i+1]), "interval_total: ", cnt_dict[i], "interval_bad_total: ",
              cnt_dict_1[i], "interval_bad_rate: ", cnt_dict_1[i]/cnt_dict[i])

cnt_dict = dict(sorted(cnt_dict.items(), key=lambda d: d[0]))
BarChart(list(cnt_dict.keys()), list(cnt_dict.values()), chart_name="ctrip_credit_score")

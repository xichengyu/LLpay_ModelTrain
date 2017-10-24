# coding=utf-8

# import sys
from pandas import DataFrame


def __getdata_of_neededadid(dataframe, wcadid):
    return dataframe[dataframe["wcAdId"] == wcadid]


def __getincome(click_cnt, agreed_cpc):
    return float(click_cnt) * agreed_cpc


def get_baseinfo(analyze_log_result):
    click_data = __getdata_of_neededadid(DataFrame(analyze_log_result[1]), "97")
    exposure_data = __getdata_of_neededadid(DataFrame(analyze_log_result[0]), "97").append(click_data,
                                                                                           ignore_index=True)
    dic_info = {
                'exposure': len(exposure_data.index),
                'click': len(click_data.index),
                'total_cost': exposure_data["price"].astype("float").sum() / 10000 / 1000
                }

    dic_info['total_income'] = __getincome(dic_info['click'], 0.45)
    dic_info['CTR'] = float(dic_info['click']) / dic_info['exposure']
    dic_info['avg_CPM'] = dic_info['total_cost'] / dic_info['exposure'] * 1000
    dic_info['avg_rCPC'] = dic_info['total_cost'] / dic_info['click']
    dic_info['total_profit'] = dic_info['total_income'] - dic_info['total_cost']
    return dic_info

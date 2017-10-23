# coding=utf-8

import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')


'''DataFrame to Json'''


def Dataframe2Json(dataframe):
    columns = dataframe.columns
    dic = {}
    for key in columns:
        dic[key] = list(dataframe[key])
    return json.JSONEncoder().encode(dic)


'''DataFrame to dict'''


def Dataframe2Dict(dataframe):
    columns = dataframe.columns
    dic={}
    for key in columns:
        dic[key] = list(dataframe[key])
    return dic
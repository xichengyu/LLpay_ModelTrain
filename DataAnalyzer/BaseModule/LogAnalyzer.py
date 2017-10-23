# coding=utf-8

import codecs
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import json
import time
import traceback
# from pandas import DataFrame

# key_words=["wcType","wcBidUnixTime","networkMode","adxCode","area","gender","price","bidMode","wcOrgId","wcBidPrice","mobileOs","wcAeId","unixTime","wcAdId","wcAcId","wcOrgBidPrice","impId","wcUid"]
log_path = "/Users/XI/Desktop/Jarvis"
output_path = "/Users/XI/Desktop/Jarvis/pCTR/data/fangdichan.csv"
div = ";"
error_count = 0


def __decodejson(json_str, div, title):
    try:
        json_dic = json.loads(json_str)
        keys = map(str, json_dic.keys())
        vals = map(str, json_dic.values())
        if title == "":
            title = div.join(["wcType", div.join(keys), "clicked"])
        return div.join(vals), str(json_dic["impId"]), str(json_dic["area"]), title
    except:
        global error_count
        error_count += 1
        return


def __getdict(title, values, div):
    dic_exposure = {}
    dic_click = {}
    title_list = title.strip().split(div)
    l = len(title_list)
    for key in title_list:
        dic_exposure[key] = []
        dic_click[key] = []
    for i, value in enumerate(values):
        line = value.strip().split(div)
        if len(line) != l:
            continue
        if line[-1] == '0':
            for j in range(l):
                dic_exposure[title_list[j]].append(line[j])
        elif line[-1] == '1':
            for j in range(l):
                dic_click[title_list[j]].append(line[j])
    return dic_exposure, dic_click


'''
check impid loss of click, which means some impids of click are not in exposure data
'''


def __clickimpidlost(dic_exposure, dic_click):
    cnt = 0
    for k in dic_click:
        if k not in dic_exposure:
            cnt += 1
    return cnt, cnt * 100.0 / len(dic_click)


def analyze_log(log_path, output_path="", output_type="dict", div=";"):  # output_type: dict; .csv file
    title = ""
    dic_click = {}
    dic_exposure = {}
    target_dir = ["click", "exposure"]
    dirlist = os.listdir(log_path)

    for dirname in dirlist:
        if dirname in target_dir:
            log_dir_path = log_path + "/" + dirname + "/"
            log_name_list = os.listdir(log_dir_path)
            for log_name in log_name_list:
                for log in codecs.open(log_dir_path + log_name, "r", "utf-8"):
                    try:
                        tmp = log.strip().split(": {")
                        typ = tmp[0].split(" - ")[-1]
                        json_str = "{" + tmp[1]
                        res = __decodejson(json_str, div, title)
                        if title == "":
                            title = res[3]
                        if typ == "exposure":
                            if res[2].find(",") == -1:  # delete abnormal area data
                                continue
                            dic_exposure[res[1]] = typ + div + res[0]
                        else:
                            dic_click[res[1]] = ""
                    except:
                        traceback.print_exc()
                        continue
    # print __clickimpidlost(dic_exposure, dic_click)
    for impId, v in dic_exposure.items():
        dic_exposure[impId] += (div + "1") if impId in dic_click else (div + "0")
    if output_type == "dict":
        result = __getdict(title, dic_exposure.values(), div)
        return result
    else:
        result = codecs.open(output_path, "w", "utf-8")
        result.write(title + "\n")
        l = len(title.strip().split(div))
        for line in dic_exposure.values():
            if len(line.strip().split(div)) != l:  # delete abnormal data with lenth over title_length
                continue
            result.write(line + "\n")


'''
transform unixtime to specific format, %y:year %m:month %d:day %H:hour %M:miniute %S:second
'''


def unixtime2hour(lis, interval):  # interval: %y %m %d %H %M %S
    return [time.strftime(interval, time.localtime(int(x))) if len(x) == 10
            else time.strftime(interval, time.localtime((int(x) + 500) / 1000)) for x in lis]


if __name__ == "__main__":
    # analyze_log(log_path, output_type="dict")
    print analyze_log(log_path, output_path, output_type="csv")
    print "log analysis complete!"

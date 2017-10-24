# coding=utf-8

# import sys

'''get original data in dict format'''
def GetDict(title, lis, div):
    dic_exposure = {}
    dic_click = {}
    title_lis = title.strip().split(div)
    clk_loc = title_lis.index('clicked')
    l = len(title_lis)
    for key in title_lis:
        dic_exposure[key] = []
        dic_click[key] = []
    for i in range(len(lis)):
        line = lis[i].strip().split(div)
        if len(line) != l:
            continue
        if line[clk_loc]=='0':
            for j in range(l):
                dic_exposure[title_lis[j]].append(line[j])
        elif line[clk_loc]=='1':
            for j in range(l):
                dic_click[title_lis[j]].append(line[j])
    return dic_exposure, dic_click


def GetOriginData(file_path, delim=",", selected_features=[]):
    dic = {}
    keys = []
    non_target = []
    for line in open(file_path, 'r'):
        line = line.strip().split(delim)
        if len(selected_features) == 0:
            selected_features = line
        for j in range(len(line)):
            if len(keys) == 0:
                if line[j] not in selected_features:
                    non_target.append(j)
                else:
                    dic[j] = []
            else:
                if j in non_target:
                    continue
                dic[j].append(line[j])
        if len(keys) == 0:
            keys = line
    for i in range(len(keys)):  # modify dict keys
        if i in non_target:
            continue
        dic[keys[i]] = dic.pop(i)
    return dic


def GetOriginData2(file_path, delim=",", selected_features=[]):
    file = open(file_path, "r").readlines()
    title = file[0]
    if len(selected_features) == 0:
        selected_features = title.strip().split(delim)
    del file[0]
    dic = GetDict(title, file, delim)
    keys = dic[0].keys()
    for key in keys:
        if key not in selected_features:
            dic[0].pop(key)
            dic[1].pop(key)
    return dic[0], dic[1]
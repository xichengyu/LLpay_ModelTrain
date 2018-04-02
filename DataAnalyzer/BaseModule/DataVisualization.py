# coding=utf-8

# import sys
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pylab as plb
import os
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']    # 用来正常显示中文标签
mpl.rcParams['axes.unicode_minus'] = False      # 用来正常显示负号


def __getxtick(xray_list, xticks):
    if xticks == "%m":
        return [x for x in range(1, 13)]
    elif xticks == "%d":
        return [x for x in range(1, 32)]
    elif xticks == "%H":
        return [x for x in range(24)]
    elif xticks == "%M":
        return [x for x in range(60)]
    elif xticks == "":
        return xray_list
    elif isinstance(xticks, list):
        return xticks


def BarChart(xray_list, yray_list, chart_name, xticks=""):
    plb.bar(xray_list, yray_list, width=0.2)
    plb.xticks(__getxtick(xray_list, xticks), fontsize=7)
    # plb.yticks([0, 20000, 40000, 60000, 80000, 100000])
    if not os.path.exists("./figures"):
        os.mkdir("./figures")
    plb.savefig("figures/" + chart_name + ".png")
    plb.close()


def LineChart(xray_list, yray_list, chart_name, xticks=""):
    plb.plot(xray_list, yray_list, linewidth=1.5)
    plb.xticks(__getxtick(xray_list, xticks))
    if not os.path.exists("./figures"):
        os.mkdir("./figures")
    plb.savefig("figures/" + chart_name + ".png")
    plb.close()


def ScatterChart(xray_list, yray_list, chart_name, xticks=""):
    plb.scatter(xray_list, yray_list)
    plb.xticks(__getxtick(xray_list, xticks))
    if not os.path.exists("./figures"):
        os.mkdir("./figures")
    plb.savefig("figures/" + chart_name + ".png")
    plb.close()

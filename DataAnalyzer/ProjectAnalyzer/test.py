# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("../BaseModule")
sys.path.append("../../Base")
import LogAnalyzer
import DataVisualization
import BaseStatisticInfo
import ListFunctions
# from pandas import DataFrame


if __name__ == '__main__':

    log_path = "/Users/XI/Desktop/code/holloween"

    # get origin data
    data = LogAnalyzer.analyze_log(log_path, output_type="dict")

    # get base information
    baseinfo = BaseStatisticInfo.get_baseinfo(data)
    print baseinfo

    exposure_data = data[0]
    click_data = data[1]

    # transform unixtime
    unixtime = LogAnalyzer.unixtime2hour(exposure_data["unixTime"], "%H")

    # draw chart
    dic_cnt = ListFunctions.Counter(unixtime)

    DataVisualization.BarChart(dic_cnt.keys(), dic_cnt.values(), chart_name="Bar_exposure", xticks="%H")
    DataVisualization.LineChart(dic_cnt.keys(), dic_cnt.values(), chart_name="Line_exposure", xticks=[x for x in range(24)])
    DataVisualization.ScatterChart(dic_cnt.keys(), dic_cnt.values(), chart_name="Scatter_exposure", xticks="%H")


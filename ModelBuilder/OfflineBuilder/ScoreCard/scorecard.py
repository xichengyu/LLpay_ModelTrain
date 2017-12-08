# coding=utf-8

import sys
import math
sys.path.append('../../BaseModule')
sys.path.append("../../../Base/DataReceiver")
sys.path.append("../../../Base/")
from print_switch import prints
from read_cnf import get_conf_info as cnf


def get_scale_location(base_score=600.0, gap=20.0, odds=10.0):
    """
    score = ln(odds)*scale + location
    :param base_score:
    :param gap:
    :param odds:
    :return: scale, location
    """
    if isinstance(base_score, float) and isinstance(gap, float):
        scale = gap/(math.log(2*odds)-math.log(odds))
        location = base_score - math.log(odds)*scale
        return scale, location
    else:
        return "Param type error, float is needed!"


if __name__ == '__main__':

    conf_info = cnf("./conf/cnf.txt")
    prints(conf_info)
    scale, location = get_scale_location(float(conf_info["base_score"]), float(conf_info["gap"]), float(conf_info["odds"]))
    prints(scale, location)



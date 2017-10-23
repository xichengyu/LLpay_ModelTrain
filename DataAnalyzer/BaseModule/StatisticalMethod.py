# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from scipy.stats import chisquare


def Chisquare(f_obs, f_exp, v):
    k = len(f_obs)
    ddof = k - 1 - v
    return chisquare(f_obs=f_obs, f_exp=f_exp, ddof=ddof)



if __name__ == '__main__':

    obs = [16, 18, 16, 14, 12, 12]
    exp = [16, 18, 7.055, 14, 12, 12]

    print Chisquare(obs, exp, v=3)

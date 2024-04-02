import numpy as np


def cg_calc(data: dict):
    sum_weight = 0
    sum_sum = 0
    for key, item in data.items():
        sum_sum += item[0] * item[1]
        sum_weight += item[0]
    return sum_sum / sum_weight
def cg_calc_oew(data: dict, c):
    sum_weight = 0
    sum_sum = 0
    for key, item in data.items():
        sum_sum += item[0] * item[1]
        sum_weight += item[0]
    return sum_sum / c.OEW
def xcg_new(Wold, Wnew, xold, xitem):
    return (Wold * xold + Wnew * xitem) / (Wold + Wnew)

def convert_global_xlemac(x, xlemac:float, mac:float):
    """Converts the cg in the global coordinate system to the local coordinate system positioned at the leading edge of the MAC
    :param x: the position of the cg in the global coordinate system
    :param xlemac: the location of the leading edge of the MAC
    :param mac: the length of the MAC"""
    if type(x) == list:
        x = np.array(x)
    return (x - xlemac) / mac
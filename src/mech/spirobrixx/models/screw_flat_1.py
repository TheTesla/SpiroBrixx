#!/usr/bin/env python3

from numba import njit
from fuzzyometry import bodies as bd
from fuzzyometry import threads as thrd
from fuzzyometry import combinations as cmb
import math
import numpy as np
import sys


def convert_params(params):
    par = params
    rt1o = float(par["rt1o"])
    pt1 = float(par["pt1"])
    pt1od = float(par["pt1od"])
    pt1odr = float(par["pt1odr"])
    rt1q = float(par["rt1ocoreq"])
    rtof = float(par["rtofase"])
    rtofc = float(par["rtofasec"])
    l = float(par["l"])
    dtp1 = float(par["dtp1"])
    ds1 = float(par["ds1"])
    name = f"screw_flat_1_l{l:03.0f}mm" \
            +f"_pt1od{pt1od*1000:01.0f}" \
            +f"_rt1o{rt1o*1000:01.0f}mm"
    par_tpl = (rt1o, pt1, pt1od, pt1odr, rt1q, \
               rtof, rtofc, l, dtp1, ds1)
    return par_tpl, name


@njit
def model_function(p):
    x, y, z, par = p

    rt1o, pt1, pt1od, pt1odr, rt1q, \
    rtof, rtofc, l, dtp1, ds1 = par

    pt1o = pt1 * (1 + pt1odr + pt1od/l)

    tz = thrd.fz_thread((x,y,pt1o*z), rt1o, 1, dtp1, 1.0)
    thread = cmb.fz_and_chamfer(rtof, tz, z-l, -z)
    screw = cmb.fz_and_chamfer(rtofc, thread, y-ds1/2, -y-ds1/2)
    if screw > 0:
        return False
    return True


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
    rhof = float(par["rhofase"])
    rtif = float(par["rtifase"])
    rtof = float(par["rtofase"])
    rh1 = float(par["rh1"])
    l = float(par["l"])
    dtp1 = float(par["dtp1"])
    lh = float(par["lhead"])
    nh = float(par["nhead"])
    ah = float(par["ahead"])
    name = f"screw_knurl_1_l{l:03.0f}mm" \
            +f"_pt1od{pt1od*1000:04.0f}" \
            +f"_rt1o{rt1o*1000:04.0f}mm"
    par_tpl = (rt1o, pt1, pt1od, pt1odr, rhof,\
               rtof, rtif, rh1, l, dtp1, lh, nh, ah)
    return par_tpl, name


@njit
def model_function(p):
    x, y, z, par = p

    rt1o, pt1, pt1od, pt1odr, rhof, \
    rtof, rtif, rh1, l, dtp1, lh, nh, ah = par

    lt = l + lh
    pt1o = pt1 * (1 + pt1odr + pt1od/l)

    tz = thrd.fz_thread((x,y,pt1o*z), rt1o, 1, dtp1, 1.0)
    th = thrd.fz_thread((x,y,0.1), rh1, nh, ah, rhof)
    thread = cmb.fz_and_chamfer(rtof, tz, z-lt, -z+lh)
    head = cmb.fz_and_chamfer(rhof, th, z-lh, -z)
    if cmb.fz_or_chamfer(rtif, thread, head) > 0:
        return False
    return True


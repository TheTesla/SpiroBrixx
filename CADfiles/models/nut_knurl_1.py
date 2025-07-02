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
    rt1i = float(par["rt1i"])
    pt1 = float(par["pt1"])
    rhof = float(par["rhofase"])
    rtif = float(par["rtifase"])
    rh1 = float(par["rh1"])
    l = float(par["l"])
    dtp1 = float(par["dtp1"])
    nh = float(par["nhead"])
    ah = float(par["ahead"])
    name = f"nut_knurl_1_l{l:03.0f}mm" \
            +f"_rt1i{rt1i*1000:04.0f}mm"
    par_tpl = (rt1i, pt1, rhof, rtif, rh1, l, dtp1, nh, ah)
    return par_tpl, name


@njit
def model_function(p):
    x, y, z, par = p

    rt1i, pt1, rhof, rtif, rh1, l, dtp1, nh, ah = par


    tz = thrd.fz_thread((x,y,pt1*z), rt1i, 1, dtp1, 1.0)
    th = thrd.fz_thread((x,y,0.1), rh1, nh, ah, rhof)
    head = cmb.fz_and_chamfer(rhof, th, z-l, -z)
    if cmb.fz_and_chamfer(rtif, head, -tz) > 0:
        return False
    return True


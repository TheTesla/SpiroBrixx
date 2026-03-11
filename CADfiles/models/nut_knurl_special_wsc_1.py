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
    name = "nut_knurl_special_wsc_1"
    par_tpl = (rt1i, pt1, rhof, rtif, rh1, l, dtp1, nh, ah)
    return par_tpl, name


@njit
def model_function(p):
    x, y, z, par = p
    if z < 0:
        return False

    rt1i, pt1, rhof, rtif, rh1, l, dtp1, nh, ah = par

    blck = bd.fz_cuboid((x,y-10-rh1+ah*2,z-l/2), (10, 20, l), rhof)
    hole = (x**2 + (z-l/2)**2)**0.5 -4

    tz = thrd.fz_thread((x,y,pt1*z), rt1i, 1, dtp1, 1.0)
    th = thrd.fz_thread((x,y,0.1), rh1, nh, ah, rhof)
    head = cmb.fz_and_chamfer(rhof, th, z-l, -z)
    if cmb.fz_and_chamfer(rtif, -hole, cmb.fz_or_chamfer(rhof, blck, cmb.fz_and_chamfer(rtif, head, -tz))) > 0:
        return False
    return True


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
    rt4i = float(par["rt4i"])
    pt4 = float(par["pt4"])
    rhof = float(par["rhofase"])
    rtif = float(par["rtifase"])
    rh4 = float(par["rh4"])
    l = float(par["l"])
    dtp4 = float(par["dtp4"])
    nh = float(par["nhead"])
    ah = float(par["ahead"])
    name = "nut_knurl_special_wsc_4"
    par_tpl = (rt4i, pt4, rhof, rtif, rh4, l, dtp4, nh, ah)
    return par_tpl, name


@njit
def model_function(p):
    x, y, z, par = p
    if z < 0:
        return False

    rt4i, pt4, rhof, rtif, rh4, l, dtp4, nh, ah = par

    yblck = -10-rh4+ah*2
    blck = bd.fz_cuboid((x,y + yblck,z-l/2), (10, 20, l), rhof)
    hole = cmb.fz_and_chamfer(rtif, (x**2 + (z-l/2)**2)**0.5 -4, rt4i+dtp4+2-y)
    cblhole = cmb.fz_and_chamfer(rtif, (x**2 + (y+yblck)**2)**0.5 -2, l/2-z)

    tz = thrd.fz_thread((x,y,pt4*z), rt4i, 4, dtp4, 1.0)
    th = thrd.fz_thread((x,y,0.1), rh4, nh, ah, rhof)
    head = cmb.fz_and_chamfer(rhof, th, z-l, -z)
    if cmb.fz_and_chamfer(rtif, -hole, -cblhole, cmb.fz_or_chamfer(rhof, blck, cmb.fz_and_chamfer(rtif, head, -tz))) > 0:
        return False
    return True


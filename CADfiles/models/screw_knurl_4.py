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
    rt4o = float(par["rt4o"])
    pt4 = float(par["pt4"])
    pt4od = float(par["pt4od"])
    pt4odr = float(par["pt4odr"])
    rt4q = float(par["rt4ocoreq"])
    rbof = float(par["rbofase"])
    rtif = float(par["rtifase"])
    rtof = float(par["rtofase"])
    rh4 = float(par["rh4"])
    l = float(par["l"])
    dtp4 = float(par["dtp4"])
    lh = float(par["lhead"])
    nh = float(par["nhead"])
    ah = float(par["ahead"])
    name = f"screw_knurl_4_l{l:03.0f}mm" \
            +f"_pt4od{pt4od*1000:04.0f}" \
            +f"_rt4o{rt4o*1000:04.0f}mm"
    par_tpl = (rt4o, pt4, pt4od, pt4odr, rt4q, rbof,\
               rtof, rtif, rh4, l, dtp4, lh, nh, ah)
    return par_tpl, name


@njit
def model_function(p):
    x, y, z, par = p

    rt4o, pt4, pt4od, pt4odr, rt4q, rbof, \
    rtof, rtif, rh4, l, dtp4, lh, nh, ah = par

    lt = l + lh
    pt4o = pt4 * (1 + pt4odr + pt4od/l)

    tz = thrd.fz_thread((x,y,pt4o*z), rt4o/4*3, 4, dtp4/3*2, 1.0)
    th = thrd.fz_thread((x,y,0.1), rh4, nh, ah, 1.0)
    thread = cmb.fz_and_chamfer(rtof, tz, -z-lt, z+lh)
    head = cmb.fz_and_chamfer(rbof, th, -z-lh, z)
    if cmb.fz_or_chamfer(rtif, thread, head) > 0:
        return False
    return True


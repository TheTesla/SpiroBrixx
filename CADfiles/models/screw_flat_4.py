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
    rtof = float(par["rtofase"])
    rtofc = float(par["rtofasec"])
    l = float(par["l"])
    dtp4 = float(par["dtp4"])
    ds4 = float(par["ds4"])
    name = f"screw_flat_4_l{l:03.0f}mm" \
            +f"_pt4od{pt4od*1000:04.0f}" \
            +f"_rt4o{rt4o*1000:04.0f}mm"
    par_tpl = (rt4o, pt4, pt4od, pt4odr, rt4q, \
               rtof, rtofc, l, dtp4, ds4)
    return par_tpl, name


@njit
def model_function(p):
    x, y, z, par = p

    rt4o, pt4, pt4od, pt4odr, rt4q, \
    rtof, rtofc, l, dtp4, ds4 = par

    pt4o = pt4 * (1 + pt4odr + pt4od/l)

    tz = thrd.fz_thread((x,y,pt4o*z), rt4o, 4, dtp4, 1.0)
    thread = cmb.fz_and_chamfer(rtof, tz, z-l, -z)
    screw = cmb.fz_and_chamfer(rtofc, thread, y-ds4/2, -y-ds4/2)
    if screw > 0:
        return False
    return True


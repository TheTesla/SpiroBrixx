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
    rs4 = float(par["rs4"])
    ns4 = float(par["ns4"])
    as4 = float(par["as4"])
    rsof = float(par["rsof"])
    name = "screw_headless_4"
    par_tpl = (rt4o, pt4, pt4od, pt4odr, rt4q, \
               rtof, rtofc, l, dtp4, rs4, ns4, as4, rsof)
    return par_tpl, name


@njit
def model_function(p):
    x, y, z, par = p

    rt4o, pt4, pt4od, pt4odr, rt4q, \
    rtof, rtofc, l, dtp4, rs4, ns4, as4, rsof = par

    pt4o = pt4 * (1 + pt4odr + pt4od/l)

    tz = thrd.fz_thread((x,y,pt4o*z), rt4o, 4, dtp4, 1.0)
    ts = thrd.fz_thread((x,y,0.1), rs4, ns4, as4, rsof)
    thread = cmb.fz_and_chamfer(rtof, tz, z-l, -z)
    screw = cmb.fz_and_chamfer(rtofc, thread, -ts)
    if screw > 0:
        return False
    return True


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
    rs1 = float(par["rs1"])
    ns1 = float(par["ns1"])
    as1 = float(par["as1"])
    rsof = float(par["rsof"])
    name = "screw_special_wsc_1"
    par_tpl = (rt1o, pt1, pt1od, pt1odr, rt1q, \
               rtof, rtofc, l, dtp1, rs1, ns1, as1, rsof)
    return par_tpl, name


@njit
def model_function(p):
    x, y, z, par = p

    rt1o, pt1, pt1od, pt1odr, rt1q, \
    rtof, rtofc, l, dtp1, rs1, ns1, as1, rsof = par

    pt1o = pt1 * (1 + pt1odr + pt1od/l)

    r = (x**2 + y**2)**0.5
    tz = thrd.fz_thread((x,y,pt1o*z), rt1o, 1, dtp1, 1.0)
    ts = thrd.fz_thread((x,y,0.1), rs1, ns1, as1, rsof)
    head = cmb.fz_and_chamfer(rtof, r - 15, 3.2 - r, -2-z, z-1) 
    thread = cmb.fz_and_chamfer(rtof, tz, z-l, -z)
    screw = cmb.fz_and_chamfer(rtofc, thread, -ts)
    if cmb.fz_or_chamfer(rtofc, screw, head) > 0:
        return False
    return True


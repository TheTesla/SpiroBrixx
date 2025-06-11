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
    rh4 = float(par["rh4"])
    l = float(par["l"])
    dtp4 = float(par["dtp4"])
    lh = float(par["lhead"])
    nh = float(par["nhead"])
    ah = float(par["ahead"])
    name = f"screw_knurl_4_l{l:03.0f}mm" \
            +f"_pt4od{pt4od*1000:04.0f}" \
            +f"_rt4o{rt4o*1000:04.0f}mm"
    return (rt4o, pt4, pt4od, pt4odr, rt4q, rh4, l, dtp4, lh, nh, ah), name


@njit
def model_function(p):
    x, y, z, par = p

    #dtp = 2.4

    #rg, pt4, pt4od, pt4odr, rt4q, rh4, l, dtp4 = par
    rt4o, pt4, pt4od, pt4odr, rt4q, rh4, l, dtp4, lh, nh, ah = par

    rg = rt4o

    f = 3
    hh = lh
    rho = rh4
    #ah = 1. *0.5
    #nh = 32
    #td = dtp * rt4q
    tdi = 0.6
    lt = l + hh + (10 - rg) + tdi
    #rti = rg - td
    #rto = rg - tdi

    #if z < 0:
    #    return False




    pt4o = pt4 * (1 + pt4odr + pt4od/(l-2))
    tz = 3*thrd.fz_thread((x,y,pt4o*z), rt4o/4*3, 4, dtp4/3*2, 1.0)
    th = 3*thrd.fz_thread((x,y,0.1), rh4, nh, ah, 1.0)

    thread = cmb.fz_and_chamfer(f, tz, -z-lt, z+hh)
    head = cmb.fz_and_chamfer(f, th, -z-hh, z)

    if cmb.fz_or_chamfer(f, thread, head) > 0:
        return False

#    ang = -math.atan2(y,x) + 0/180*math.pi
#    rh = rho - ah*(math.sin(ang *nh)+1)/2
#    sti = fzCylRnd((x, y, z-lt/2), lt/2-f, rti - f) - f
#    sto = fzCylRnd((x, y, z-lt/2), lt/2-f, rto - f) - f
#    sh = fzCylRnd((x, y, z-hh/2), hh/2-f, rh - f) - f
#    if not (max(0,f-sti)**2 + max(0,f-sh)**2)**0.5 - f < 0:
#        return True
#    if not (max(0,f-sto)**2 + max(0,f-sh)**2)**0.5 - f > 0:
#        return False
#
#    tn = max((z - lt)/2 + 1, 0)
#
#    pt4o = pt4 * (1 + pt4odr + pt4od/(l-2))
#
#    if screw4(x,y,z,rg,pt4o,rt4q,tn):
#        return True
#
#    return False
    return True


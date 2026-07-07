#!/usr/bin/env python3

from numba import njit
from fuzzyometry import bodies as bd
from fuzzyometry import threads as thrd
from fuzzyometry import combinations as cmb
import numpy as np

def convert_params(params):
    par = params
    l = int(par["l"])
    w = int(par["w"])
    rt4i = float(par["rt4i"])
    pt4 = float(par["pt4"])
    d = float(par["dgrid"])
    dwall = float(par["dwall"])
    rbofase = float(par["rbofase"])
    rtifase = float(par["rtifase"])
    dtp4 = float(par["dtp4"])
    name = f"thin_screwbarA2_4_{l:02}_{w:02}"
    return (rt4i, pt4, d, dwall, rbofase, rtifase, l, w, dtp4), name


@njit
def model_function(p):
    x, y, z, par = p
    rt4i, pt4, d, dwall, rbofase, rtifase, l, w, dtp4 = par

    xr = x % d - d/2
    yr = y % d - d/2
    zr = z % d - d/2

    odd = l%2
    lm = (l+odd) / 2
    xm = abs(x-odd*d/2) + odd*d/2


    cut = (xm-d)*(w-1)/(lm-1)-y
    cutstep = 1.*round((xm-d)*(w-1.)/(lm-1.)/d-0.5)-1.*round(y/d-0.5)
    tx = thrd.fz_thread((yr,zr,pt4*xm-0.25), rt4i, 4, dtp4, 1.0) \
         if cutstep < 0 else rbofase
    ty = thrd.fz_thread((zr,xr,pt4*y-0.25), rt4i, 4, dtp4, 1.0) \
         if cutstep < 0 else rbofase
    tz = thrd.fz_thread((xr,yr,pt4*z-0.25), rt4i, 4, dtp4, 1.0) \
         if cutstep < 0 else rbofase

    a = bd.fz_cuboid((xm-lm*d/2+rbofase/2,y-w*d/2,z-dwall/2), (lm*d+rbofase,w*d,dwall), rbofase)
    screwbar = cmb.fz_and_chamfer(rtifase, a, -tx, -ty, -tz)
    if cmb.fz_and_chamfer(rbofase, screwbar, cut) > 0:
        return False

    return True







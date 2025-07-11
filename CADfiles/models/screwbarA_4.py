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
    h = int(par["h"])
    rt4i = float(par["rt4i"])
    pt4 = float(par["pt4"])
    d = float(par["dgrid"])
    rbofase = float(par["rbofase"])
    rtifase = float(par["rtifase"])
    dtp4 = float(par["dtp4"])
    name = f"screwbarA_4_{l:02}_{w:02}_{h:02}"
    return (rt4i, pt4, d, rbofase, rtifase, l, w, h, dtp4), name


@njit
def model_function(p):
    x, y, z, par = p
    rt4i, pt4, d, rbofase, rtifase, l, w, h, dtp4 = par

    xr = x % d - d/2
    yr = y % d - d/2
    zr = z % d - d/2

    cut = (x-d)*(w-1)/(l-1)-y
    cutstep = 1.*round((x-d)*(w-1.)/(l-1.)/d-0.5)-1.*round(y/d-0.5)
    tx = thrd.fz_thread((yr,zr,pt4*x-0.25), rt4i, 4, dtp4, 1.0) \
         if cutstep < 0 else rbofase
    ty = thrd.fz_thread((zr,xr,pt4*y-0.25), rt4i, 4, dtp4, 1.0) \
         if cutstep < 0 else rbofase
    tz = thrd.fz_thread((xr,yr,pt4*z-0.25), rt4i, 4, dtp4, 1.0) \
         if cutstep < 0 else rbofase

    a = bd.fz_cuboid((x-l*d/2,y-w*d/2,z-h*d/2), (l*d,w*d,h*d), rbofase)
    screwbar = cmb.fz_and_chamfer(rtifase, a, -tx, -ty, -tz)
    if cmb.fz_and_chamfer(rbofase, screwbar, cut) > 0:
        return False

    return True







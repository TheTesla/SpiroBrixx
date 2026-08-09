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
    rc = float(par["rc"])
    xc = float(par["xc"])
    yc = float(par["yc"])
    name = f"clamp_screwbarI_4_{l:02}_{w:02}_{h:02}"
    return (rt4i, pt4, d, rbofase, rtifase, l, w, h, dtp4, rc, xc, yc), name


@njit
def model_function(p):
    x, y, z, par = p
    rt4i, pt4, d, rbofase, rtifase, l, w, h, dtp4, rc, xc, yc = par

    #pc = 60
    #rc = 3

    xd = np.floor(x/d)*d + d/2
    yd = np.floor(y/d)*d + d/2
    xd2 = np.floor(3*x/d)*d/3 + d/6
    yd2 = np.floor(3*y/d)*d/3 + d/6

    xr = x % d - d/2
    yr = y % d - d/2
    zr = z % d - d/2

    tx = thrd.fz_thread((yr,zr,pt4*x-0.25), rt4i, 4, dtp4, 1.0)
    ty = thrd.fz_thread((zr,xr,pt4*y-0.25), rt4i, 4, dtp4, 1.0)
    tz = thrd.fz_thread((xr,yr,pt4*z-0.25), rt4i, 4, dtp4, 1.0)
    if (xd2 - xc)**2 + (yd - yc)**2 < (rc+rt4i+dtp4/2+rtifase)**2:
        tx = 1000
    if (xd - xc)**2 + (yd2 - yc)**2 < (rc+rt4i+dtp4/2+rtifase)**2:
        ty = 1000
    if (xd - xc)**2 + (yd - yc)**2 < (rc+rt4i+dtp4/2+rtifase)**2:
        tz = 1000


    a = bd.fz_cuboid((x-l*d/2,y-w*d/2,z-h*d/2), (l*d,w*d,h*d), rbofase)
    b = bd.fz_circle((x-xc, y-yc), rc) #+ rbofase
    if cmb.fz_and_chamfer(rtifase, a, -b, -tx, -ty, -tz) > 0:
        return False

    return True







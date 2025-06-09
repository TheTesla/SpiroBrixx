#!/usr/bin/env python3

from numba import njit
from fuzzyometry import bodies as bd
from fuzzyometry import threads as thrd
from fuzzyometry import combinations as cmb


def convert_params(params):
    par = params
    l = int(par["l"])
    w = int(par["w"])
    h = int(par["h"])
    rt4i = float(par["rt4i"])
    pt4 = float(par["pt4"])
    d = float(par["dgrid"])
    rbofase = float(par["rbofase"])
    rbifase = float(par["rbifase"])
    rtifase = float(par["rtifase"])
    dtp4 = float(par["dtp4"])
    name = f"screwbarY_4_{l:02}_{w:02}_{h:02}"
    return (rt4i, pt4, d, rbofase, rbifase, rtifase, l, w, h, dtp4), name


@njit
def model_function(p):
    x, y, z, par = p
    rt4i, pt4, d, rbofase, rbifase, rtifase, l, w, h, dtp4 = par

    re2 = rbifase
    re3 = re2
    re4 = re2
    l2 = l - 1
    w2 = w - 1
    h2 = h
    l3 = l
    w3 = w - 1
    h3 = h - 1
    l4 = l - 1
    w4 = w
    h4 = h - 1

    xr = x % d - d/2
    yr = y % d - d/2
    zr = z % d - d/2

    tx = thrd.fz_thread((yr,zr,pt4*x-0.25), rt4i/4*3, 4, dtp4/3*2, 1.0)
    ty = thrd.fz_thread((zr,xr,pt4*y-0.25), rt4i/4*3, 4, dtp4/3*2, 1.0)
    tz = thrd.fz_thread((xr,yr,pt4*z-0.25), rt4i/4*3, 4, dtp4/3*2, 1.0)

    a = bd.fz_cuboid((x-l*d/2,y-w*d/2,z-h*d/2), (l*d,w*d,h*d), rbofase)
    b = bd.fz_cuboid((x-l2*d/2,y-w2*d/2,z-h2*d/2), (l2*d,w2*d,h2*d), re2)
    c = bd.fz_cuboid((x-l3*d/2,y-w3*d/2,z-h3*d/2), (l3*d,w3*d,h3*d), re3)
    e = bd.fz_cuboid((x-l4*d/2,y-w4*d/2,z-h4*d/2), (l4*d,w4*d,h4*d), re4)

    if cmb.fz_and_chamfer(rtifase, a, -b, -c, -e, -tx, -ty, -tz) > 0:
        return False

    return True


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
    dwall = float(par["dwall"])
    rbofase = float(par["rbofase"])
    rbifase = float(par["rbifase"])
    rtifase = float(par["rtifase"])
    dtp4 = float(par["dtp4"])
    name = f"thin_screwbarLA_4_out_{l:02}_{w:02}_{h:02}"
    return (rt4i, pt4, d, dwall, rbofase, rbifase, rtifase, l, w, h, dtp4), name


@njit
def model_function(p):
    x, y, z, par = p
    rt4i, pt4, d, dwall, rbofase, rbifase, rtifase, l, w, h, dtp4 = par

    xr = x % d - d/2
    yr = y % d - d/2
    zr = z % d - d/2

    cutz = (x-d)*(w-1)/(l-1)+y-w*d
    cutstepz = 1.*round((x-d)*(w-1.)/(l-1.)/d-0.5)+1.*round(y/d+0.5-w)
    tx = thrd.fz_thread((yr,zr,pt4*x-0.25), rt4i, 4, dtp4, 1.0) \
         if cutstepz < 0 else rbofase
    ty = thrd.fz_thread((zr,xr,pt4*y-0.25), rt4i, 4, dtp4, 1.0) \
         if cutstepz < 0 else rbofase
    tz = thrd.fz_thread((xr,yr,pt4*z-0.25), rt4i, 4, dtp4, 1.0) \
         if cutstepz < 0 else rbofase

    a = bd.fz_cuboid((x-l*d/2+dwall/2,y-w*d/2+dwall/2,z-h*d/2+dwall/2), \
                     (l*d+dwall,w*d+dwall,h*d+dwall), rbofase)
    b = bd.fz_cuboid((x-l*d/2,y-w*d/2,z-h*d/2), (l*d,w*d,h*d), rbifase)
    screwbar = cmb.fz_and_chamfer(rtifase, a, -tx, -ty, -tz, -b)
    if cmb.fz_and_chamfer(rbofase, screwbar, cutz) > 0:
        return False

    return True



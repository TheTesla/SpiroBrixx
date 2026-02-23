#!/usr/bin/env python3

from numba import njit
from fuzzyometry import gears as gr
from fuzzyometry import bodies as bd
from fuzzyometry import threads as thrd
from fuzzyometry import combinations as cmb
import numpy as np

def convert_params(params):
    par = params
    z = int(par["z"])
    m = float(par["m"])
    alpha = float(par['alpha'])
    rt4i = float(par["rt4i"])
    pt4 = float(par["pt4"])
    d = float(par["dgrid"])
    dwall = float(par["dwall"])
    rbofase = float(par["rbofase"])
    rtifase = float(par["rtifase"])
    dtp4 = float(par["dtp4"])
    name = f"thin_screwgear_4_{z:02}_{m:02}_{alpha:03}"
    return (rt4i, pt4, d, dwall, rbofase, rtifase, z, m, alpha, dtp4), name


@njit
def model_function(p):
    x, y, z, par = p
    rt4i, pt4, d, dwall, rbofase, rtifase, Z, m, alpha, dtp4 = par

    xr = x % d - d/2
    yr = y % d - d/2
    zr = z % d - d/2

    tx = thrd.fz_thread((yr,zr,pt4*x-0.25), rt4i, 4, dtp4, 1.0)
    ty = thrd.fz_thread((zr,xr,pt4*y-0.25), rt4i, 4, dtp4, 1.0)
    tz = thrd.fz_thread((xr,yr,pt4*z-0.25), rt4i, 4, dtp4, 1.0)

    #a = bd.fz_cuboid((x-l*d/2,y-w*d/2,z-dwall/2), (l*d,w*d,dwall), rbofase)
    a = 30*gr.evolvente(p, (Z, m, alpha))
    #if cmb.fz_and_chamfer(rtifase, -tx, -ty, -tz, cmb.fz_and_chamfer(rbofase, a, -z, z-dwall)) > 0:
    if cmb.fz_and_chamfer(rbofase, a, -z, z-dwall) > 0:
        return False

    return True







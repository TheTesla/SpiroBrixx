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

    xr = (x + d/2) % d - d/2
    yr = (y + d/2) % d - d/2
    zr = (z + d/2) % d - d/2

    r = (x**2 + y**2)**0.5
    #cut = (x-d)*(w-1)/(l-1)-y
    #cutstep = 1.*round((x-d)*(w-1.)/(l-1.)/d-0.5)-1.*round(y/d-0.5)
    cutstep = 1. * (round(x/d)**2 + round(y/d)**2)**0.5 - Z*(m-2.5)/2/d
    #tx = thrd.fz_thread((yr,zr,pt4*x-0.25), rt4i, 4, dtp4, 1.0) \
    #     if cutstep < 0 else rtifase
    #ty = thrd.fz_thread((zr,xr,pt4*y-0.25), rt4i, 4, dtp4, 1.0) \
    #     if cutstep < 0 else rtifase
    tz = thrd.fz_thread((xr,yr,pt4*z-0.25), rt4i, 4, dtp4, 1.0) \
         if cutstep < 0 else rtifase
    

    a = gr.evolvente(p, (Z, m, alpha))
    #if cmb.fz_and_chamfer(rtifase, -tz, cmb.fz_and_chamfer(rbofase, a, -z, z-dwall)) > 0:
    #if cmb.fz_and_chamfer(rbofase, cmb.fz_and_chamfer(rtifase, -tz, a), -z, z-dwall) > 0:
    if cmb.fz_and_chamfer(rbofase, a, cmb.fz_and_chamfer(rtifase, -tz, -z, z-dwall)) > 0:
    #if cmb.fz_and_chamfer(rtifase, -tz, a, -z, z-dwall) > 0:
    #if cmb.fz_and_chamfer(rbofase, a, -z, z-dwall) > 0:
        return False

    return True







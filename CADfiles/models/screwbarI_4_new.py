#!/usr/bin/env python3

from numba import njit
from common.spirostd import screw4
from fuzzyometry import bodies as bd
from fuzzyometry import threads as thrd
from fuzzyometry import combinations as cmb
import numpy as np

def convert_params(params):
    par = params
    l = int(par["l"])
    w = int(par["w"])
    h = int(par["h"])
    rg = float(par["rt4i"])
    ra = float(par["rt4jntsphr"])
    pt4 = float(par["pt4"])
    d = float(par["dgrid"])
    re = float(par["rbofase"])
    rt4q = float(par["rt4icoreq"])
    rge = float(par["rtifase"])
    dtp4 = float(par["dtp4"])
    name = f"screwbarI_4_new_{l:02}_{w:02}_{h:02}"
    return (rg, ra, pt4, d, re, rt4q, rge, l, w, h, dtp4), name


@njit
def model_function(p):
    x, y, z, par = p
    rg, ra, pt4, d, re, rt4q, rge, l, w, h, dtp = par

    xr = x % d - d/2
    yr = y % d - d/2
    zr = z % d - d/2
    rgi = rg - dtp * rt4q

    #cx = bd.fz_circle((z%d-d/2,y%d-d/2,x), rgi)
    #cy = bd.fz_circle((x%d-d/2,z%d-d/2,y), rgi)
    #cz = bd.fz_circle((x%d-d/2,y%d-d/2,z), rgi)
    cx = thrd.fz_thread((zr,yr,pt4*-x+np.pi/4.2), rg/4*3, 4, dtp/3*2, 1.0)
    cy = thrd.fz_thread((xr,zr,pt4*-y+np.pi/4.2), rg/4*3, 4, dtp/3*2, 1.0)
    cz = thrd.fz_thread((xr,yr,pt4*z+np.pi/4.2), rg/4*3, 4, dtp/3*2, 1.0)

    a = bd.fz_cuboid((x-l*d/2,y-w*d/2,z-h*d/2), (l*d,w*d,h*d), re)
    if cmb.fz_and_chamfer(0.5*rge, a, -cx, -cy, -cz) > 0:
        return False

    #if ra**2 > xr**2 + yr**2 + zr**2:
    #    return False
    #if thrd.fz_thread((xr,yr,z), rg, 4, dtp, pt4):
    #    return False
    #if screw4(xr,zr,-y, rg, pt4, rt4q):
    #    return False
    #if screw4(zr,yr,-x, rg, pt4, rt4q):
    #    return False
    return True





#def params_screwbarI_4(profile, parameters):
#    par = profile | parameters
#    l = int(par["l"])
#    w = int(par["w"])
#    h = int(par["h"])
#    rg = float(par["rt4i"])
#    ra = float(par["rt4jntsphr"])
#    pt4 = float(par["pt4"])
#    d = float(par["dgrid"])
#    re = float(par["rbofase"])
#    rt4q = float(par["rt4icoreq"])
#    rge = float(par["rtifase"])
#    dpt4 = float(par["dpt4"])
#    name = f"screwbarI_4_{l:02}_{w:02}_{h:02}"
#    return (rg, ra, pt4, d, re, rt4q, rge, l, w, h, dpt4), name
#


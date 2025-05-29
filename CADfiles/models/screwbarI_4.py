#!/usr/bin/env python3

from numba import njit
from common.spirostd import screw4
from fuzzyometry import bodies as bd
from fuzzyometry import combinations as cmb


@njit
def screwbarI_4(p):
    x, y, z, par = p

    #dtp = 2.4 # thread profile depht
    rg, ra, pt4, d, re, rei, rt4q, rge, l, w, h, dtp = par

    rgi = rg - dtp * rt4q

    cx = bd.fz_circle((z%d-d/2,y%d-d/2,x), rgi)
    cy = bd.fz_circle((x%d-d/2,z%d-d/2,y), rgi)
    cz = bd.fz_circle((x%d-d/2,y%d-d/2,z), rgi)

    a = bd.fz_cuboid((x-l*d/2,y-w*d/2,z-h*d/2), (l*d,w*d,h*d), re)
    if cmb.fz_and_chamfer(rge, a, -cx, -cy, -cz) > 0:
        return False

    xr = x % d - d/2
    yr = y % d - d/2
    zr = z % d - d/2
    if ra**2 > xr**2 + yr**2 + zr**2:
        return False
    if screw4(xr,yr,z, rg, pt4, rt4q):
        return False
    if screw4(xr,zr,-y, rg, pt4, rt4q):
        return False
    if screw4(zr,yr,-x, rg, pt4, rt4q):
        return False
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


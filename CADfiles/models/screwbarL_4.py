#!/usr/bin/env python3

from numba import njit
from common.spirostd import screw4
from fuzzyometry import bodies as bd
from fuzzyometry import combinations as cmb


@njit
def screwbarL_4(p):
    x, y, z, par = p

    #dtp = 2.4 # thread profile depht
    rg, ra, pt4, d, re, rei, rt4q, rge, l, w, h, dtp = par

    re2 = rei
    re3 = re2
    re4 = re2
    rgi = rg - dtp * rt4q
    l2 = l - 1
    w2 = w - 1
    h2 = h

    cx = bd.fz_circle((z%d-d/2,y%d-d/2,x), rgi)
    cy = bd.fz_circle((x%d-d/2,z%d-d/2,y), rgi)
    cz = bd.fz_circle((x%d-d/2,y%d-d/2,z), rgi)

    a = bd.fz_cuboid((x-l*d/2,y-w*d/2,z-h*d/2), (l*d,w*d,h*d), re)
    b = bd.fz_cuboid((x-l2*d/2,y-w2*d/2,z-h2*d/2), (l2*d,w2*d,h2*d), re2)
    if cmb.fz_and_chamfer(rge, a, -b, -cx, -cy, -cz) > 0:
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

#1def new_screwbarL_4(profile, parameters):
#1    par = profile | parameters
#1    l = int(par["l"])
#1    w = int(par["w"])
#1    h = int(par["h"])
#1    rg = float(par["rt4i"])
#1    ra = float(par["rt4jntsphr"])
#1    pt4 = float(par["pt4"])
#1    d = float(par["dgrid"])
#1    re = float(par["rbofase"])
#1    rei = float(par["rbifase"])
#1    rt4q = float(par["rt4icoreq"])
#1    rge = float(par["rtifase"])
#1    name = f"screwbarL_4_{l:02}_{w:02}_{h:02}"
#1    @njit
#1    def f(x, y, z):
#1        return screwbarL_4((x,y,z), (rg, ra, pt4, d, re, rei, rt4q, rge, l, w, h))
#1    return f, name


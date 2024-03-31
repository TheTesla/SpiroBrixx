#!/usr/bin/env python3

from numba import njit
from common.spirostd import screw4


@njit
def fuzzCylInfH(p):
    x, y = p[:2]
    return (x**2 + y**2)**0.5

@njit
def fuzzBlockRound(p,s):
    x, y, z = p
    w, l, h = s
    d = (min(w-x, w+x, 0)**2 + min(l-y, l+y, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    d += max(min(abs(x),w)-w, min(abs(y),l)-l, min(abs(z),h)-h)
    return d

@njit
def screwbarI_4(p, profile, parameters):
    x, y, z = p

    rg, ra, d, re, rgi, rge = profile
    l, w, h = parameters

    cx = fuzzCylInfH((z%d-d/2,y%d-d/2,x)) - rgi
    cy = fuzzCylInfH((x%d-d/2,z%d-d/2,y)) - rgi
    cz = fuzzCylInfH((x%d-d/2,y%d-d/2,z)) - rgi

    a = fuzzBlockRound((x-l*d/2,y-w*d/2,z-h*d/2),(l*d/2-re,w*d/2-re,h*d/2-re)) - re
    if (max(0,a+rge)**2 + max(0,rge-cx)**2 + max(0,rge-cy)**2 + max(0,rge-cz)**2)**0.5 - rge> 0:
        return False

    xr = x % d - d/2
    yr = y % d - d/2
    zr = z % d - d/2
    if ra**2 > xr**2 + yr**2 + zr**2:
        return False
    if screw4(xr,yr,z,rg):
        return False
    if screw4(xr,zr,-y,rg):
        return False
    if screw4(zr,yr,-x,rg):
        return False
    return True

def new_screwbarI_4(profile, parameters):
    l = int(parameters["l"])
    w = int(parameters["w"])
    h = int(parameters["h"])
    rg = float(profile["rt4i"])
    ra = float(profile["rt4jntsphr"])
    d = float(profile["dgrid"])
    re = float(profile["rbofase"])
    rgi = float(profile["rt4ocore"])
    rge = float(profile["rtifase"])
    name = f"screwbarI_4_{l:02}_{w:02}_{h:02}"
    @njit
    def f(x, y, z):
        return screwbarI_4((x,y,z), (rg, ra, d, re, rgi, rge), (l, w, h))
    return f, name



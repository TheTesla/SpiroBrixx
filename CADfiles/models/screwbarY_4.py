#!/usr/bin/env python3

from numba import njit
from common.spirostd import screw4, block


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
def screwbarY_4(p, par):
    x, y, z = p

    dtp = 2.4 # thread profile depht
    rg, ra, pt4, d, re, rei, rt4q, rge, l, w, h = par

    re2 = rei
    re3 = re2
    re4 = re2
    rgi = rg - dtp * rt4q
    l2 = l - 1
    w2 = w - 1
    h2 = h
    l3 = l
    w3 = w - 1
    h3 = h - 1
    l4 = l - 1
    w4 = w
    h4 = h - 1

    cx = fuzzCylInfH((z%d-d/2,y%d-d/2,x)) - rgi
    cy = fuzzCylInfH((x%d-d/2,z%d-d/2,y)) - rgi
    cz = fuzzCylInfH((x%d-d/2,y%d-d/2,z)) - rgi

    a = fuzzBlockRound((x-l*d/2,y-w*d/2,z-h*d/2),(l*d/2-re,w*d/2-re,h*d/2-re)) - re
    b = \
    fuzzBlockRound((x-l2*d/2,y-w2*d/2,z-h2*d/2),(l2*d/2-re2,w2*d/2-re2,h2*d/2-re2)) - re2
    c = \
    fuzzBlockRound((x-l3*d/2,y-w3*d/2,z-h3*d/2),(l3*d/2-re3,w3*d/2-re3,h3*d/2-re3)) - re3
    e = \
    fuzzBlockRound((x-l4*d/2,y-w4*d/2,z-h4*d/2),(l4*d/2-re4,w4*d/2-re4,h4*d/2-re4)) - re4
    if (max(0,a+rge)**2 + max(0,rge-b)**2 + max(0,rge-c)**2 + max(0,rge-e)**2 + max(0,rge-cx)**2 + max(0,rge-cy)**2 + max(0,rge-cz)**2)**0.5 - rge> 0:
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

def new_screwbarY_4(profile, parameters):
    par = profile | parameters
    l = int(par["l"])
    w = int(par["w"])
    h = int(par["h"])
    rg = float(par["rt4i"])
    ra = float(par["rt4jntsphr"])
    pt4 = float(par["pt4"])
    d = float(par["dgrid"])
    re = float(par["rbofase"])
    rei = float(par["rbifase"])
    rt4q = float(par["rt4icoreq"])
    rge = float(par["rtifase"])
    name = f"screwbarY_4_{l:02}_{w:02}_{h:02}"
    @njit
    def f(x, y, z):
        return screwbarY_4((x,y,z), (rg, ra, pt4, d, re, rei, rt4q, rge, l, w, h))
    return f, name


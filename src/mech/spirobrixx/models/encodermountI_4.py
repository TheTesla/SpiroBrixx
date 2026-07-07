#!/usr/bin/env python3

import numpy as np
from numba import njit
from common.spirostd import screw4
from math import atan2, sin, cos, pi, floor
from fuzzyometry import bodies as bd
from fuzzyometry import combinations as cmb


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
def encodermountI_4(p, par):
    x, y, z = p

    dtp = 2.4 # thread profile depht
    rg, ra, pt4, d, re, rt4q, rge, l, w, h = par

    rgi = rg - dtp * rt4q

    rgenc = 19.5
    rgencc = 10
    reenc = 1
    dm = 2
    rmenc = 1.5
    nmc = 3
    rmc = 15
    rgc = 14
    agc = 15/180*pi


    cx = bd.fz_circle((z%d-d/2,y%d-d/2,x), rgi) if abs(x-l*d/2) > rgenc else rge
    cy = bd.fz_circle((x%d-d/2,z%d-d/2,y), rgi) if abs(x-l*d/2) > rgenc else rge
    cz = bd.fz_circle((x%d-d/2,y%d-d/2,z), rgi) if abs(x-l*d/2) > rgenc else rge

    cc = bd.fz_circle((z-d,(x-l*d/2)*cos(agc)+(y-w*d/2)*sin(agc), \
                 (x-l*d/2)*sin(agc)+(y-w*d/2)*cos(agc)), rgc) \
                         if y < w*d/2 else rge
    cccz = bd.fz_circle((x-l*d/2,y-w*d/2,z), rgencc)*2
    angcmz = floor(0.5+(atan2(y-w*d/2,x-l*d/2)/pi/2)*nmc)/nmc*pi*2
    xcmz = x-rmc*cos(angcmz)-l*d/2
    ycmz = y-rmc*sin(angcmz)-w*d/2
    cmz = 2*2*bd.fz_circle((xcmz,ycmz,z), rmenc)
    ccz = ((max(0,bd.fz_circle((x-d/2*l,y-d/2*w,z), rgenc))**2 +
              max(0,reenc+dm-z)**2)**0.5 - reenc)
    ccz = rge if z < dm else ccz

    a = bd.fz_cuboid((x-l*d/2,y-w*d/2,z-h*d/2), (l*d,w*d,h*d), re)
    if cmb.fz_and_chamfer(rge, a, -cx, -cy, -cz, -cc, -ccz, -cccz, -cmz) > 0:
        return False

    xr = x % d - d/2
    yr = y % d - d/2
    zr = z % d - d/2
    if ra**2 > xr**2 + yr**2 + zr**2 and abs(x-l*d/2) > rgenc:
        return False
    if screw4(xr,yr,z, rg, pt4, rt4q) and abs(x-l*d/2) > rgenc:
        return False
    if screw4(xr,zr,-y, rg, pt4, rt4q) and abs(x-l*d/2) > rgenc:
        return False
    if screw4(zr,yr,-x, rg, pt4, rt4q) and abs(x-l*d/2) > rgenc:
        return False
    return True

def new_encodermountI_4(profile, parameters):
    par = profile | parameters
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
    name = f"encodermountI_4_{l:02}_{w:02}_{h:02}"
    @njit
    def f(x, y, z):
        return encodermountI_4((x,y,z), (rg, ra, pt4, d, re, rt4q, rge, l, w, h))
    return f, name



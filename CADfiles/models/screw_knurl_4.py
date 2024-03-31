#!/usr/bin/env python3

from xyzcad import render
from numba import njit
import math
import numpy as np
import sys

@njit
def screwprofile(x):
    x = x / (2*math.pi)
    return min(max(3*(x if x < 0.5 else 1-x), 0.3), 1.2)

@njit
def fzCylRnd(p,h,r):
    x, y, z = p
    rc = (x**2 + y**2)**0.5
    d = (min(r-rc, r+rc, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    return d


@njit
def screw_knurl_4(p, profile, parameters):
    x, y, z = p
    rg, pt4 = profile
    l = parameters

    f = 3
    hh = 14
    rho = 14
    ah = 1
    nh = 30
    td = 2.4
    tdi = 0.6
    lt = l + hh + (10 - rg) + tdi
    rti = rg - td
    rto = rg - tdi

    if z < 0:
        return False

    ang = -math.atan2(y,x) + 0/180*math.pi
    rh = rho - ah*(math.sin(ang *nh)+1)/2
    sti = fzCylRnd((x, y, z-lt/2), lt/2-f, rti - f) - f
    sto = fzCylRnd((x, y, z-lt/2), lt/2-f, rto - f) - f
    sh = fzCylRnd((x, y, z-hh/2), hh/2-f, rh - f) - f
    if not (max(0,f-sti)**2 + max(0,f-sh)**2)**0.5 - f < 0:
        return True
    if not (max(0,f-sto)**2 + max(0,f-sh)**2)**0.5 - f > 0:
        return False


    r = 2*screwprofile((4*(2*math.pi*pt4*z/4+ang+math.pi))%(2*math.pi)) + (x**2 + y**2)**0.5
    if r < rg:
        return True

    return False

def new_screw_knurl_4(profile, parameters):
    rg = float(profile["rt4o"])
    pt4 = float(profile["pt4"])
    l = float(parameters["l"])
    name = f"screw_knurl_4_{l:03.0f}mm"
    @njit
    def f(x,y,z):
        return screw_knurl_4((x,y,z), (rg, pt4), (l))
    return f, name



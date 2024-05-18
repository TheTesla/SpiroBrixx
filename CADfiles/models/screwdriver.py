#!/usr/bin/env python3

from xyzcad import render
from numba import njit
import math
import numpy as np
import sys

@njit
def screwprofile(x, m=1, n=0):
    x = x / (2*math.pi)
    return max(m*min(3*(x if x < 0.5 else 1-x), 1.2)+n, 0.3)

@njit
def fzCylRnd(p,h,r):
    x, y, z = p
    rc = (x**2 + y**2)**0.5
    d = (min(r-rc, r+rc, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    return d


#def knurl(x,y,z):

@njit
def screwdriver(p, profile, parameters):
    x, y, z = p
    rg, pt4, pt4od, rh4 = profile
    l = parameters

    #l = 10

    rs = 15
    f = 8
    fi = 1
    hh = 70
    rho = 25
    rhi = rh4 +0.4
    hhi = 14
    ah = 1
    nh = 40
    nhi = 30
    td = 10
    tdi = 1
    lt = l + hh #+ tdi
    rg = rs + td
    rti = rg - td
    rto = rg - tdi

    if z < 0:
        return False

    ang = -math.atan2(y,x) + 0/180*math.pi
    rh = rho - ah*(math.sin(ang *nh)+1)/2
    sti = fzCylRnd((x, y, z-lt/2), lt/2-f, rti - f) - f
    sh = fzCylRnd((x, y, z-hh/2), hh/2-f, rh - f) - f
    solid = (max(0,f-sti)**2 + max(0,f-sh)**2)**0.5 - f
    rhig = rhi - ah*(math.sin(ang *nhi)+1)/2
    shi = fzCylRnd((x, y, z-lt), hhi, rhig - fi) - fi
    if (max(0,fi-solid)**2 + max(0,fi-shi)**2)**0.5 - fi > 0:
        return False
    return True


def new_screwdriver(profile, parameters):
    rt4o = float(profile["rt4o"])
    pt4 = float(profile["pt4"])
    pt4od = float(profile["pt4od"])
    rh4 = float(profile["rh4"])
    l = float(parameters["l"])
    name = f"screwdriver_l{l:03.0f}mm" \
            +f"_pt4od{pt4od*1000:04.0f}" \
            +f"_rt4o{rt4o*1000:04.0f}mm"
    @njit
    def f(x,y,z):
        return screwdriver((x,y,z), (rt4o, pt4, pt4od, rh4), (l))
    return f, name



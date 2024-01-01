#!/usr/bin/env python3

from xyzcad import render
from numba import njit #jit
import math
import numpy as np
import sys
from common.spirostd import screw4, block


a = sys.argv[1:]

l = float(a[0])
w = float(a[1])
if len(a) > 2:
    p = float(a[2])
else:
    p = 1.0

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
def f(x,y,z):
    rg = 10.1
    ra = rg*1.2
    d = 2*15
    re = 3
    rgi = rg/1.3
    rge = 3
    h = 1

    cz = fuzzCylInfH((x%d-d/2,y%d-d/2,z)) - rgi

    a = \
    fuzzBlockRound((x-l*d/2,y-w*d/2,z-h*d/4+rg/2),(l*d/2-re,w*d/2-re,h*d/4-re-rg/2)) - re
    if (max(0,a+rge)**2 + max(0,rge-cz)**2)**0.5 - rge> 0:
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

render.renderAndSave(f,
                     f'screwbar_flat4_45_{l:02.0f}_{w:02.0f}_{p*1000:04.0f}u.stl', p)


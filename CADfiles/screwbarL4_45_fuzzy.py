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
h = float(a[2])
if len(a) > 3:
    p = float(a[3])
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
    re2 = 1
    rgi = rg/1.3
    rge = 3
    l2 = l
    w2 = 1
    h2 = 1

    cx = fuzzCylInfH((z%d-d/2,y%d-d/2,x)) - rgi
    cy = fuzzCylInfH((x%d-d/2,z%d-d/2,y)) - rgi
    cz = fuzzCylInfH((x%d-d/2,y%d-d/2,z)) - rgi

    a = fuzzBlockRound((x-l*d/2,y-w*d/2,z-h*d/2),(l*d/2-re,w*d/2-re,h*d/2-re)) - re
    b = \
    fuzzBlockRound((x-l2*d/2,y-w2*d/2,z-h2*d/2),(l2*d/2-re2,w2*d/2-re2,h2*d/2-re2)) - re2
    if (max(0,a+rge)**2 + max(0,rge-b)**2 + max(0,rge-cx)**2 + max(0,rge-cy)**2 + max(0,rge-cz)**2)**0.5 - rge> 0:
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
                     f'screwbarL4_45_{l:02.0f}_{w:02.0f}_{h:02.0f}_{p*1000:04.0f}u.stl', p)


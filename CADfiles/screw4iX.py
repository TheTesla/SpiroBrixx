#!/usr/bin/env python3

from xyzcad import render
from numba import njit
import math
import numpy as np

@njit
def screwprofile(x):
    x = x / (2*math.pi)
    return min(max(3*(x if x < 0.5 else 1-x), 0.3), 1.2)

@njit
def fzBlkRnd(p,s):
    if len(s) == 2:
        x, y = p[:2]
        l, w = s
        d = (min(w-x, w+x, 0)**2 + min(l-y, l+y, 0)**2)**0.5
        d += max(min(abs(x),w)-w, min(abs(y),l)-l)
        return d
    x, y, z = p[:3]
    l, w, h = s[:3]
    d = (min(w-x, w+x, 0)**2 + min(l-y, l+y, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    d += max(min(abs(x),w)-w, min(abs(y),l)-l, min(abs(z),h)-h)
    return d

@njit
def fzCylRnd(p,h,r):
    x, y, z = p
    rc = (x**2 + y**2)**0.5
    d = (min(r-rc, r+rc, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    return d

@njit
def f(x,y,z):
    l = 77
    rg = 10 -0.2
    ra = 10
    rr = 14
    rf = rg+3
    hh = 12
    f = 1.5

    s = fzCylRnd((x, y, z), l/2, rg - 0.6 - 2*f) - f
    c1 = fzBlkRnd((x, y), (0, 4)) - 1
    c2 = fzBlkRnd((x, y), (4, 0)) - 1
    if not (max(0,s)**2 + max(0,f-c1)**2 + max(0,f-c2)**2)**0.5 - f < 0:
        return False

    ang = -math.atan2(y,x) + 0/180*math.pi
    r = 2*screwprofile((4*(2*math.pi/6*1*z/4+ang+math.pi))%(2*math.pi)) + (x**2 + y**2)**0.5
    if r < rg:
        return True

    return False

render.renderAndSave(f, 'screw4iX.stl', 0.1)


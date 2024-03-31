#!/usr/bin/env python3

from xyzcad import render
from numba import njit
import math
import numpy as np
import sys

a = sys.argv[1:]

l = float(a[0])
if len(a) > 1:
    p = float(a[1])
else:
    p = 1.0

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
    x, y, z = p[:3]
    rc = (x**2 + y**2)**0.5
    d = (min(r-rc, r+rc, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    return d

rg = 10 -0.1 -0.1 #-0.05

@njit
def f(x,y,z):
    #rg = 10 -0.1 -0.1 #-0.05
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


    r = 2*screwprofile((4*(2*math.pi/6*1*z/4+ang+math.pi))%(2*math.pi)) + (x**2 + y**2)**0.5
    if r < rg:
        return True

    return False

render.renderAndSave(f, f'screw4knrl_{l:02.0f}_rg{rg*1000:04.0f}u_p{p*1000:04.0f}u.stl', p)


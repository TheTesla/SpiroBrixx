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
def f(x,y,z):
    rg = 10.1
    ra = rg*1.3
    d = 2*15
    re = 3

    if y < 0:
        return False
    if x < 0:
        return False
    if y > d/2:
        if x < (d-y)+10:
            return False
    #y = d + (y - d) * (1 if x > d/2 else (1/((x+0.001)/(d/2))))
    #y = max(y,d/2)
    #x = max(x,d/2)

    if not block((x-l*d/2,y-w*d/2,z-h*d/2),(l*d,w*d,h*d),re):
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
                     f'screwbar4_45_split_dowel_{l:02.0f}_{w:02.0f}_{h:02.0f}_{p*1000:04.0f}u.stl', p)


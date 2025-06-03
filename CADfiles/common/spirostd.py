#!/usr/bin/env python3

from numba import njit
import math

@njit
def screwprofile(x, m=1, n=0):
    x = x / (2*math.pi)
    return max(m*min(3*(x if x < 0.5 else 1-x), 1.2)+n, 0.3)


@njit
def screw4(x,y,z,rg,pt4o=1,m=1,n=0):
    ang = -math.atan2(y,x)
    pp = (4*(2*math.pi*pt4o*z/4+ang+1.25*math.pi))%(2*math.pi)
    r = 2*screwprofile(pp, m=m, n=n) + (x**2 + y**2)**0.5
    return r < rg

@njit
def block(p, s, r=1):
    x = p[0]
    y = p[1]
    z = p[2]
    l = s[0] - 2*r
    w = s[1] - 2*r
    h = s[2] - 2*r
    return r**2 > (x - ((x if x < l/2 else l/2) if x > -l/2 else -l/2))**2\
                 +(y - ((y if y < w/2 else w/2) if y > -w/2 else -w/2))**2\
                 +(z - ((z if z < h/2 else h/2) if z > -h/2 else -h/2))**2

def output_filename(model_name, profile):
    res = float(profile["resolution"])
    #extension = str(profile["extension"])
    tdir = str(profile["target_dir"])
    profile_name = profile["name"] if "name" in profile \
                    else str(profile["__name__"]).split(".")[-1]
    return f'{tdir}/{model_name}_{profile_name}_p{res*1000:04.0f}u.stl'


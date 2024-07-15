#!/usr/bin/env python3

from xyzcad import render
from numba import njit
from common.spirostd import screw4, block
import math
import numpy as np
import sys

#@njit
#def screwprofile(x, m=1, n=0):
#    x = x / (2*math.pi)
#    return max(m*min(3*(x if x < 0.5 else 1-x), 1.2)+n, 0.3)

@njit
def fzCylRnd(p,h,r):
    x, y, z = p
    rc = (x**2 + y**2)**0.5
    d = (min(r-rc, r+rc, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    return d

@njit
def fuzzBlockRound(p,s):
    x, y, z = p
    w, l, h = s
    d = (min(w-x, w+x, 0)**2 + min(l-y, l+y, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    d += max(min(abs(x),w)-w, min(abs(y),l)-l, min(abs(z),h)-h)
    return d

@njit
def screw_knurl_4(p, par):
    x, y, z = p

    dtp = 2.4

    rg, pt4, pt4od, pt4odr, rt4q, rh4, l = par

    f = 3
    hh = 14
    rho = rh4
    ah = 1
    nh = 32
    td = dtp * rt4q
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

    tn = max((z - lt)/2 + 1, 0)

    pt4o = pt4 * (1 + pt4odr + pt4od/(l-2))

    if screw4(x,y,z,rg,pt4o,rt4q,tn):
        return True

    return False




def new_screw_knurl_4(profile, parameters):
    par = profile | parameters
    rt4o = float(par["rt4o"])
    pt4 = float(par["pt4"])
    pt4od = float(par["pt4od"])
    pt4odr = float(par["pt4odr"])
    rt4q = float(par["rt4ocoreq"])
    rh4 = float(par["rh4"])
    l = float(par["l"])
    name = f"screw_knurl_4_l{l:03.0f}mm" \
            +f"_pt4od{pt4od*1000:04.0f}" \
            +f"_rt4o{rt4o*1000:04.0f}mm"
    @njit
    def f(x,y,z):
        return screw_knurl_4((x,y,z), (rt4o, pt4, pt4od, pt4odr, rt4q, rh4, l))
    return f, name


def new_screw_knurl_4_mold(profile, parameters):
    par = profile | parameters
    rt4o = float(par["rt4o"])
    pt4 = float(par["pt4"])
    pt4od = float(par["pt4od"])
    pt4odr = float(par["pt4odr"])
    rt4q = float(par["rt4ocoreq"])
    rh4 = float(par["rh4"])
    l = float(par["l"])
    f = 1
    fi = 3
    name = f"screw_knurl_4_mold_l{l:03.0f}mm" \
            +f"_pt4od{pt4od*1000:04.0f}" \
            +f"_rt4o{rt4o*1000:04.0f}mm"
    @njit
    def h(x,y,z):
        if screw_knurl_4((x,y,z), (rt4o+0.1, pt4, pt4od, pt4odr, rt4q, rh4, l)):
            return False
        r = (x**2 + y**2)**0.5
        molds = fzCylRnd((x-z/40, y-z/40, z-(l+14)/2-0.6/2), (l+14)/2-f+0.6
                         +1,rh4 - f+1)
        if molds > 0 and molds < 4:
            x = x + abs(2-molds) -2
            y = y - abs(2-molds) +2
        if x < 0:
            return False
        if y < 0:
            return False
        if (z-2*((l+14)/2-f+0.6-1))/6>r:
            return False
        blk1 = fuzzBlockRound((x-rh4+f-6-5-z/40,y-z/40,z-(l+14+f)/2),(5,2,(l+14+6*2+f+0.6)/2))-f
        blk2 = fuzzBlockRound((x-z/40,y-rh4+f-6-5-z/40,z-(l+14+f)/2),(2,5,(l+14+6*2+f+0.6)/2))-f
        r = (x**2 + y**2)**0.5
        ang = -math.atan2(y,x) + 0/180*math.pi
        zo = 0
        moldh = fzCylRnd((x-z/40, y-z/40, z-(l+14)/2-0.6/2), (l+14)/2-f+0.6
                         +6,rh4 - f+6)
        return (max(0,moldh-f)**2 + max(0,f-blk1)**2 + max(0,f-blk2)**2)**0.5 - f < 0

    return h, name

def new_screw_knurl_4_mold_base(profile, parameters):
    par = profile | parameters
    rt4o = float(par["rt4o"])
    pt4 = float(par["pt4"])
    pt4od = float(par["pt4od"])
    pt4odr = float(par["pt4odr"])
    rt4q = float(par["rt4ocoreq"])
    rh4 = float(par["rh4"])
    l = float(par["l"])
    f = 1
    fi = 3
    name = f"screw_knurl_4_mold_base_l{l:03.0f}mm" \
            +f"_pt4od{pt4od*1000:04.0f}" \
            +f"_rt4o{rt4o*1000:04.0f}mm"
    @njit
    def h(x,y,z):
        moldho = fzCylRnd((x, y, z-(l+14)/2-0.6/2), (l+14)/2-f+0.6
                         +3,rh4 - f+6+10)
        blk1 = fuzzBlockRound((abs(x)-rh4+f-6-5-z/80,abs(y)-z/80,z-(l+14+f)/2),\
                (5-0.05,2-0.15,(l+14+6*2+f+0.6)/2))-f
        blk2 = fuzzBlockRound((abs(x)-z/80,abs(y)-rh4+f-6-5-z/80,z-(l+14+f)/2),\
                (2-0.15,5-0.05,(l+14+6*2+f+0.6)/2))-f

        r = (x**2 + y**2)**0.5
        ang = -math.atan2(y,x) + 0/180*math.pi
        zo = 0
        moldh = fzCylRnd((abs(x)-z/80, abs(y)-z/80, z-(l+14)/2-0.6/2), (l+14)/2-f+0.6
                         +6,rh4 - f+6+0.05)
        hl = (max(0,moldh-f)**2 \
            + max(0,f-blk1)**2 + max(0,f-blk2)**2 )**0.5 - 1.01*f
        if (max(0,moldho-f)**2 + max(0,f-hl)**2)**0.5 -f> 0:
            return False

        return True

    return h, name





#!/usr/bin/env python3

from xyzcad import render
from numba import njit
from common.spirostd import screw4
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
def screw_knurl_4(p, par):
    x, y, z = p

    dtp = 2.4

    rg, pt4, pt4od, pt4odr, rt4q, rh4, l = par

    f = 3
    hh = 14
    rho = rh4
    ah = 1
    nh = 30
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
    f = 0.5
    fi = 3
    name = f"screw_knurl_4_mold_l{l:03.0f}mm" \
            +f"_pt4od{pt4od*1000:04.0f}" \
            +f"_rt4o{rt4o*1000:04.0f}mm"
    @njit
    def h(x,y,z):
        if screw_knurl_4((x,y,z), (rt4o, pt4, pt4od, pt4odr, rt4q, rh4, l)):
            return False
        r = (x**2 + y**2)**0.5
        ang = -math.atan2(y,x) + 0/180*math.pi
        zo = 0
        if r > rh4+3 and z > 10:
            zo = (rh4+3-r)*(1+math.sin(10*ang))
        moldh = fzCylRnd((x, y, zo+z+10-14+fi), 20/2-f, rh4 - f+6) - f
        return moldh < 0

    @njit
    def m(x,y,z):
        if screw_knurl_4((x,y,z), (rt4o, pt4, pt4od, pt4odr, rt4q, rh4, l)):
            return False
        r = (x**2 + y**2)**0.5
        ang = -math.atan2(y,x) + 0/180*math.pi
        zo = 0
        if r > rh4+3:
            zo = (rh4+3-r)*(1+math.sin(10*ang))
        moldm = fzCylRnd((x, y, zo+z-14+fi/2), fi/2-f, rh4 - f+6) - f
        return moldm < 0

    @njit
    def t(x,y,z):
        if screw_knurl_4((x,y,z), (rt4o, pt4, pt4od, pt4odr, rt4q, rh4, l)):
            return False
        r = (x**2 + y**2)**0.5
        ang = -math.atan2(y,x) + 0/180*math.pi
        zo = 0
        if r > rh4+3 and z < 10+14:
            zo = (rh4+3-r)*(1+math.sin(10*ang))
        rf = 0
        if z > l + 14:
            rf = max(1,z - l - 14 -1 -2)
        moldt = fzCylRnd((x, y, zo+z-14-l/2-6/2), l/2-f+6/2, rh4 - f+6) - f
        return moldt < 0 and r > rf
    return h, m, t, name





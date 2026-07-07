#!/usr/bin/env python3

from numba import njit
from fuzzyometry import bodies as bd
from fuzzyometry import threads as thrd
from fuzzyometry import combinations as cmb
import math
import numpy as np
import sys

def convert_params(params):
    par = params
    rhof = float(par["rhofase"])
    rtif = float(par["rtifase"])
    rtof = float(par["rtofase"])
    rhsd = float(par["rhsd"])
    l = float(par["l"])
    dwall = float(par["dwalltool"])
    lh = float(par["lhead"])
    nh = float(par["nhead"])
    ah = float(par["ahead"])
    rsdhndl = float(par["rsdhndl"])
    lsdhndl = float(par["lsdhndl"])
    nsdhndl = float(par["nsdhndl"])
    osdhndlfase = float(par["osdhndlfase"])
    isdhndlfase = float(par["isdhndlfase"])
    name = f"screwdriver_l{l:03.0f}mm" \
            +f"_rh{rhsd*1000:04.0f}mm"
    par_tpl = (rhof, rsdhndl, lsdhndl, nsdhndl, osdhndlfase, isdhndlfase, \
               rtof, rtif, rhsd, l, dwall, lh, nh, ah)
    return par_tpl, name


@njit
def model_function(p):
    x, y, z, par = p

    rhof, rsdhndl, lsdhndl, nsdhndl, osdhndlfase, isdhndlfase, \
    rtof, rtif, rhsd, l, dwall, lh, nh, ah = par

    lt = l + lh

    shaftc = bd.fz_circle((x,y), rhsd+dwall)
    thndl = thrd.fz_thread((x,y,0.1), rsdhndl, nsdhndl, ah, osdhndlfase)
    th = thrd.fz_thread((x,y,0.1), rhsd, nh, ah, rhof)
    head = cmb.fz_and_chamfer(rhof, th, l-z)
    shaft = cmb.fz_and_chamfer(rhof, shaftc, -head, lsdhndl/2-z, z-lt)
    hndl = cmb.fz_and_chamfer(osdhndlfase, thndl, -z, z-lsdhndl)

    if cmb.fz_or_chamfer(isdhndlfase, shaft, hndl) > 0:
        return False
    return True



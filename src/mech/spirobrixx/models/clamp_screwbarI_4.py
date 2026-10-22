#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Stefan Helmert <stefan@entroserv.de>
#
# SPDX-License-Identifier: CERN-OHL-S-2.0


from numba import njit
from fuzzyometry import bodies as bd
from fuzzyometry import threads as thrd
from fuzzyometry import combinations as cmb
import numpy as np

def convert_params(params):
    par = params
    l = float(par["l"])
    w = float(par["w"])
    h = float(par["h"])
    rt4i = float(par["rt4i"])
    pt4 = float(par["pt4"])
    d = float(par["dgrid"])
    rbofase = float(par["rbofase"])
    rtifase = float(par["rtifase"])
    dtp4 = float(par["dtp4"])
    rc = float(par["rc"])
    xc = float(par["xc"])
    yc = float(par["yc"])
    name = f"clamp_screwbarI_4_{l:02}_{w:02}_{h:02}"
    return (rt4i, pt4, d, rbofase, rtifase, l, w, h, dtp4, rc, xc, yc), name


@njit
def model_function(p):
    x, y, z, par = p
    color = 1
    rt4i, pt4, d, rbofase, rtifase, l, w, h, dtp4, rc, xc, yc = par

    rt = rt4i + 2 * dtp4
    rco = rc + d/10

    xd = np.floor(x/d)*d + d/2
    yd = np.floor(y/d)*d + d/2
    xd2 = np.floor(5*x/d)*d/5 + d/10
    yd2 = np.floor(5*y/d)*d/5 + d/10

    xr = x % d - d/2
    yr = y % d - d/2
    zr = z % d - d/2

    tx = thrd.fz_thread((yr,zr,pt4*x-0.25), rt4i, 4, dtp4, 1.0)
    ty = thrd.fz_thread((zr,xr,pt4*y-0.25), rt4i, 4, dtp4, 1.0)
    tz = thrd.fz_thread((xr,yr,pt4*z-0.25), rt4i, 4, dtp4, 1.0)
    txsl = rtifase
    txsu = rtifase
    tysl = rtifase
    tysu = rtifase
    if (xd + d/10*2 - xc)**2 + (yd - yc)**2 < (rco+rt)**2:
        color += 1
        txsu = -xr
    if (xd - d/10*2 - xc)**2 + (yd - yc)**2 < (rco+rt)**2:
        color += 2
        txsl = xr
    if (xd - xc)**2 + (yd + d/10*2 - yc)**2 < (rco+rt)**2:
        color += 4
        tysu = -yr
    if (xd - xc)**2 + (yd - d/10*2 - yc)**2 < (rco+rt)**2:
        color += 8
        tysl = yr
    if (xd - xc)**2 + (yd - yc)**2 < (rco+rt)**2:
        color += 16
        tz = 1000
    if yd + rt > w*d:
        tz = 1000
        tx = 1000
    if xd + rt > l*d:
        tz = 1000
        ty = 1000

    a = bd.fz_cuboid((x-l*d/2,y-w*d/2,z-h*d/2), (l*d,w*d,h*d), rbofase)
    b = bd.fz_circle((x-xc, y-yc), rc)
    bo = bd.fz_circle((x-xc, y-yc), rco)
    txc = cmb.fz_and_chamfer(rtifase, tx, -bo, -txsl, -txsu)
    tyc = cmb.fz_and_chamfer(rtifase, ty, -bo, -tysl, -tysu)
    tzc = cmb.fz_and_chamfer(rtifase, tz, -bo)
    if cmb.fz_and_chamfer(rtifase, a, -b, -txc, -tyc, -tzc) > 0:
        return False

    return color







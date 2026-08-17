#!/usr/bin/env python3

from numba import njit
from fuzzyometry import bodies as bd
from fuzzyometry import threads as thrd
from fuzzyometry import combinations as cmb
import numpy as np

def convert_params(params):
    par = params
    l = int(par["l"])
    w = int(par["w"])
    h = int(par["h"])
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
    txs = rtifase
    tys = rtifase
    if cmb.fz_and_chamfer(rco, abs(yd - yc) - rt - rco, xd - xc - rco + d/10*3) < 0:
        txs = -xr + d/10*3 #- rtifase
    if cmb.fz_and_chamfer(rco, abs(yd - yc) - rt - rco, -xd + xc - rco + d/10*3) < 0:
        txs = xr + d/10*3 #- rtifase
    if cmb.fz_and_chamfer(rco, abs(xd - xc) - rt - rco, yd - yc - rco + d/10*3) < 0:
        tys = -yr + d/10*3 #- rtifase
    if cmb.fz_and_chamfer(rco, abs(xd - xc) - rt - rco, -yd + yc - rco + d/10*3) < 0:
        tys = yr + d/10*3 #- rtifase
    if (xd - xc)**2 + (yd - yc)**2 < (rco+rt)**2:
        tz = 1000

    #rcoa = rc + 1 #rt4i+dtp4/2+rtifase
    #xcdla = np.floor(5*(xc-rcoa)/d)*d/5 - d/10
    #xcdua = np.floor(5*(xc+rcoa)/d+0.99)*d/5 + d/10
    #xcda = (xcdua + xcdla)/2
    #lcda = xcdua - xcdla
    #ycdla = np.floor(5*(yc-rcoa)/d)*d/5 - d/10
    #ycdua = np.floor(5*(yc+rcoa)/d+0.99)*d/5 + d/10
    #ycda = (ycdua + ycdla)/2
    #wcda = ycdua - ycdla
    #rcob = rc + 1 #rt4i+dtp4/2+rtifase
    #xcdlb = np.floor(5*(xc-rcob)/d)*d/5 - d/10
    #xcdub = np.floor(5*(xc+rcob)/d+0.99)*d/5 + d/10
    #xcdb = (xcdub + xcdlb)/2
    #lcdb = xcdub - xcdlb
    #ycdlb = np.floor((yc-rcob)/d)*d - d/2
    #ycdub = np.floor((yc+rcob)/d+0.99)*d + d/2
    #ycdb = (ycdub + ycdlb)/2
    #wcdb = ycdub - ycdlb

    a = bd.fz_cuboid((x-l*d/2,y-w*d/2,z-h*d/2), (l*d,w*d,h*d), rbofase)
    b = bd.fz_circle((x-xc, y-yc), rc) #+ rbofase
    bo = bd.fz_circle((x-xc, y-yc), rco) #+ rbofase
    #cx = bd.fz_cuboid((x-xcda,y-ycdb,z-h*d/2), (lcda, wcdb, h*d), rbofase)
    #cy = bd.fz_cuboid((x-xcdb,y-ycda,z-h*d/2), (lcdb, wcda, h*d), rbofase)
    txc = cmb.fz_and_chamfer(rtifase, tx, -bo, -txs)
    tyc = cmb.fz_and_chamfer(rtifase, ty, -bo, -tys)
    tzc = cmb.fz_and_chamfer(rtifase, tz, -bo)
    if cmb.fz_and_chamfer(rtifase, a, -b, -txc, -tyc, -tzc) > 0:
        return False

    return True







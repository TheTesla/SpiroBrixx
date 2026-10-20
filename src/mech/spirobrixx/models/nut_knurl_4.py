#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Stefan Helmert <stefan@entroserv.de>
#
# SPDX-License-Identifier: CERN-OHL-S-2.0


from numba import njit
from fuzzyometry import bodies as bd
from fuzzyometry import threads as thrd
from fuzzyometry import combinations as cmb
import math
import numpy as np
import sys


def convert_params(params):
    par = params
    rt4i = float(par["rt4i"])
    pt4 = float(par["pt4"])
    rhof = float(par["rhofase"])
    rtif = float(par["rtifase"])
    rh4 = float(par["rh4"])
    l = float(par["l"])
    dtp4 = float(par["dtp4"])
    nh = float(par["nhead"])
    ah = float(par["ahead"])
    name = "nut_knurl_4"
    par_tpl = (rt4i, pt4, rhof, rtif, rh4, l, dtp4, nh, ah)
    return par_tpl, name


@njit
def model_function(p):
    x, y, z, par = p

    rt4i, pt4, rhof, rtif, rh4, l, dtp4, nh, ah = par


    tz = thrd.fz_thread((x,y,pt4*z), rt4i, 4, dtp4, 1.0)
    if nh < 1:
        th = bd.fz_circle((x,y),rh4)
    else:
        th = thrd.fz_thread((x,y,0.1), rh4, nh, ah, rhof)
    head = cmb.fz_and_chamfer(rhof, th, z-l, -z)
    if cmb.fz_and_chamfer(rtif, head, -tz) > 0:
        return False
    return True


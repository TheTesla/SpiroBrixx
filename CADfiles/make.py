#!/usr/bin/env python3

from xyzcad import render

from common.spirostd import output_filename
from models import screwbarL_4, screwbarY_4, screwbarI_4, screwbarI_4X1, \
        screw_knurl_4, screwdriver, screwbarI_4X0, screwbarA_4, \
        screw_knurl_1, screw_flat_1, nut_knurl_1, thin_screwbarA_4,\
        thin_screwbarI_4, thin_screwbarL_4_in, thin_screwbarL_4_out, \
        thin_screwbarLL_4_out, thin_screwbarLL_4_in, thin_screwbarAA_4_out,\
        thin_screwbarAA_4_in, thin_screwbarLA_4_in,\
        thin_screwbarUU_4_in, thin_screwbarUU_4_out, screwdriver, screw_flat_4,\
        thin_screwbarU_4_in, thin_screwbarU_4_out
from profiles import defaultnew

from numba.typed import Dict
from numba import njit

from multiprocessing import Process

import time


profile = defaultnew.__dict__

def convert_params(profile, parameters):
    par = profile | parameters
    l = int(par["l"])
    w = int(par["w"])
    h = int(par["h"])
    rg = float(par["rt4i"])
    ra = float(par["rt4jntsphr"])
    pt4 = float(par["pt4"])
    d = float(par["dgrid"])
    re = float(par["rbofase"])
    rei = float(par["rbifase"])
    rt4q = float(par["rt4icoreq"])
    rge = float(par["rtifase"])
    dtp4 = float(par["dtp4"])
    name = f"_{l:02}_{w:02}_{h:02}"
    return (rg, ra, pt4, d, re, rei, rt4q, rge, l, w, h, dtp4), name


def start_proc(p, max_proc=3):
    while sum([e.is_alive() for e in p]) >= max_proc:
        time.sleep(0.1)
    p[-1].start()

def create_screwbarL_4(profile, parameters):
    params, name = convert_params(profile, parameters)
    render.renderAndSave(screwbarL_4.screwbarL_4,
                         output_filename("screwbarL_4"+name, profile),
                         profile["resolution"], params)
    #f, name = screwbarL_4.new_screwbarL_4(profile, parameters)
    #render.renderAndSave(f, output_filename(name, profile), profile["resolution"])

def create_screwbarY_4(profile, parameters):
    params, name = convert_params(profile, parameters)
    render.renderAndSave(screwbarY_4.screwbarY_4,
                         output_filename("screwbarY_4"+name, profile),
                         profile["resolution"], params)
    #f, name = screwbarY_4.new_screwbarY_4(profile, parameters)
    #render.renderAndSave(f, output_filename(name, profile), profile["resolution"])

def create_screwbarI_4(profile, parameters):
    params, name = convert_params(profile, parameters)
    render.renderAndSave(screwbarI_4.screwbarI_4,
                         output_filename("screwbarI_4"+name, profile),
                         profile["resolution"], params)

def create_screwbarI_4_dict(profile, parameters):
    params, name = convert_params(profile, parameters)
    par = profile | parameters
    parD = Dict()
    for k, v in par.items():
        parD[k] = v
    render.renderAndSave(screwbarI_4_dict.screwbarI_4,
                         output_filename(name, profile),
                         profile["resolution"], parD)

def create_screw_knurl_4(profile, parameters):
    f, name = screw_knurl_4.new_screw_knurl_4(profile, parameters)
    render.renderAndSave(f, output_filename(name, profile), profile["resolution"])

def create_screwdriver(profile, parameters):
    f, name = screwdriver.new_screwdriver(profile, parameters)
    render.renderAndSave(f, output_filename(name, profile), profile["resolution"])

@njit
def screwbar_diff(p):
    #a = screwbarI_4.model_function(p)
    a = screwbarI_4_new.model_function((-p[0]+30, -p[1]+30, p[2], p[3]))
    b = screwbarI_4_new.model_function(p)
    if a and b:
        return 1
    elif a and not b:
        return 2
    elif b and not a:
        return 3
    return 0


def make_model(model, params):
    params, name = model.convert_params(params)
    render.renderAndSave(model.model_function, output_filename(name, profile),
                         profile["resolution"], params)

#parameters = {"l": 1, "w": 1, "h": 1}
#params, name = screwbarI_4_new.convert_params(profile | parameters)
#render.renderAndSave(screwbar_diff, output_filename(name, profile)+"_diff.obj",
#                         profile["resolution"], params)

#t_list = []

#profile["resolution"] = 0.8

#parameters = {"l": 90}
#t = Process(target=create_screwdriver, args=(profile, parameters,))
#t_list.append(t)
#start_proc(t_list)

#for x in range(1,5):
#    print(x)
#    parameters = {"l": x, "w": x, "h": 1}
#    t = Process(target=create_screwbarL_4, args=(profile, parameters,))
#    t_list.append(t)
#    start_proc(t_list)

#for x in range(1,11):
#    print(x)
#    parameters = {"l": 2, "w": 2, "h": x}
#    t = Process(target=create_screwbarL_4, args=(profile, parameters,))
#    t_list.append(t)
#    start_proc(t_list)
#
#for x in range(1,3):
#    print(x)
#    parameters = {"l": x, "w": x, "h": x}
#    t = Process(target=create_screwbarY_4, args=(profile, parameters,))
#    t_list.append(t)
#    start_proc(t_list)
#


parameters = {"l": 5, "w": 3, "h": 2}
profile["resolution"] = 0.8
#make_model(screwbarA_4, profile | parameters)
#make_model(thin_screwbarA_4, profile | parameters)
#make_model(thin_screwbarLL_4_out, profile | parameters)
#make_model(thin_screwbarAA_4_out, profile | parameters)
#make_model(thin_screwbarAA_4_in, profile | parameters)
make_model(thin_screwbarLA_4_in, profile | parameters)
#make_model(thin_screwbarLL_4_in, profile | parameters)



#parameters = {"l": 8, "rtifase": 1.0, "rhofase": 1.0}
#make_model(nut_knurl_1, profile | parameters)
#
#parameters = {"l": 150}
#make_model(screwdriver, profile | parameters)
#for l in [12, 35, 60, 65, 200, 270]:
#    print(f"Screw length: {l} mm")
#    parameters = {"l": l} #, "w": 3, "h": 3}
#    make_model(screw_knurl_1, profile | parameters)
#    make_model(screw_knurl_4, profile | parameters)
#    make_model(screw_flat_4, profile | parameters)
#    make_model(screw_flat_1, profile | parameters)
#
#parameters = {"l": 2, "w": 1, "h": 1}
#make_model(screwbarI_4X0, profile | parameters)
#make_model(screwbarI_4X1, profile | parameters)
#parameters = {"l": 1, "w": 1, "h": 2}
#make_model(screwbarI_4X0, profile | parameters)
#make_model(screwbarI_4X1, profile | parameters)
#parameters = {"l": 2, "w": 1, "h": 2}
#make_model(screwbarI_4X0, profile | parameters)
#make_model(screwbarI_4X1, profile | parameters)
##make_model(screwbarY_4, profile | parameters)
##make_model(screwbarL_4, profile | parameters)
#parameters = {"l": 10, "w": 1, "h": 1}
#make_model(screwbarI_4, profile | parameters)
##make_model(thin_screwbarI_4, profile | parameters)
##make_model(thin_screwbarL_4_in, profile | parameters)
##make_model(thin_screwbarL_4_out, profile | parameters)
##make_model(thin_screwbarUU_4_in, profile | parameters)
##make_model(thin_screwbarUU_4_out, profile | parameters)
#parameters = {"l": 8, "w": 1, "h": 1}
#make_model(thin_screwbarU_4_in, profile | parameters)
#make_model(thin_screwbarU_4_out, profile | parameters)
#parameters = {"l": 2, "w": 1, "h": 1}
#make_model(thin_screwbarU_4_in, profile | parameters)
#make_model(thin_screwbarU_4_out, profile | parameters)
##make_model(screwbarI_4, profile | parameters)
    #create_screwbarI_4_dict(profile, parameters)
    #create_screwbarI_4(profile, parameters)
    #create_screwbarL_4(profile, parameters)
    #create_screwbarY_4(profile, parameters)



#for l in [35, 60, 65, 90, 95]:
#    print(l)
#    parameters = {"l": l}
#    t = Process(target=create_screw_knurl_4, args=(profile, parameters,))
#    t_list.append(t)
#    start_proc(t_list)

#for t in t_list:
#    t.join()


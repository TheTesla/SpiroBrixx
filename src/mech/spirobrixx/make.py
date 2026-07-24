#!/usr/bin/env python3

from numba import njit
import numpy as np
from pathlib import Path
import argparse

from common.spirostd import make_model
from models import screwbarL_4, screwbarY_4, screwbarI_4, screwbarI_4X1, \
        screw_knurl_4, screwdriver, screwbarA_4, \
        screw_headless_4, thin_screwbarO_4_in, thin_screwbarA2_4,\
        screw_knurl_1, screw_flat_1, nut_knurl_1, thin_screwbarA_4,\
        thin_screwbarI_4, thin_screwbarL_4_in, thin_screwbarL_4_out, \
        thin_screwbarLL_4_out, thin_screwbarLL_4_in, thin_screwbarAA_4_out,\
        thin_screwbarAA_4_in, thin_screwbarLA_4_in,\
        thin_screwbarUU_4_in, thin_screwbarUU_4_out, screwdriver, screw_flat_4,\
        thin_screwbarU_4_in, thin_screwbarU_4_out,\
        thin_screwgear_4, screw_special_wsc_1, nut_knurl_special_wsc_1,\
        nut_knurl_special_wsc_4
from profiles import defaultnew

parser = argparse.ArgumentParser()
parser.add_argument("--output_dir", type=Path, required=True)
args = parser.parse_args()
output_dir = args.output_dir


profile = defaultnew.__dict__


profile["target_dir"] = output_dir / profile["target_dir"]

print(f"Output Path: {profile['target_dir']}")

profile["resolution"] = 0.3

# -------- Standard Bars 4 start --------
for l in range(1,12):
    for w in [1, 2, 3, 5]:
        if w >= l:
            parameters = {"l": l, "w": w, "h": 1}
            make_model(screwbarI_4, profile, parameters)

# -------- L Bars 4 start --------
for l in [2, 3, 5]:
    for w in [2, 3, 5]:
        if w >= l:
            parameters = {"l": l, "w": w, "h": 1}
            make_model(screwbarL_4, profile, parameters)

for l in [2]:
    for w in [2]:
        for h in [2, 3, 5, 8, 10, 12]:
            if w >= l:
                parameters = {"l": l, "w": w, "h": h}
                make_model(screwbarL_4, profile, parameters)

# -------- Y Bars 4 start --------
for h in [2, 3, 5]:
    for w in [2, 3, 5]:
        for l in [2, 3, 5, 8]:
            if w >= h and l >= w:
                parameters = {"l": l, "w": w, "h": h}
                make_model(screwbarY_4, profile, parameters)



# -------- Standard Screws 4 start --------
for l in [35, 60, 65, 90, 95]:
    print(f"Screw length: {l} mm")
    parameters = {"l": l, "rtofase": 1, "ns4": 6, "as4": 0.2, "rs4": 2.8 } #, "w": 3, "h": 3}
    make_model(screw_knurl_4, profile, parameters)

# -------- Flat Screws 4 start --------
for l in [60, 65, 90, 95]:
    print(f"Screw length: {l} mm")
    parameters = {"l": l, "rtofase": 1, "ns4": 6, "as4": 0.2, "rs4": 2.8 } #, "w": 3, "h": 3}
    make_model(screw_flat_4, profile, parameters)

# -------- Headless Screws 4 start -----------
for l in [35, 60, 65, 90, 95]:
    print(f"Screw length: {l} mm")
    parameters = {"l": l, "rtofase": 1, "ns4": 6, "as4": 0.2, "rs4": 2.8 } #, "w": 3, "h": 3}
    make_model(screw_headless_4, profile, parameters)

# -------- Screws 1 start -----------
for l in [95]:
    print(f"Screw length: {l} mm")
    parameters = {"l": l, "rtofase": 1, "ns4": 6, "as4": 0.2, "rs4": 2.8 } #, "w": 3, "h": 3}
    make_model(screw_knurl_1, profile, parameters)
    make_model(screw_flat_1, profile, parameters)




parameters = {"l": 3, "w": 3, "h": 1}
profile["resolution"] = 0.3
make_model(screwbarA_4, profile, parameters)




#make_model(thin_screwbarA_4, profile | parameters)
#make_model(thin_screwbarLL_4_out, profile | parameters)
#make_model(thin_screwbarAA_4_out, profile | parameters)
#make_model(thin_screwbarAA_4_in, profile | parameters)
#make_model(thin_screwbarLA_4_in, profile | parameters)
#make_model(thin_screwbarLL_4_in, profile | parameters)


#parameters = {"l": 1, "w": 5, "h": 1}
#make_model(screwbarI_4X0_round, profile, parameters)

#for z in [5, 7, 9, 13, 17, 20, 25,37, 55]:
#for z in [7, 9 ,11, 25, 37, 55, 73]:
#    parameters = {"z": z, "m": 5, "alpha": 20/180*np.pi, "rbofase": 1, "resolution": 0.3}
#    make_model(thin_screwgear_4, profile, parameters)
#parameters = {"l": 5, "w": 1, "h": 1}
#make_model(screwbarI_4, profile, parameters)
#parameters = {"l": 5, "w": 1, "h": 2}
#make_model(screwbarI_4, profile, parameters)
#parameters = {"l": 3, "w": 1, "h": 1}
#make_model(screwbarI_4, profile, parameters)
#parameters = {"l": 2, "w": 2, "h": 1}
#make_model(screwbarL_4, profile, parameters)

#make_model(clamp_screwbarI_4, profile, parameters)
#make_model(screwbar7_4, profile, parameters)

parameters = {"l": 10, "rtifase": 1.0, "rhofase": 1.0}
#make_model(nut_knurl_special_wsc_1, profile, parameters)
make_model(nut_knurl_special_wsc_4, profile, parameters)
#
#parameters = {"l": 150}
#parameters = {"l": 30, "resolution": 0.3}
parameters = {"l": 30, "rtofase": 1, "ns1": 0, "as1": 0.2, "rs1": 5.2 } #, "w": 3, "h": 3}
#make_model(screw_headless_4, profile, parameters)
#make_model(screw_special_wsc_1, profile, parameters)
#make_model(screwdriver, profile | parameters)

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
#parameters = {"l": 5, "w": 3, "h": 1}
#make_model(thin_screwbarA2_4, profile | parameters)
#parameters = {"l": 6, "w": 3, "h": 1}
#make_model(thin_screwbarA2_4, profile | parameters)
#for l in [2,3]:
#    parameters = {"l": l, "w": l, "h": 1}
#    make_model(screwbarA_4, profile | parameters)
#    make_model(thin_screwbarA_4, profile | parameters)
#    make_model(thin_screwbarLL_4_out, profile | parameters)
#    make_model(thin_screwbarAA_4_out, profile | parameters)
#    make_model(thin_screwbarAA_4_in, profile | parameters)
#    make_model(thin_screwbarLA_4_in, profile | parameters)
#    make_model(thin_screwbarLL_4_in, profile | parameters)
    #make_model(screwbarI_4, profile | parameters)
    #make_model(thin_screwbarO_4_in, profile | parameters)
    #make_model(thin_screwbarA2_4, profile | parameters)
    #make_model(thin_screwbarL_4_in, profile | parameters)
    #make_model(thin_screwbarL_4_out, profile | parameters)
##make_model(thin_screwbarI_4, profile | parameters)
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





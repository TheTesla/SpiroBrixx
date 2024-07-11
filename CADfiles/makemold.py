#!/usr/bin/env python3

from xyzcad import render

from common.spirostd import output_filename
from models import screw_knurl_4_mold
from profiles import default

from multiprocessing import Process

import time


profile = default.__dict__

def start_proc(p, max_proc=16):
    while sum([e.is_alive() for e in p]) > max_proc:
        time.sleep(0.1)
    p[-1].start()

def create_screw_knurl_4_mold_h(profile, parameters):
    h, m, t, name = screw_knurl_4_mold.new_screw_knurl_4_mold(profile, parameters)
    render.renderAndSave(h, output_filename(name+"_h", profile), profile["resolution"])

def create_screw_knurl_4_mold_m(profile, parameters):
    h, m, t, name = screw_knurl_4_mold.new_screw_knurl_4_mold(profile, parameters)
    render.renderAndSave(m, output_filename(name+"_m", profile), profile["resolution"])

def create_screw_knurl_4_mold_t(profile, parameters):
    h, m, t, name = screw_knurl_4_mold.new_screw_knurl_4_mold(profile, parameters)
    render.renderAndSave(t, output_filename(name+"_t", profile), profile["resolution"])


t_list = []

for l in [35]:
    print(l)
    parameters = {"l": l}
    th = Process(target=create_screw_knurl_4_mold_h, args=(profile, parameters,))
    t_list.append(th)
    start_proc(t_list)
    tm = Process(target=create_screw_knurl_4_mold_m, args=(profile, parameters,))
    t_list.append(tm)
    start_proc(t_list)
    tt = Process(target=create_screw_knurl_4_mold_t, args=(profile, parameters,))
    t_list.append(tt)
    start_proc(t_list)

for t in t_list:
    t.join()


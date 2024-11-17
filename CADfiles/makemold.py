#!/usr/bin/env python3

from xyzcad import render

from common.spirostd import output_filename
from models import screw_knurl_4_mold
from profiles import default

from multiprocessing import Process

import time


profile = default.__dict__

def start_proc(p, max_proc=0):
    while sum([e.is_alive() for e in p]) > max_proc:
        time.sleep(0.1)
    p[-1].start()

def create_screw_knurl_4_mold(profile, parameters):
    h, name = screw_knurl_4_mold.new_screw_knurl_4_mold(profile, parameters)
    render.renderAndSave(h, output_filename(name, profile), 0.1)

def create_screw_knurl_4_mold_base(profile, parameters):
    h, name = screw_knurl_4_mold.new_screw_knurl_4_mold_base(profile, parameters)
    render.renderAndSave(h, output_filename(name, profile), 0.1)


t_list = []

for l in [35]:
    print(l)
    parameters = {"l": l}
    th = Process(target=create_screw_knurl_4_mold, args=(profile, parameters,))
    t_list.append(th)
    start_proc(t_list)
    tb = Process(target=create_screw_knurl_4_mold_base, args=(profile, parameters,))
    t_list.append(tb)
    start_proc(t_list)

for t in t_list:
    t.join()


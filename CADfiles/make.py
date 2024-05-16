#!/usr/bin/env python3

from xyzcad import render

from common.spirostd import output_filename
from models import screwbarI_4, screw_knurl_4, screwdriver
from profiles import default

from multiprocessing import Process

import time


profile = default.__dict__

def start_proc(p, max_proc=14):
    while sum([e.is_alive() for e in p]) > max_proc:
        time.sleep(0.1)
    p[-1].start()

def create_screwbarI_4(profile, parameters):
    f, name = screwbarI_4.new_screwbarI_4(profile, parameters)
    render.renderAndSave(f, output_filename(name, profile), profile["resolution"])

def create_screw_knurl_4(profile, parameters):
    f, name = screw_knurl_4.new_screw_knurl_4(profile, parameters)
    render.renderAndSave(f, output_filename(name, profile), profile["resolution"])

def create_screwdriver(profile, parameters):
    f, name = screwdriver.new_screwdriver(profile, parameters)
    render.renderAndSave(f, output_filename(name, profile), profile["resolution"])

parameters = {"l": 90}

t_list = []

t = Process(target=create_screwdriver, args=(profile, parameters,))
t_list.append(t)
start_proc(t_list)

for h in range(1,13):
    print(h)
    parameters = {"l": 1, "w": 1, "h": h}
    t = Process(target=create_screwbarI_4, args=(profile, parameters,))
    t_list.append(t)
    start_proc(t_list)

for l in [35, 60, 65, 90, 95, 120]:
    print(l)
    parameters = {"l": l}
    t = Process(target=create_screw_knurl_4, args=(profile, parameters,))
    t_list.append(t)
    start_proc(t_list)

for t in t_list:
    t.join()


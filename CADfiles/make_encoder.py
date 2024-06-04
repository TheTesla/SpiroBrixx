#!/usr/bin/env python3

from xyzcad import render

from common.spirostd import output_filename
from models import encodermountI_4, notched_screwbarI_4, screwbarY_4, screwbarI_4, screw_knurl_4, screwdriver
from profiles import default

from multiprocessing import Process

import time


profile = default.__dict__

def create_encodermountI_4(profile, parameters):
    f, name = encodermountI_4.new_encodermountI_4(profile, parameters)
    render.renderAndSave(f, output_filename(name, profile), 0.2)#profile["resolution"])

def create_notched_screwbarI_4(profile, parameters):
    f, name = notched_screwbarI_4.new_notched_screwbarI_4(profile, parameters)
    render.renderAndSave(f, output_filename(name, profile), 0.7)#profile["resolution"])

parameters = {"l": 5, "w": 2, "h": 1}
#create_encodermountI_4(profile, parameters)
parameters = {"l": 2, "w": 1, "h": 1}
create_notched_screwbarI_4(profile, parameters)


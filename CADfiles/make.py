#!/usr/bin/env python3

from xyzcad import render

from common.spirostd import output_filename
from models import screwbarI_4, screw_knurl_4
from profiles import default

profile = default.__dict__


parameters = {"l": 4, "w": 1, "h": 1}

#f, name = screwbarI_4.new_screwbarI_4(profile, parameters)

#render.renderAndSave(f, output_filename(name, profile), profile["resolution"])

parameters = {"l": 35}

f, name = screw_knurl_4.new_screw_knurl_4(profile, parameters)

render.renderAndSave(f, output_filename(name, profile), profile["resolution"])


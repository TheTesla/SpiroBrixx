#!/usr/bin/env python3

from xyzcad import render

from common.spirostd import output_filename
from models import screwbarI_4, screw_knurl_4
from profiles import default

profile = default.__dict__

for h in range(1,4):
    parameters = {"l": 1, "w": 1, "h": h}
    f, name = screwbarI_4.new_screwbarI_4(profile, parameters)
    render.renderAndSave(f, output_filename(name, profile), profile["resolution"])


for l in [35, 60, 65, 90, 95, 120]:
    parameters = {"l": l}
    f, name = screw_knurl_4.new_screw_knurl_4(profile, parameters)
    render.renderAndSave(f, output_filename(name, profile), profile["resolution"])


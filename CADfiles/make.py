#!/usr/bin/env python3

from xyzcad import render

from models import screwbarI_4
from profiles import default

profile = default.__dict__


parameters = {"l": 4, "w": 1, "h": 1}

f = screwbarI_4.new_screwbarI_4(profile, parameters)

render.renderAndSave(f, f'build/test.stl', profile["resolution"])


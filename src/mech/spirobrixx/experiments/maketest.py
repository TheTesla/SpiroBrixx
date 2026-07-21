#!/usr/bin/env python3

from xyzcad import render

from common.spirostd import output_filename
from models import screw_knurl_4_mold
from profiles import default


import time


profile = default.__dict__

def create_screw_knurl_4_mold(profile, parameters):
    h, name = screw_knurl_4_mold.new_screw_knurl_4_mold(profile, parameters)
    render.renderAndSave(h, output_filename(name, profile), 0.1)



l = 35
parameters = {"l": l}
create_screw_knurl_4_mold(profile, parameters)


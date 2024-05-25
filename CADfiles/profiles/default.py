

resolution = 0.2
extension = "stl"
target_dir = "build"


# four-start thread radius
pt4 = 1/6 # pitch
pt4od = 0.9 # thread of screw shortened, absolute value
pt4odr = 0.000 # thread of screw shortened, relative value

rt4 = 10 # radius
rt4od = -0.3 # smaler screw radius
rt4id = +0.1 # bigger nut radius
rt4ocoreq = 1.5
rt4icoreq = rt4ocoreq
rt4jntsphr = 12
rh4 = 13

rt4o = rt4 + rt4od
rt4i = rt4 + rt4id
rt4ocore = rt4o/rt4ocoreq
rt4icore = rt4i/rt4icoreq


# one-start thread radius
pt1 = 4/6
rt1 = 10
rt1od = +0.1
rt1id = -0.1
rt1ocoreq = 1.5

rt1o = rt1 + rt1od
rt1i = rt1 + rt1id
rt1ocore = rt1i/rt1ocoreq


# dimensions
dgrid = 30
dwall = 3


# fases
rbofase = 3
rbifase = 2
rtifase = 4
#rtofase = 3



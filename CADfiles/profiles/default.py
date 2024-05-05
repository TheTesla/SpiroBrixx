

resolution = 0.2
extension = "stl"
target_dir = "build"


# four-start thread radius
pt4 = 1/6
pt4od = 5.3
rt4 = 10
rt4od = -0.3
rt4id = +0.1
rt4ocoreq = 1.3
rt4jntsphr = 12

rt4o = rt4 + rt4od
rt4i = rt4 + rt4id
rt4ocore = rt4/rt4ocoreq


# one-start thread radius
pt1 = 4/6
rt1 = 10
rt1od = +0.1
rt1id = -0.1
rt1ocoreq = 1.3

rt1o = rt1 + rt1od
rt1i = rt1 + rt1id
rt1ocore = rt1/rt1ocoreq


# dimensions
dgrid = 30
dwall = 3


# fases
rbofase = 3
rbifase = 2
rtifase = 3
#rtofase = 3



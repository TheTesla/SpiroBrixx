

resolution = 0.2
extension = "stl"
target_dir = "build"


# four-start thread radius
pt4 = 1/6 # pitch
pt4od = 0.9 # thread of screw shortened, absolute value
pt4odr = 0.000 # thread of screw shortened, relative value

rt4 = 7.76 # radius
rt4od = -0.225 # smaler screw radius
rt4id = +0.08 # bigger nut radius
rt4ocoreq = 1.5
rt4icoreq = rt4ocoreq
rt4jntsphr = 12
dtp4 = 1.6

# flat screw
ds4 = 10.0 # thickness

rt4o = rt4 + rt4od
rt4i = rt4 + rt4id
rt4ocore = rt4o/rt4ocoreq
rt4icore = rt4i/rt4icoreq


# one-start thread radius
pt1 = pt4
pt1od = 1.0
pt1odr = 0.000

rt1 = rt4
rt1od = rt4od
rt1id = rt4id
rt1ocoreq = rt4ocoreq
dtp1 = dtp4

rt1o = rt1 + rt1od
rt1i = rt1 + rt1id
rt1ocore = rt1i/rt1ocoreq



# dimensions
dgrid = 30
dwall = 3


# fases
rbofase = 3
rbifase = 2
rtifase = 3
rtofase = 3
rtofasec = 1 # fase at cut of flat screw

# screw head
lhead = 14
nhead = 32
ahead = 0.5
rhofase = 2.5
rh4 = 12.5
rh1 = 12.5


rhsd = rh4 + 0.1
rsdhndl = 25
lsdhndl = 50
nsdhndl = 48
osdhndlfase = 9
isdhndlfase = 6

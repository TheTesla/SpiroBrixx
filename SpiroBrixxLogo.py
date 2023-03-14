#!/usr/bin/env python3

import drawsvg as draw

x = 5
k = 1
ra = 4
c = 'black'
w = 2.5

d = draw.Drawing(205, 40, origin=(-89,-21), displayInline=False)
m = draw.Mask('mask')


r = draw.Rectangle(-10, -10, 20, 20, rx=ra, fill='#ffffff', stroke_width=w, stroke=c)
d.append(r)

d.append(draw.Circle(0, 0, 10-x, fill='white', stroke_width=w, stroke=c))

p = draw.Path(stroke_width=w, stroke=c, fill='black', fill_opacity=0)
p.M(0-x*k, -10)
p.C(5.5-x, -10, 10-x, -5.5, 10-x, 0)
d.append(p)
p = draw.Path(stroke_width=w, stroke=c, fill='black', fill_opacity=0)
p.M(0+x*k, 10.0)
p.C(-5.5+x, 10.0, -10.0+x, 5.5, -10.0+x, 0)
d.append(p)
p = draw.Path(stroke_width=w, stroke=c, fill='black', fill_opacity=0)
p.M(0, 10.0-x)
p.C(5.5, 10.0-x, 10.0, 5.5-x, 10.0, 0-x*k)
d.append(p)
p = draw.Path(stroke_width=w, stroke=c, fill='black', fill_opacity=0)
p.M(0, -10.0+x)
p.C(-5.5, -10.0+x, -10.0, -5.5+x, -10.0, 0+x*k)
d.append(p)

for i in [0,1]:
    x = i * 15 +90
    p = draw.Path(stroke_width=w, stroke=c, fill='black', fill_opacity=0)
    p.M(x-30.0, 0)
    p.C(x, 35.0, x, -35.0, x+30.0, 0)
    d.append(p)
    p.M(x-30.0, 0)
    p.C(x, -35.0, x, 35.0, x+30.0, 0)
    d.append(p)

r = draw.Rectangle(55, -20, 25, 50, fill='none', stroke_width=w, stroke='#ffffff')
m.append(r)
r = draw.Rectangle(115, -20, 25, 50, fill='#ffffff', stroke_width=w, stroke='#ffffff')
d.append(r)

p = draw.Text('Spir', 40, -95, 10, fill='black', style="font-family: osifont")
d.append(p)
p = draw.Text('Bri', 40, 16, 10, fill='black', style="font-family: osifont")
d.append(p)

d.append(m)

d.set_pixel_scale(2)

d.save_svg('SpiroBrixxLogo.svg')
d.save_png('SpiroBrixxLogo.png')


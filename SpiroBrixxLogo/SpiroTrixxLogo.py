#!/usr/bin/env python3

import drawsvg as draw

x = 5
k = 1
ra = 4
c = 'black'
w = 2.5
ls = -5.5 +2
ws = 5
xxp = 0


ws += ls -5
d = draw.Drawing(220+10*ls+ws+xxp, 41, origin=(-99-11*ls/2-1,-21), displayInline=False)
clip = draw.ClipPath()

r = draw.Rectangle(-10, -10, 20, 20, rx=ra, fill='none', stroke_width=w, stroke=c)
d.append(r)

d.append(draw.Circle(0, 0, 10-x, fill='none', stroke_width=w, stroke=c))

r = draw.Rectangle((115+55-7)/2+3*ls+ws+xxp, -20, 25+7, 50)
clip.append(r)

p = draw.Path(stroke_width=w, stroke=c, fill=c, fill_opacity=0)
p.M(0-x*k, -10)
p.C(5.5-x, -10, 10-x, -5.5, 10-x, 0)
d.append(p)
p = draw.Path(stroke_width=w, stroke=c, fill=c, fill_opacity=0)
p.M(0+x*k, 10.0)
p.C(-5.5+x, 10.0, -10.0+x, 5.5, -10.0+x, 0)
d.append(p)
p = draw.Path(stroke_width=w, stroke=c, fill=c, fill_opacity=0)
p.M(0, 10.0-x)
p.C(5.5, 10.0-x, 10.0, 5.5-x, 10.0, 0-x*k)
d.append(p)
p = draw.Path(stroke_width=w, stroke=c, fill=c, fill_opacity=0)
p.M(0, -10.0+x)
p.C(-5.5, -10.0+x, -10.0, -5.5+x, -10.0, 0+x*k)
d.append(p)

for i in [0,1]:
    x = i * 15 +90+3*ls+ws + xxp
    p = draw.Path(stroke_width=w, stroke=c, fill=c, fill_opacity=0,
            clip_path=clip)
    p.M(x-30.0, 0)
    p.C(x, 35.0, x, -35.0, x+30.0, 0)
    d.append(p)
    p.M(x-30.0, 0)
    p.C(x, -35.0, x, 35.0, x+30.0, 0)
    d.append(p)


p = draw.Text('Spir', 40, -101-4*ls, 10, fill=c, style="font-family: osifont",
        letter_spacing=ls)
d.append(p)
p = draw.Text('Tri', 40, 18+ws, 10, fill=c, style="font-family: osifont",
        letter_spacing=ls)
d.append(p)

d.set_pixel_scale(2)

d.save_svg('SpiroTrixxLogo.svg')
d.save_png('SpiroTrixxLogo.png')


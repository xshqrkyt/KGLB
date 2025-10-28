import numpy as np
from math import cos, sin, pi
import math
import random as rnd
from PIL import Image, ImageOps
import time
img_mat = np.zeros((2000, 2000, 3), dtype=np.uint8)
z = []
for i in range(2000):

    z.append([])
    for j in range(2000):
        z[i].append(10000000)


def barcordcheck(x, y, x0, y0, x1, y1, x2, y2):
    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2))/((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2))/((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda2 = 1.0 - lambda0 - lambda1
    return lambda0 >= 0 and lambda1 >= 0 and lambda2 >= 0


def normal(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    return np.cross([x1 - x2, y1 - y2, z1 - z2], [x1-x0, y1-y0, z1-z0])

def zboof(x, y, x0, y0, z0, x1, y1, z1, x2, y2, z2):
    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda2 = 1.0 - lambda0 - lambda1
    return z0*lambda0 + z1*lambda1 + z2*lambda2

def normalcheck(n):
    l = [0, 0, 1]
    return ((n[0]*l[0] + n[1]*l[1] + n[2]*l[2])/(math.sqrt(n[0]**2 + n[1]**2 + n[2]**2)*math.sqrt(l[0]**2 + l[1]**2 + l[2]**2))) < 0
def endzone(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    lx = [x0, x1, x2]
    ly = [y0, y1, y2]
    for i in range(3):
        if lx[i] < 0:
            lx[i] = 0
        if ly[i] < 0:
            ly[i] = 0
        if lx[i] > 2000 - 1:
            lx[i] = 2000 - 1
        if ly[i] > 2000 - 1:
            ly[i] = 2000 - 1
    xmin = int(min(lx))
    xmax = int(max(lx))
    ymin = int(min(ly))
    ymax = int(max(ly))
    n = normal(x0, y0, z0, x1, y1, z1, x2, y2, z2)
    l = [0, 0, 1]
    if normalcheck(n):
        color = int((rnd.choice([0])))
        cpower = int(-255*((n[0] * l[0] + n[1] * l[1] + n[2] * l[2]) / (
                    math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2) * math.sqrt(l[0] ** 2 + l[1] ** 2 + l[2] ** 2))))
        for i in range(xmin, xmax + 1):
            for j in range(ymin, ymax + 1):
                if barcordcheck(i, j, x0, y0, x1, y1, x2, y2):
                    zb = zboof(i, j, x0, y0, z0, x1, y1, z1, x2, y2, z2)
                    if  zb < z[i][j]:
                        z[i][j] = zb
                        img_mat[j, i, color] = cpower






file = open('model_1.obj')
v = []
vt = []
vn = []
f = []
for s in file:
    sp = s.split()
    if(sp[0]=='v'):
        v.append([float(sp[1]), float(sp[2]), float(sp[3])])
        # img_mat[(int(8000*float(sp[2])) + 1000), (int(float(sp[1])*8000 + 1000))] = 255
    if (sp[0] == 'vt'):
        vt.append([sp[1], sp[2]])
    if (sp[0] == 'vn'):
        vn.append([sp[1], sp[2], sp[3]])
    if (sp[0] == 'f'):
        f.append([int(sp[1].split('/')[0]),int(sp[2].split('/')[0]), int(sp[3].split('/')[0])])
# for k in range(13):
#     x0, y0 = 100, 100
#     x1 = int(100 + 95 * cos(2 * pi * k / 13))
#     y1 = int(100 + 95 * sin(2 * pi * k / 13))
#     #draw_line(img_mat, x0, y0, x1, y1)
#     #x_loop_line(img_mat, x0, y0, int(x1), int(y1))
#     #x_loop_line_fixed1(img_mat, x0, y0, int(x1), int(y1))
#     #x_loop_line_fixed2(img_mat, x0, y0, int(x1), int(y1))
#     #x_loop_fin(img_mat, x0, y0, int(x1), int(y1))
#     draw_line2(img_mat, x0, y0, x1, y1)
for k in range(len(f)):
    x0 = v[f[k][0]-1][0]
    y0 = v[f[k][0] - 1][1]
    z0 = v[f[k][0] - 1][2]
    x1 = v[f[k][1] - 1][0]
    y1 = v[f[k][1] - 1][1]
    z1 = v[f[k][1] - 1][2]
    x2 = v[f[k][2] - 1][0]
    y2 = v[f[k][2] - 1][1]
    z2 = v[f[k][2] - 1][2]
    endzone(x0*9000 + 1000, y0*9000 + 1000,z0*9000 + 1000, x1*9000 + 1000, y1*9000 + 1000, z1*9000 + 1000, x2*9000 + 1000, y2*9000 + 1000, z2*9000 + 1000)



img = Image.fromarray(img_mat, mode="RGB")
img = ImageOps.flip(img)
img.save("img3.png")

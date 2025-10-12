import numpy as np
from math import cos, sin, pi
import math
import random as rnd
from PIL import Image, ImageOps
import time
img_mat = np.zeros((2000, 2000, 3), dtype=np.uint8)



def draw_line2(image, x0, y0, x1, y1, color=255):
    y = y0
    dy = 2 * abs(y1 - y0)
    derror = 0.0
    y_update = 1 if y1 > y0 else -1
    xchange = False
    if (abs(x0 - x1) < abs(y0 - y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if (x0 > x1):
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    for x in range(x0, x1):
        t = (x - x0) / (x1 - x0)
        y = round((1.0 - t) * y0 + t * y1)
        if (xchange):
            image[x, y] = color
        else:
            image[y, x] = color
        derror += dy
        if (derror > (x1 - x0)):
            derror -= 2 * (x1 - x0)
            y += y_update
start_time = time.time()
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
for k in range(len(f)):
    x0 = v[f[k][0]-1][0]
    y0 = v[f[k][0] - 1][1]
    x1 = v[f[k][1] - 1][0]
    y1 = v[f[k][1] - 1][1]
    x2 = v[f[k][2] - 1][0]
    y2 = v[f[k][2] - 1][1]
    draw_line2(img_mat, int(x0*9000 + 1000), int(y0*9000 + 1000), int(x1*9000 + 1000), int(y1*9000 + 1000))
    draw_line2(img_mat, int(x1 * 9000 + 1000), int(y1 * 9000 + 1000), int(x2 * 9000 + 1000), int(y2 * 9000 + 1000))
    draw_line2(img_mat, int(x0 * 9000 + 1000), int(y0 * 9000 + 1000), int(x2 * 9000 + 1000), int(y2 * 9000 + 1000))


#for k in range(13):
    #x0, y0 = 100, 100
    #x1 = int(100 + 95 * cos(2 * pi * k / 13))
    #y1 = int(100 + 95 * sin(2 * pi * k / 13))
    #draw_line(img_mat, x0, y0, x1, y1)
    #x_loop_line(img_mat, x0, y0, int(x1), int(y1))
    #x_loop_line_fixed1(img_mat, x0, y0, int(x1), int(y1))
    #x_loop_line_fixed2(img_mat, x0, y0, int(x1), int(y1))
    #x_loop_fin(img_mat, x0, y0, int(x1), int(y1))
    #draw_line2(img_mat, x0, y0, x1, y1)
#print("--- %s seconds ---" % (time.time() - start_time))
img = Image.fromarray(img_mat, mode="RGB")
img = ImageOps.flip(img)
img.save("img.png")

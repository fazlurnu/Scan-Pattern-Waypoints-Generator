# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 22:16:23 2020

@author: My Laptop
"""

import matplotlib.pyplot as plt
from math import atan2, tan, sqrt, pow, cos, sin
from numpy import rad2deg, deg2rad

orientation = 45
xStart = 2
yStart = 1
line1 = [(xStart,yStart), (xStart + 1 * cos(deg2rad(orientation)), yStart + 1 * sin(deg2rad(orientation)))]
clearance = 0.5

lines = []
lines.append(line1)

for i in range (3):
    lines.append([])
    for point in line1:
        x1, y1 = point
        x2 = x1 + (i+1) * clearance * cos(deg2rad(orientation+90))
        y2 = y1 + (i+1) * clearance * sin(deg2rad(orientation+90))
        
        lines[i+1].append((x2, y2))
        
for line in lines:
    x = [line[0][0], line[1][0]]
    y = [line[0][1], line[1][1]]
    
    plt.plot(x, y, "-r*")
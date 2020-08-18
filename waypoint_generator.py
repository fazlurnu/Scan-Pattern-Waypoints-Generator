# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:11:01 2020

@author: My Laptop
"""

import matplotlib.pyplot as plt
from math import atan2
from numpy import rad2deg, deg2rad

def drawROI(ROI):
    x = []
    y = []
    
    for points in ROI:
        x.append(points[0])
        y.append(points[1])
        
    plt.plot(x, y, "-r.", linewidth = 2, markersize = 10)
    plt.title("Grid Scan Waypoint Generator")
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    
def getOrientation(ROI):
    point1 = ROI[0]
    point2 = ROI[1]
    diffX = point2[0] - point1[0]
    diffY = point2[1] - point1[1]
    
    orientation = atan2(diffY, diffX)
    
    return orientation
    
def main(ROI, orientation=None):
    
    if (ROI[-1] != ROI[0]):
        ROI.insert(len(ROI), ROI[0])
        
    if(orientation==None):
        orientation = getOrientation(ROI)
        print(rad2deg(orientation))
    else:
        print(orientation)
        
    drawROI(ROI)
    
if __name__ == "__main__":
    ROI = [(0,0), (1,1), (2,3), (1,3), (0,2)]
    main(ROI)
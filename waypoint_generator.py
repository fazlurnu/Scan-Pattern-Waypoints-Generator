# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:11:01 2020

@author: My Laptop
"""

import matplotlib.pyplot as plt
from math import atan2, tan
from numpy import rad2deg, deg2rad

clearance = 0.5

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

def getGradient(orientation):
    return tan(orientation)
    
def getFurthestX(ROI):
    furthestX = 0
    for point in ROI:
        if(point[0] > furthestX):
            furthestX = point[0]
            
    return furthestX

def drawScanLines(ROI, gradient):
    for i in range(5):    
        x1 = ROI[0][0]
        y1 = ROI[0][0]+clearance*(i+1)
        point1 = (x1, y1)
        x2 = getFurthestX(ROI)
        point2 = (x2, gradient*x2 + clearance*(i+1))
        
        x = [point1[0], point2[0]]
        y = [point1[1], point2[1]]
        
        plt.plot(x, y, "-b.", linewidth = 2, markersize = 10)
        plt.title("Grid Scan Waypoint Generator")
        plt.xlabel("x-axis")
        plt.ylabel("y-axis")
        
def main(ROI, orientation = None):
    
    if (ROI[-1] != ROI[0]):
        ROI.insert(len(ROI), ROI[0])
    
    if(orientation==None):
        orientation = getOrientation(ROI)
        print(rad2deg(orientation))
    else:
        print(rad2deg(orientation))
        
    gradient = getGradient(orientation)
    
    drawROI(ROI)
    drawScanLines(ROI, gradient)    
    
if __name__ == "__main__":
    ROI = [(0,0), (1,1.2), (2.1,3), (0.75,3), (0,2)]
    main(ROI)
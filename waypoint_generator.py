# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:11:01 2020

@author: My Laptop
"""

import matplotlib.pyplot as plt

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
    
def main(ROI):
    
    if (ROI[-1] != ROI[0]):
        ROI.insert(len(ROI), ROI[0])
        
    drawROI(ROI)
    
if __name__ == "__main__":
    ROI = [(0,0), (0,1), (1,2), (2,3)]
    main(ROI)
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:11:01 2020

@author: My Laptop
"""

import matplotlib.pyplot as plt
from math import atan2, tan, sqrt, pow
from numpy import rad2deg, deg2rad

clearance = 0.5

def drawROI(ROI):
    x = []
    y = []
    
    for points in ROI:
        x.append(points[0])
        y.append(points[1])
        
    plt.plot(x, y, "-c.", linewidth = 2, markersize = 10)
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
    if tan(orientation) != 0:
        return tan(orientation)
    else:
        return tan(orientation) + 0.00001
    
def getMaxX(ROI):
    maxX = 0
    for point in ROI:
        if(point[0] > maxX):
            maxX = point[0]
            
    return maxX

def getMinX(ROI):
    minX = 1000
    for point in ROI:
        if(point[0] < minX):
            minX = point[0]
            
    return minX

def getMaxY(ROI):
    maxY = 0
    for point in ROI:
        if(point[1] > maxY):
            maxY = point[1]
            
    return maxY

def getMinY(ROI):
    minY = 1000
    for point in ROI:
        if(point[1] < minY):
            minY = point[1]
            
    return minY

def getROILines(ROI):
    ROILines = []

    for i in range(len(ROI)-1):
        point1 = ROI[i]
        point2 = ROI[i+1]

        line = (point1, point2)
        ROILines.append(line)

    return ROILines

def getScanLines(ROI, gradient, display = False):
    scanLines = []
    
    for i in range(8):    
        x1 = getMinX(ROI)
        y1 = getMinY(ROI)+clearance*(i)
        point1 = (x1, y1)
        x2 = getMaxX(ROI)
        point2 = (x2, gradient*x2 + clearance*(i))
        
        x = [point1[0], point2[0]]
        y = [point1[1], point2[1]]
        
        scanLines.append((point1, point2))
        
        if (display):
            plt.plot(x, y, "-b.", linewidth = 2, markersize = 10)
            plt.title("Grid Scan Waypoint Generator")
            plt.xlabel("x-axis")
            plt.ylabel("y-axis")
    
    return scanLines
    
def getIntersectionPoint(line1, line2):
    x1,y1 = line1[0]
    x2,y2 = line1[1]
    x3,y3 = line2[0]
    x4,y4 = line2[1]

    numeratorX = (x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4)
    numeratorY = (x1*y2-y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
    denum = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)

    xIntersect = numeratorX/denum
    yIntersect = numeratorY/denum

    return xIntersect, yIntersect

def distance(point1, point2):
    diffX = point1[0] - point2[0]
    diffY = point1[1] - point2[1]
    
    return sqrt(pow(diffX, 2) + pow(diffY, 2))
    
    
def pointIsInScanLine(point, line):
    tolerance = 0.00001
    
    point1 = line[0]
    point2 = line[1]
    
    distance1 = distance(point1, point) + distance(point2, point)
    distance2 = distance(point1, point2)
    
    if (distance1 - distance2 < abs(tolerance)):
        return True
    else:
        return False
    
def getIntersectionPoints(ROILines, scanLines, display = False):
    intersectionPoints = []
    
    for i in range(len(scanLines)):
        for j in range(len(ROILines)):
            intersectionPoint = getIntersectionPoint(scanLines[i], ROILines[j])
            
            cond = pointIsInScanLine(intersectionPoint, scanLines[i])
            cond2 = pointIsInScanLine(intersectionPoint, ROILines[j])
            
            if (cond and cond2):
                intersectionPoints.append(intersectionPoint)
                
                if (display):
                    plt.plot(intersectionPoint[0], intersectionPoint[1], "g*")
                
                    index = str(len(intersectionPoints))
                    plt.text(intersectionPoint[0]+0.01, intersectionPoint[1]+0.01, s = index)
                
    return intersectionPoints

def getWaypoints(intersectionPoints):
    waypoints = []
    counter = 0
    while(len(intersectionPoints) > 0):
        if (counter % 2 == 0):
            point1 = intersectionPoints.pop(1)
            point2 = intersectionPoints.pop(0)
            
        else:
            point1 = intersectionPoints.pop(0)
            point2 = intersectionPoints.pop(0)
            
        waypoints.append(point1)
        waypoints.append(point2)
        
        counter+=1
    
    for i in range(len(waypoints) - 1):
        x1,y1 = waypoints[i]
        x2,y2 = waypoints[i+1]
        
        plt.plot([x1,x2], [y1,y2], "-k*")
        index = str(i)
        
        plt.text(x1+0.01, y1+0.01, s = index, color = 'b')
        
    return waypoints

def main(ROI, orientation = None):
    
    if (ROI[-1] != ROI[0]):
        ROI.insert(len(ROI), ROI[0])
    
    if(orientation==None):
        orientation = getOrientation(ROI)
        
    gradient = getGradient(orientation)
    
    drawROI(ROI)
    scanLines = getScanLines(ROI, gradient, display=False)
    ROILines = getROILines(ROI)
    intersectionPoints = getIntersectionPoints(ROILines, scanLines)
    waypoints = getWaypoints(intersectionPoints)
    #print(intersectionPoints)
    

        
if __name__ == "__main__":
    ROI = [(0.1,0.1), (0.5,0.1), (2.1,3), (0.75,4), (0,2)]
    main(ROI, deg2rad(40))
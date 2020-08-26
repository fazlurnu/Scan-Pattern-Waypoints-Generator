# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:11:01 2020

@author: My Laptop
"""

import matplotlib.pyplot as plt
from math import atan2, tan, sqrt, pow, cos, sin
from math import pi as M_PI
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
        return tan(orientation)
    
def getMaxX(ROI):
    maxX = 0
    outerPoint = (0,0)
    
    for point in ROI:
        if(point[0] > maxX):
            maxX = point[0]
            outerPoint = point
            
    return outerPoint

def getMinX(ROI):
    minX = 1000
    outerPoint = (1000, 1000)
    
    for point in ROI:
        if(point[0] < minX):
            minX = point[0]
            outerPoint = point
            
    return outerPoint

def getMaxY(ROI):
    maxY = 0
    outerPoint = (0,0)
    for point in ROI:
        if(point[1] > maxY):
            maxY = point[1]
            outerPoint = point
            
    return outerPoint

def getMinY(ROI):
    minY = 1000
    outerPoint = (1000, 1000)
    for point in ROI:
        if(point[1] < minY):
            minY = point[1]
            outerPoint = point
            
    return outerPoint

def getROILines(ROI):
    ROILines = []

    for i in range(len(ROI)-1):
        point1 = ROI[i]
        point2 = ROI[i+1]

        line = (point1, point2)
        ROILines.append(line)

    return ROILines

def getScanLines(ROI, orientation, display = False):
    scanLinesTop = []
    scanLinesDown = []

    length = 3*(getMaxX(ROI)[0] - getMinX(ROI)[0])

    counter = 0
    
    centroidPoint = getCentroid(ROI)
    xCentroid, yCentroid = centroidPoint
    
    xStart1 = xCentroid - length/2 * cos(orientation)
    yStart1 = yCentroid - length/2 * sin(orientation)
    xStart2 = xStart1 + length * cos(orientation)
    yStart2 = yStart1 + length * sin(orientation)
    
    line1 = [(xStart1 ,yStart1), (xStart2, yStart2)]
    
    scanLinesTop.append(line1)
    
    maxDistance = 0
    for point in ROI:
        distPoint2Centroid = distance(point, centroidPoint)
        if (distPoint2Centroid > maxDistance):
            maxDistance = distPoint2Centroid
        
    outerScanLines1 = scanLinesTop[0]
    distanceScanlineToCentroid = getDistanceLineToPoint(outerScanLines1, centroidPoint)
    
    while (distanceScanlineToCentroid < maxDistance):
        scanLinesTop.append([])
        scanLinesDown.append([])
        counter += 1
        
        for point in line1:
            x1, y1 = point
            x2 = x1 + counter * clearance * cos(orientation + M_PI/2)
            y2 = y1 + counter * clearance * sin(orientation + M_PI/2)
            
            scanLinesTop[-1].append((x2, y2))
            
        for point in line1:
            x1, y1 = point
            x2 = x1 - counter * clearance * cos(orientation + M_PI/2)
            y2 = y1 - counter * clearance * sin(orientation + M_PI/2)
            
            scanLinesDown[-1].append((x2, y2))
        
        outerScanLines1 = scanLinesTop[-1]
        distanceScanlineToCentroid = abs(getDistanceLineToPoint(outerScanLines1, centroidPoint))
        
    scanLinesTopReversed = []
    
    for i in range(len(scanLinesTop)-1, -1, -1):
        scanLinesTopReversed.append(scanLinesTop[i])
        
    if (display):
        for i, line in enumerate(scanLinesTopReversed):
            x = (line[0][0], line[1][0])
            y = (line[0][1], line[1][1])
            plt.plot(x, y, "-b.", linewidth = 2, markersize = 10)
            plt.title("Grid Scan Waypoint Generator")
            plt.xlabel("x-axis")
            plt.ylabel("y-axis")
            
            index = (i)
            plt.text(x[0]+0.01, y[0]+0.01, s = index)
            
        for i, line in enumerate(scanLinesDown):
            x = (line[0][0], line[1][0])
            y = (line[0][1], line[1][1])
            plt.plot(x, y, "-g.", linewidth = 2, markersize = 10)
            plt.title("Grid Scan Waypoint Generator")
            plt.xlabel("x-axis")
            plt.ylabel("y-axis")
            
            index = (i)
            plt.text(x[0]+0.01, y[0]+0.01, s = index)
    
    return scanLinesTopReversed + scanLinesDown
    
def getCentroid(ROI):
    xTotal = 0
    yTotal = 0
    n = len(ROI)
    
    for point in ROI:
        x, y = point
        xTotal += x
        yTotal += y
        
    return (xTotal/n, yTotal/n)

def getIntersectionPoint(line1, line2):
    x1,y1 = line1[0]
    x2,y2 = line1[1]
    x3,y3 = line2[0]
    x4,y4 = line2[1]

    numeratorX = (x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4)
    numeratorY = (x1*y2-y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
    
    denum = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
    
    if (denum == 0):
        denum = 1

    xIntersect = numeratorX/denum
    yIntersect = numeratorY/denum

    return xIntersect, yIntersect

def getDistanceLineToPoint(line, point):
    x0, y0 = point
    x1, y1 = line[0]
    x2, y2 = line[1]
    
    numerator = (y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1
    denum = distance((x1, y1), (x2, y2))

    return numerator/denum
    
def distance(point1, point2):
    diffX = point1[0] - point2[0]
    diffY = point1[1] - point2[1]
    
    return sqrt(pow(diffX, 2) + pow(diffY, 2))
    
    
def pointIsInScanLine(point, line):
    tolerance = 0.01
    
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
    tolerance = 0.01
    
    for i in range(len(scanLines)):
        for j in range(len(ROILines)):
            intersectionPoint = getIntersectionPoint(scanLines[i], ROILines[j])
            
            cond = pointIsInScanLine(intersectionPoint, scanLines[i])
            cond2 = pointIsInScanLine(intersectionPoint, ROILines[j])
            
            if (cond and cond2):
                isInIntersectionPoints = False
                
                for point in intersectionPoints:
                    pointDistance = distance(intersectionPoint, point)
                    
                    if (pointDistance < tolerance):
                        isInIntersectionPoints = isInIntersectionPoints or True
                        
                if (not isInIntersectionPoints):
                    intersectionPoints.append(intersectionPoint)
                
                if (display):
                    plt.plot(intersectionPoint[0], intersectionPoint[1], "g*")
                
                    index = str(i) + ", " + str(j)
                    print(intersectionPoint)
                    plt.text(intersectionPoint[0]+0.01, intersectionPoint[1]+0.01, s = index)
                
    return intersectionPoints

def getWaypoints(intersectionPoints, display = True):
    waypoints = []
    counter = 1
    while(len(intersectionPoints) > 1):
        if (counter % 2 == 0):
            point1 = intersectionPoints.pop(1)
            point2 = intersectionPoints.pop(0)
        else:
            point1 = intersectionPoints.pop(0)
            point2 = intersectionPoints.pop(0)
            
        if (point1 not in waypoints):
            waypoints.append(point1)
        if (point2 not in waypoints):
            waypoints.append(point2)
        
        counter+=1
    
    if (display):
        for i in range(len(waypoints) - 1 ):
            x1,y1 = waypoints[i]
            x2,y2 = waypoints[i+1]
            
            plt.plot([x1,x2], [y1,y2], "-k*")
            clearanceDisplay = 0.5
            rangePlot = [getMinX(ROI)[0]- clearanceDisplay, getMaxX(ROI)[0] + clearanceDisplay, getMinY(ROI)[1] - clearanceDisplay, getMaxY(ROI)[1] + clearanceDisplay]
            plt.axis(rangePlot)
            index = str(i)
            
            plt.text(x1+0.01, y1+0.01, s = index, color = 'b')
        
    return waypoints

def main(ROI, orientation = None):
    
    if (ROI[-1] != ROI[0]):
        ROI.insert(len(ROI), ROI[0])
    
    if(orientation==None):
        orientation = getOrientation(ROI)
        
    drawROI(ROI)
    scanLines = getScanLines(ROI, orientation, display=True)
    ROILines = getROILines(ROI)
    intersectionPoints = getIntersectionPoints(ROILines, scanLines, display=True)
    waypoints = getWaypoints(intersectionPoints, display=False)
    #print(intersectionPoints)
    

        
if __name__ == "__main__":
    ROI = [(2,-2), (2.8,3), (0.75,5), (0,2), (0.1,-1.1)]
    #ROI = [(0,0), (1, 0), (1, 1.1), (0,1.1)]
    #for i in range(10, 80, 10):
    #    fig = plt.figure(str(i))
    
    main(ROI, deg2rad(90))
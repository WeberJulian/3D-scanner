# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:04:30 2018

@author: Julian Weber
"""

# Format point = [(x,y,z), (r,g,b)] or point = (x,y,z)
# Format cloud = [point1, point2, ...]

# Exemple cloud = [(1.45,2.23,3.94), (2.21,3.18,4.87), (3.14,4.65,5.17)]
# Exemple cloud = [[(1.45,2.23,3.94), (50,255,10)], [(2.21,3.18,4.87), (60,25,100)], [(3.14,4.65,5.17), (50,55,255)]]

import numpy as np

def converter(cloud):
    numberOfPoint = len(cloud)
    header = """ply
format ascii 1.0
element vertex %d
property float x
property float y
property float z
property uchar diffuse_red
property uchar diffuse_green
property uchar diffuse_blue
end_header
""" %(numberOfPoint)
    body = ''
    if type(cloud[0]) == tuple :
        for i in range(numberOfPoint):
            body = body + """%f %f %f
"""%(cloud[i][0], cloud[i][1], cloud[i][2])
        file = header + body
    else:
        for i in range(numberOfPoint):
            body = body + """%f %f %f %d %d %d
"""%(cloud[i][0][0], cloud[i][0][1], cloud[i][0][2], cloud[i][1][0], cloud[i][1][1], cloud[i][1][2])
        file = header + body
    return file
        
def translate(cloud, vect):
    cloud2 = []
    for i in range(len(cloud)):
        cloud2.append([(cloud[i][0][0]+vect[0], cloud[i][0][1]+vect[1], cloud[i][0][2]+vect[2]), (cloud[i][1][0], cloud[i][1][1], cloud[i][1][2])])
    return cloud2

def coord(point):
    return [point[0][0], point[0][1], point[0][2]]

def rotate(cloud, ax, ay, az):
    nbPoints = len(cloud)
    c, s = np.cos(ax), np.sin(ax)
    Rx = np.array((((1, 0, 0), (0, c, -s), (0, s, c))))
    c, s = np.cos(ay), np.sin(ay)
    Ry = np.array((((c, 0, s), (0, 1, 0), (-s, 0, c))))
    c, s = np.cos(az), np.sin(az)
    Rz = np.array((((c, -s, 0), (s, c, 0), (0, 0, 1))))
    for i in range(nbPoints):
        point = coord(cloud[i])
        point = np.matmul(Rx, point)
        point = np.matmul(Ry, point)
        point = np.matmul(Rz, point)
        cloud[i] = [(point[0], point[1], point[2]), (cloud[i][1][0], cloud[i][1][1], cloud[i][1][2])]     
    return cloud

def calculateCenter(cloud):
    avg = [0,0,0]
    nbPoints = len(cloud)
    for i in range(nbPoints):
        avg[0] += cloud[i][0][0]
        avg[1] += cloud[i][0][1] 
        avg[2] += cloud[i][0][2] 
    avg = np.array([avg[0]/nbPoints, avg[1]/nbPoints, avg[2]/nbPoints])
    return avg

def move(cloud, w):
    x, y, z, ax, ay, az = w[0], w[1], w[2], w[3], w[4], w[5]
    #return rotate(translate(cloud, (x,y,z)),ax,ay,az)
    return translate(rotate(np.copy(cloud),ax,ay,az), (x,y,z))

def evaluation(cloud, cloud2, every):
    score = 0
    for i in range(len(cloud2)):
        for j in range(0, len(cloud), every):
            score += dist(cloud[j][0],cloud2[i][0])*(dist(cloud[j][1],cloud2[i][1])/65025+1)
    return score/every/10000

def dist(u, v):
    return (u[0]-v[0])*(u[0]-v[0])+(u[1]-v[1])*(u[1]-v[1])+(u[2]-v[2])*(u[2]-v[2])


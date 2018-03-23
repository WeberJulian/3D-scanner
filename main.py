# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 14:19:38 2018

@author: Julian Weber
"""
# Format point = [(x,y,z), (r,g,b)] or point = (x,y,z)
# Format cloud = [point1, point2, ...]

# Exemple cloud = [(1.45,2.23,3.94), (2.21,3.18,4.87), (3.14,4.65,5.17)]
# Exemple cloud = [[(1.45,2.23,3.94), (50,255,10)], [(2.21,3.18,4.87), (60,25,100)], [(3.14,4.65,5.17), (50,55,255)]]

import PointCloudHandler as pch
import random as rd
import numpy as np
import time as ti


def evaluation(cloud, cloud2, every):
    score = 0
    for i in range(len(cloud2)):
        for j in range(0, len(cloud), every):
            score += dist(cloud[j][0],cloud2[i][0])*dist(cloud[j][1],cloud2[i][1])
    return score

def dist(u, v):
    return (u[0]-v[0])*(u[0]-v[0])+(u[1]-v[1])*(u[1]-v[1])+(u[2]-v[2])*(u[2]-v[2])


def genererPave():
    cloud = []
    for k in range(400):
        for i in range(5):
            cloud.append([(rd.random()*2-1,rd.random()*2-1,k/100),(255,255-int(k/400*255),int(k/400*255))])
    return cloud

# Generation du pavé
time = ti.clock()
cloud = genererPave()
cloud2 = pch.move(cloud, 3, -4, 10, np.pi/2, np.pi/3, np.pi/3)
text = pch.converter(cloud+cloud2)
print(evaluation(cloud, cloud2, 8))
file = open("file.ply", "w")
file.write(text)
file.close()
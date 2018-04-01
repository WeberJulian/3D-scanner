# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 13:27:34 2018

@author: Julian Weber
"""

import PointCloudHandler as pch
import numpy as np

def moveVect(w, n):
    vect = [0,0,0,0,0,0]
    vect[n] = w[n]
    return vect

def gradiant(cloud, cloud2, every, w, prev):
    distance = []
    for i in range(6):
        dist = (prev - pch.evaluation(cloud, pch.move(cloud2, moveVect(w,i)), every))/w[i]
        distance.append(dist)
    return np.array(distance)

def gradiantDescent(w, n, threshold, every, cloud, cloud2, maxIteration):
    i = 0
    newDist = pch.evaluation(cloud, pch.move(cloud2,w), 100)
    prevDist = newDist
    history = [w]
    print("itération %d, loss : %f"%(i, newDist))
    while prevDist >= newDist and i < maxIteration and newDist > threshold:
        w = w - n * gradiant(cloud, cloud2, every, w, newDist)
        prevDist = newDist
        newDist = pch.evaluation(cloud, pch.move(cloud2,w), 100)
        history.append(w)
        i += 1
        print("itération %d, loss : %f"%(i, newDist))
    return history[i-1]
    
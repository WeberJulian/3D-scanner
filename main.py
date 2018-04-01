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
import Optimization as opti

def genererPave():
    cloud = []
    for k in range(400):
        for i in range(5):
            cloud.append([(rd.random()*2-1,rd.random()*2-1,k/100),(255,255-int(k/400*255),int(k/400*255))])
    return cloud

# Generation du pavé
cloud = genererPave()
# On crée un deuxième nuage qui est le résultat d'une transformation sur le premier
cloud2 = pch.move(cloud, [-5, -2, -3, np.pi/8, np.pi/6, np.pi/7])

# On écrit les deux nuages dans un fichier PLY
text = pch.converter(cloud+cloud2)
file = open("input.ply", "w")
file.write(text)
file.close()

#On initialise le vecteur translation
w = [rd.random()/10,rd.random()/10,rd.random()/10,rd.random()/10,rd.random()/10,rd.random()/10]
#Learning rate
n = 0.1
maxIteration = 50
print("Situation initiale, distance : %f"%(pch.evaluation(cloud, cloud2, 100)))

#On utilise la descente de gradiant pour essayer de superposer les nuages
w = opti.gradiantDescent(w, n, 0.1, 100, cloud, cloud2, maxIteration)


print("Situation finale, distance : %f"%(pch.evaluation(cloud, pch.move(cloud2,w), 100)))
print(w)

#On écrit la situation finale dans un PLY
cloud2 = pch.move(cloud, w)
text = pch.converter(cloud+cloud2)
file = open("output.ply", "w")
file.write(text)
file.close()

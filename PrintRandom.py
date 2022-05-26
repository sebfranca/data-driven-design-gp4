# -*- coding: utf-8 -*-
"""
Created on Thu May 26 16:21:54 2022

@author: sebas
"""
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np


with open('C:/Users/sebas/Documents/Ecole/EPFL/Master4/Cours/DataDrivenDesign/Project/Librairies/Abaqus_results/Tables/Random_values.pkl','rb') as file:
    res = pickle.load(file)

min_poisson = min(res['poisson'])
idxp = np.argmin(res['poisson'])
max_volume = max([v if v<1e5 else 0 for i,v in enumerate(res['volume'])])
idxv = np.argmin(res['volume'])

print("Minimal poisson ratio = {} \nObtained at \nAngle {} \nTd {} \nTv {} \nX {} \nY {} \n \n \n".format(
    min_poisson,
    res['diag_strut_angle'][idxp],
    res['diag_thickness'][idxp],
    res['vert_thickness'][idxp],
    res['nb_cells_x'][idxp],
    res['nb_cells_y'][idxp]    
    ))
print("Maximal volume = {} \nObtained at \nAngle {} \nTd {} \nTv {} \nX {} \nY {}".format(
    max_volume,
    res['diag_strut_angle'][idxv],
    res['diag_thickness'][idxv],
    res['vert_thickness'][idxv],
    res['nb_cells_x'][idxv],
    res['nb_cells_y'][idxv]    
    ))


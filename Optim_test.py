# -*- coding: utf-8 -*-
"""
Created on Fri May  6 15:44:47 2022

@author: cedri
"""
import sys
sys.path.append('Librairies')
from helper_functions import *
from sys import path
path.append('C:/Users/cedri/anaconda3/Lib/site-packages')

import numpy as np

from AuxeticOptimization import *
import subprocess



aux_opt = AuxeticOptimization()

bounds = {'nb_cells_x': {'lower': 5,
                         'upper': 10},
          'nb_cells_y': {'lower': 5,
                         'upper': 10},
          'AR': {'lower': 1,
                  'upper': 6}}

params = {'bounds': bounds,
          'acquisition_type': 'EI',
          'acquisition_weight': .4,
          'max_iter': 20,
          'max_time': None,
          'eps': 1e-8,
          'verbosity': True,
          'tolerance': 1e-8,
          'kappa': 1.96,                # The higher, the more exploration
          'xi': 1e-2,                   # Controls how much improvement we want over the previous value
          'mode': 'real'}                    

material = {'E': 2.5e6,
            'density':1,
            'nu': .33}

aux_opt.optimParams(params=params,
                    objective_scaling_Poisson=1, # to be changed according to the study
                    objective_scaling_surface=0, # to be changed according to the study
                    textile_dimensions=(50,50),
                    load_value=10,
                    material=material,
                    optimizer='skopt',
                    load=True)

aux_opt.train_skopt()

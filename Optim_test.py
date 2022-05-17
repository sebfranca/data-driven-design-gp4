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
          'strut_angle': {'lower': 70,
                          'upper': 80}}

params = {'bounds': bounds,
          'acquisition_type': 'EI',
          'acquisition_weight': .4,
          'max_iter': 10,
          'max_time': None,
          'eps': 1e-8,
          'verbosity': True,
          'tolerance': 1e-8}

material = {'E': 2e6,
            'density':1,
            'nu': .33}

aux_opt.optimParams(params=params,
                    objective_scaling=1,
                    textile_dimensions=(50,50),
                    load_value=10,
                    material=material,
                    optimizer='skopt')

aux_opt.train_skopt()

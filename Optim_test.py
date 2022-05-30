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
import os



aux_opt = AuxeticOptimization()

bounds = {'nb_cells_x': {'lower': 4,
                         'upper': 15},
          'nb_cells_y': {'lower': 2,
                         'upper': 10},
          'AR': {'lower': 2,
                  'upper': 10}}

params = {'bounds': bounds,
          'acquisition_type': 'gp_hedge',
          'max_iter': 200, # Number of bayesian opt. iterations
          'eps': 1e-8, # Stopping tolerance, not important
          'verbosity': True,
          'kappa': 1.96,                # The higher, the more exploration
          'xi': 5e-2,                   # Controls how much improvement we want over the previous value
          'mode': 'real',
          'remove_fails': True,
          'n_jobs': 12,
          'nb_iter_wo_save': 20}                    

material = {'E': 3.3e3,
            'density':1.14e-9,
            'nu': .41}

aux_opt.optimParams(params=params,
                    objective_scaling_Poisson=1, # to be changed according to the study
                    objective_scaling_surface=0, # to be changed according to the study
                    textile_dimensions=(50,50),
                    load_value=10, # load in Newton
                    material=material,
                    optimizer='skopt', 
                    load=False, # False : re-start and overwrite, True : load ancient optimization
                    result_folder_name='poisson_only_gphedge') # Name of the file, to be changed if a new
                                                           # optimization is requested, put old name
                                                           # if old optim. to be reloaded

aux_opt.train_skopt()

subprocess.run(["Librairies/rm_rpy_rec"], shell=True)

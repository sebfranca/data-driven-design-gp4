# -*- coding: utf-8 -*-
"""
Created on Fri May  6 15:44:47 2022

@author: cedri
"""
import sys
sys.path.append('Librairies')
from helper_functions import *
from sys import path
path.append('C:/Users/sebas/Lib/site-packages')

import numpy as np

from AuxeticOptimization import *
import subprocess

mode = 'random' #'optimizing' or 'sensitivity' or 'random'

if mode=='optimizing':

    aux_opt = AuxeticOptimization()
    
    bounds = {'nb_cells_x': {'lower': 5,
                             'upper': 10},
              'nb_cells_y': {'lower': 5,
                             'upper': 10},
              'AR': {'lower': 1,
                      'upper': 8}}
    
    params = {'bounds': bounds,
              'acquisition_type': 'EI',
              'acquisition_weight': .4, # Supposed to change explor/exploit ratio (check in skopt doc)
              'max_iter': 100, # Number of bayesian opt. iterations
              'max_time': None,
              'eps': 1e-8, # Stopping tolerance, not important
              'verbosity': True,
              'tolerance': 1e-8,
              'kappa': 1.96,                # The higher, the more exploration
              'xi': 1e-2,                   # Controls how much improvement we want over the previous value
              'mode': 'real'}                    
    
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
                        result_folder_name='Obj_poisson_only') # Name of the file, to be changed if a new
                                                               # optimization is requested, put old name
                                                               # if old optim. to be reloaded

    aux_opt.train_skopt()

if mode=='sensitivity':
    aux_opt = AuxeticOptimization()
    
    # bounds = {'nb_cells_x': {'lower': 5,
    #                          'upper': 10},
    #           'nb_cells_y': {'lower': 5,
    #                          'upper': 10},
    #           'AR': {'lower': 1,
    #                   'upper': 8}}
    num_grid = 3
    n_samples = 2 #for random search
    
    
    
    params = { 'verbosity': True,
              'mode':'real'
              }                    
    
    material = {'E': 3.3e3,
                'density':1.14e-9,
                'nu': .41}
    
    aux_opt.optimParams(   min_diag_strut_angle = 50,
                           max_diag_strut_angle = 89,
                           num_diag_strut_angle = num_grid,
                           min_diag_strut_thickness    = 0.5,
                           max_diag_strut_thickness    = 2,
                           num_diag_strut_thickness    = num_grid,
                           min_vert_strut_thickness    = 0.5,
                           max_vert_strut_thickness    = 2,
                           num_vert_strut_thickness    = num_grid,
                           min_nb_cells_x     = 2,
                           max_nb_cells_x     = 10,
                           min_nb_cells_y     = 2,
                           max_nb_cells_y     = 10,
        
                        params=params,
                        objective_scaling_Poisson=1, # to be changed according to the study
                        objective_scaling_surface=1, # to be changed according to the study
                        textile_dimensions=(50,50),
                        load_value=10, # load in Newton
                        material=material,
                        optimizer='sensitivity', 
                        load=False, # False : re-start and overwrite, True : load ancient optimization
                        result_folder_name='Sensitivity') # Name of the file, to be changed if a new
                                                               # optimization is requested, put old name
                                                               # if old optim. to be reloaded

    aux_opt.run_sensitivity()
    
if mode=='random':
    aux_opt = AuxeticOptimization()
    
    # bounds = {'nb_cells_x': {'lower': 5,
    #                          'upper': 10},
    #           'nb_cells_y': {'lower': 5,
    #                          'upper': 10},
    #           'AR': {'lower': 1,
    #                   'upper': 8}}
    n_samples = 2 #for random search
    
    
    
    params = { 'verbosity': True,
              'mode':'real'
              }                    
    
    material = {'E': 3.3e3,
                'density':1.14e-9,
                'nu': .41}
    
    aux_opt.optimParams(   min_diag_strut_angle = 50,
                           max_diag_strut_angle = 89,
                           min_diag_strut_thickness    = 0.5,
                           max_diag_strut_thickness    = 2,
                           min_vert_strut_thickness    = 0.5,
                           max_vert_strut_thickness    = 2,
                           min_nb_cells_x     = 2,
                           max_nb_cells_x     = 10,
                           min_nb_cells_y     = 2,
                           max_nb_cells_y     = 10,
        
                        params=params,
                        objective_scaling_Poisson=1, # to be changed according to the study
                        objective_scaling_surface=1, # to be changed according to the study
                        textile_dimensions=(50,50),
                        load_value=10, # load in Newton
                        material=material,
                        optimizer='sensitivity', 
                        load=False, # False : re-start and overwrite, True : load ancient optimization
                        israndom = True,
                        n_samples = n_samples,
                        result_folder_name='Random') # Name of the file, to be changed if a new
                                                               # optimization is requested, put old name
                                                               # if old optim. to be reloaded

    aux_opt.run_sensitivity()
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 09:41:44 2022

@author: cedri
"""

import sys

sys.path.append('Librairies')

from PyAuxeticWrapper import *

aux_anal = AuxeticAnalysis()

# vert_strut_thickness = 2
# diag_strut_thickness = 2

# unit_cell_params={'vert_strut_thickness': vert_strut_thickness,
#                 'diag_strut_thickness': diag_strut_thickness,
#                 'diag_strut_angle': diag_strut_angle,
#                 'extrusion_depth': 2,
#                 'nb_cells_x': nb_cells_x,
#                 'nb_cells_y': nb_cells_y}


aux_anal.defineParams(unit_cell_params={'vert_strut_thickness': 1.5,
                                        'diag_strut_thickness': 1.5,
                                        'diag_strut_angle': 60,
                                        'extrusion_depth': 2,
                                        'nb_cells_x': 2,
                                        'nb_cells_y': 2},
                      textile_dimensions=(20,20),
                      load_direction='x',
                      load_type='force',
                      load_value=10,
                      seed_size=.2,
                      time_period=1.0  ,
                      init_inc_size=0.1 ,
                      min_inc_size=0.05,
                      max_inc_size=0.1 ,
                      max_num_inc=100,
                      num_cpus=6,
                      material={'E': 2e6,
                                'nu': .33,
                                'density': 1},
                      export_ribbon_width=4,
                      result_folder_name='Test2')

aux_anal.createAnalysis()       
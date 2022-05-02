# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 09:41:44 2022

@author: cedri
"""

import sys

sys.path.append('Librairies')

from PyAuxeticWrapper import *

aux_anal = AuxeticAnalysis()

aux_anal.defineParams(unit_cell_params={'vert_strut_thickness': .5,
                                        'diag_strut_thickness': .5,
                                        'diag_strut_angle': 60,
                                        'extrusion_depth': 2,
                                        'vert_bounding_box': 3,
                                        'horz_bounding_box': 3},
                      cast_dimensions=(50,50),
                      load_direction='x',
                      load_type='disp',
                      load_value=1,
                      seed_size=.1,
                      num_cpus=6,
                      material={'E': 70e9,
                                'nu': .33,
                                'density': 1},
                      export_ribbon_width=4,
                      result_folder_name='Test2')

aux_anal.createAnalysis()   
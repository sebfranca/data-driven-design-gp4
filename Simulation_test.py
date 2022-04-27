# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 09:41:44 2022

@author: cedri
"""

from PyAuxeticWrapper import *

aux_anal = AuxeticAnalysis()

aux_anal.defineParams(unit_cell_params={'vert_strut_thickness': 2,
                                        'diag_strut_thickness': 1.5,
                                        'diag_strut_angle': 70,
                                        # 'aspect_ratio': ,
                                        'extrusion_depth': 5,
                                        'vert_bounding_box': 24,
                                        'horz_bounding_box': 20},
                      num_cell_repeat= (8,3),
                      load_direction='x',
                      load_value=20,
                      material={'E': 70e9,
                                'nu': .33,
                                'density': 1},
                      export_ribbon_width=4,
                      result_folder_name='Test1')

aux_anal.createAnalysis()   
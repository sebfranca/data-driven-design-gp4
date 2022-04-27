# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 08:38:37 2022

@author: cedri
"""

import numpy as np
import sys
import os
from helper_functions import *

# Import the necessary libraries:
pyauxetic_library_path = 'C:/SIMULIA/Abaqus/6.14-1/code/python2.7/lib/abaqus_plugins/pyauxetic-main'
command_path = 'C:/SIMULIA/Abaqus/Commands'
abaqus_path = 'C:/SIMULIA/Abaqus/6.14-1/cod/python2.7/lib'
sys.path.append(pyauxetic_library_path)
sys.path.append(command_path)
sys.path.append(abaqus_path)

from pyauxetic.classes.auxetic_unit_cell_params import *
from pyauxetic.classes.auxetic_structure_params import *
from pyauxetic.main import main_single

structure_type = 'reentrant2d_planar_shell'
structure_name = 'reentrant_planar_test_1'
folder_name = structure_name

setPath = os.path.join(r'C://Users//cedri//OneDrive//Documents//Mécanique\ -\ EPFL//Master\ IV//Data-driven-design-and-fabrication-methods//Abaqus_results//', 
                       structure_name)

if not os.path.exists(setPath):
    os.makedirs(setPath)
    
os.chdir(setPath)

## A single set of unit cell parameters:
# Method 1:
unit_cell_params = Reentrant2DUcpBox(
    id                   = 1  ,
    extrusion_depth      = 5  ,
    horz_bounding_box    = 20 ,
    vert_bounding_box    = 24 ,
    vert_strut_thickness = 2  ,
    diag_strut_thickness = 1.5,
    diag_strut_angle     = 70
    )

## A list of unit cell parameters:
# Define three unit cells for a non-uniform structure or a batch of uniform structures.
# Note that the first argument (id) is unique for each unit cell.
unit_cell_params_list = []
# (id, extrusion_depth, horz_bounding_box, vert_bounding_box,
#  vert_strut_thickness, diag_strut_thickness, diag_strut_angle)
unit_cell_params_list.append( Reentrant2DUcpBox(1, 5, 20, 24, 3.0, 1.5, 60) )
unit_cell_params_list.append( Reentrant2DUcpBox(2, 5, 20, 24, 3.0, 1.5, 60) )
unit_cell_params_list.append( Reentrant2DUcpBox(3, 5, 20, 24, 2.0, 1.5, 60) )

# Defining the structure of auxetic cells
# Uniform structure (i.e. with only 1 type of cell)
pattern_params = PatternParams(
  pattern_mode    = 'uniform',
  num_cell_repeat = (8, 3)   ,
  structure_map   = None
)

pattern_params = PatternParams(
    pattern_mode = 'uniform',
    num_cell_repeat = (8,3)
    )

# Non-uniform structure, with many cells IDs which must be defined before
# structure_map = np.array([
#     [1, 2, 4, 9, 10, 8, 7, 4, 2, 2],
#     [1, 2, 4, 9, 10, 8, 1, 4, 2, 2],
#     [1, 2, 4, 9, 10, 8, 7, 4, 2, 2],
#     [1, 2, 4, 9, 10, 8, 7, 4, 2, 2],
# ])

# Define the PatternParams object.
# structure_map must be flipped and transposed because of the way
# python iterates over it.
# Note that num_cell_repeat is set to None.
# pattern_params = PatternParams(
#   pattern_mode    = 'nonuniform',
#   num_cell_repeat = None        ,
#   structure_map   = np.fliplr( structure_map.T )
# )

# Define the LoadingParams object.
loading_params = LoadingParams(
    type      = 'disp',
    direction = 'x'   ,
    data      = 20.0
)

E, nu = 70e9, .3
material_params = MaterialParams(
    density      = 1.00,
    elastic = (E, nu)
    )

step_params = StepParams(
    time_period   = 0.1  ,
    init_inc_size = 0.01 ,
    min_inc_size  = 0.005,
    max_inc_size  = 0.05 ,
    max_num_inc   = 10000
)

job_params = JobParams(
    description          = 'This is a sample job.',
    numCpus              = 4 ,
    memoryPercent        = 80,
    explicitPrecision    = 'SINGLE',
    nodalOutputPrecision = 'SINGLE',
)

loading_params = LoadingParams(
    type      = 'disp',
    direction = 'x'   ,
    data      = 20.0
)

mesh_params = MeshParams(
    seed_size    = 1.0       ,
    elem_shape   = 'QUAD'    ,
    elem_code    = ('CPE4H') ,
    elem_library = 'STANDARD'
)

output_params = OutputParams(
    result_folder_name     = folder_name,
    save_cae               = True,
    save_odb               = True,
    save_job_files         = True,
    export_ribbon_width    = 4.0 ,
    export_stl             = True,
    export_stp             = True
)

run_analysis = True


auxeticObj = main_single(structure_type  , structure_name,
                         unit_cell_params, pattern_params,
                         material_params ,                
                         loading_params  , mesh_params   ,
                         job_params      , output_params ,
                         step_params     , run_analysis)

# subprocess.call("C:\SIMULIA\Abaqus\Commands\abq6141.bat python cae noGUI=Cast_simulation_V1.py")
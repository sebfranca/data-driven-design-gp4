# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 08:37:18 2022

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

class AuxeticAnalysis:
    
    def __init__(self):
        LOG('Define analysis')
    
    def defineParams(self, 
                     unit_cell_params,
                     cast_dimensions,
                     load_direction,
                     load_value,
                     material,
                     export_ribbon_width,
                     result_folder_name,
                     load_type='disp',
                     uniform=True,
                     time_period=1.0  ,
                     init_inc_size=0.1 ,
                     min_inc_size=0.05,
                     max_inc_size=0.1 ,
                     max_num_inc=100,
                     job_description='Sample job',
                     num_cpus=4,
                     max_memory_percent=80,
                     elem_shape='QUAD',
                     elem_code='CPE4H',
                     save_cae=False,
                     export_stl=False,
                     export_stp=False
                     ):
        
        self.unit_cell_params_list       = unit_cell_params
        self.cast_dimensions             = cast_dimensions
        self.load_type                   = load_type
        self.load_direction              = load_direction
        self.load_value                  = load_value
        self.material                    = material
        self.export_ribbon_width         = export_ribbon_width
        self.result_folder_name          = result_folder_name
        self.uniform                     = uniform
        self.load_type                   = load_type
        self.time_period                 = time_period
        self.init_inc_size               = init_inc_size
        self.min_inc_size                = min_inc_size
        self.max_inc_size                = max_inc_size
        self.max_num_inc                 = max_num_inc
        self.job_description             = job_description
        self.num_cpus                    = num_cpus
        self.max_memory_percent          = max_memory_percent
        self.elem_shape                  = elem_shape
        self.elem_code                   = elem_code
        self.save_cae                    = save_cae
        self.export_stl                  = export_stl
        self.export_stp                  = export_stp
        
    def createAnalysis(self):
        
        self.setDirectory() # Set working directory
        
        if self.uniform: 
            self.vert_strut_thickness       = self.unit_cell_params_list['vert_strut_thickness']
            self.diag_strut_thickness       = self.unit_cell_params_list['diag_strut_thickness']
            self.diag_strut_angle           = self.unit_cell_params_list['diag_strut_angle']
            # self.aspect_ratio               = self.unit_cell_params_list['aspect_ratio']
            self.extrusion_depth            = self.unit_cell_params_list['extrusion_depth']
            self.horz_bounding_box          = self.unit_cell_params_list['horz_bounding_box']
            self.vert_bounding_box          = self.unit_cell_params_list['vert_bounding_box']
            
            
        
            self.unit_cell_params = Reentrant2DUcpBox(
                id                   = 1  ,
                extrusion_depth      = self.extrusion_depth  ,
                horz_bounding_box    = self.horz_bounding_box ,
                vert_bounding_box    = self.vert_bounding_box ,
                vert_strut_thickness = self.vert_strut_thickness  ,
                diag_strut_thickness = self.diag_strut_thickness,
                diag_strut_angle     = self.diag_strut_angle
                )
            
            pattern_params = PatternParams(
              pattern_mode    = 'uniform',
              num_cell_repeat = self.estimateNbCells(),
              structure_map   = None
            )
            
        loading_params = LoadingParams(
            type      = self.load_type,
            direction = self.load_direction,
            data      = self.load_value
        )
        
        material_params = MaterialParams(
            density      = self.material['density'],
            elastic = (self.material['E'], self.material['nu'])
            )
        
        step_params = StepParams(
            time_period   = self.time_period  ,
            init_inc_size = self.init_inc_size ,
            min_inc_size  = self.min_inc_size,
            max_inc_size  = self.max_inc_size ,
            max_num_inc   = self.max_num_inc
        )
        
        job_params = JobParams(
            description          = self.job_description,
            numCpus              = self.num_cpus ,
            memoryPercent        = self.max_memory_percent,
            explicitPrecision    = 'SINGLE',
            nodalOutputPrecision = 'SINGLE',
        )
        
        mesh_params = MeshParams(
            seed_size    = 1.0       ,
            elem_shape   = self.elem_shape    ,
            elem_code    = (self.elem_code) ,
            elem_library = 'STANDARD'
        )
        
        output_params = OutputParams(
            result_folder_name     = self.result_folder_name,
            save_cae               = self.save_cae,
            save_odb               = True,
            save_job_files         = True,
            export_ribbon_width    = self.export_ribbon_width ,
            export_stl             = self.export_stl,
            export_stp             = self.export_stp
        )
        
        run_analysis = True
        structure_type = 'reentrant2d_planar_shell'
        structure_name = 'reentrant_planar'
        
        auxeticObj = main_single(structure_type  , structure_name,
                                 self.unit_cell_params, pattern_params,
                                 material_params ,                
                                 loading_params  , mesh_params   ,
                                 job_params      , output_params ,
                                 step_params     , run_analysis)
        
        results = auxeticObj.output_table
        
        output_table_labels = ['Inc', 'Time',
                               'U_ld', 'U_td_mean', 'U_td_midpoint',
                               'strain_ld', 'strain_td_mean', 'strain_td_midpoint',
                               'poisson_midpoint', 'poisson_mean']
        
        self.output = {label: results[i] for i, label in enumerate(output_table_labels)}
        
        try:
            with open(os.path.join(os.getcwd(),'results.txt'),'w+') as file:
                file.write(str(self.output))
        except IOerror as e:
            LOG(e)
            
        LOG(os.getcwd())
        
    def setDirectory(self):
        
        setPath = os.path.join('../Abaqus_results', 
                               self.result_folder_name)
        
        if not os.path.exists(setPath):
            LOG('does not exist')
            os.makedirs(setPath)
            
        os.chdir(setPath)
        
        try:
            with open(os.path.join(os.getcwd(),'log.txt'),'w+') as file:
                file.write('Analysis started')
                LOG('Successfully written file')
            file.close()
        except IOError as e:
            LOG(e)
            
    def estimateNbCells(self):
        
        x_dim, y_dim = self.cast_dimensions[0], self.cast_dimensions[1]
        
        nb_x = np.floor(x_dim / self.horz_bounding_box)
        nb_y = np.floor(y_dim / self.vert_bounding_box)
        
        self.residual_x = x_dim - nb_x * self.horz_bounding_box
        self.residual_y = y_dim - nb_y * self.vert_bounding_box
        
        return (nb_x,nb_y)



# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 08:37:18 2022

@author: cedri
"""

import numpy as np
import sys
import os
import pickle, io, json
from helper_functions import *

# Import the necessary libraries:
# pyauxetic_library_path = 'C:/SIMULIA/Abaqus/6.14-1/code/python2.7/lib/abaqus_plugins/pyauxetic-main'
pyauxetic_library_path = os.path.join(os.getcwd(),'pyauxetic-main')
command_path = 'C:/SIMULIA/Abaqus/Commands'
abaqus_path = 'C:/SIMULIA/Abaqus/6.14-1/code/python2.7/lib'
sys.path.append(pyauxetic_library_path)
sys.path.append(command_path)
sys.path.append(abaqus_path)



class AuxeticAnalysis:
    
    def __init__(self):
        LOG('Define analysis')
    
    def defineParams(self, 
                     unit_cell_params,
                     textile_dimensions,
                     load_value,
                     material,
                     load_direction='x',
                     export_ribbon_width=5,
                     result_folder_name='analysis',
                     load_type='force',
                     uniform=True,
                     time_period=1.0,
                     init_inc_size=0.1,
                     min_inc_size=0.001,
                     max_inc_size=0.1,
                     max_num_inc=100,
                     job_description='Sample job',
                     num_cpus=4,
                     max_memory_percent=80,
                     seed_size=1,
                     elem_shape='QUAD',
                     elem_code='CPE4H',
                     save_cae=False,
                     export_stl=False,
                     export_stp=False
                     ):
        
        self.unit_cell_params_list       = unit_cell_params
        self.textile_dimensions          = textile_dimensions
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
        self.seed_size                   = seed_size
        self.elem_shape                  = elem_shape
        self.elem_code                   = elem_code
        self.save_cae                    = save_cae
        self.export_stl                  = export_stl
        self.export_stp                  = export_stp
        
    def createAnalysis(self):
        
        self.setDirectory() # Set working directory
        
        if self.uniform: 
            if 'vert_strut_thickness' in self.unit_cell_params_list.keys():
                self.vert_strut_thickness       = self.unit_cell_params_list['vert_strut_thickness']
                self.diag_strut_thickness       = self.unit_cell_params_list['diag_strut_thickness']
                self.diag_strut_angle           = self.unit_cell_params_list['diag_strut_angle']
                self.AR = -1
                
            else:
                self.AR                         = self.unit_cell_params_list['AR']
            
            # self.aspect_ratio               = self.unit_cell_params_list['aspect_ratio']
            self.extrusion_depth            = self.unit_cell_params_list['extrusion_depth']
            self.nb_cells_x                 = self.unit_cell_params_list['nb_cells_x']
            self.nb_cells_y                 = self.unit_cell_params_list['nb_cells_y']
            
            self.horz_bounding_box, self.vert_bounding_box = self.estimateCellsSize()
            
            if self.AR!=-1:
                self.vert_strut_thickness = self.horz_bounding_box / self.AR
                self.diag_strut_thickness = self.vert_strut_thickness
            
            
                self.diag_strut_angle = 50
            
            test_not_passed = True
            
            for k in range(50):
            
                horz_bounding_box    = self.horz_bounding_box / 2.0
                vert_bounding_box    = self.vert_bounding_box / 2.0
                vert_strut_thickness = self.vert_strut_thickness
                diag_strut_angle     = self.diag_strut_angle
                diag_strut_thickness = self.diag_strut_thickness
                tail_strut_thickness = self.vert_strut_thickness
                
                diag_strut_angle_rad      = np.deg2rad(diag_strut_angle)
                tail_strut_thickness_half = tail_strut_thickness / 2.0
                diag_strut_length = (horz_bounding_box - tail_strut_thickness_half) / np.sin(diag_strut_angle_rad)
                vert_strut_length_half = ( vert_bounding_box
                                      + (diag_strut_length         * np.cos(diag_strut_angle_rad) )
                                      + (diag_strut_thickness      / np.sin(diag_strut_angle_rad) )
                                      + (tail_strut_thickness_half / np.tan(diag_strut_angle_rad) ) ) / 2.0
                vert_strut_length = vert_strut_length_half * 2.0
                tail_strut_length = ( vert_strut_length_half
                                      - (diag_strut_thickness      / np.sin(diag_strut_angle_rad) )
                                      - (tail_strut_thickness_half / np.tan(diag_strut_angle_rad) ) )
                
                ## These dimensions only work if diag_line1 ends higher than tail_hline.
                if tail_strut_length >= ( diag_strut_length * np.cos(diag_strut_angle_rad) ):
                    test_not_passed = False
                    break
                if self.AR !=-1:
                    self.diag_strut_angle = np.random.randint(self.diag_strut_angle,89,1)[0]
        
            self.unit_cell_params = Reentrant2DUcpBox(
                id                   = 1  ,
                extrusion_depth      = self.extrusion_depth  ,
                horz_bounding_box    = self.horz_bounding_box ,
                vert_bounding_box    = self.vert_bounding_box ,
                vert_strut_thickness = self.vert_strut_thickness  ,
                diag_strut_thickness = self.diag_strut_thickness,
                diag_strut_angle     = self.diag_strut_angle
                )
            
            # Check seed size as a fct of the smallest elements
            self.seed_size = np.min([self.vert_strut_thickness,
                                     self.diag_strut_thickness,
                                     self.extrusion_depth])/2.5
            
            pattern_params = PatternParams(
              pattern_mode    = 'uniform',
              num_cell_repeat = (self.nb_cells_x,self.nb_cells_y),
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
            seed_size    = self.seed_size       ,
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
        structure_name = self.result_folder_name
        
        debug = {}
        debug['nb_cells_x'] = self.nb_cells_x
        debug['nb_cells_y'] = self.nb_cells_y
        debug['AR'] = self.AR
        debug['extrusion'] = self.extrusion_depth
        debug['angle'] = self.diag_strut_angle
        debug['vert_th'] = self.vert_strut_thickness
        debug['diag_th'] = self.diag_strut_thickness
        debug['vert_bb'] = self.vert_bounding_box
        debug['horz_bb'] = self.horz_bounding_box
        debug['seed_size'] = self.seed_size
        debug['k'] = k
        
        with open('Debug.pkl','w+') as file:
            json.dump(debug,file)
            
        if test_not_passed:
            
            self.output = {}
            self.output['poisson_mean'] = 1e6
            self.output['volume'] = 1e6
            
        else:
        
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
                                   'poisson_midpoint', 'poisson_mean','volume']
            
            results_file = os.path.join(os.getcwd(),'../Tables/results.csv')
            
            if not os.path.exists(os.path.join(os.getcwd(),'../Tables')):
                os.makedirs(os.path.join(os.getcwd(),'../Tables'))
                
            self.output = {}
            self.output = {label: results[-1,i] for i, label in enumerate(output_table_labels)}
            
            try:
                with open(results_file,'w+') as file:
                    file.write(str(self.output))
            except IOerror as e:
                LOG(e)
            
        self.resetDirectory()
        
    def setDirectory(self):
        
        setPath = os.path.join(os.getcwd(),'Abaqus_results', 
                               self.result_folder_name)
        
        if not os.path.exists(setPath):
            LOG('results directory does not exist')
            os.makedirs(setPath)
            
        os.chdir(setPath)
        
        try:
            with open(os.path.join(os.getcwd(),'log.txt'),'w+') as file:
                file.write('Analysis started')
                LOG('Successfully written file')
            file.close()
        except IOError as e:
            LOG(e)
            
    def resetDirectory(self):
        
        LOG('changing path')
        setPath = os.path.join(os.getcwd(),'../../')
            
        os.chdir(setPath)
            
    def estimateCellsSize(self):
        
        nb_x, nb_y = self.nb_cells_x, self.nb_cells_y
        
        size_x = self.textile_dimensions[0] / nb_x
        size_y = self.textile_dimensions[1] / nb_y
        
        return size_x, size_y

if __name__ == '__main__':
    
    pyauxetic_library_path = os.path.join(os.getcwd(),'../pyauxetic-main')
    command_path = 'C:/SIMULIA/Abaqus/Commands'
    abaqus_path = 'C:/SIMULIA/Abaqus/6.14-1/cod/python2.7/lib'
    sys.path.append(pyauxetic_library_path)
    sys.path.append(command_path)
    sys.path.append(abaqus_path)
    sys.stderr.write(pyauxetic_library_path)
    
    from pyauxetic.classes.auxetic_unit_cell_params import *
    from pyauxetic.classes.auxetic_structure_params import *
    from pyauxetic.main import main_single
    
    with io.open('Params.pkl','r') as file:
        params = json.load(file)
    
    if 'AR' in params.keys():
    
        unit_cell_params={'AR': params['AR'],
                          'extrusion_depth': params['extrusion_depth'],
                          'nb_cells_x': int(params['nb_cells_x']),
                          'nb_cells_y': int(params['nb_cells_y'])}
    
    else:
        unit_cell_params={'vert_strut_thickness': params['vert_strut_thickness'],
                          'diag_strut_thickness': params['diag_strut_thickness'],
                          'diag_strut_angle': params['diag_strut_angle'],
                          'extrusion_depth': params['extrusion_depth'],
                          'nb_cells_x': int(params['nb_cells_x']),
                          'nb_cells_y': int(params['nb_cells_y'])}
    
    aux_anal = AuxeticAnalysis()
    
    aux_anal.defineParams(unit_cell_params,
                          params['textile_dimensions'],
                          params['load_value'],
                          params['material'],
                          result_folder_name=str(params['folder']))
    
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    
    if params['mode'] == 'debug':
        objective = 1e6
    else:
        aux_anal.createAnalysis()
        
        if 'AR' in params.keys():
            objective = (aux_anal.output['poisson_mean'] * params['objective_scaling_Poisson'] + 
                      aux_anal.output['volume'] / aux_anal.extrusion_depth * params['objective_scaling_surface'])
        else:
            volume = aux_anal.output['volume']
            poisson = aux_anal.output['poisson_mean']
    
    if 'AR' in params.keys():
        output = {'objective': objective,
                  'vert': aux_anal.vert_strut_thickness,
                  'diag': aux_anal.diag_strut_thickness,
                  'angle': aux_anal.diag_strut_angle,
                  'extrusion': aux_anal.extrusion_depth,
                  'seed': aux_anal.seed_size}
    else:
        output = {'volume': volume,
                  'poisson': poisson,
                  'vert': aux_anal.vert_strut_thickness,
                  'diag': aux_anal.diag_strut_thickness,
                  'angle': aux_anal.diag_strut_angle,
                  'extrusion': aux_anal.extrusion_depth,
                  'seed': aux_anal.seed_size}
    
    with open('Output.pkl','w+') as file:
        json.dump(output,file)
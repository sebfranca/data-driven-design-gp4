# -*- coding: utf-8 -*-
"""
Created on Tue May  3 17:31:09 2022

@author: sebas
"""
import sys
import numpy as np
import csv
import os

sys.path.append('Librairies')

from PyAuxeticWrapper import *

def main():
    mode = 'debug' #'running' or 'debug'
    
    
    fixed_params = {
        'extrusion_depth': 5,
        'textile_dimensions': (100,100),
        'load_direction': 'x',
        'load_type': 'force',
        'load_value': 10,
        'seed_size': 1,
        'time_period': 1.0  ,
        'init_inc_size': 0.1 ,
        'min_inc_size': 0.05,
        'max_inc_size': 0.1 ,
        'max_num_inc': 100,
        'num_cpus': 4,
        'material': {'E': 2e6,
                  'nu': .33,
                  'density': 1},
        'export_ribbon_width':4,
        }
    
    
    
    if mode=='running':
        angles = {
            'fixed':60,
            'values': np.linspace(50,70,10)
            }
        vert_strut_thicknesses = {
            'fixed': 2,
            'values': np.linspace(1,3,10)
            }
            
        diag_strut_thicknesses = {
            'fixed': 2,
            'values': np.linspace(1,3,10)
            }
            
        nb_cells_x = {
            'fixed': 8,
            'values': [i for i in range(5,15)]
            }
            
        nb_cells_y = {
            'fixed': 8,
            'values': [i for i in range(5,15)]
            }
        
    if mode=='debug':
        angles = {
            'fixed':60,
            'values': [60,70]
            }
        vert_strut_thicknesses = {
            'fixed': 2,
            'values': [2,2.1]
            }
            
        diag_strut_thicknesses = {
            'fixed': 2,
            'values': [2,2.1]
            }
            
        nb_cells_x = {
            'fixed': 8,
            'values': [8,9]
            }
            
        nb_cells_y = {
            'fixed': 8,
            'values': [8,9]
            }
    
    
    
    
    sensitivityParameters = {
        'fixed_params': fixed_params,
        'angles': angles,
        'vert_strut_thicknesses': vert_strut_thicknesses,
        'diag_strut_thicknesses': diag_strut_thicknesses,
        'nb_cells_x': nb_cells_x,
        'nb_cells_y': nb_cells_y
        }
    
    runFullAnalysis(sensitivityParameters)


def runFullAnalysis(params):
    runAnalysis('angle_sensitivity','Angle','angles',params)
    runAnalysis('vert_t_sensitivity','VertT','vert_strut_thicknesses',params)
    runAnalysis('diag_t_sensitivity','DiagT','diag_strut_thicknesses',params)
    runAnalysis('nb_x_sensitivity','NbX','nb_cells_x',params)
    runAnalysis('nb_y_sensitivity','NbY','nb_cells_y',params)  
    
def runAnalysis(friendly_name, job_name, probed_var_name, params):   
    #Current work directory (saved to avoid imbricated files)
    initialPath = os.getcwd()
    output_volume = []
    output_poisson = []  
    
    #Copy params, except for the probed variable
    simu_params = dict()
    for key in params.keys():
        if key!=probed_var_name and key!='fixed_params':
            simu_params[key] = params[key]['fixed']
    simu_params['fixed_params'] = params['fixed_params']
    
    #Changing values of the probed variable
    probed_var_values = params[probed_var_name]['values']
    
    for xvalue in probed_var_values:
        #Abaqus job names do not accept specific characters like "."
        #--> Need to convert to an int (done after multiplication to
        #avoid losing the decimal values)
        folder_name = job_name + str(int(xvalue*100)) 
        
        #Retrieve the changing value
        simu_params [probed_var_name] = xvalue
                
        #Create the analysis and run it
        aux_anal = AuxeticAnalysis()
        aux_anal.defineParams(unit_cell_params={'vert_strut_thickness': simu_params['vert_strut_thicknesses'],
                                                'diag_strut_thickness': simu_params['diag_strut_thicknesses'],
                                                'diag_strut_angle': simu_params['angles'],
                                                'extrusion_depth': simu_params['fixed_params']['extrusion_depth'],
                                                'nb_cells_x': simu_params['nb_cells_x'],
                                                'nb_cells_y': simu_params['nb_cells_y']},
                              textile_dimensions=simu_params['fixed_params']['textile_dimensions'],
                              load_direction=simu_params['fixed_params']['load_direction'],
                              load_type=simu_params['fixed_params']['load_type'],
                              load_value=simu_params['fixed_params']['load_value'],
                              seed_size=simu_params['fixed_params']['seed_size'],
                              time_period=simu_params['fixed_params']['time_period'],
                              init_inc_size=simu_params['fixed_params']['init_inc_size'],
                              min_inc_size=simu_params['fixed_params']['min_inc_size'],
                              max_inc_size=simu_params['fixed_params']['max_inc_size'],
                              max_num_inc=simu_params['fixed_params']['max_num_inc'],
                              num_cpus=simu_params['fixed_params']['num_cpus'],
                              material=simu_params['fixed_params']['material'],
                              export_ribbon_width=simu_params['fixed_params']['export_ribbon_width'],
                              result_folder_name=folder_name)
        aux_anal.createAnalysis()  
        
        #need to reset the working dir to avoid imbricated files
        os.chdir(initialPath) 
        
        #Read relevant outputs
        volume, poisson = readResults(folder_name)
        output_volume.append(volume)
        output_poisson.append(poisson)
    
    #Write the results to a text file located in Python_results
    saveResults(friendly_name,probed_var_values,output_volume,output_poisson)
    
    LOG('\n \n' + 'Results for ' + friendly_name + ' were saved! \n \n')
    
def readResults(folder_name):    
    file = open(os.path.join(os.getcwd(), 'Abaqus_results', 'Tables', folder_name+' results.csv'))
    csvreader = csv.reader(file)
    
    #retrieve header and rows
    header = []
    ignore = next(csvreader) #ignore first line 'Modeling and post-processing done by PyAuxetic 2.0.1'
    header = next(csvreader) 
    rows = []
    for row in csvreader:
        rows.append(row)
    
    #retrieve column indices
    idx_poisson = header.index(' poisson_mean')
    idx_volume = header.index(' volume')
    
    #Extract values from last step
    volume = rows[-1][idx_volume]
    poisson = rows[-1][idx_poisson]
    
    return volume, poisson   

def saveResults(probed_var_name, probed_var_values, res_vol, res_poisson):
    python_results_path = os.path.join(os.getcwd(),'Python_results')
    if not os.path.exists(python_results_path):
        LOG('python results directory does not exist')
        os.makedirs(python_results_path)
    
    with open(os.path.join(python_results_path, probed_var_name + ".txt"), "w") as f:
        f.write("Variable_value\n")
        for xvalue in probed_var_values:
            f.write(str(xvalue) + ",")
        f.write("\nResulting_volume\n")
        for volume in res_vol:
            f.write(str(volume) + ",")
        f.write("\nResulting_poisson\n")
        for poisson in res_poisson:
            f.write(str(poisson) + ",")


if __name__ == '__main__':
    main()
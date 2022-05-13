# -*- coding: utf-8 -*-
"""
Created on Tue May  3 20:07:45 2022

@author: cedri
"""

from PyAuxeticWrapper import *
import GPyOpt as GP
from helper_functions import *
import os, sys, pickle, subprocess, json

class AuxeticOptimization(AuxeticAnalysis):
    def __init__(self):
        super().__init__()
        
    def optimParams(self,
                    params,
                    objective_scaling,
                    textile_dimensions,
                    load_value,
                    material,
                    result_folder_name='analysis',
                    extrusion_depth=5,
                    optimizer='BayesOpt',
                    bo_init=None
                    ):
        
        self.params = {}
        self.params['optimizer']                      = optimizer
        self.params['objective_scaling']              = objective_scaling
        self.params['textile_dimensions']             = textile_dimensions
        self.params['load_value']                     = load_value
        self.params['material']                       = material
        self.params['extrusion_depth']                = extrusion_depth
        self.params['folder']                         = result_folder_name
        
        self.result_folder_name                       = result_folder_name
        self.bo_init                                  = bo_init
        self.space                                    = []
        self.objective                                = []
        self.results                                  = {'nb_cells_x': [],
                                                         'nb_cells_y': [],
                                                         'strut_angle': [],
                                                         'obj': [],
                                                         'vert_thickness': [],
                                                         'diag_thickness': [],
                                                         'extrusion_depth': [],
                                                         'seed_size': []}
        
        if self.params['optimizer'] == 'BayesOpt':
            self.bounds                  = params['bounds']
            self.acquisition_type        = params['acquisition_type']
            self.acquisition_weight      = params['acquisition_weight']
            self.max_iter                = params['max_iter']
            self.max_time                = params['max_time']
            self.eps                     = params['eps']
            self.verbosity               = params['verbosity']
            self.tolerance               = params['tolerance']
            
            # self.domain = {'nb_cells_x': (self.bounds['nb_cells_x']['lower'],
            #                               self.bounds['nb_cells_x']['upper']),
            #                'nb_cells_y': (self.bounds['nb_cells_y']['lower'],
            #                               self.bounds['nb_cells_y']['upper']),
            #                'strut_angle': (self.bounds['strut_angle']['lower'],
            #                                self.bounds['strut_angle']['upper'])
                           # }
    
            self.feasible_region = [{'name': 'strut_angle', 'type': 'continuous', 'domain': [self.bounds['strut_angle']['lower'],
                                                                              self.bounds['strut_angle']['upper']]},
                     {'name': 'nb_cells_x', 'type': 'discrete', 'domain': np.arange(self.bounds['nb_cells_x']['lower'],
                                                                                    self.bounds['nb_cells_x']['upper'])},
                     {'name': 'nb_cells_y', 'type': 'discrete', 'domain': np.arange(self.bounds['nb_cells_y']['lower'],
                                                                                    self.bounds['nb_cells_y']['upper'])}]
                                                   
                                                   
            constraints = [{'name': 'constr_1', 'constraint': '-x[:,1] -.5 + abs(x[:,0]) - np.sqrt(1-x[:,0]**2)'},
                           {'name': 'constr_2', 'constraint': 'x[:,1] +.5 - abs(x[:,0]) - np.sqrt(1-x[:,0]**2)'}]
             
            
    def setIODirectory(self):
        
        setPath = os.path.join(os.getcwd(),'../../')
            
        os.chdir(setPath)
            
    def loss(self, query):
        
        self.space = {'strut_angle': query[0,0],
                      'nb_cells_x': query[0,1],
                      'nb_cells_y': query[0,2]}
        
        with open('Params.pkl','w+') as file:
            json.dump({**self.space,**self.params},file)
         
        p=subprocess.run(r'C:/SIMULIA/abaqus/Commands/abaqus cae noGUI=PyAuxeticWrapper.py', 
                         stdout=subprocess.PIPE,
                         shell=True,
                         stderr=subprocess.PIPE)
        # print(p.stderr)
        # print(p.stdout)
        
        with open('Output.pkl','rb') as file:
            output = json.load(file)
            
        self.objective = output['objective']
        self.vert_strut_thickness = output['vert']
        self.diag_strut_thickness = output['diag']
        self.seed_size = output['seed']
        self.extrusion_depth = output['extrusion']
        
        return self.objective
    
    def train(self):
        
        os.chdir(os.path.join(os.getcwd(),'Librairies'))
        
        # BO object
        self.bo = GP.methods.BayesianOptimization(f=self.loss,
                                                  domain=self.feasible_region,
                                                  acquisition_type='EI',
                                                  model_type='sparseGP')
        
        k = 1
        nb_steps = int(self.max_iter/k)
        
        for n in range(nb_steps):
            # Run the optimization                                                  
            self.bo.run_optimization(max_iter=(n + 1)*k, 
                                    max_time=self.max_time, 
                                    eps=self.tolerance, 
                                    verbosity=self.verbosity) 
            print('Iteration {}, current point {}, current objective {}'.format(n,
                                                                              self.space,
                                                                              self.objective))
            self.results['nb_cells_x'].append(self.space['nb_cells_x'])
            self.results['nb_cells_y'].append(self.space['nb_cells_y'])
            self.results['strut_angle'].append(self.space['strut_angle'])
            self.results['obj'].append(self.objective)
            self.results['vert_thickness'].append(self.vert_strut_thickness)
            self.results['diag_thickness'].append(self.diag_strut_thickness)
            self.results['extrusion_depth'].append(self.extrusion_depth)
            self.results['seed_size'].append(self.seed_size)
            
            with open(os.path.join(os.getcwd(),'Abaqus_results/Tables',self.params['folder']+'_results.json'),'w+') as file:
                json.dump(self.results,file)
                
        self.bo.plot_acquisition()
        
        LOG('Optimization finished after %i iterations, best params : \n%s \n, best obj : %.3f'%(
            self.bo.num_acquisitions, 
            self.bo.x_opt, 
            self.bo.fx_opt))
        
        
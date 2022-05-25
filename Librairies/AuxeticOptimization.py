# -*- coding: utf-8 -*-
"""
Created on Tue May  3 20:07:45 2022

@author: cedri
"""

from PyAuxeticWrapper import *
import GPyOpt as GP
from helper_functions import *
import os, sys, pickle, subprocess, json
import skopt, time

class AuxeticOptimization(AuxeticAnalysis):
    def __init__(self):
        super().__init__()
        
    def optimParams(self,
                    params,
                    objective_scaling_Poisson,
                    objective_scaling_surface,
                    textile_dimensions,
                    load_value,
                    material,
                    result_folder_name='analysis',
                    extrusion_depth=4,
                    optimizer='BayesOpt',
                    load=False
                    ):
        
        self.params = {}
        self.params['optimizer']                      = optimizer
        self.params['objective_scaling_Poisson']      = objective_scaling_Poisson
        self.params['objective_scaling_surface']      = objective_scaling_surface
        self.params['textile_dimensions']             = textile_dimensions
        self.params['load_value']                     = load_value
        self.params['material']                       = material
        self.params['extrusion_depth']                = extrusion_depth
        self.params['folder']                         = result_folder_name
        
        self.result_folder_name                       = result_folder_name
        self.load                                     = load
        self.space                                    = []
        self.objective                                = []
        self.failed                                   = False
        self.prev_iter                                = 0
        
        if self.load:
            with open(os.path.join(os.getcwd(),'Librairies/Abaqus_results/Tables',self.params['folder']+'_values.pkl'),'rb') as file:
                self.results = pickle.load(file)
            
        else:
            self.results                                  = {'nb_cells_x': [],
                                                             'nb_cells_y': [],
                                                             'AR': [],
                                                             'obj': [],
                                                             'vert_thickness': [],
                                                             'diag_thickness': [],
                                                             'diag_strut_angle': [],
                                                             'extrusion_depth': [],
                                                             'seed_size': [],
                                                             'xi': params['xi'],
                                                             'kappa': params['kappa'],
                                                             'acq_weight': params['acquisition_weight'],
                                                             'acq_type': params['acquisition_type'],
                                                             'bounds': params['bounds']}
        self.base_iters = len(self.results['nb_cells_x'])
        
        if self.params['optimizer'] == 'BayesOpt':
            self.bounds                  = params['bounds']
            self.acquisition_type        = params['acquisition_type']
            self.acquisition_weight      = params['acquisition_weight']
            self.max_iter                = params['max_iter']
            self.max_time                = params['max_time']
            self.eps                     = params['eps']
            self.verbosity               = params['verbosity']
            self.tolerance               = params['tolerance']
            self.mode                    = params['mode']
            
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
             
        elif self.params['optimizer'] == 'skopt':
            self.bounds                  = params['bounds']
            self.acquisition_type        = params['acquisition_type']
            self.acquisition_weight      = params['acquisition_weight']
            self.max_iter                = params['max_iter']
            self.max_time                = params['max_time']
            self.eps                     = params['eps']
            self.verbosity               = params['verbosity']
            self.tolerance               = params['tolerance']
            self.kappa                   = params['kappa']
            self.xi                      = params['xi']
            self.mode                    = params['mode']
            
    def setIODirectory(self):
        
        setPath = os.path.join(os.getcwd(),'../../')
            
        os.chdir(setPath)
            
    def loss(self, librairy, query=None, **kwargs):
        
        if librairy == 'GPyOpt':
            self.space = {'strut_angle': query[0,0],
                          'nb_cells_x': query[0,1],
                          'nb_cells_y': query[0,2]}
        elif librairy == 'skopt':
            self.space = {'AR': float(kwargs['params']['AR']),
                          'nb_cells_x': int(kwargs['params']['nb_cells_x']),
                          'nb_cells_y': int(kwargs['params']['nb_cells_y']),
                          'mode': self.mode}
        print('\n')   
        print('='*100)
        print('Analysis started for datapoint {} at time {}'.format(self.space,time.strftime('%d/%m/%Y %H:%M:%S')))
        print('='*100)
        print('\n') 
        
        with open('Params.pkl','w+') as file:
            json.dump({**self.space,**self.params},file)
         
        start = time.time()
        p=subprocess.run(r'C:/SIMULIA/abaqus/Commands/abaqus cae noGUI=PyAuxeticWrapper.py', 
                         stdout=subprocess.PIPE,
                         shell=True,
                         stderr=subprocess.PIPE)
        self.duration = time.time() - start
        
        print('STDOUT : \n{}'.format(p.stdout))
        print('STDERR : \n{}'.format(p.stderr))
        
        with open('Output.pkl','rb') as file:
            output = json.load(file)
            
        self.objective = output['objective']
        self.vert_strut_thickness = output['vert']
        self.diag_strut_thickness = output['diag']
        self.diag_strut_angle = output['angle']
        self.seed_size = output['seed']
        self.extrusion_depth = output['extrusion']
        
        if self.objective == 1e6:
            
            self.failed = True
            if len(self.results['obj']) == 0:
                self.objective = 1e3
            else:
                self.objective = 1.2*np.max(self.results['obj'])
        
        return self.objective
    
    def train_skopt(self):
        os.chdir(os.path.join(os.getcwd(),'Librairies'))
        
        SPACE = [skopt.space.Real(self.bounds['AR']['lower'], 
                                  self.bounds['AR']['upper'], 
                                  name='AR', 
                                  prior='uniform'),
                 skopt.space.Integer(self.bounds['nb_cells_x']['lower'], 
                                     self.bounds['nb_cells_x']['upper'], 
                                     name='nb_cells_x', 
                                     prior='uniform'),
                 skopt.space.Integer(self.bounds['nb_cells_y']['lower'], 
                                     self.bounds['nb_cells_y']['upper'], 
                                     name='nb_cells_y', 
                                     prior='uniform')]
        
        @skopt.utils.use_named_args(SPACE)
        def objective(**params):
            all_params = {**params}
            return 1.0 * self.loss(librairy='skopt',params=all_params)
        
        def callback(res):
            n = len(res.x_iters)
            if self.prev_iter != n and type(self.space) == dict:
                
                print('\n')
                print('#'*100)
                if self.failed:
                    obj = 'ANALYSIS UNFEASIBLE'
                    self.failed = False
                else:
                    obj = self.objective
                print('Iteration {}/{} results at current point {} : current objective {}'.format(n,
                                                                                                 self.base_iters+self.max_iter,
                                                                                                 self.space,
                                                                                                 obj))
                print('Analysis duration {}'.format(self.duration))
                print('#'*100)
                print('\n')
                
                self.results['nb_cells_x'].append(self.space['nb_cells_x'])
                self.results['nb_cells_y'].append(self.space['nb_cells_y'])
                self.results['AR'].append(self.space['AR'])
                self.results['obj'].append(self.objective)
                self.results['vert_thickness'].append(self.vert_strut_thickness)
                self.results['diag_thickness'].append(self.diag_strut_thickness)
                self.results['diag_strut_angle'].append(self.diag_strut_angle)
                self.results['extrusion_depth'].append(self.extrusion_depth)
                self.results['seed_size'].append(self.seed_size)
                
                with open(os.path.join(os.getcwd(),'Abaqus_results/Tables',self.params['folder']+'_values.pkl'),'wb') as file:
                    pickle.dump(self.results,file)
                    
            self.prev_iter = n
                
        intermediate_save = os.path.join(os.getcwd(),
                                         'Abaqus_results/Tables',self.params['folder']+'_persistent.pkl')
        nb_iter_without_save = 5
        nb_saves = int(self.max_iter / nb_iter_without_save)
        if self.load:
            loaded_space = skopt.load(intermediate_save)
            
            for k in range(nb_saves):
                res_gp = skopt.gp_minimize(objective, 
                                           SPACE, 
                                           n_calls=nb_iter_without_save,
                                           acq_func="EI",
                                           n_random_starts=0,
                                           callback=[callback],
                                           x0=loaded_space.x_iters,
                                           y0=loaded_space.func_vals,
                                           kappa=self.kappa,
                                           xi=self.xi)
                
                res_gp['specs']['args'].pop('callback')
                skopt.dump(res_gp,intermediate_save,store_objective=False)
                loaded_space = skopt.load(intermediate_save)
            
        else:
            res_gp = skopt.gp_minimize(objective, 
                                       SPACE, 
                                       acq_func="EI",
                                       n_random_starts=5,
                                       callback=[callback],
                                       n_calls=nb_iter_without_save,
                                       kappa=self.kappa,
                                       xi=self.xi)
            
            res_gp['specs']['args'].pop('callback')
            skopt.dump(res_gp,intermediate_save,store_objective=False)
            
            
            for k in range(nb_saves-1):
                loaded_space = skopt.utils.load(intermediate_save)
                res_gp = skopt.gp_minimize(objective, 
                                           SPACE, 
                                           n_calls=nb_iter_without_save,
                                           acq_func="EI",
                                           n_random_starts=0,
                                           callback=[callback],
                                           x0=loaded_space.x_iters,
                                           y0=loaded_space.func_vals,
                                           kappa=self.kappa,
                                           xi=self.xi)
                
                res_gp['specs']['args'].pop('callback')
                skopt.dump(res_gp,intermediate_save,store_objective=False)
        
    def train_GPyOpt(self):
        
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
        
        
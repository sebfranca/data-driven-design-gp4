# -*- coding: utf-8 -*-
"""
Created on Tue May  3 20:07:45 2022

@author: cedri
"""

from PyAuxeticWrapper import *
import GPyOpt as GP

class AuxeticOptimization(AuxeticAnalysis):
    def __init__(self):
        super().__init()
        
    def optimParams(self,
                    params,
                    objective_scaling,
                    textile_dimensions,
                    load_value,
                    material,
                    extrusion_depth,
                    optimizer='BayesOpt'
                    ):
        
        self.optimizer                      = optimizer
        self.objective_scaling              = objective_scaling
        self.textile_dimensions             = textile_dimensions
        self.load_value                     = load_value
        self.material                       = material
        self.extrusion_depth                = extrusion_depth
        
        if self.optimizer == 'BayesOpt':
            self.bounds                  = params['bounds']
            self.acquisition_type        = params['acquisition_type']
            self.acquisition_weight      = params['acquisition_weight']
            self.max_iter                = params['max_iter']
            self.max_time                = params['max_time']
            self.eps                     = params['eps']
            
    def loss(self, domain):
        
        unit_cell_params={'vert_strut_thickness': domain[0,0],
                          'diag_strut_thickness': domain[0,1],
                          'diag_strut_angle': domain[0,2],
                          'extrusion_depth': self.extrusion_depth,
                          'nb_cells_x': domain[0,3],
                          'nb_cells_y': domain[0,4]}
        
        super().defineParams(unit_cell_params,
                             self.textile_dimensions,
                             self.load_value,
                             self.material)
        
        super().createAnalysis()
        
        objective = (self.output['poisson_mean'][-1] + 
                     self.output['volume'] / self.extrusion_depth * self.objective_scaling)
        
        return objective
        
    def train(self):
        
        myBopt = GPyOpt.methods.BayesianOptimization(f=self.loss,                   
                                                     domain=self.bounds,        
                                                     acquisition_type=self.acquisition_type,
                                                     exact_feval=True,
                                                     acquisition_weight=self.acquisition_weight) 
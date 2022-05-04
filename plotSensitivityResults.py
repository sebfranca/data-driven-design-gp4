# -*- coding: utf-8 -*-
"""
Created on Wed May  4 11:36:05 2022

@author: sebas
"""
import os,sys
import matplotlib.pyplot as plt

path_to_results = 'C:/Users/sebas/Documents/Ecole/EPFL/Master4/Cours/DataDrivenDesign/Project/Python_results'
all_filenames = ['angle_sensitivity.txt',
             'vert_t_sensitivity.txt',
             'diag_t_sensitivity.txt',
             'nb_x_sensitivity.txt']
all_varnames = ['angle','vertT','diagT','NbX']
thickness = 1.0


xvalues = dict()
volumes = dict()
poisson = dict()

#store into the dictionaries
for i,filename in enumerate(all_filenames):
    varname = all_varnames[i]
    
    with open(os.path.join(path_to_results,filename),'r') as f:
        Lines=f.readlines()
        
        var_values = Lines[1][:-2].split(",")
        res_volumes = Lines[3][1:-2].split(", ")
        res_poisson = Lines[5][1:-2].split(", ")
        
        for j in range(len(var_values)):
            var_values[j] = float(var_values[j])
            res_volumes[j] = float(res_volumes[j])/thickness
            res_poisson[j] = float(res_poisson[j])
        
        xvalues[varname] = var_values
        volumes[varname] = res_volumes
        poisson[varname] = res_poisson
        
#Make the graphs
for i,varname in enumerate(all_varnames):
    plt.figure(num=i)
    fig, axs = plt.subplots(2, 1, constrained_layout=True)
    fig.suptitle('Sensitivity analysis : ' + varname, fontsize=16)
    
    axs[0].scatter(xvalues[varname],volumes[varname], label="Volume")
    axs[0].set_title('Volume variation')
    axs[0].set_xlabel(varname)
    axs[0].set_ylabel("Volume")
    
    axs[1].scatter(xvalues[varname],poisson[varname], label="Poisson ratio")
    axs[1].set_title("Poisson ratio variation")
    axs[1].set_xlabel(varname)
    axs[1].set_ylabel("Poisson ratio")
    
    plt.show()
        
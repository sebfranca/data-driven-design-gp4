# -*- coding: utf-8 -*-
"""
Created on Thu May 26 12:39:39 2022

@author: sebas
"""
import os
import pickle
import matplotlib.pyplot as plt


with open('C:/Users/sebas/Documents/Ecole/EPFL/Master4/Cours/DataDrivenDesign/Project/Librairies/Abaqus_results/Tables/Sensitivity_values.pkl','rb') as file:
    res = pickle.load(file)
    
gridsize = 20
minx = 2
maxx = 10
gridsize2 = len(range(minx,maxx+1))

names = ['diag_strut_angle', 'diag_thickness', 'vert_thickness', 'nb_cells_x', 'nb_cells_y', 'volume','poisson']
friendly = ['angle', 'td', 'tv', '# cells x', '# cells y', 'volume', 'poisson']
friendly_with_units = ['angle [°]', 'td [mm]', 'tv [mm]', '# cells x', '# cells y']

res_angle = dict()
res_td = dict()
res_tv = dict()
res_x = dict()
res_y = dict()


for name in names:
    res_angle[name] = res[name][0:gridsize]
    res_td[name] = res[name][gridsize: 2*gridsize]
    res_tv[name] = res[name][2*gridsize: 3*gridsize]
base_idx = 3*gridsize

for name in names:
    res_x[name] = res[name][base_idx : base_idx + gridsize2]
    res_y[name] = res[name][base_idx + gridsize2 : base_idx + 2*gridsize2]

MIN_P = 5e8
MAX_P = -5e8
MIN_V = 5e8
MAX_V = -5e8

for name in ['poisson','volume']:
    for R in [res_angle, res_td, res_tv, res_x, res_y]:
        for i, v in enumerate(R[name]):
            if v>1e5:
                R[name][i] = None
                
            else:
                if name=='poisson':
                    if v<MIN_P: MIN_P = v
                    if v>MAX_P: MAX_P = v
                elif name=='volume':
                    if v<MIN_V: MIN_V = v
                    if v>MAX_V: MAX_V = v

factor = 0.1
for an_idx, res in enumerate([res_angle, res_td, res_tv, res_x, res_y]):
    
    fig, axs = plt.subplots(2, sharex=True)
    fig.suptitle("Sensitivity analysis : {}".format(friendly[an_idx]))
    axs[0].plot(res[names[an_idx]], res['poisson'])
    axs[0].scatter(res[names[an_idx]], res['poisson'])
    axs[0].grid()
    axs[0].set_title("Poisson ratio")
    axs[0].set_ylabel("Poisson ratio [-]")
    axs[0].set_ylim(bottom=MIN_P-factor*abs(MIN_P), top=MAX_P + factor*abs(MAX_P))
    
    axs[1].plot(res[names[an_idx]], res['volume'])
    axs[1].scatter(res[names[an_idx]], res['volume'])
    axs[1].grid()
    axs[1].set_title("Volume")
    axs[1].set_ylabel("Volume [mm^3]")
    axs[1].set_xlabel(friendly_with_units[an_idx])
    axs[1].set_ylim(bottom=MIN_V-factor*abs(MIN_V), top=MAX_V + factor*abs(MAX_V))
    
plt.figure()
plt.axis('off')
plt.text(0.3,0.1, "Fixed angle: {}".format(res_td["diag_strut_angle"][0]), clip_on=False)
plt.text(0.3,0.3, "Fixed td: {}".format(res_angle["diag_thickness"][0]), clip_on=False)
plt.text(0.3,0.5, "Fixed tv: {}".format(res_angle["vert_thickness"][0]), clip_on=False)
plt.text(0.3,0.7, "Fixed nb cells x: {}".format(res_angle["nb_cells_x"][0]), clip_on=False)
plt.text(0.3,0.9, "Fixed nb cells y: {}".format(res_angle["nb_cells_y"][0]), clip_on=False)
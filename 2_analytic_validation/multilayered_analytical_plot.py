# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 17:10:20 2022

@author: milon
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker

import mpl_toolkits.axisartist as axisartist

# plt.rcParams['font.size'] = 25.0
# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = 'Arial'
# plt.rcParams['font.weight'] = 'bold'
# plt.rcParams['axes.labelsize'] = 'medium'
# plt.rcParams['axes.labelweight'] = 'bold'
# plt.rcParams['axes.linewidth'] = 1.2
# plt.rcParams['lines.linewidth'] = 0.3

from define_colors import *
color = colors[0]

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': True,
})

#Load data
data = np.loadtxt('results_openmc_multilayered.txt')
#Ignore all zeros
PHT = np.zeros((100, 33))
for i in range(100):
    PHT[i] = data[i*33:33*(i+1)]   

#Calculate mean and std  
mean = np.zeros(33)
std = np.zeros(33)

for i in range(33):
    mean[i] = np.mean(PHT[:,i])
    std[i] = np.std(PHT[:,i])


for i in range(33):
    if mean[32-i] <= 0.000000000000001:
        mean = np.delete(mean, 32-i)
        std = np.delete(std, 32-i)
    
print('This are the mean values\n {}'.format(mean))

print('This are the std \n {}'.format(std))

#Comparison to Sood 2004

Sood04 = np.array([0.56116619, 0.02409558, 0.06195740, 0.02156830, 0.049044545, 0.00280990, 0.01297187, 0.00226777,
                   0.10942557, 0.02979685, 0.01372311, 0.03354201, 0.00528230, 0.01193924, 0.00302856, 0.0573804])
    
#Results from ProbTree
analy_0 = {0: 0.561329022358257,
 0.2: 0.0237685679449077,
 0.4: 0.0630209468948048,
 0.6: 0.0197690310224596,
 0.8: 0.0499450800617007,
 1.0: 0.00280989550115659,
 1.2: 0.0130114829651646,
 1.4: 0.00218852928949916,
 1.6: 0.109465181289042,
 2.0: 0.0303790151051969,
 2.2: 0.0125587643222950,
 2.4: 0.0342983395143937,
 2.6: 0.00500296971417419,
 2.8: 0.0120878716787918,
 3.0: 0.00287259688207117,
 3.2: 0.0574927054560848}

analy = np.array(list(analy_0.values()))

energy = np.array(list(analy_0.keys()))
label = []
for i in range(len(energy)):
    label.append('{}'.format(energy[i]))


fig, axarray = plt.subplots(2, 1, figsize = (6.8,4.5), sharex=True, gridspec_kw={'height_ratios': [2, 1]}) #sharex = geteilte xAchse
axarray[0].grid('x')
axarray[1].grid('x')
p1 = axarray[0].bar(energy+0.025, mean, width = 0.05, color=colors[0], label = "OpenMC")
p2 = axarray[0].bar(energy-0.025, analy, width = 0.05, color=colors[1], label = "Analytical results")

#axarray[0].text(0.06, 0.5, "0.5613")#, rotation=90)
#axarray[0].text(0.175, 0.03, "0.0238", rotation=90)
#axarray[0].text(0.375, 0.08, "0.0630", rotation=90)

#axarray[0].set_ylim(0,10**5)

axarray[1].errorbar(energy, mean-analy, yerr=std, markersize = 2, elinewidth=1, capsize = 3, color='black', fmt='o', markeredgecolor='black', barsabove = True)
axarray[1].axhline(y=0, color='black', linestyle='--')
axarray[0].set_ylabel('Pulse-height tally result')


axarray[0].set_yticks([0.01, 0.1], [r"$10^{-2}$", r"$10^{-1}$"])

axarray[1].set_xticks(list(energy[:9]) + [1.8] + list(energy[9:]), label[:9] + [""] + label[9:], rotation = 45)


axarray[0].tick_params(labelbottom=False)
axarray[1].tick_params(labelbottom=True)
axarray[0].set_yscale('log')
axarray[1].set_ylabel('Difference')#, horizontalalignment='right')
axarray[1].set_xlabel('Energy [MeV]')
axarray[0].legend()#borderpad = 1.2, handlelength = 1.7)

axarray[1].set_yticks([-0.0001, 0, 0.0001], [r"$-10^{-4}$", "0.0", r"$10^{-4}$"])
axarray[0].yaxis.set_label_coords(-0.1, 0.5)

#axarray[1].legend(loc="upper right", ncol=1)

#Function to adjust the y label of the residuals (only works for this specific scale!)
#f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
#def g(val, pos=None):
#    if val < 0:
#        return "$10^{-4}$"
#    elif val > 0:
#        return "$10^{4}$"
#    else:
#        return "0"
#
#fmt = mticker.FuncFormatter(g)
#axarray[1].yaxis.set_major_formatter(fmt)
plt.savefig('/home/cpf/Desktop/publications-in-work/Implementation-and-Validation-of-the-Pulse-Height-Tally-in-OpenMC/figures/pgf_tworegion_new.pgf', bbox_inches = 'tight')

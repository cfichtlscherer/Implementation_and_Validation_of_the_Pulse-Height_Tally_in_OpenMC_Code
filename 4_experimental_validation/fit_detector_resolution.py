"""
Mär 25, 2021
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License

Fit the detector resolution function from Heath Figure 6 (p. 19)
"""

import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit

import matplotlib

from define_colors import *

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

figures_path = '/home/cpf/Desktop/publications-in-work/Implementation-and-Validation-of-the-Pulse-Height-Tally-in-OpenMC/figures/'

#def func1(x, a, b):
#    return a * x**-0.5 + b

#def func1(x, a, b):
#    return a * x**-0.5 + b
#
#def func1(x, a, b, c):
#    return (((a + b*x) **0.5)/x + c)

def func1(E, a, b, c):
    return ((a + b*((E + c*(E**2))**0.5)) / E)

det_2_energy = np.array([0.060, 0.110, 0.145, 0.160, 0.165, 0.275, 0.320, 0.390, 0.470, 0.530, 0.660, 0.830, 0.930, 1.100, 1.275, 1.500, 1.750, 2.100, 2.700])
det_2_resolu = np.array([17.55, 14.60, 13.35, 13.10, 12.90, 11.20, 10.70, 10.00, 09.40, 09.10, 08.20, 07.50, 07.25, 06.80, 06.40, 06.00, 05.70, 05.35, 05.00])

#det_5_energy = np.array([0.110, 0.160, 0.280, 0.315, 0.470, 0.510, 0.600, 0.770, 1.550, 2.200])
#det_5_resolu = np.array([14.10, 12.60, 10.40, 10.10, 08.80, 08.50, 08.00, 07.25, 05.45, 04.70])

popt2_1, pcov2_1 = curve_fit(func1, det_2_energy, det_2_resolu)
#popt5_1, pcov5_1 = curve_fit(func1, det_5_energy, det_5_resolu)

print("detector2: " + str(popt2_1))
#print("detector5: " + str(popt5_1))

mse_2_results = func1(det_2_energy, popt2_1[0], popt2_1[1], popt2_1[2])
mse_2_dif = (mse_2_results - det_2_resolu)**2
mse_2_res = (np.mean(mse_2_dif))**0.5

print("mse detector 2: " + str(mse_2_res))

#mse_5_results = func1(det_5_energy, popt5_1[0], popt5_1[1])
#mse_5_dif = (mse_5_results - det_5_resolu)**2
#mse_5_res = (np.mean(mse_5_dif))**0.5

#print("mse detector 5: " + str(mse_5_res))

x_values = np.linspace(0.05, 3.0, 100)
print(popt2_1[1])
y_2_1 = func1(x_values, popt2_1[0], popt2_1[1], popt2_1[2])
#y_5_1 = func1(x_values, popt5_1[0], popt5_1[1])


plt.figure(figsize=(6.8,2.8))
plt.plot(x_values, y_2_1, linestyle="-", color=colors[0])
#plt.plot(x_values, y_5_1, linestyle="-", color=colors[1])
#plt.plot(det_2_energy, det_2_resolu, label="3\"\,$\\times$\,3\" - NaI detector", linestyle = "", marker = ".", color=colors[0])
plt.plot(det_2_energy, det_2_resolu, label="Detector resolution", linestyle = "", marker = ".", color=colors[0])
#plt.plot(det_5_energy, det_5_resolu, label="3\" x 3\" - NaI detector, model 2", linestyle = "", marker = ".", color=colors[1])

################################################################################
################################################################################
# plot experimental resolutions

e_all = np.load("e_all.npy")
res_all = np.load("res_all.npy")

plt.plot(e_all, res_all, marker=".", linestyle="", color=colors[1], label="Experiments analyzed")

nuc_names = ["Al-28","Cs-137", "Co-60-1", "Co-60-2", "Zn-65", "Rb-86", "Y-88", "Ba-140", "Au-198", "Mn-54"]

for i, n in enumerate(nuc_names):
    x_shift = 0
    y_shift = 0
    if n == "Al-28":
        y_shift = 1.45
        plt.text(e_all[i] + x_shift, res_all[i] + y_shift, n, fontsize=8)
    if n == "Y-88":
        y_shift = 0.5
        plt.text(e_all[i] + x_shift, res_all[i] + y_shift, n, fontsize=8)
    if n == "Zn-65":
        y_shift = 2.1
        plt.text(e_all[i] + x_shift, res_all[i] + y_shift, n, fontsize=8)
    if n == "Co-60-1":
        y_shift = 0.8
        plt.text(e_all[i] + x_shift, res_all[i] + y_shift, "Co-60$_{1}$", fontsize=8)
    if n == "Co-60-2":
        y_shift = 0.5
        plt.text(e_all[i] + x_shift, res_all[i] + y_shift, "Co-60$_{2}$", fontsize=8)
    if n == "Rb-86":
        y_shift = 2.8
        plt.text(e_all[i] + x_shift, res_all[i] + y_shift, n, fontsize=8)
    if n == "Cs-137":
        y_shift = 0.5
        plt.text(e_all[i] + x_shift, res_all[i] + y_shift, n, fontsize=8)
    if n == "Ba-140":
        y_shift = 0.6
        plt.text(e_all[i] + x_shift, res_all[i] + y_shift, n, fontsize=8)
    if n == "Au-198":
        y_shift = 0.8
        plt.text(e_all[i] + x_shift, res_all[i] + y_shift, n, fontsize=8)
    if n == "Mn-54":
        y_shift = 0.4
        plt.text(e_all[i] + x_shift, res_all[i] + y_shift, n, fontsize=8)


"""
al_energy = 1778.987 / 1000
al_resolution = 0.059232034544745064 * 100
plt.text(al_energy, al_resolution+3, 'Al-28')
plt.plot((al_energy, al_energy+0.1), (al_resolution+0.3, al_resolution+2.8), linewidth=0.8, color="black")
plt.plot(al_energy, al_resolution, marker=".", color=colors[4])

cs_energy = 0.662
cs_resolution = 8.553
plt.plot(cs_energy, cs_resolution, marker=".", color=colors[4])
 
co_energy_1 = 0.662
co_resolution_1 = 7.27
plt.plot(co_energy_1, co_resolution_1, marker=".", color=colors[4])
"""


################################################################################
################################################################################

#plt.title("25.03.2021 fit the detector resolution (Heath Figure 6, p.19) by the function f(x) = a* x**-0.5 + b")
plt.xlabel("Gamma Ray Energy [MeV]")
plt.ylabel("Detector Resolution [%]")
plt.legend(loc="upper right")
plt.grid()
plt.savefig(figures_path + 'detector_resolution.pgf', bbox_inches='tight')

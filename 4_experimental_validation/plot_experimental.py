"""
Feb 25, 2021
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License

TODO:
    unten drunter gamma peaks / half life time etc
    achsen einheitlich machen
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

from define_colors import *

from heath_experimental_spectra import *


matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

figures_path = '/home/cpf/Desktop/publications-in-work/Implementation-and-Validation-of-the-Pulse-Height-Tally-in-OpenMC/figures/'

def generate_histogram(file_path, number_bins):
    """ generates the histogram from the from the pht tally produced .txt file"""

    cell = 0 # the cell we want to analyze
    pht_output_b = pd.read_csv(file_path, sep=",", header=None)
    cell_pht_output_b = np.asarray(pht_output_b[cell])
    cell_pht_clean_b = cell_pht_output_b[cell_pht_output_b != 0]
    bins = np.linspace(0, number_bins*10**4, number_bins)

    values_b, b = np.histogram(cell_pht_clean_b, bins)

    return values_b.astype(float)

fig, ax = plt.subplots(3, 3, figsize=(6.8, 5.0))

#fig.suptitle("Experimental Validation", fontweight='bold')


left  = 0.125  # the left side of the subplots of the figure
right = 0.9    # the right side of the subplots of the figure
bottom = 0.1   # the bottom of the subplots of the figure
top = 0.9     # the top of the subplots of the figure
wspace = 0.3   # the amount of width reserved for blank space between subplots
hspace = 0.4   # the amount of height reserved for white space between subplots
plt.subplots_adjust(left, bottom, right, top, wspace, hspace)


loadpath = "/home/cpf/Desktop/open_projects/f8_validation/experimental_validation_f8/experimental_openmc_calculation-2-01042022/experimental_broadened_spectra/"
energy_path = "/home/cpf/Desktop/open_projects/f8_validation/experimental_validation_f8/experimental_openmc_calculation/"

nuc_names = ["Na-24", "Al-28", "S-37", "Co-60", "Zn-65", "Y-88", "Cs-137", "Ce-139", "Au-198"]

#particles_simulation = 10 * 10**7 *0.038
particles_simulation = 1

################################################################################
print("rb86")
ax[1, 1].title.set_text('Rb-86')
ax[1, 1].plot(np.arange(len(rb_86)) + 0.5, np.asarray(rb_86), color=colors[0])
ax[1, 1].grid()
rb_86_simulation = np.load(loadpath + "Rb-86-broaded.npy")
source_particles = 2.37 * 10**7 # from heath
detector_efficiency = 0.015 # read out heath p.
particles_simulation = 1
rb_86_simulation *= ( source_particles / particles_simulation * detector_efficiency)

energies = np.load(energy_path + "Rb-86-energies.npy")
for en in energies:
    ax[1, 1].axvline(en / 10, color=colors[2])

ax[1, 1].plot((np.arange(len(rb_86)) + 0.5)[:-1], np.asarray(rb_86_simulation), color=colors[1])
ax[1, 1].set_yscale('log')
ax[1, 1].set_ylim(bottom=10)

################################################################################
print("al28")
ax[0, 0].title.set_text('Al-28')
ax[0, 0].plot(np.arange(2, len(al_28)+2) + 0.5, np.asarray(al_28), color=colors[0], label="Experiment")
ax[0, 0].grid()
al_28_simulation = np.load(loadpath + "Al-28-broaded.npy")
source_particles = 4.33 * 10**7 # from heath
detector_efficiency = 0.02 # read out heath p.
particles_simulation = 1
al_28_simulation *= (source_particles / particles_simulation * detector_efficiency)

energies = np.load(energy_path + "Al-28-energies.npy")
for en in energies:
    ax[0, 0].axvline(en / 10, color=colors[2])

ax[0, 0].plot((np.arange(len(al_28)) + 0.5)[:-1], np.asarray(al_28_simulation), color=colors[1], label="Simulation")
ax[0, 0].set_ylabel("Counts")
ax[0, 0].set_yscale('log')
ax[0, 0].legend(loc="lower left")
ax[0, 0].set_ylim(bottom=1)
################################################################################
print("ba140")
ax[2, 1].title.set_text('Ba-140$^{*}$')
ax[2, 1].plot(np.arange(-1, len(ba_140)-1) + 0.5, np.asarray(ba_140), color=colors[0], label="Experiment")
ax[2, 1].grid()
#file_path = loadpath + "Ba-140.npy"
#ba_140_simulation = np.load(file_path)
ba_140_simulation = np.load(loadpath + "Ba-140-broaded.npy")
ba_140_simulation = ba_140_simulation / np.linalg.norm(ba_140_simulation, 1) * np.sum(np.asarray(ba_140[1:]))
intensities = np.load(energy_path + "Ba-140-intensities.npy")
energies = np.load(energy_path + "Ba-140-energies.npy")
for ind, en in enumerate(energies):
    if intensities[ind] / np.sum(intensities) < 0.01:
        ax[2, 1].axvline(en / 10, color=colors[2], linewidth=1, ls=":")
    else:
        ax[2, 1].axvline(en / 10, color=colors[2])
ax[2, 1].plot((np.arange(len(ba_140_simulation)) + 0.5), np.asarray(ba_140_simulation), color=colors[1], label="Simulation")
ax[2, 1].set_xlabel("Energy [MeV]")
ax[2, 1].set_yscale('log')
# ax[2, 1].text(68.5, 17500, r'\texttimes', style='normal', bbox=dict(facecolor= 'gray', alpha= 0.3, boxstyle='round,pad=0.2'))
ax[2, 1].set_ylim(bottom=1)
################################################################################
print("c60")
ax[0, 2].title.set_text('Co-60')
ax[0, 2].plot(np.arange(1, len(co_60)+1) +0.5, np.asarray(co_60), color=colors[0])
ax[0, 2].grid()
file_path = loadpath + "Co-60.npy"
co_60_simulation = np.load(loadpath + "Co-60-broaded.npy")

source_particles = 1.055 * 10**8 # from heath
detector_efficiency = 0.015 # read out heath p.
co_60_simulation *= (source_particles / particles_simulation * detector_efficiency)

first_peak = 0
second_peak = 0

intensities = np.load(energy_path + "Co-60-intensities.npy")
energies = np.load(energy_path + "Co-60-energies.npy")
for ind, en in enumerate(energies):
    if intensities[ind] / np.sum(intensities) < 0.01:
        ax[0, 2].axvline(en / 10, color=colors[2], linewidth=1, ls=":")
    else:
        print(intensities[ind] / np.sum(intensities))
        if first_peak == 0: first_peak = (en/10)
        else: second_peak = (en/10)
        ax[0, 2].axvline(en / 10, color=colors[2])

#ax[0, 2].axvline(2*first_peak, color=colors[3], linewidth=1, ls=":")
#ax[0, 2].axvline(2*second_peak, color=colors[3], linewidth=1, ls=":")
ax[0, 2].axvline(first_peak+second_peak, color=colors[3], linewidth=1, ls=":")
ax[0, 2].plot((np.arange(len(co_60)) + 0.5)[1:], np.asarray(co_60_simulation) * 2, color=colors[1])
ax[0, 2].set_yscale('log')

################################################################################
print("zn65")
ax[1, 0].title.set_text('Zn-65')
ax[1, 0].plot(np.arange(len(zn_65))+0.5, np.asarray(zn_65), color=colors[0])
ax[1, 0].grid()
#file_path = loadpath + "Zn-65.npy"
zn_65_simulation = np.load(loadpath + "Zn-65-broaded.npy")
## 04.12.2021 to account for beta+ 511 keV peak
source_particles = 6.33 * 10**7 # from heath / second factor 04.12.2021 to account for the normalization of the spectrum # factor 0.5 since 2 gammas are created
detector_efficiency = 0.015 # read out heath p. 90
particles_simulation = 1
zn_65_simulation *= (source_particles / particles_simulation * detector_efficiency)

intensities = np.load(energy_path + "Zn-65-intensities.npy")
energies = np.load(energy_path + "Zn-65-energies.npy")
for ind, en in enumerate(energies):
    if intensities[ind] / np.sum(intensities) < 0.01:
        ax[1, 0].axvline(en / 10, color=colors[2], linewidth=1, ls=":")
    else:
        ax[1, 0].axvline(en / 10, color=colors[2])

ax[1, 0].set_ylabel("Counts")
ax[1, 0].plot((np.arange(len(zn_65)) + 0.5)[:-1], np.asarray(zn_65_simulation), color=colors[1])
ax[1, 0].set_yscale('log')
ax[1, 0].set_ylim(bottom=30)

################################################################################
print("y88")
ax[1, 2].title.set_text('Y-88$^{*}$')
#äax[1, 2].text(100, 10**6, 'spectrum normalized with total counts', fontsize=6, ha='center')
#ax[1, 2].title(r'\fontsize{12pt}{3em}\selectfont{}{Y-88\r}{\fontsize{6pt}{3em}\selectfont{}(spectrum normalized with total counts)}')
ax[1, 2].plot(np.arange(1, len(y_88)+1) + 0.5, np.asarray(y_88), color=colors[0])
ax[1, 2].grid()
y_88_simulation = np.load(loadpath + "Y-88-broaded.npy")
#source_particles = ?? # from heath
#detector_efficiency = ?? # read out heath p. 90
#y_88_simulation *= (source_particles / particles_simulation * detector_efficiency)

intensities = np.load(energy_path + "Y-88-intensities.npy")
energies = np.load(energy_path + "Y-88-energies.npy")
for ind, en in enumerate(energies):
    if intensities[ind] / np.sum(intensities) < 0.01:
        ax[1, 2].axvline(en / 10, color=colors[2], linewidth=1, ls=":")
    else:
        ax[1, 2].axvline(en / 10, color=colors[2])

y_88_simulation = y_88_simulation / np.linalg.norm(y_88_simulation, 1) * np.sum(np.asarray(y_88[1:]))
ax[1, 2].plot((np.arange(len(y_88)) + 0.5)[1:], np.asarray(y_88_simulation), color=colors[1])
ax[1, 2].set_yscale('log')

# ax[1, 2].text(310, 106000, r'\texttimes', style='normal', bbox=dict(facecolor= 'gray', alpha= 0.3, boxstyle='round,pad=0.2'))

################################################################################
print("cs137")
ax[2, 0].title.set_text('Cs-137')
ax[2, 0].plot(np.arange(len(cs_137))+0.5, np.asarray(cs_137), color=colors[0])
ax[2, 0].grid()
cs_137_simulation = np.load(loadpath + "Cs-137-broaded.npy")
source_particles = 3.07 * 10**7 # from heath
detector_efficiency = 0.02 # read out heath p. 90
cs_137_simulation *= (source_particles / particles_simulation * detector_efficiency)

intensities = np.load(energy_path + "Cs-137-intensities.npy")
energies = np.load(energy_path + "Cs-137-energies.npy")
for ind, en in enumerate(energies):
    if intensities[ind] / np.sum(intensities) < 0.01:
        ax[2, 0].axvline(en / 10, color=colors[2], linewidth=1, ls=":")
    else:
        ax[2, 0].axvline(en / 10, color=colors[2])

ax[2, 0].plot((np.arange(len(cs_137_simulation))+0.5), np.asarray(cs_137_simulation), color=colors[1])
ax[2, 0].set_ylabel("Counts")
ax[2, 0].set_xlabel("Energy [MeV]")
ax[2, 0].set_yscale('log')
ax[2, 0].set_ylim(bottom=100)

################################################################################
print("mn54")
ax[0, 1].title.set_text('Mn-54')
ax[0, 1].plot(np.arange(len(mn_54)) + 0.5, np.asarray(mn_54), color=colors[0])
ax[0, 1].grid()
mn_54_simulation = np.load(loadpath + "Mn-54-broaded.npy")
source_particles = 3.07 * 10**7 # from heath
detector_efficiency = 0.02 # read out heath p. 90
mn_54_simulation *= (source_particles / particles_simulation * detector_efficiency)

intensities = np.load(energy_path + "Mn-54-intensities.npy")
energies = np.load(energy_path + "Mn-54-energies.npy")
for ind, en in enumerate(energies):
    if intensities[ind] / np.sum(intensities) < 0.01:
        ax[0, 1].axvline(en / 10, color=colors[2], linewidth=1, ls=":")
    else:
        ax[0, 1].axvline(en / 10, color=colors[2])

ax[0, 1].plot((np.arange(len(mn_54)) + 0.5)[:-1], np.asarray(mn_54_simulation), color=colors[1])
ax[0, 1].set_yscale('log')
ax[0, 1].set_ylim(bottom=5)

################################################################################
print("Au198")
ax[2, 2].title.set_text('Au-198$^{*}$')
ax[2, 2].plot(np.arange(0, len(au_198)-1) + 0.5, np.asarray(au_198[1:]), color=colors[0])
ax[2, 2].grid()
au_198_simulation = np.load(loadpath + "Au-198-broaded.npy")
#source_particles = ??
#detector_efficiency = ?? # read out heath p. 90
#au_198_simulation *= (source_particles / particles_simulation * detector_efficiency)

intensities = np.load(energy_path + "Au-198-intensities.npy")
energies = np.load(energy_path + "Au-198-energies.npy")
for ind, en in enumerate(energies):
    if intensities[ind] / np.sum(intensities) < 0.01:
        ax[2, 2].axvline(en / 10, color=colors[2], linewidth=1, ls=":")
    else:
        ax[2, 2].axvline(en / 10, color=colors[2])

au_198_simulation = au_198_simulation / np.linalg.norm(au_198_simulation, 1) * np.sum(np.asarray(au_198[1:]))
ax[2, 2].plot((np.arange(len(au_198)) + 0.5)[:-1], np.asarray(au_198_simulation), color=colors[1])
ax[2, 2].set_xlabel("Energy [MeV]")
ax[2, 2].set_yscale('log')
#ax[2, 2].text(115, 113000, r'\texttimes', style='normal') #, bbox=dict(facecolor= 'gray', alpha= 0.3, boxstyle='round,pad=0.2'))

################################################################################

ax[0,0].set_xticks([0, 100, 200])
ax[0,0].set_xticklabels([0, 1.0 ,2.0])

ax[1,0].set_xticks([0, 50, 100])
ax[1,0].set_xticklabels([0,0.5,1.0])

ax[2,0].set_xticks([0, 50, 100])
ax[2,0].set_xticklabels([0, 0.5, 1.0])

ax[0,1].set_xticks([0, 50 ,100, 150])
ax[0,1].set_xticklabels([0, 0.5, 1.0 ,1.5])

ax[1,1].set_xticks([0, 50, 100])
ax[1,1].set_xticklabels([0, 0.5 ,1.0])

ax[2,1].set_xticks([0, 25, 50, 75])
ax[2,1].set_xticklabels([0, 0.25, 0.5, 0.75])

ax[0,2].set_xticks([0, 100, 200])
ax[0,2].set_xticklabels([0, 1.0, 2.0])

ax[1,2].set_xticks([0, 100, 200, 300])
ax[1,2].set_xticklabels([0, 1.0, 2.0, 3.0])

ax[2,2].set_xticks([0, 50, 100])
ax[2,2].set_xticklabels([0,0.5,1.0])


plt.savefig(figures_path + 'experimental_all.pgf', bbox_inches='tight')


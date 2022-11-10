# Implementation and Validation of the Pulse-Height Tally in OpenMC Code

All input files, results of the simulations, and scripts for the paper </br>

**Implementation and Validation of the Pulse-Height Tally in OpenMC** </br>

by: Christopher Fichtlscherer, Milon Miah, Friederike Frieß, Malte Göttsche, Moritz Kütt 

are contained in this repository.

### 1) Run time Analysis

The folder *geant-time* and *openmc-time* contain the detector simulations. The file *runtimes* contains the results of these simulations.

### 2) Analytic Validation

The file *results_openmc_multilayered.txt* contains the results of the OpenMC simulation in the simplified version. The script *multilayered_analytical_plot.py* produces Figure 4. The file *define_colors.py* contains the used colors defined in a python dictionary.

### 3) Software-based Validation

Many incorrect simulations were performed for this validation step. We show here only the correct results used at the end. The script *plots_paper.py* creates Figure 6 and Figure 7 of the paper. 
The folders *run-27*, *run-42*, *run-43*, and *run-44* contain the respective simulation results, input files, and log files, which contain further information about the simulations.

### 4) Experimental Validation

The script *fit_detector_resolution.py* fits the detector resolution of the results in Heath. It creates Figure 9. The file *heath_experimental_spectra.py* contains the measurement results, read out by hand in form of lists. The folder *isotope_emissions* contains the intensities, the energies and the used bins for the nine analyzed isotopes. The simulated energies and intensities are listed below (energies in keV, intensities in fractions):

**Al-28** - [1778.987], [1.]

**Mn-54** - [ 13.846,  29.966,  43.8  ,  63.17 ,  99.49 , 113.51 , 118.837, 132.687, 162.66 , 183.83 , 275.18 , 304.849, 418.44 , 423.722, 437.575, 467.5  , 537.261, 551.08 , 699.89 ], [2.19366653e-02, 2.53587851e-01, 3.50986645e-05, 5.26479968e-07, 3.50986645e-07, 2.89563982e-04, 1.09683327e-03, 3.64148645e-03,       1.11876993e-01, 1.75493323e-05, 6.58099960e-06, 7.72170620e-02, 6.58099960e-05, 5.66843432e-02, 3.47038046e-02, 3.50986645e-05, 4.38733307e-01, 5.61578633e-05, 1.49169324e-05] 

**Co-60** - [ 347.14 ,  826.1  , 1173.228, 1332.492, 2158.57 , 2505.692], [3.75283523e-05, 3.80287303e-05, 4.99627464e-01, 5.00290965e-01, 6.00453637e-06, 1.00075606e-08]

**Rb-86** - [1077.],  [1.]

**Y-88** - [ 850.6,  898.042, 1382.2, 1836.063, 2734., 3219.7], [3.38090333e-04, 4.83571627e-01, 1.07574197e-04, 5.12258080e-01, 3.68825817e-03, 3.63703237e-05]

**Cs-137** - [283.5  , 661.657], [6.81546471e-06, 9.99993185e-01]

**Ba-140** - [ 13.846,  29.966,  43.8  ,  63.17 ,  99.49 , 113.51 , 118.837, 132.687, 162.66 , 183.83 , 275.18 , 304.849, 418.44 , 423.722, 437.575, 467.5  , 537.261, 551.08 , 699.89 ], [2.19366653e-02, 2.53587851e-01, 3.50986645e-05, 5.26479968e-07, 3.50986645e-07, 2.89563982e-04, 1.09683327e-03, 3.64148645e-03, 1.11876993e-01, 1.75493323e-05, 6.58099960e-06, 7.72170620e-02, 6.58099960e-05, 5.66843432e-02, 3.47038046e-02, 3.50986645e-05, 4.38733307e-01, 5.61578633e-05, 1.49169324e-05]

**Au-198** - [411.80205,  675.8836 , 1087.6842], [0.99001863, 0.00833596, 0.00164541]

**Zn-65** - [344.95, 770.6, 1115.539], [5.05542888e-05, 5.35515787e-05, 9.99895894e-01] (additional 511 keV gammas added in the script)

The script *experimental_setup.py* runs the simulation for the eight isotopes: Al-28, Mn-54, Co-60, Rb-86, Y-88, Cs-137, Ba-140, Au-198.  The script *broadening_spectrum*, broads the simulated PHT results. 

The entire routine for simulation of Zn-65 with the additional 511keV peak is carried out in the folder *Zn-65-511peak*.

The results of these simulations can be found in *experimental_broadened_spectra*.

The file *plot_experimental.py* creates Figure 10.

The file *define_colors.py* contains the used colors for the plotting in form of a dictionary.

### 5) TikZ Figures

This folder contains the scripts for the three TikZ graphics used.
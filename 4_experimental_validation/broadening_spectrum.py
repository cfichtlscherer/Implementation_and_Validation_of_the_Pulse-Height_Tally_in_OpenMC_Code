"""
Nov 05, 2021
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License

This skript broadens a gamma spectrum.
"""

import numpy as np
import matplotlib.pyplot as plt 
from tqdm import tqdm

def broadening_spectrum(isotope_name, energy_bins):
    spectrum = np.load(isotope_name + ".npy")[1:]
    number_particles = 10**7

    E1 = energy_bins[0]
    E2 = energy_bins[-1]
    number_bins = len(energy_bins)
    
    bin_boarders = energy_bins
    bin_centers = np.asarray(list(bin_boarders)[:-1]) + (bin_boarders[1] - bin_boarders[0])/2
    #a = 3.991 * 10**-3 # MeV**0.5
    a = 3.377 * 10**-3 # MeV**0.5
    b = 3.756 * (1000**-0.5)  # MeV the two factors since we are working now with keV
    
    # b = 3.991 * 10**-2 # MeV**0.5
    # a = 3.756 * (100**-0.5)  # MeV the two factors since we are working now with keV

    # be carful a=b and b=a in comparison to the paper 
    # we give E in 10**4 so a and b must be scaled by 10**-2

    c = 0
    
    #def FWHM(a, b, c, E):
    #    return a + b*(E + c*(E**2))**0.5
    #
    #def sigma(a, b, c, E):
    #    return FWHM(a, b, c, E) / (8 * np.log(2)**0.5)
    #
    #def gauss(a, b, c, E):
    #    return np.random.normal(loc=E, scale=sigma(a, b, c, E))
    #
    def gauss(a,b,c,E):
        sigma = (a*(E**0.5) + (b*E)) / (2 * (2*np.log(2))**0.5)
        return np.random.normal(loc=E, scale=sigma)
    
    spectrum_multiplied = (spectrum * number_particles).astype(int)
    new_values = []
    
    for i in tqdm(range(1, number_bins-2)):
        E = bin_centers[i]
        for j in range(spectrum_multiplied[i]):
            new_values += [gauss(a, b, c, E)]
    
    counts, bins = np.histogram(new_values, bins=bin_boarders)
    counts_normal = counts/np.sum(counts)
    np.save(isotope_name + "-broaded", counts_normal)


nuc_names = ["Al-28", "Mn-54", "Co-60", "Rb-86", "Y-88", "Cs-137", "Ba-140", "Au-198"]                   
energy_bin_list = [np.linspace(0, 2.2e6, 221),                                                           
                   np.linspace(0, 1.1e6, 111),                                                           
                   np.linspace(0, 2.58e6, 259),                                                          
                   np.linspace(0, 1.26e6, 127),                                                          
                   np.linspace(0, 2.58e6, 259),                                                        
                   np.linspace(0, 0.8e6, 81),                                                            
                   np.linspace(0, 0.7e6, 71),                                                            
                   np.linspace(0, 1.20e6, 121)]                                                                                     

#nuc_names = ["Al-28", "Co-60", "Rb-86", "Y-88"]
#energy_bin_list = [np.linspace(0, 2.2e6, 221),                                                           
#                   np.linspace(0, 2.58e6, 259),                                                          
#                   np.linspace(0, 1.26e6, 127),
#                   np.linspace(0, 2.58e6, 259),                                                        
#                   ] 

for i, isotope in enumerate(nuc_names):
    broadening_spectrum(isotope, energy_bin_list[i])



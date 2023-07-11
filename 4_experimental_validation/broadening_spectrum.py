"""
Jul 11, 2023
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License
"""

import numpy as np


def gauss(E, a=1, b=1, c=1):
    sigma = (a + b * (E + c * E**2)**0.5) / (2 * (2 * np.log(2))**0.5)
    return np.random.normal(loc=E, scale=sigma)


def broad_spectrum(pulse_height_values, energy_bin_boarders):

    energy_bin_centers = (energy_bin_boarders[1:] + energy_bin_boarders[:-1]) / 2
   
    # values are in keV
    a, b, c = -0.643e3, 6.794, 0.258e-3
    number_broadening_samples = 1e7

    samples = np.random.choice(energy_bin_centers[1:], size=int(number_broadening_samples), p=pulse_height_values[1:]/np.sum(pulse_height_values[1:]))
    broaded_pulse_height_values = gauss(samples, a, b, c)

    broaded_spectrum, _ = np.histogram(broaded_pulse_height_values, bins=energy_bin_boarders[1:])
    renormalized_broaded_spectrum = broaded_spectrum / np.sum(broaded_spectrum)
    renormalized_broaded_spectrum = np.array([0] + list(renormalized_broaded_spectrum))
    
    return renormalized_broaded_spectrum


nuc_names = ["Al-28", "Mn-54", "Co-60", "Rb-86", "Y-88", "Cs-137", "Ba-140", "Au-198", "Zn-65"]                   
energy_bin_list = [np.linspace(0, 2.2e6, 221),                                                           
                   np.linspace(0, 1.1e6, 111),                                                           
                   np.linspace(0, 2.58e6, 259),                                                          
                   np.linspace(0, 1.26e6, 127),                                                          
                   np.linspace(0, 2.58e6, 259),                                                        
                   np.linspace(0, 0.8e6, 81),                                                            
                   np.linspace(0, 0.7e6, 71),                                                            
                   np.linspace(0, 1.20e6, 121),
                   np.linspace(0, 1.30e6, 131)]                                                                                     

for i, isotope in enumerate(nuc_names):
    pulse_height_values = np.load("simulation_results/" + isotope + ".npy")
    renormalized_broaded_spectrum = broad_spectrum(pulse_height_values, energy_bin_list[i])
    np.save("experimental_broadened_spectra/" + isotope + "-broaded", renormalized_broaded_spectrum)
    print(isotope)


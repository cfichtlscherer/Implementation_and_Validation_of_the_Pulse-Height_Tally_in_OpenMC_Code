"""
Nov 05, 2021
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License

This skript broadens a gamma spectrum.
"""

import numpy as np
import matplotlib.pyplot as plt 
from tqdm import tqdm

spectrum = np.load("zn_spectrum_sharp.npy")[1:]

number_particles = 10**7

E1 = 0
E2 = 1.3
number_bins = 130
bin_boarders = np.linspace(E1, E2, number_bins + 1)
bin_centers = np.asarray(list(bin_boarders)[:-1]) + (bin_boarders[1] - bin_boarders[0])/2

a = 3.377 * 10**-3 # MeV**0.5                                                     
b = 3.756 * (1000**-0.5)  # MeV the two factors since we are working now with keV 

#a = 3.756 * 10**-2 # MeV
#b = 3.991 * 10**-2 # MeV**0.5

a,b = b,a

c = 0

def FWHM(a, b, c, E):
    return a + b*(E + c*(E**2))**0.5

def sigma(a, b, c, E):
    return FWHM(a, b, c, E) / (8 * np.log(2)**0.5)

def gauss(a, b, c, E):
    return np.random.normal(loc=E, scale=sigma(a, b, c, E))

def gauss(a,b,c,E):
    sigma = (a*(E**0.5) + (b*E)) / (2 * (2*np.log(2))**0.5)
    return np.random.normal(loc=E, scale=sigma)

spectrum_multiplied = (spectrum * number_particles).astype(int)

new_values = []

for i in tqdm(range(number_bins - 1)):
    E = bin_centers[i + 1]
    for j in range(spectrum_multiplied[i]):
        new_values += [gauss(a, b, c, E)]
    

counts, bins = np.histogram(new_values, bins=bin_boarders)
counts_normal = counts/np.sum(counts)
np.save("counts_normal", counts_normal)
print(len(counts_normal))
plt.plot(np.log(counts_normal))
plt.show()

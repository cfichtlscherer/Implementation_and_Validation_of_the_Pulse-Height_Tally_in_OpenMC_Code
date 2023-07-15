"""
Apr 02, 2022
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License
"""

import numpy as np
from tqdm import tqdm
import os 
import matplotlib.pyplot as plt

import sys
sys.path.insert(1, '..')
from evaluate_runs import ks_test

all_ks_test_results = []

for i in tqdm(range(1, 301)):
    if "mcnp_spectrum_" + str(i) + ".npy" in os.listdir():
        mcnp_spectrum = np.load("mcnp_spectrum_" + str(i) + ".npy")[4:-1]
        openmc_spectrum = np.load("openmc_results_" + str(i*1e4) + ".npy")[3:-1]
        plt.semilogy(mcnp_spectrum, label="mcnp")
        plt.semilogy(openmc_spectrum, label="openmc")
        plt.legend()
        #plt.semilogy(mcnp_spectrum - openmc_spectrum)
        plt.show()
        ks_test_result = ks_test(mcnp_spectrum, openmc_spectrum)
        all_ks_test_results += [ks_test_result]

np.save("all_ks_test_results", np.asarray(all_ks_test_results))




"""
Sep 30, 2021
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License
"""

import numpy as np
import matplotlib.pyplot as plt 

bins = np.linspace(0,0.662,2048)

tally_values = np.genfromtxt("build/pht_tally_output_geant.txt", delimiter=",")[:-1]

hist, bin_edges = np.histogram(tally_values, bins=bins)

plt.plot(np.log(hist))
plt.show()


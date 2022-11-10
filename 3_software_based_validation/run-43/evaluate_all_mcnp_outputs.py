"""
Apr 01, 2022
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License
"""

import numpy as np
from tqdm import tqdm

def extract_spectrum_mcnp(mcnp_outputfile):
    """ this function extracts the pht output of a mcnp calculation"""

    mcnp_f = open(mcnp_outputfile, "r").read()
    mcnp_start = mcnp_f.rfind("tally type 8    pulse height distribution.")
    mcnp_end = mcnp_f.find("results of 10 statistical checks for the estimated answer for the tally fluctuation", mcnp_start)

    mcnp_f_cut = mcnp_f[mcnp_start+273:mcnp_end-184]    # "273" and "184" are a try-and-error result
    mcnp_data_array = np.fromstring(mcnp_f_cut, sep=" ")

    mcnp_energy_bin = mcnp_data_array[0::3]             # numpy slicing
    mcnp_counts = mcnp_data_array[1::3]
    mcnp_error = mcnp_data_array[2::3]

    mcnp_resized_counts = mcnp_counts

    return mcnp_resized_counts

for i in tqdm(range(1, 301)):
    mcnp_outputfile = "mcnp_input_" + str(i) + ".o"
    mcnp_resized_counts = extract_spectrum_mcnp(mcnp_outputfile)
    np.save("mcnp_spectrum_" + str(i), mcnp_resized_counts)


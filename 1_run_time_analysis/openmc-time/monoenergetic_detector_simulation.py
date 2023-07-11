"""
Sep 24, 2020
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License

Simulating a Gamma source with a detector.
"""

import numpy as np
import matplotlib.pyplot as plt
import openmc
import pandas as pd
import time as time

from models import run_openmc


times = []

for i in range(100):
    t0 = time.time()

    endfb_71_lanl = "/home/cpf/all_openmc_xsections/lanl_based/mcnp_endfb71/cross_sections.xml"
    parameter_dic = {"cross_sections_openmc": endfb_71_lanl,
                 "energy": 0.6617 * 1e6,
                 "number_particles": 1e6,
                 "density": 3.667,
                 "radius": 2.84,
                 "comment": "run time"}

    bins_middle = np.linspace(parameter_dic["energy"] / 2048, parameter_dic["energy"], 2048)                     
    parameter_dic["bins"] = [0, 0.001, 1] + list(bins_middle + 0.5 * (bins_middle[2] - bins_middle[1])) + [20e6] 

    run_openmc(parameter_dic)
    times += [time.time() - t0]
    print(times)
    print(sum(times)/(i+1))


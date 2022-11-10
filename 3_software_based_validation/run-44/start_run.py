"""
Mär 13, 2022
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License

Check if this setting was already run
Create new folder, runs openmc script in it, places MCNP script in it.
"""

import numpy as np
import matplotlib.pyplot as plt
import os as os
import openmc
import hashlib as hashlib
import time as time

from models import run_openmc
from models import build_mcnp_input


def generate_logfile(parameter_dic):
    """ generates the logfile """

    model_file = open("models.py", "r").read()
    hash_value_model = hashlib.sha256(model_file.encode("utf-8")).hexdigest()[0:10]

    parameter_dic_file = str(parameter_dic)
    hash_value_parameter_dic = hashlib.sha256(parameter_dic_file.encode("utf-8")).hexdigest()[0:10]

    logfile = open("logfile", "a+")
    logfile.write("Time of Execution:".ljust(30, " ") + time.strftime("%H:%M:%S-%d.%m.%Y") + "\n\n")
    logfile.write("Hash Value Model:".ljust(30, " ") + hash_value_model + "\n")
    logfile.write("Hash Value Parameters:".ljust(30, " ") + hash_value_parameter_dic + "\n")
    logfile.write("Comment:".ljust(30, " ") + parameter_dic["comment"] + "\n\n")

    for key in parameter_dic.keys():
        logfile.write((str(key) + ":").ljust(30, " ") + str(parameter_dic[key]) + "\n")

    logfile.close()


def check_originality(parameter_dic):
    """ checks if this run has been performed before,
    by comparing the hash value of the models.py script
    and the parameter_dic """

    # determine the hash values of the current run
    model_file = open("models.py", "r").read()
    hash_value_model = hashlib.sha256(model_file.encode("utf-8")).hexdigest()[0:10]

    parameter_dic_file = str(parameter_dic)
    hash_value_parameter_dic = hashlib.sha256(parameter_dic_file.encode("utf-8")).hexdigest()[0:10]

    # go through all logfiles and search for these hash values
    files_here = os.listdir()
    runs = [f for f in files_here if "run-" in f]

    for run in runs:
        if "big" not in run:
            logfile = open(run + "/logfile", "r").read()
            hash_model_calc = logfile[logfile.find("Hash Value Model:")+30:logfile.find("Hash Value Model:")+40]
            hash_para_calc = logfile[logfile.find("Hash Value Parameters:")+30:logfile.find("Hash Value Parameters:")+40]
            if hash_value_model + hash_value_parameter_dic == hash_model_calc + hash_para_calc:
                return False, run

    return True, "xxx"


def start_run(parameter_dic):
    """ creates a folder and in it the MCNP input file
    runs the openmc file in this folder"""

    new, name = check_originality(parameter_dic)
    if new is False:
        print("Run exists already - " + name)
        exit()

    files_here = os.listdir()
    runs = [f for f in files_here if "run-" in f]
    new_folder = "run-" + str(len(runs) + 1 - 7)

    os.system("mkdir " + new_folder)
    generate_logfile(parameter_dic)

    # check here if this run exists already

    os.system("mv logfile " + new_folder)

    build_mcnp_input(parameter_dic)
    os.system("mv mcnp_input " + new_folder)

    run_openmc(parameter_dic)
    os.system("mv *.xml *.out *.h5 *.npy " + new_folder)

    os.system("cp models.py start_run.py " + new_folder)


def start_big_run(parameter_dic):
    """ creates a folder and in it the MCNP input file
    runs the openmc file in this folder"""

    files_here = os.listdir()
    runs = [f for f in files_here if "run-" in f]
    new_folder = "run-" + str(len(runs) + 1 - 7)

    os.system("mkdir " + new_folder)
    generate_logfile(parameter_dic)

    # check here if this run exists already

    os.system("mv logfile " + new_folder)
    
    shift = 20

    #for energy in range(1,301):
    for energy in [145, 169, 193, 241, 268, 284]:
        parameter_dic["energy"] = energy * 1e4
        bins_middle = np.linspace(parameter_dic["energy"] / 2048, parameter_dic["energy"], 2048)
        parameter_dic["bins"] = [0, 0.001, 1] + list(bins_middle + 0.5 * (bins_middle[2] - bins_middle[1]) + shift) + [20e6]
        build_mcnp_input(parameter_dic)
        os.system("mv mcnp_input " + new_folder + "/mcnp_input_" + str(energy))

    os.system("cp models.py start_run.py " + new_folder)


def start_big_openmc_run(parameter_dic, folder_name):
    """starts openmc runs the openmc file in this folder"""

    if folder_name not in os.listdir():
        os.system("mkdir " + folder_name)
    
    for energy in [300, 250, 200, 150] + list(range(1,301)):   # start with these numbers to control results early
        parameter_dic["energy"] = energy * 1e4
        bins_middle = np.linspace(parameter_dic["energy"] / 2048, parameter_dic["energy"], 2048)
        parameter_dic["bins"] = [0, 0.001, 1] + list(bins_middle + 0.5 * (bins_middle[2] - bins_middle[1])) + [20e6]

        if "openmc_results_" + str(energy) + ".npy" not in os.listdir(folder_name):             
            run_openmc(parameter_dic)                                             
            os.system("mv openmc_results.npy " + folder_name +"/openmc_results_" + str(energy) + ".npy")


def start_run_32(parameter_dic):
    """starts openmc runs the openmc file in this folder"""

    for energy in [145, 169, 193, 241, 268, 284]:
        parameter_dic["energy"] = energy * 1e4
        parameter_dic["bins"] = np.load("run-32/bins-" + str(energy) + ".npy")

        if "openmc_results_" + str(energy) + ".npy" not in os.listdir("run-32"):             
            run_openmc(parameter_dic)                                             
            os.system("mv openmc_results.npy run-32/openmc_results_" + str(energy) + ".npy")

def start_run_33(parameter_dic, folder_name):
    """starts openmc runs the openmc file in this folder"""

    if folder_name not in os.listdir():
        os.system("mkdir " + folder_name)
    
    for energy in [145, 169, 193, 241, 268, 284]:
        parameter_dic["energy"] = energy * 1e4
        bins_middle = np.linspace(parameter_dic["energy"] / 2048, parameter_dic["energy"], 2048)
        parameter_dic["bins"] = [0, 0.001, 1] + list(bins_middle + 0.5 * (bins_middle[2] - bins_middle[1]) + 20) + [20e6]

        if "openmc_results_" + str(energy) + ".npy" not in os.listdir(folder_name):             
            run_openmc(parameter_dic)                                             
            os.system("mv openmc_results.npy " + folder_name +"/openmc_results_" + str(energy) + ".npy")

# Cross-sections Overview OpenMC
# https://openmc.org/

endfb_71_official = "/home/cpf/all_openmc_xsections/official_libraries/endfb71_hdf5/cross_sections.xml"   # Official Data Library - ENDF/B-VII.1
endfb_80_official = "/home/cpf/all_openmc_xsections/official_libraries/endfb80_hdf5/cross_sections.xml"   # Official Data Library - ENDF/B-VIII.0
jeff_33_official = "/home/cpf/all_openmc_xsections/official_libraries/jeff33_hdf5/cross_sections.xml"     # Official Data Library - JEFF3.3

endfb_70_lanl = "/home/cpf/all_openmc_xsections/lanl_based/mcnp_endfb70/cross_sections.xml"               # LANL-Based Data Library - ENDF/B-VII.0
endfb_71_lanl = "/home/cpf/all_openmc_xsections/lanl_based/mcnp_endfb71/cross_sections.xml"               # LANL-Based Data Library - ENDF/B-VII.1
endfb_80_lanl = "/home/cpf/all_openmc_xsections/lanl_based/lib80x_hdf5/cross_sections.xml"                # LANL-Based Data Library - ENDF/B-VIII.0

jeff_32_other = "/home/cpf/all_openmc_xsections/other_libraries/jeff32_hdf5/cross_sections.xml"           # Other Data Library - JEFF3.2
jeff_33_other = "/home/cpf/all_openmc_xsections/other_libraries/jeff-3.3-hdf5/cross_sections.xml"         # Other Data Library - JEFF3.3
fendl_32_other = "/home/cpf/all_openmc_xsections/other_libraries/fendl-3.2-hdf5/cross_sections.xml"       # Other Data Library - FENDL3.2

# Cross-sections Overview MCNP
# Listing of Available ACE Data Tables Formerly Appendix G of the MCNP Manual - 2017

#ENDFB_VI_8 = ".84p"    # seems to be the right choice, from 2012
eprdata14 = ".14p"    # seems to be the right choice, from 2012

################################################################################
################################################################################
################################################################################

parameter_dic = {"cross_sections_openmc": endfb_71_lanl,
                 "cross_sections_mcnp": eprdata14,
                 "energy": 2.0 * 1e6,
                 "number_particles": 1e8,
                 "density": 3.667,
                 "radius": 2.84, 
                 "comment": "shift of energy bins by some eV to the right"}

bins_middle = np.linspace(parameter_dic["energy"] / 2048, parameter_dic["energy"], 2048)
parameter_dic["bins"] = [0, 0.001, 1] + list(bins_middle + 0.5 * (bins_middle[2] - bins_middle[1])) + [20e6]

#start_run_33(parameter_dic, "run-44")
start_big_run(parameter_dic)
#start_big_openmc_run(parameter_dic, "big_run-5-openmc")

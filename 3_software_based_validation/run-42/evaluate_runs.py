"""
Mär 13, 2022
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License
Is coming when the first MCNP input file was created.
Creates a plot of the spectrum.
Writes important numbers eg height photo-peak into the logfile.
"""

import numpy as np
import matplotlib.pyplot as plt
import os as os
import openmc
import hashlib as hashlib
import time as time


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


def ks_test(dis_1, dis_2):                                                              
    """calculates the maximum absolute norm difference of the cummulated distributions  
    Input: two distributions of the same size                                           
    Output: Maximum distance of the cumulated functions"""                              
                                                                                        
    cum_dis_1 = np.cumsum(dis_1) / np.sum(dis_1)
    cum_dis_2 = np.cumsum(dis_2) / np.sum(dis_2)                             
                                                                                        
    max_distance = np.max(abs(cum_dis_1 - cum_dis_2))                                   
                                                                                        
    return max_distance                                                                 


def write_to_logfile(run_name):
    """writes height of the full energy peak and their quotient to the logfile"""

    mcnp_spectrum = extract_spectrum_mcnp(run_name + "/outp")
    openmc_spectrum = np.load(run_name + "/openmc_results.npy")

    full_energy_peak_mcnp = mcnp_spectrum[-2]
    full_energy_peak_openmc = openmc_spectrum[-2]
    negative_bin_mcnp = mcnp_spectrum[0]
    sum_openmc = np.sum(openmc_spectrum)
    sum_mcnp = np.sum(mcnp_spectrum[1:])
    
    sum_openmc_after_three = np.sum(openmc_spectrum[3:])
    sum_mcnp_after_three = np.sum(mcnp_spectrum[4:])

    ks_test_result = ks_test(openmc_spectrum, mcnp_spectrum[1:])
    ks_test_result_after_three_bins = ks_test(openmc_spectrum[3:], mcnp_spectrum[4:])

    relative_quotient = full_energy_peak_openmc / full_energy_peak_mcnp

    evaluation_file = open("evaluate_runs.py", "r").read()
    hash_value_evaluation = hashlib.sha256(evaluation_file.encode("utf-8")).hexdigest()[0:10]

    logfile = open(run_name + "/logfile", "a+")

    if hash_value_evaluation not in evaluation_file:
        logfile.write("\n \n")
        logfile.write("EVALUATION".ljust(30, " ") + time.strftime("%H:%M:%S-%d.%m.%Y").ljust(30, " ") + hash_value_evaluation + "\n")
        logfile.write("Negative energy bin MCNP:".ljust(30, " ") + str(negative_bin_mcnp) + "\n")
        logfile.write("Sum MCNP (no neg. bin):".ljust(30, " ") + str(sum_mcnp) + "\n")
        logfile.write("Sum OpenMC:".ljust(30, " ") + str(sum_openmc) + "\n")
        logfile.write("Sum MCNP ([3:]):".ljust(30, " ") + str(sum_mcnp_after_three) + "\n")
        logfile.write("Sum OpenMC ([3:]):".ljust(30, " ") + str(sum_openmc_after_three) + "\n")
        logfile.write("Full energy peak MCNP:".ljust(30, " ") + str(full_energy_peak_mcnp) + "\n")
        logfile.write("Full energy peak OpenMC:".ljust(30, " ") + str(full_energy_peak_openmc) + "\n")
        logfile.write("Relative Quotient:".ljust(30, " ") + str(relative_quotient) + "\n")
        logfile.write("KS-test value:".ljust(30, " ") + str(ks_test_result) + "\n")
        logfile.write("KS-test value [3:]:".ljust(30, " ") + str(ks_test_result_after_three_bins))
    logfile.close()


def generate_spectra_plot(run_name):

    mcnp_spectrum = extract_spectrum_mcnp(run_name + "/outp")[1:]
    openmc_spectrum = np.load(run_name + "/openmc_results.npy")

    fig, ax1 = plt.subplots(figsize=(20, 15))

    ax2 = ax1.twinx()

    ax1.semilogy(mcnp_spectrum, label="MCNP")
    ax1.semilogy(openmc_spectrum, label="OpenMC", alpha=0.7)
    ax1.grid()
    ax1.set_xlabel("Bin number")
    ax1.set_ylabel("Intensity")
    ax1.legend()

    relative_error = 100*(abs(openmc_spectrum - mcnp_spectrum)/mcnp_spectrum)
    ax2.plot(relative_error, color="black", alpha=0.5)
    ax2.set_ylabel("Relative Error [%]")

    plt.savefig(run_name + "/comparison_plot.pdf")


def generate_spectra_sub_plot(run_name):

    mcnp_spectrum = extract_spectrum_mcnp(run_name + "/outp")[1:]
    openmc_spectrum = np.load(run_name + "/openmc_results.npy")
    
    fig = plt.figure(figsize=(20,15))
    gs = fig.add_gridspec(2, hspace=0)

    axs = gs.subplots(sharex=True, sharey=False)
    

    axs[0].semilogy(mcnp_spectrum, label="MCNP")
    axs[0].semilogy(openmc_spectrum, label="OpenMC", alpha=0.7)
    axs[0].grid()
    axs[0].set_xlabel("Bin number")
    axs[0].set_ylabel("Intensity")
    axs[0].legend()
    
    relative_error = 100*(abs(openmc_spectrum - mcnp_spectrum)/mcnp_spectrum)
    
    axs[1].plot(relative_error, color="black", marker=",", ls="")
    axs[1].plot(relative_error, color="black", ls="-", lw=0.5, alpha=0.5)
    axs[1].set_ylabel("Relative Error")
    axs[1].grid()
    
    for ax in axs:
        ax.label_outer()
    plt.savefig(run_name + "/comparison_sub_plot.pdf")


def generate_spectra_sub_plot_after_three(run_name):

    mcnp_spectrum = extract_spectrum_mcnp(run_name + "/outp")[4:]
    openmc_spectrum = np.load(run_name + "/openmc_results.npy")[3:]
    
    fig = plt.figure(figsize=(20,15))
    gs = fig.add_gridspec(2, hspace=0)

    axs = gs.subplots(sharex=True, sharey=False)
    

    axs[0].semilogy(mcnp_spectrum, label="MCNP")
    axs[0].semilogy(openmc_spectrum, label="OpenMC", alpha=0.7)
    axs[0].grid()
    axs[0].set_xlabel("Bin number")
    axs[0].set_ylabel("Intensity")
    axs[0].legend()
    
    relative_error = 100*(abs(openmc_spectrum - mcnp_spectrum)/mcnp_spectrum)
    
    axs[1].plot(relative_error, color="black", marker=",", ls="")
    axs[1].plot(relative_error, color="black", ls="-", lw=0.5, alpha=0.5)
    axs[1].set_ylabel("Relative Error")
    axs[1].grid()
    
    for ax in axs:
        ax.label_outer()
    plt.savefig(run_name + "/comparison_sub_plot_after_three.pdf")


def evaluate_run(run_name):
    """ runs the functions defined above to do a total evaluation of the run"""

    write_to_logfile(run_name)
    generate_spectra_plot(run_name)
    generate_spectra_sub_plot(run_name)
    generate_spectra_sub_plot_after_three(run_name)
    os.system("cp evaluate_runs.py " + run_name)

evaluate_run("run-27")

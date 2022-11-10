"""
Apr 01, 2022
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License
"""

import numpy as np
import matplotlib.pyplot as plt

import matplotlib
import matplotlib.ticker as mticker

from evaluate_runs import *

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': True,
})

colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

def get_mcnp_error(run):
    """ this function extracts the error of the pht of the output of a mcnp calculation"""

    mcnp_outputfile = run + "/outp"

    mcnp_f = open(mcnp_outputfile, "r").read()
    mcnp_start = mcnp_f.rfind("tally type 8    pulse height distribution.")
    mcnp_end = mcnp_f.find("results of 10 statistical checks for the estimated answer for the tally fluctuation", mcnp_start)

    mcnp_f_cut = mcnp_f[mcnp_start+273:mcnp_end-184]    # "273" and "184" are a try-and-error result
    mcnp_data_array = np.fromstring(mcnp_f_cut, sep=" ")

    mcnp_energy_bin = mcnp_data_array[0::3]             # numpy slicing
    mcnp_counts = mcnp_data_array[1::3]
    mcnp_error = mcnp_data_array[2::3]

    mcnp_resized_counts = mcnp_counts

    return mcnp_error


def generate_spectra_sub_plot_after_three():

    mcnp_spectrum = extract_spectrum_mcnp("run-42/outp")[4:-1]
    openmc_spectrum = np.load("run-27/openmc_results.npy")[3:-1]

    std = get_mcnp_error("run-27")[4:-1]

    print("length spectrum:".ljust(60), len(mcnp_spectrum))

    #fig, axarray = plt.subplots(2, 1, figsize = (6.8,4.5), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
    fig = plt.figure(figsize=(6.8,4.5))
    gs = fig.add_gridspec(2, hspace=0)

    axs = gs.subplots(sharex=True, sharey=False)

    axs[0].semilogy(openmc_spectrum, label="OpenMC", color=colors[0], lw=1)
    axs[0].semilogy(mcnp_spectrum, label="MCNP", color=colors[1], lw=1, alpha=0.7)
    axs[0].grid()

    # insert zoom in plot 1
    axins = axs[0].inset_axes([0.05, 0.5, 0.2, 0.4]) # [x0, y0, width, height]
    axins.semilogy(openmc_spectrum, color=colors[0])#, marker="x", markersize=1)
    axins.semilogy(mcnp_spectrum, color=colors[1])#, marker="x", markersize=1)
    x1, x2, y1, y2 = 85, 120, 1.7e-4, 2.5e-4
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.get_xaxis().set_ticks([])
    axins.get_yaxis().set_ticks([])
    axins.get_xaxis().set_visible(False)
    axins.get_yaxis().set_visible(False)
    axs[0].indicate_inset_zoom(axins, edgecolor="black")

    # insert zoom in plot 2
    axins = axs[0].inset_axes([0.3, 0.5, 0.2, 0.4]) # [x0, y0, width, height]
    axins.semilogy(openmc_spectrum, color=colors[0])#, marker="x", markersize=1)
    axins.semilogy(mcnp_spectrum, color=colors[1])#, marker="x", markersize=1)
    x1, x2, y1, y2 = 1830, 1900, 1.5e-5, 3.5e-5
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.get_xaxis().set_ticks([])
    axins.get_yaxis().set_ticks([])
    axins.get_xaxis().set_visible(False)
    axins.get_yaxis().set_visible(False)
    axs[0].indicate_inset_zoom(axins, edgecolor="black")

    # insert zoom in plot 3
    axins = axs[0].inset_axes([0.6, 0.5, 0.2, 0.4]) # [x0, y0, width, height]
    axins.semilogy(openmc_spectrum, color=colors[0])#, marker="x", markersize=1)
    axins.semilogy(mcnp_spectrum, color=colors[1])#, marker="x", markersize=1)
    x1, x2, y1, y2 = 1930, 1970, 2e-4, 1.5e-3
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.get_xaxis().set_ticks([])
    axins.get_yaxis().set_ticks([])
    axins.get_xaxis().set_visible(False)
    axins.get_yaxis().set_visible(False)
    axs[0].indicate_inset_zoom(axins, edgecolor="black")

    axs[0].set_xlabel("Bin number")
    axs[0].set_ylabel("Intensity")
    axs[0].legend()


    important_energies = [0.001, 33.2, 184.0, 478.0, 633.01, 661.7]
    axs[1].set_xticks([round(i/661.7*2047) for i in important_energies], [r"$10^{-6}$"] + [round(i/1000,4) for i in important_energies if i > 1], rotation=45)

    print("xticks bins".ljust(50), [round(i/661.7*2047) for i in important_energies])

    relative_error = (openmc_spectrum - mcnp_spectrum)/mcnp_spectrum
    axs[1].plot(relative_error, color="black", marker=",", ls="")
    axs[1].plot(relative_error, color="black", ls="-", lw=0.8, alpha=0.5)
#    axs[1].plot(2*std, color=colors[2], lw=0.5, alpha=0.5, label="Uncertainties")
#    axs[1].plot(-2*std, color=colors[2], lw=0.5, alpha=0.5)
    axs[1].set_xlabel("Energy [MeV]")
    axs[1].set_ylabel("Relative Error")
    axs[1].set_xlim(-100,2158)
#    axs[1].legend()
    axs[1].grid()

    print("in 1 std: ", sum((abs(relative_error) < 1*std).astype(int)) / len(std) )
    print("in 2 std: ", sum((abs(relative_error) < 2*std).astype(int)) / len(std) )
    print("in 3 std: ", sum((abs(relative_error) < 3*std).astype(int)) / len(std) )

    for ax in axs:
        ax.label_outer()

    plt.savefig("/home/cpf/Desktop/publications-in-work/Implementation-and-Validation-of-the-Pulse-Height-Tally-in-OpenMC/figures/cs_137.pgf", bbox_inches = 'tight')


def generate_ks_test_plot():
    plt.figure(figsize=(6.8,3.5))

    plt.xlabel("Gamma ray Energy [MeV]")
    plt.ylabel("Kolmogorov-Smirnov test statistic")

    problem_indices = [145, 169, 193, 241, 268, 284]
    ks_test_results = np.load("run-43/all_ks_test_results.npy")
    ks_test_results_problems = [ks_test_results[i-1] for i in problem_indices]
    print(ks_test_results_problems)
    ks_test_results_new = np.load("run-44/all_ks_test_results.npy")
    print(ks_test_results_new)
    ks_tests_cleaned = ks_test_results.copy()
    for index, value in enumerate(problem_indices):
        ks_tests_cleaned[value - 1] = ks_test_results_new[index] 
    
    cutted_beginning = 4
    viewed_range = range(1,301)[cutted_beginning:]

    plt.plot(range(301), 301 * [0.03], color =colors[1], ls="--", marker="")
    #plt.text(260, 0.031, "$d_{0.05} = 0.03$")
    plt.text(4, 0.0315, "$d_{0.05} = 0.03$")

    plt.plot(viewed_range, ks_test_results[cutted_beginning:], color=colors[0], alpha=0.3, label="Original test results")
#    plt.plot(viewed_range, ks_tests_cleaned[cutted_beginning:], color=colors[0], label="Energy shift of problematic bins")
    plt.plot(viewed_range, ks_tests_cleaned[cutted_beginning:], color=colors[0], label="Falsely bins shifted")
    
    plt.plot(problem_indices, ks_test_results_problems, marker="x", ls="", color=colors[0], alpha=0.3)
    # plt.plot(problem_indices, [ks_test_results[i] for i in problem_indices], marker="x", ls="", color=colors[0])
    
    #plt.axis([0, 300, -0.002, 0.05])     #  plt.axis([xmin,xmax,ymin,ymax])

    plt.plot(66 - cutted_beginning, np.load("run-43/all_ks_test_results.npy")[65 - cutted_beginning], marker=".", color="black")

    plt.grid()
    plt.legend()
    plt.xticks([0, 50, 100, 150, 200, 250, 300], ["0.0", "0.5", "1.0", "1.5", "2.0", "2.5", "3.0"])
    plt.xlim(0,300)
    #plt.ylim(0,0.22)


    plt.text(50, 0.015, "Cs-137 spectrum")
    plt.plot([62.5, 68], [0.0015, 0.014], color="black", marker="", lw=0.5)

    plt.savefig("/home/cpf/Desktop/publications-in-work/Implementation-and-Validation-of-the-Pulse-Height-Tally-in-OpenMC/figures/ks_tests.pgf", bbox_inches = 'tight')


#generate_spectra_sub_plot_after_three()
generate_ks_test_plot()


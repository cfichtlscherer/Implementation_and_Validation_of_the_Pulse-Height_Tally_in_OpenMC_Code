"""
Jan 31, 2021
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License

This Python skript runs all the small commands for generating the pulse height tally spectrum.
"""

import numpy as np
import matplotlib.pyplot as plt 

import os as os

import pandas as pd

import time as time

#os.system("cd /home/cpf/geant/geant4.10.06-install/bin && source geant4.sh")
#input("-> source activated?")
#os.system("mkdir drm_results")


def run_one_energy(energy):
    """ runs the G4 calculation for one energy"""

    path = "/home/cpf/Desktop/geant_compton_edge-02122021-time/TestEm4/src/"
    
    os.system("cp /home/cpf/Desktop/geant_compton_edge-02122021-time/TestEm4/src/PrimaryGeneratorAction.cc " + path)

    # Read in the file
    with open(path + 'PrimaryGeneratorAction.cc', 'r') as file :
      filedata = file.read()
    
    # Replace the target string
    filedata = filedata.replace('XXXXXXXXXX', str(energy))
    
    # Write the file out again
    with open(path + 'PrimaryGeneratorAction.cc', 'w') as file:
      file.write(filedata)

    os.system("rm -r build")
    os.system("mkdir build")
    os.system("cd build && cmake -DGeant4_DIR=/home/cpf/geant/geant4.10.06.p02-install/lib/Geant4-10.6.3 /home/cpf/Desktop/geant_compton_edge-02122021-time/TestEm4")
    os.system("cd build && make")
    os.system("cd build && ./TestEm4 TestEm4.in")
    os.system("cp plotHisto.C build")
    os.system("cd build && root -b -q plotHisto.C")
    data = np.genfromtxt("build/pht_tally_output_geant.txt", delimiter=",")[:-1]  

    save_path = "/home/cpf/Desktop/geant_compton_edge-02122021-time/TestEm4/drm_results/"

    geant_spectrum, bin_edges = np.histogram(data, bins=list(np.linspace(0, energy/100, 2049)))
    geant_spectrum = geant_spectrum / 10**7
    np.save(save_path + str(energy), geant_spectrum)

t0 = time.time()
for i in range(66,67):
    energy = i / 100
    save_path = "/home/cpf/Desktop/geant_compton_edge-02122021-time/TestEm4/drm_results/"
    if os.path.isfile(save_path + str(energy) + ".npy") == False:
        run_one_energy(energy)

print("time: ", time.time() - t0)

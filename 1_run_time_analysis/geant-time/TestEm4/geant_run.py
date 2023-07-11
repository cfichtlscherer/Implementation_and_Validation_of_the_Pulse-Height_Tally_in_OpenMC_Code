"""
Jan 31, 2021
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License

This Python skript runs all the small commands for generating the pulse height tally spectrum.
"""

import numpy as np
import matplotlib.pyplot as plt 
import time
import os as os

import pandas as pd

#os.system("cd /home/cpf/geant/geant4.10.06-install/bin && source geant4.sh")
input("-> source activated?")

times = []

#for i in range(100):
for i in range(1):

    t0 = time.time()

    os.system("rm -r build")
    print("-> build dir deleted")
    os.system("mkdir build")
    print("-> build dir generated")
    os.system("cd build && cmake -DGeant4_DIR=/home/cpf/Codes/geant4-v11.1.0-install/lib/Geant4-11.1.2 " +
            "/home/cpf/Desktop/Implementation_and_Validation_of_the_Pulse-Height_Tally_in_OpenMC_Code/1_run_time_analysis/geant-time/TestEm4")
    print("-> cmake command")
    os.system("cd build && make -j1")
    print("-> run make file")
    os.system("cd build && ./TestEm4 TestEm4.in")

    times += [time.time() - t0]                     
    print(times)
    print(len(times))
    print(sum(times)/len(times))
print(times)                                        
print(sum(times)/100)                               


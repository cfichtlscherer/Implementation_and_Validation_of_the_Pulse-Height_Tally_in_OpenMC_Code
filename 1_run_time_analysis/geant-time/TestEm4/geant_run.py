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

#os.system("cd /home/cpf/geant/geant4.10.06-install/bin && source geant4.sh")
input("-> source activated?")
os.system("rm -r build")
print("-> build dir deleted")
os.system("mkdir build")
print("-> build dir generated")
os.system("cd build && cmake -DGeant4_DIR=/home/cpf/geant/geant4.10.06-install/lib/Geant4-10.6.3 " +
        "/home/cpf/Desktop/geant_compton_edge-02122021/TestEm4")
print("-> cmake command")
os.system("cd build && make -j8")
print("-> run make file")
os.system("cd build && ./TestEm4 TestEm4.in")
print("-> ran the executable")
os.system("python3 plot_txt.py")

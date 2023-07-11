"""
Jul 11, 2023
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License
"""

import numpy as np
import matplotlib.pyplot as plt 
import time
import os as os

import pandas as pd

times = []

for i in range(100):

    t0 = time.time()
    os.system("cd build && ./TestEm4 TestEm4.in")
    times += [time.time() - t0]                     
    print(times)
    print(len(times))
    print(sum(times)/len(times))

print(times)                                        
print(sum(times)/100)                               


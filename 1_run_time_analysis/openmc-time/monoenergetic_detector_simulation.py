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


t0 = time.time()
##################################### Materials ####################################################

alu = openmc.Material()
alu.add_element('Al', 1)
alu.temperature = 300        
alu.set_density('g/cm3', 2.7)

sodium_iodide = openmc.Material()
sodium_iodide.add_element('Na', 1)
sodium_iodide.add_element('I', 1)           
sodium_iodide.temperature = 300        
sodium_iodide.set_density('g/cm3', 3.667)    

oxide = openmc.Material()
oxide.add_nuclide('O16', 0.4) # same as MCNP atom or weight fraction
oxide.add_element('Al', 0.6)
oxide.temperature = 300        
oxide.set_density('g/cm3', 3.97)

iron = openmc.Material()
iron.add_element('Fe', 1)
iron.temperature = 300        
iron.set_density('g/cm3', 7.874)

air = openmc.Material()
air.add_element('N', 4)
air.add_nuclide('O16', 1)           
air.temperature = 300        
air.set_density('g/cm3', 0.000000000000000000001)    

mats = openmc.Materials([alu, sodium_iodide, oxide, iron, air])       
# cross sections ENDF/B-VII.1 from https://openmc.org/lanl-data-libraries/
# photons eprdata14 library 
mats.cross_sections = '/home/cpf/xsections/endfb71/endfb71_hdf5/cross_sections.xml'  
mats.export_to_xml()   

##################################### Geometry #####################################################
# & (intersection), | (union), and ~ (complement):

c1 = openmc.ZCylinder(r=2.54)
c2 = openmc.ZCylinder(r=2.70)
c3 = openmc.ZCylinder(r=2.84)

z1 = openmc.ZPlane(z0=0.00)
z2 = openmc.ZPlane(z0=0.10)
z3 = openmc.ZPlane(z0=5.18)
z4 = openmc.ZPlane(z0=7.18)

s = openmc.Sphere(r=10, boundary_type='vacuum')

crystal = openmc.Cell(name="crystal")
crystal.region = -c1 & -z3 & +z2
crystal.fill = sodium_iodide

oxide_layer = openmc.Cell(name="oxyde")
oxide_layer.region = +c1 & -c2 &-z3 & +z2
oxide_layer.fill = oxide

alu_casing = openmc.Cell()
alu_casing.region = +c2 & -c3 & -z4 & +z1
alu_casing.fill = alu

alu_window = openmc.Cell()
alu_window.region = -c2 & -z2 & +z1
alu_window.fill = alu

iron_back = openmc.Cell()
iron_back.region = -c2 & -z4 & +z3
iron_back.fill = iron

sourrounding = openmc.Cell()
sourrounding.region = -s & ~(-c3 & -z4 & +z1)
sourrounding.fill = air

cell_list = [crystal, oxide_layer, alu_casing, alu_window, iron_back, sourrounding]

universe = openmc.Universe(cells=cell_list)
geometry = openmc.Geometry(universe)             
geometry.export_to_xml()                     

if False:
    universe.plot(origin=(0, 0, 0), width=(15, 15),basis='xy')
    plt.show()
    universe.plot(origin=(0, 0, 0), width=(15, 15),basis='xz')
    plt.show()
    universe.plot(origin=(0, 0, 0), width=(15, 15),basis='yz')
    plt.show()

##################################### Settings #####################################################

source = openmc.Source()                                

# define the source as a disk
r = openmc.stats.Uniform(0, 0.01)
phi = openmc.stats.Uniform(0.0, 2*np.pi)
z = openmc.stats.Uniform(-1, -1)
source.space = openmc.stats.CylindricalIndependent(r, phi, z, origin=(0, 0, -1))

direction_array = np.array([0,0,1])
source.angle = openmc.stats.Monodirectional(direction_array) 
source.energy = openmc.stats.Discrete([0.66e6], [1.0]) # unit is ev
source.particle = 'photon'

settings = openmc.Settings()
settings.temperature = {'method': 'interpolation'}                    
settings.particles = 1000000
settings.batches = 1
settings.seed = 1
settings.photon_transport = True
settings.source = source
#settings.electron_treatment = 'led'
settings.run_mode = 'fixed source'

settings.export_to_xml()                           

############################### Tallies ############################################################

number_bins = 2049
bins_both = np.linspace(0, 0.66e6, number_bins)

tallies = openmc.Tallies()

cell_filter = openmc.CellFilter(crystal)
energy_filter = openmc.EnergyFilter(bins_both)

tally = openmc.Tally(name='test tally')
tally.filters = [cell_filter, energy_filter]
tally.scores = ['pulse-height']
tallies.append(tally)
tallies.export_to_xml()

################################################################################

openmc.run(openmc_exec='/home/cpf/openmc/build/bin/openmc', threads=1)

############################### Process Tallies ####################################################

print(time.time() - t0)

#sp = openmc.StatePoint('statepoint.1.h5')
#tally = sp.get_tally(name="test tally")
#data = tally.get_values(scores=['pulse-height']).flatten()
#print("New Tally Data")
#print(data)
#print("sum new tally: ", np.sum(data))
#print("len new tally: ", len(data))
#pht_output = pd.read_csv('pht_tally_output.txt', sep=",", header=None)
#cell_pht_output = np.asarray(pht_output[0])
#cell_pht_clean = cell_pht_output 
#cell_pht_clean = cell_pht_output[cell_pht_output != 0]

#values, b = np.histogram(cell_pht_clean, bins_both)

#values = values / np.sum(values) 
#print(values)
#print("sum txt: ", np.sum(values))
#print("len txt: ", len(values))

#plt.plot(data, label="new tally", ls="", marker="x")
#plt.plot(values, label="old txt", ls="", marker="x")
#plt.legend()
#plt.show()

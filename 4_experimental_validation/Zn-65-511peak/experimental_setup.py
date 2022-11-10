"""
Sep 24, 2020
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License

Simulating a Gamma source with a detector.
3" x 3" NaI detector, experimental setup.
"""

import numpy as np
import matplotlib.pyplot as plt
import openmc
import pandas as pd
import os as os

def run_experimental_spectrum(energy_list, intensity_list, seed=i):
    """ runs an experimental spectrum""" 
    
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
    air.set_density('g/cm3', 0.001225)    
    
    mats = openmc.Materials([alu, sodium_iodide, oxide, iron, air])       
    # cross sections ENDF/B-VII.1 from https://openmc.org/lanl-data-libraries/
    # photons eprdata14 library 
    mats.cross_sections = '/home/cpf/xsections/endfb71/endfb71_hdf5/cross_sections.xml'  
    mats.export_to_xml()   
    
    ##################################### Geometry #####################################################
    # & (intersection), | (union), and ~ (complement):
    
    c1 = openmc.ZCylinder(r=3.81)
    c2 = openmc.ZCylinder(r=3.86)
    c3 = openmc.ZCylinder(r=3.91)
    
    z1 = openmc.ZPlane(z0=0.00)
    z2 = openmc.ZPlane(z0=0.05)
    z3 = openmc.ZPlane(z0=0.10)
    z4 = openmc.ZPlane(z0=7.72)
    z5 = openmc.ZPlane(z0=7.77)
    z6 = openmc.ZPlane(z0=8.00)
    
    s = openmc.Sphere(r=25, boundary_type='vacuum')
    
    crystal = openmc.Cell(name="crystal")
    crystal.region = -c1 & -z4 & +z3
    crystal.fill = sodium_iodide
    
    oxide_layer_s = openmc.Cell()
    oxide_layer_s.region = +c1 & -c2 &-z4 & +z2
    oxide_layer_s.fill = oxide
    
    oxide_layer_t = openmc.Cell()
    oxide_layer_t.region = -c2 &-z3 & +z2
    oxide_layer_t.fill = oxide
    
    alu_casing_s = openmc.Cell()
    alu_casing_s.region = +c2 & -c3 & -z4 & +z2
    alu_casing_s.fill = alu
    
    alu_casing_t = openmc.Cell()
    alu_casing_t.region = -c3 & -z2 & +z1
    alu_casing_t.fill = alu
    
    iron_back = openmc.Cell()
    iron_back.region = -c3 & -z6 & +z4
    iron_back.fill = iron
    
    sourrounding = openmc.Cell()
    sourrounding.region = -s & ~(-c3 & -z6 & +z1)
    sourrounding.fill = air
    
    cell_list = [crystal, oxide_layer_s, oxide_layer_t, alu_casing_s, alu_casing_t, iron_back, sourrounding]
    
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
    # r = openmc.stats.Uniform(0, 2.54)
    # phi = openmc.stats.Uniform(0.0, 2*np.pi)
    # z = openmc.stats.Uniform(-10, -10)
    # source.space = openmc.stats.CylindricalIndependent(r, phi, z, origin=(0, 0, -10))
    
    #direction_array = np.array([0,0,1])
    #source.angle = openmc.stats.Monodirectional(direction_array) 
    
    source.space = openmc.stats.Point((-10.0, 0, 0))

    #direction_array = np.array([0,0,1])
    #source.angle = openmc.stats.Monodirectional(direction_array)

    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Discrete(energy_list, intensity_list) # unit is ev
    source.particle = 'photon'
    
    settings = openmc.Settings()
    settings.temperature = {'method': 'interpolation'}                     
    settings.particles = 10**10
    settings.batches = 1                                                  
    settings.seed = seed
    settings.photon_transport = True
    settings.source = source
    settings.run_mode = 'fixed source'
    
    settings.export_to_xml()                           
    
    number_bins = 131
    bins_both = np.linspace(0, 1.3e6, number_bins)

    tallies = openmc.Tallies()

    cell_filter = openmc.CellFilter(crystal)
    energy_filter = openmc.EnergyFilter(bins_both)

    tally = openmc.Tally(name='test tally')
    tally.filters = [cell_filter, energy_filter]
    tally.scores = ['pulse-height']
    tallies.append(tally)
    tallies.export_to_xml()

    openmc.run(openmc_exec='/home/cpf/openmc/build/bin/openmc')


nuc_names = ["Zn-65"]

for nuc in nuc_names:
    energy_array = np.load(nuc + "-energies.npy") * 10**3 # output of pyne is in keV
    intensity_array = np.load(nuc + "-intensities.npy")
    
    energy_list = list(energy_array)[:1] + [511000.0] + list(energy_array)[1:]
    
    intensity_array = (1-2*0.0142) * intensity_array / np.sum(intensity_array)              # 1.42., dass wir beta+ haben, aber dann entstehen zwei photonen, deshalb mal factor 2
    intensity_list = list(intensity_array)[:1] + [2*0.0142] + list(intensity_array)[1:] 
    
    # intensity_array = 0.5 * intensity_array / np.sum(intensity_array)
    # intensity_list = list(intensity_array)[:1] + [0.5] + list(intensity_array)[1:] 

    print(energy_list)
    print(intensity_list)

    run_experimental_spectrum(energy_list, intensity_list, seed = 1)

sp = openmc.StatePoint('statepoint.1.h5')
tally = sp.get_tally(name="test tally")
data = tally.get_values(scores=['pulse-height']).flatten()
# plt.plot(np.log(data[1:]), label="new tally", ls="", marker="x")
# plt.show()
    
np.save("zn_spectrum_sharp", data)

"""
Mär 12, 2022
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License

A structural search for the differences in the pht values
between OpenMC and MCNP.
"""

import numpy as np
import os as os
import openmc
import datetime as dt
import matplotlib.pyplot as plt


def run_openmc(seed):
    
    alu = openmc.Material()
    alu.add_nuclide('Al27', 1)      
    alu.set_density('g/cm3', 100.0)   

    materials = openmc.Materials([alu])
    materials.cross_sections = "/home/cpf/all_openmc_xsections/lanl_based/mcnp_endfb71/cross_sections.xml" 
    materials.export_to_xml()
    
    c1 = openmc.ZCylinder(r=np.log(2))                                                                  
    z1 = openmc.ZPlane(z0=0.0)                                                                    
    z2 = openmc.ZPlane(z0=np.log(2))                                                                    
    z3 = openmc.ZPlane(z0=2*np.log(2))                                                                    
    s = openmc.Sphere(r=12, boundary_type='vacuum')                                                
                                                                                                   
    cylinder1 = openmc.Cell()                                                          
    cylinder1.region = -c1 & +z1 & -z2                                                               
    cylinder1.fill = alu
 
    cylinder2 = openmc.Cell()                                                          
    cylinder2.region = -c1 & +z2 & -z3 
    cylinder2.fill = alu 
                                                                                                  
    surrounding = openmc.Cell()                                                                   
    surrounding.region = -s & ~(-c1 & -z3 & +z1)                                                  
                                                                                                   
    cell_list = [cylinder1, cylinder2, surrounding]             
                                                                                                   
    universe = openmc.Universe(cells=cell_list)                                                    
    geometry = openmc.Geometry(universe)                                                           
    geometry.export_to_xml()                                                                       

    settings = openmc.Settings()
    settings.seed = seed
    settings.particles = int(1e7)
    settings.batches = 1
    settings.photon_transport = True

    source = openmc.Source()
    source.particle = 'photon'
    source.space = openmc.stats.Point((0.0, 0.0, 0.0))
    source.energy = openmc.stats.Discrete(3.2e6, [1.0])
    source.angle = openmc.stats.Monodirectional([0,0,1])
    settings.source = source
    
    settings.run_mode = 'fixed source'
    settings.cutoff = {"energy_photon": 0.15e6}
    settings.export_to_xml()

    tallies = openmc.Tallies()
    cell_filter = openmc.CellFilter(cylinder2)

    # OpenMC - MCNP -> different handling of bin boarders -> shift openmc bins by epsilon
    energy_bins = 1e6 * 0.1 * np.arange(34)
    energy_filter = openmc.EnergyFilter(energy_bins)

    tally = openmc.Tally(name='pht tally')
    tally.filters = [cell_filter, energy_filter]
    tally.scores = ['pulse-height']
    tallies.append(tally)
    tallies.export_to_xml()
	
    openmc.run(openmc_exec='/home/cpf/Desktop/openmc/build/bin/openmc', threads=8)

    sp = openmc.StatePoint('statepoint.1.h5')
    tally = sp.get_tally(name="pht tally")
    openmc_values = tally.get_values(scores=['pulse-height']).flatten()
    np.save("results/analytic_pht_results_" + str(seed), openmc_values)
    print(openmc_values)


for seed in range(1,101):
    if "analytic_pht_results_" + str(seed) + ".npy" not in os.listdir("results"):
        run_openmc(seed) 

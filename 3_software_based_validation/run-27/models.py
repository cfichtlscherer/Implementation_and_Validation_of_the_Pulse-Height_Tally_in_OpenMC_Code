"""
Mär 12, 2022
Christopher Fichtlscherer (fichtlscherer@mailbox.org)
GNU General Public License

A structural search for the differences in the pht values
between OpenMC and MCNP.
"""

import numpy as np
import openmc
import datetime as dt
import matplotlib.pyplot as plt


def run_openmc(parameter_dic):

    alu = openmc.Material()         
    alu.add_nuclide('Al27', 1)      
    alu.temperature = 293           
    alu.set_density('g/cm3', 2.7)   

    sodium_iodide = openmc.Material()
    sodium_iodide.add_element('Na', 1)
    sodium_iodide.add_element('I', 1)
    sodium_iodide.temperature = 293
    sodium_iodide.set_density('g/cm3', parameter_dic["density"])
    
    oxide = openmc.Material()                                                                       
    oxide.add_nuclide('O16', 0.4) # same as MCNP atom or weight fraction                            
    oxide.add_element('Al', 0.6)                                                                    
    oxide.temperature = 293                                                                         
    oxide.set_density('g/cm3', 3.97)                                                                

    air = openmc.Material()                               
    air.add_nuclide('N14', 4)                               
    air.add_nuclide('O16', 1)                             
    air.temperature = 293                                
    air.set_density('g/cm3', 0.001225)    

    materials = openmc.Materials([alu, sodium_iodide, oxide, air])
    materials.cross_sections = parameter_dic["cross_sections_openmc"]

    materials.export_to_xml()
    
    c1 = openmc.ZCylinder(r=2.54)                                                                  
    c2 = openmc.ZCylinder(r=2.70)                                                                  
    c3 = openmc.ZCylinder(r=2.84)                                                                  
                                                                                                   
    z1 = openmc.ZPlane(z0=0.00)                                                                    
    z2 = openmc.ZPlane(z0=0.10)                                                                    
    z3 = openmc.ZPlane(z0=5.18)                                                                    
    z4 = openmc.ZPlane(z0=7.18)                                                                    
                                                                                                   
    s = openmc.Sphere(r=10, boundary_type='vacuum')                                                
                                                                                                   
    crystal = openmc.Cell(cell_id=1)                                                          
    crystal.region = -c1 & -z3 & +z2                                                               
    crystal.fill = sodium_iodide                                                                   
                                                                                                   
    oxide_layer = openmc.Cell(cell_id=2)                                                                    
    oxide_layer.region = +c1 & -c2 &-z3 & +z2                                                      
    oxide_layer.fill = oxide                                                                       
                                                                                                   
    alu_casing = openmc.Cell(cell_id=3)                                                                     
    alu_casing.region = +c2 & -c3 & -z4 & +z1                                                      
    alu_casing.fill = alu                                                                          
                                                                                                   
    alu_window = openmc.Cell(cell_id=4)                                                                     
    alu_window.region = -c2 & -z2 & +z1                                                            
    alu_window.fill = alu                                                                          
                                                                                                   
    alu_back = openmc.Cell(cell_id=5)                                                                       
    alu_back.region = -c2 & -z4 & +z3                                                              
    alu_back.fill = alu                                                                            
                                                                                                   
    sourrounding = openmc.Cell(cell_id=6)                                                                   
    sourrounding.region = -s & ~(-c3 & -z4 & +z1)                                                  
    sourrounding.fill = air                                                                        
                                                                                                   
    cell_list = [crystal, oxide_layer, alu_casing, alu_window, alu_back, sourrounding]             
                                                                                                   
    universe = openmc.Universe(cells=cell_list)                                                    
    geometry = openmc.Geometry(universe)                                                           
    geometry.export_to_xml()                                                                       

    settings = openmc.Settings()
    settings.particles = int(parameter_dic["number_particles"])
    settings.batches = 1
    settings.photon_transport = True

    source = openmc.Source()
    source.library = 'custom_source/build/libsource.so' 
    source.parameters = "radius=" + str(2.84) + ',energy=' + str(parameter_dic["energy"]) 
    settings.source = source

    settings.run_mode = 'fixed source'
    settings.export_to_xml()

    tallies = openmc.Tallies()
    cell_filter = openmc.CellFilter(crystal)

    # OpenMC - MCNP -> different handling of bin boarders -> shift openmc bins by epsilon
    energy_bins = parameter_dic["bins"][:2] + [i + 1e-6 for i in parameter_dic["bins"][2:]]
    energy_filter = openmc.EnergyFilter(energy_bins)

    tally = openmc.Tally(name='pht tally')
    tally.filters = [cell_filter, energy_filter]
    tally.scores = ['pulse-height']
    tallies.append(tally)
    tallies.export_to_xml()

    openmc.run(openmc_exec='/home/cpf/openmc/build/bin/openmc')

    sp = openmc.StatePoint('statepoint.1.h5')
    tally = sp.get_tally(name="pht tally")
    openmc_values = tally.get_values(scores=['pulse-height']).flatten()
    np.save("openmc_results", openmc_values)


def build_mcnp_input(parameter_dic):
    mcnp_input = open("mcnp_input", "a+")
    mcnp_input.write("MCNP INPUT FILE - " + str(dt.date.today()) + "\n")
    mcnp_input.write("C -----CELLS".ljust(60, "-") + "\n")
    mcnp_input.write("  1   2 -3.667000  -11  22 -23                IMP:P=1\n")
    mcnp_input.write("  2   3 -3.970000   11 -12  22 -23            IMP:P=1\n")
    mcnp_input.write("  3   1 -2.700000   12 -13  21 -24            IMP:P=1\n")
    mcnp_input.write("  5   1 -2.700000  -12      21 -22            IMP:P=1\n")
    mcnp_input.write("  6   1 -2.700000  -12      23 -24            IMP:P=1\n")
    mcnp_input.write("  7   5 -0.001225  #1 #2 #3 #5 #6 -99         IMP:P=1\n")
    mcnp_input.write("  9   0             99                        IMP:P=0\n")
    mcnp_input.write("C -----CELLS END + NEWLINE".ljust(60, "-") + "\n" + "\n")
    mcnp_input.write("C -----SURFACES".ljust(60, "-") + "\n")
    mcnp_input.write(" 99  SO  10.00\n")
    mcnp_input.write(" 11  CZ   2.54\n")
    mcnp_input.write(" 12  CZ   2.70\n")
    mcnp_input.write(" 13  CZ   2.84\n")
    mcnp_input.write(" 21  PZ   0.00\n")
    mcnp_input.write(" 22  PZ   0.10\n")
    mcnp_input.write(" 23  PZ   5.18\n")
    mcnp_input.write(" 24  PZ   7.18\n")
    mcnp_input.write("C -----SURFACES END + NEWLINE".ljust(60, "-") + "\n" + "\n")
    mcnp_input.write("C -----MATERIALS".ljust(60, "-") + "\n")
    mcnp_input.write("M1     13027.84p  1.00000 \n") 
    mcnp_input.write("M2     11023.84p  0.50000 \n") 
    mcnp_input.write("       53127.84p  0.50000 \n") 
    mcnp_input.write("M3     13027.84p  0.60000 \n") 
    mcnp_input.write("       8016.84p   0.40000 \n") 
    mcnp_input.write("M5     07014.84p  3.985348\n") 
    mcnp_input.write("       07015.84p  0.014652\n") 
    mcnp_input.write("       08016.84p  1.00000 \n") 
    mcnp_input.write("C -----SETTINGS".ljust(60, "-") + "\n")
    mcnp_input.write("MODE   P\n")
    mcnp_input.write("NPS    " + str(int(parameter_dic["number_particles"])) + "\n")
    mcnp_input.write("CUT:p  j 0.001\n")
    mcnp_input.write("SDEF   POS 0 0 -1 AXS 0 0 1 EXT 0 RAD d1 VEC 0 0 1 DIR 1 ERG " + str(parameter_dic["energy"]/1e6) + " PAR 2\n")
    mcnp_input.write("SI1    0 2.84 \n")
    mcnp_input.write("SP1    -21 1\n")
    mcnp_input.write("F8:P   1\n")
    mcnp_input.write("E8     ")
    for index, energy_value in enumerate(parameter_dic["bins"]):
        mcnp_input.write('{:.13f}'.format(energy_value/1e6) + "   ")
        if index % 4 == 0:
            mcnp_input.write("\n       ")
    mcnp_input.write("\n")
    mcnp_input.write("PRINT")
    mcnp_input.close()

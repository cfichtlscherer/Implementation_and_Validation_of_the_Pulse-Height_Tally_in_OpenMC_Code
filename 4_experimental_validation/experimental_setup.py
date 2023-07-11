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

from heath_experimental_spectra import *

def run_experimental_spectrum(nuc, energy_list, intensity_list, bins):
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
    mats.cross_sections = '/home/cpf/all_openmc_xsections/lanl_based/mcnp_endfb71/cross_sections.xml'
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

    ##################################### Settings #####################################################

    source = openmc.Source()
    source.space = openmc.stats.Point((-10.0, 0, 0))
    source.angle = openmc.stats.Isotropic()
    source.energy = openmc.stats.Discrete(energy_list, intensity_list) # unit is ev
    source.particle = 'photon'

    settings = openmc.Settings()
    settings.temperature = {'method': 'interpolation'}
    settings.particles = 10**9
    settings.batches = 1
    settings.seed = 1
    settings.photon_transport = True
    settings.source = source
    settings.run_mode = 'fixed source'
    settings.export_to_xml()

    tallies = openmc.Tallies()

    cell_filter = openmc.CellFilter(crystal)
    energy_filter = openmc.EnergyFilter(bins)

    tally = openmc.Tally(name='pht tally')
    tally.filters = [cell_filter, energy_filter]
    tally.scores = ['pulse-height']
    tallies.append(tally)
    tallies.export_to_xml()

    openmc.run(openmc_exec='/home/cpf/Desktop/openmc/build/bin/openmc')

    sp = openmc.StatePoint('statepoint.1.h5')
    tally = sp.get_tally(name="pht tally")
    openmc_values = tally.get_values(scores=['pulse-height']).flatten()
    np.save("simulation_results/" + nuc, openmc_values)



nuc_names = ["Al-28", "Mn-54", "Co-60", "Rb-86", "Y-88", "Cs-137", "Ba-140", "Au-198", "Zn-65"]

for nuc in nuc_names:
    if nuc + ".npy" not in os.listdir("simulation_results"):
        if nuc == "Zn-65":
            energy_array = np.load(nuc + "-energies.npy") * 10**3 # output of pyne is in keV
            intensity_array = np.load(nuc + "-intensities.npy")
            energy_list = list(energy_array)[:1] + [511000.0] + list(energy_array)[1:]

            # 1.42% for beta+ decay, factor 2 since there are two photons asociated for every beta+
            intensity_array = (1-2*0.0142) * intensity_array / np.sum(intensity_array)             
            intensity_list = list(intensity_array)[:1] + [2*0.0142] + list(intensity_array)[1:]

            energies, intensities = energy_list, intensity_list
        else:
            energies = np.load("isotope_emissions/energies/" + nuc + "-energies.npy") * 10**3 # output of pyne is in keV
            intensities = np.load("isotope_emissions/intensities/" + nuc + "-intensities.npy")
        
        bins = np.load("isotope_emissions/bins/pht_bins_" + nuc + ".npy")
        run_experimental_spectrum(nuc, energies, intensities, bins)


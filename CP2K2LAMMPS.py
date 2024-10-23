# This scipt will convert a .cif file into a CP2K input file
# JHarle - Michalchuk Group - University of Birmingham

import re
#import os # Use this for creating file names? Or add copies of the the CP2K .inp and .cif files to ADMIN directory
import numpy as np
#import matplotlib.pyplot as plt

# Open .cif file and read Coordinates and Cell Angles and Lengths
coordinates = []
with open("cif.cif","r") as cif_file:
    #Atom Coordinates:
    for coordinates in cif_file:
        if re.match(r"\b([A-Z][a-z]?)\s+[\d.-]+\s+([\d.]+)\s+([\d.]+)\s+([\d.]+", line):
        coordinates.append(line)
        
    #Angles and Side Lengths:
    A_length = re.search(r"_cell_length_a\s+(\d+\.?\d*)",r)
    B_length = re.search(r"_cell_length_b\s+(\d+\.?\d*)",r)
    C_length = re.search(r"_cell_length_c\s+(\d+\.?\d*)",r)
    alpha_angle = re.search(r"_cell_angle_alpha\s+(\d+\.?\d*)",r)
    beta_angle = re.search(r"_cell_angle_beta\s+(\d+\.?\d*)",r)
    gamma_angle = re.search(r"_cell_angle_gamma\s+(\d+\.?\d*)",r)

# Create new .inp file for CP2K: 

w = inp_file.write
basis_set = BASIS_SET DZVP-MOLOPT-SR-GTH

with open("new.inp","w") as inp_file:
    w("&GLOBAL")
    w(f" PROJECT {filename}")
    w(" RUN_TYPE MD") # Hard coded to be be MD, but maybe this will evolve into a script that can generate any type of CP2K .inp file?
    w(" PRINT_LEVEL")
    w("&END GLOBAL")
    w("\n")
    w("&Force_EVAL")
    w(" METHOD Quickstep")
    w("\n")
    w("     &DFT")
    w("         DFT_SET_FILE_NAME")
    w("         POTENTIAL_FILE_NAME")
    w("     &MGRID")
    w("         CUTOFF 1200") # Hard coded to 1200, feel free to change
    w("     &END MGRID")
    w("\n")
    w("     &XC")
    w("         &XC_FUNCTIONAL PBE")
    w("         &END XC_FUNCTIONAL")
    w("     &END XC")
    w("\n")
    w(" &END DFT")
    w("\n")
    w(" &SUBSYS")
    w("     &CELL")
    w(f"            {A_length}")
    w(f"            {B_length}")
    w(f"            {C_length}")
    w("     &END CELL")
    w("     &COORD")
    w(f"            {coordinates}")
    w("     &END COORD")
  
    #  BASIS SETS AND POTENTIALS FOR HYDROGEN, OXYGEN, CARBON AND NITROGEN. POTENTIALS ARE TAKEN FROM CP2K
  
    w("     &KIND H") 
    w(f"              {basis_set}")
    w("             POTENTIAL GTH-PBE-q1") 
    w("     &END KIND")
    w("\n")
    w("     &KIND O")
    w(f"             {basis_set}") 
    w("             POTENTIAL GTH-PBE-q6")
    w("     &END KIND")
    w("     &KIND C") 
    w(f"              {basis_set}")
    w("             POTENTIAL GTH-PBE-q4")
    w("     &END KIND")
    w("\n")
    w("     &KIND N")
    w(f"             {basis_set}")
    w("             POTENTIAL GTH-PBE-q5")
    w("     &END KIND")
    w("\n")
    w(" &END SUBSYS")
    w("&END FORCE_EVAL")
    w("\n")

    # MD PERAMETERS

    w("&MOTION")
    w(" &MD")
    w("     ENSEMBLE NVT")
    w("     STEPS 10000")
    w("     TIMESTEP 1.0")
    w("     TEMPERATURE 300")
    w("     &THERMOSTAT")
    w("         TYPE NOSE")
    w("         REGION GLOBAL")
    w("         TIMECON 1000")
    w("     &END THERMOSTAT")
    w(" &END MD")
    w("\n")
    w(" &PRINT")
    w("     &TRAJECTORY")
    w("         FORMAT XYZ")
    w(f"         FILENAME {filename}.traj")
    w("         STRIDE 5")
    w("     &END TRAJECTORY")
    w("\n")
    w("     &VELOCITIES")
    w(f"         FILENAME"+ {filename}+ ".out")
    w("         STRIDE 5")
    w("     &END VELOCITIES")
    w(" &END PRINT")
    w("&END MOTION")


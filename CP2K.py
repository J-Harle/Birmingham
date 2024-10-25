# This scipt will convert a .cell file into a CP2K input file
# JHarle - Michalchuk Group - University of Birmingham

import re
#import os # Use this for creating file names? Or add copies of the the CP2K .inp and .cell files to ADMIN directory
import numpy as np
#import matplotlib.pyplot as plt

# Open .cell file and read Coordinates and Cell Angles and Lengths
coordinates = []
indent = " " * 12 #This is just to get each set of coordinates and vector lengths to indent properly

with open("petn.cell","r") as cell_file:
    lines = cell_file.read().splitlines()
    # Atom Coordinates:
    coord_start = lines.index("%BLOCK POSITIONS_FRAC") + 1 
    coord_end = lines.index("%ENDBLOCK POSITIONS_FRAC")
    for index, line in enumerate(lines[coord_start:coord_end]):
        coords = list(map(str, line.split()))
        if index == 0: # Not smart enough to work out why the first line indents twice, this is just to avoid dealing with the problem
            fordinates = f"{coords[0]:<5} {float(coords[1]):.12f} {float(coords[2]):.12f} {float(coords[3]):.12f}"
        else:
            fordinates = f"{indent}{coords[0]:<5} {float(coords[1]):.12f} {float(coords[2]):.12f} {float(coords[3]):.12f}"
        coordinates.append(fordinates)
        line_coords = "\n".join(coordinates)


    # Side Lengths:
    start_side_search = lines.index("%BLOCK LATTICE_CART") + 2
    end_side_search = lines.index("%ENDBLOCK LATTICE_CART")
    side_lengths = []
    for index, line in enumerate(lines[start_side_search:end_side_search]):
        s = list(map(float, line.split()))
        if index == 0:
            fides = f"{float(s[0]):.5f} {float(s[1]):.5f} {float(s[2]):.5f}"
        else:
            fides = f"{indent}{float(s[0]):.5f} {float(s[1]):.5f} {float(s[2]):.5f}"
        side_lengths.append(fides)
        vector_matrix = "\n".join(side_lengths)

# Calculate vector angles from the matrix given in the .cell file - use np?


# Create new .inp file for CP2K: 

basis_set = "BASIS_SET DZVP-MOLOPT-SR-GTH"
filename = "placeholder" # Use OS to get dynamic naming 
with open("new.inp","w") as inp_file:
    w = inp_file.write
    w("&GLOBAL\n")
    w(f" PROJECT {filename}\n")
    w(" RUN_TYPE MD\n") # Hard coded to be be MD, but maybe this will evolve into a script that can generate any type of CP2K .inp file?
    w(" PRINT_LEVEL\n")
    w("&END GLOBAL\n")
    w("\n")
    w("&Force_EVAL\n")
    w(" METHOD Quickstep\n")
    w("\n")
    w("     &DFT\n")
    w("         DFT_SET_FILE_NAME\n")
    w("         POTENTIAL_FILE_NAME\n")
    w("     &MGRID\n")
    w("         CUTOFF 1200\n") # Hard coded to 1200, feel free to change
    w("     &END MGRID\n")
    w("\n")
    w("     &XC\n")
    w("         &XC_FUNCTIONAL PBE\n")
    w("         &END XC_FUNCTIONAL\n")
    w("     &END XC\n")
    w("\n")
    w(" &END DFT\n")
    w("\n")
    w(" &SUBSYS\n")
    w("     &CELL\n")
    w("         CARTESIAN\n")
    w(f"            {vector_matrix}\n")#Change this to whatever the matrix is called
    w("     &END CELL\n")
    w("     &COORD\n")
    w(f"            {line_coords}\n")
    w("     &END COORD\n")

    # BASIS SETS AND POTENTIALS FOR HYDROGEN, OXYGEN, CARBON AND NITROGEN. POTENTIALS ARE TAKEN FROM CP2K
    # There is definetely a way that I can automate this so that when the coordinates are read, the correct potentials are taken from Git

    w("     &KIND H\n")
    w(f"             {basis_set}\n")
    w("             POTENTIAL GTH-PBE-q1\n")
    w("     &END KIND\n")
    w("\n")
    w("     &KIND O\n")
    w(f"             {basis_set}\n")
    w("             POTENTIAL GTH-PBE-q6\n")
    w("     &END KIND\n")
    w("     &KIND C\n")
    w(f"             {basis_set}\n")
    w("             POTENTIAL GTH-PBE-q4\n")
    w("     &END KIND\n")
    w("\n")
    w("     &KIND N\n")
    w(f"             {basis_set}\n")
    w("             POTENTIAL GTH-PBE-q5\n")
    w("     &END KIND\n")
    w("\n")
    w(" &END SUBSYS\n")
    w("&END FORCE_EVAL\n")
    w("\n")

    # MD PERAMETERS - NOT FINISHED

    w("&MOTION\n")
    w(" &MD\n")
    w("     ENSEMBLE NVT\n")
    w("     STEPS 10000\n")
    w("     TIMESTEP 1.0\n")
    w("     TEMPERATURE 300\n")
    w("     &THERMOSTAT\n")
    w("         TYPE NOSE\n")
    w("         REGION GLOBAL\n")
    w("         TIMECON 1000\n")
    w("     &END THERMOSTAT\n")
    w(" &END MD\n")
    w("\n")
    w(" &PRINT\n")
    w("     &TRAJECTORY\n")
    w("         FORMAT XYZ\n")
    w(f"         FILENAME {filename}.traj\n")
    w("         STRIDE 5\n")
    w("     &END TRAJECTORY\n")
    w("\n")
    w("     &VELOCITIES\n")
    w(f"         FILENAME {filename}.out\n")
    w("         STRIDE 5\n")
    w("     &END VELOCITIES\n")
    w(" &END PRINT\n")
    w("&END MOTION\n")



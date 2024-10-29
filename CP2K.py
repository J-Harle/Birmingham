# This script will convert a .cell file into a CP2K .inp file
# JHarle - Michalchuk Group - University of Birmingham

import re
import numpy as np

# Open .cell file and read Coordinates and Cell Angles and Lengths
coordinates = []
indent = " " * 12  # Indentation for coordinates

with open("petn.cell", "r") as cell_file:
    lines = cell_file.read().splitlines()
    
    # Atom Coordinates:
    coord_start = lines.index("%BLOCK POSITIONS_FRAC") + 1 
    coord_end = lines.index("%ENDBLOCK POSITIONS_FRAC")
    for index, line in enumerate(lines[coord_start:coord_end]):
        coords = list(map(str, line.split()))
        if index == 0: 
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

# Create new .inp file for CP2K:
basis_set = "BASIS_SET DZVP-MOLOPT-SR-GTH"
filename = "petn"
with open(f"{filename}_CP2K.inp", "w") as inp_file:
    w = inp_file.write
    w("&GLOBAL\n")
    w(f" PROJECT {filename}_MD\n")
    w(" RUN_TYPE MD\n")  # Hard coded to be MD
    w(" PRINT_LEVEL MEDIUM\n")
    w("&END GLOBAL\n\n")
    
    w("&FORCE_EVAL\n")
    w(" METHOD Quickstep\n\n")
    
    w("     &DFT\n")
    w("         DFT_SET_FILE_NAME G06\n")
    w("         POTENTIAL_FILE_NAME POTENTIAL_GTH\n")
    w("     &MGRID\n")
    w("         CUTOFF 89 \n")  # Hard coded to 89 ~1200 eV
    w("         REL_CUTOFF 40\n")
    w("     &END MGRID\n\n")
    
    w("     &XC\n")
    w("         &XC_FUNCTIONAL PBE\n")
    w("             &PBE\n")
    w("             &END PBE\n")
    w("         &END XC_FUNCTIONAL\n")
    w("         &VDW_POTENTIAL\n")
    
    w("             POTENTIAL_TYPE_POTENTIAL\n")
    w("             &PAIR_POTENTIAL\n")
    w("                 TYPE DFTD2\n")
    w("                 PARAMETER_FILE_NAME dftd2.dat\n")
    w("                 REFERENCE_FUNCTIONAL PBE\n")
    w("             &END PAIR_POTENTIAL\n")
    w("         &END VDW_POTENTIAL\n")
    w("     &END XC\n\n")

    w("&SUBSYS\n")
    w("     &CELL\n")
    w("         CARTESIAN\n")
    w(f" 		{vector_matrix}\n")
    w("     &END CELL\n")
    w("     &COORD\n")
    w(f"            {line_coords}n")
    w("     &END COORD\n")
    w("     &KIND H\n")
    w("             BASIS_SET DZVP-MOLOPT-SR-GTH\n")
    w("             POTENTIAL GTH-PBE-q1\n")
    w("     &END KIND\n")
    w(" &END SUBSYS\n")
    w("&END FORCE_EVAL\n\n")
    
    w("&MOTION\n")
    w(" &MD\n")
    w("     ENSEMBLE NVT\n")
    w("     STEPS 10000\n")
    w("     TIMESTEP 0.5\n")
    w("     TEMPERATURE 300.0\n")
    w("     TEMPERATURE_TOLERANCE 0.5\n")
    w("     PRESSURE 1.0\n\n")
    w("     &THERMOSTAT\n")
    w("         TYPE NOSE\n")
    w("         REGION GLOBAL\n")
    w("         &NOSE\n")
    w("             TIMECON 1000\n")
    w("             LENGTH 3\n")
    w("             YOSHIDA 3\n")
    w("         &END NOSE\n")
    w("     &END THERMOSTAT\n\n")
    w("     &BAROSTAT\n")
    w("         TYPE ISOTROPIC\n")
    w("         TIMECON 2000.0\n")
    w("     &END BAROSTAT\n")
    w(" &END MD\n\n")
    
    w(" &PRINT\n")
    w("     &TRAJECTORY\n")
    w("         FORMAT XYZ\n")
    w("         FILENAME petn_traj.xyz\n")
    w("         STRIDE 5\n")
    w("     &END TRAJECTORY\n\n")
    w("     &VELOCITIES\n")
    w("         FILENAME petn_vel.xyz\n")
    w("         STRIDE 5\n")
    w("     &END VELOCITIES\n\n")
    w("     &ENERGY\n")
    w("         FILENAME petn_energy.xyz\n")
    w("         STRIDE 5\n")
    w("     &END ENERGY\n\n")
    w("     &FORCES\n")
    w("         FILENAME petn_forces.xyz\n")
    w("         STRIDE 5\n")
    w("     &END FORCES\n\n")
    w("     &RESTART\n")
    w("         BACKUP_COPIES 3\n")
    w("     &END RESTART\n")
    w(" &END PRINT\n")
    w("&END MOTION\n\n")
    
    w("&EXT_RESTART\n")
    w(f"  RESTART_FILE_NAME {filename}_MD.restart\n")
    w("  RESTART_DEFAULT F\n")
    w("  RESTART_POS T\n")
    w("&END EXT_RESTART\n")

#This script submits all .cell files in a folder to the queue
import os
import subprocess
import time

# Reads current directory and finds all .cell files
cell_files = [f for f in os.listdir('.') if f.endswith('.cell')]

for cell_file in cell_files:
    jobname = cell_file[:-5]
    print(f"Processing file: {cell_file}")

    for i in range(2,81):
        value = f"{i:03d}"

    # Simulating a .bash file for each submission
    batch_script = f"""#!/bin/bash
#SBATCH --time=2:00:00
#SBATCH --mail-user=
#SBATCH --ntasks=25
#SBATCH --nodes=1-10
#SBATCH --qos=bbdefault
#SBATCH --account=
#SBATCH --job-name={jobname}
#SBATCH --mem=50gb

set -e
 
module purge; module load bluebear
module load bear-apps/2023a
module load CASTEP/24.1-foss-2023a
 
mpirun -np $SLURM_NTASKS castep.mpi {value}petn

 
exit
"""

    # Submit the job to SLURM
    process = subprocess.Popen(['sbatch'], stdin=subprocess.PIPE)
    process.communicate(input=batch_script.encode())

    print(f"Submitted job for {cell_file}")
    time.sleep(0.2)

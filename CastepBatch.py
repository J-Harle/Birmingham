#This script should be located within a main directory, and submits all .cell files located in any sub-directories
import os
import subprocess
import time

# Process each directory and find all .cell files
for root, dirs, files in os.walk('.'):
    cell_files = [f for f in files if f.endswith('.cell')]

    # Process each cell file found
    for cell_file in cell_files:
        jobname = cell_file[:-5]  # Remove the .cell extension
        print(f"Processing file: {cell_file} in directory: {root}")

        # Loop over values from 002 to 080
        for i in range(2, 81):
            value = f"{i:03d}"

            # Simulating a .bash file for each submission
            batch_script = f"""#!/bin/bash
#SBATCH --time=10:00
#SBATCH --mail-user=jxh1695@student.bham.ac.uk
#SBATCH --ntasks=64
#SBATCH --nodes=1
#SBATCH --qos=bbshort
#SBATCH --account=michaaal-jharl
#SBATCH --job-name={jobname}
#SBATCH --mem=50gb

set -e
 
module purge; module load bluebear
module load bear-apps/2023a
module load CASTEP/24.1-foss-2023a
 
mpirun -np $SLURM_NTASKS castep.mpi {value}petn

exit
"""

            # Create the full path to the .bash file
            batch_file_path = os.path.join(root, f"{jobname}_{value}.sh")

            # Write the batch script to the .bash file
            with open(batch_file_path, 'w') as batch_file:
                batch_file.write(batch_script)

            # Submit the job to SLURM
            process = subprocess.Popen(['sbatch', batch_file_path], stdin=subprocess.PIPE)
            process.communicate()

            print(f"Submitted job for {cell_file} with value {value}")
            time.sleep(0.2)  # Optional sleep to avoid overwhelming the scheduler

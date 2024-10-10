import re
import os

# Number of subdirectories and files to process
num_dirs = 19  # For directories 002 to 020

# Store the current working directory
original_directory = os.getcwd()

# Open a text file to write the results
with open("FinalEnergies.txt", "w") as output_file:
    try:
        for counter in range(2, 21):  # Loop through directories and files from 002 to 020
            subdirectory = f"{counter:03d}"  # Format the subdirectory name (e.g., 002, 003, ..., 020)
            filename = f"{subdirectory}petn.castep"  # Each file is named like 002petn.castep, 003petn.castep, etc.
            SCF_values = []

            # Check if the subdirectory exists
            if not os.path.isdir(subdirectory):
                output_file.write(f"Subdirectory {subdirectory} does not exist.\n")
                continue

            # Construct the full path to the file
            file_path = os.path.join(subdirectory, filename)

            if not os.path.isfile(file_path):
                output_file.write(f"{filename} does not exist in subdirectory {subdirectory}.\n")
                continue

            try:
                # Open and search for "Final energy" values in the file
                with open(file_path, 'r') as file:
                    for line in file:
                        # Look for lines containing "Final energy = " followed by the energy value and "eV"
                        match = re.search(r"Final energy\s*=\s*([\d\.\-Ee]+)\s*eV", line)
                        if match:
                            SCF_values.append(match.group(1))  # Capture the numeric energy value

                # Write results to the output file
                if SCF_values:
                    output_file.write(f"Final energy values in {filename} (in subdirectory {subdirectory}):\n")
                    for value in SCF_values:
                        output_file.write(f"{value} eV\n")
                else:
                    output_file.write(f"No 'Final energy' values found in {filename} (in subdirectory {subdirectory}).\n")

            except Exception as e:
                output_file.write(f"An error occurred while processing {filename} in {subdirectory}: {e}\n")

    except Exception as e:
        output_file.write(f"An error occurred while processing the subdirectories: {e}\n")

    finally:
        # Change back to the original directory
        os.chdir(original_directory)


import re
import os

# Number of files to process
num_files = 19  # Since files range from 002 to 020, this gives us 19 files

# Path to the subdirectory where the log files are located
subdirectory = "subdirectory_name"  # Replace with the actual subdirectory name

# Store the current working directory
original_directory = os.getcwd()

# Open a text file to write the results
with open("FinalEnergies.txt", "w") as output_file:
    try:
        # Change to the subdirectory
        os.chdir(subdirectory)
        
        for counter in range(2, 21):  # Files numbered from 002 to 020
            filename = f"{counter:03d}petn.castep"  # Format counter as three digits (e.g., 002, 003, ..., 020)
            SCF_values = []

            if not os.path.isfile(filename):
                output_file.write(f"{filename} does not exist in {subdirectory}.\n")
                continue

            try:
                with open(filename, 'r') as file:
                    for line in file:
                        # Look for lines containing "Final energy" followed by a value
                        match = re.search(r"Final energy\s+([\d\.\-Ee]+)", line)
                        if match:
                            SCF_values.append(match.group(1))

                if SCF_values:
                    output_file.write(f"Final energy values in {filename}:\n")
                    for value in SCF_values:
                        output_file.write(f"{value}\n")
                else:
                    output_file.write(f"No 'Final energy' values found in {filename}\n")
            
            except Exception as e:
                output_file.write(f"An error occurred while processing {filename}: {e}\n")

    except Exception as e:
        output_file.write(f"An error occurred while navigating to the subdirectory: {e}\n")
    
    finally:
        # Change back to the original directory
        os.chdir(original_directory)

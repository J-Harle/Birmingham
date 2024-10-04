import numpy as np

with open("petn.cell", "r") as text:
    body = text.readlines()

# Loop to create files with updated kpoint values
for i in np.arange(0.02, 0.81, 0.01):
    i = np.round(i, 2)  # Round the value of `i` to 2 decimal places to avoid floating-point issues

    # Create a new list for the modified content
    updated_body = []

    # Filter out the existing 'kpoint_mp_spacing' line
    for line in body:
        if "kpoint_mp_spacing" not in line:
            updated_body.append(line)

    # Append the new 'kpoint_mp_spacing' value
    updated_body.append(f"\nkpoint_mp_spacing : {i:.2f}\n")

    # Write to a new output file
    OutputFile = f"{int(i * 100):03d}petn.cell"
    with open(OutputFile, "w") as outputfile:
        outputfile.writelines(updated_body)


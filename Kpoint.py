import numpy as np

with open("petn.cell", "r") as template_file:
    body = template_file.readlines()

for i in np.arange(0.02, 0.80, 0.01):
    OutputFile = f"{i:.2f}petn.cell
    with open(OutputFile, "w") as outputfile:
        outputfile.writelines(body)
        outputfile.write(f"kpoint_mp_spacing : {i:.2f}\n") 

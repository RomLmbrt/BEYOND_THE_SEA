import aerosandbox as asb
import aerosandbox.numpy as np
import os
from pprint import pprint

file_name = "R1 V5 Satori 3 copy.dat"

airfoil = asb.Airfoil(coordinates = (os.path.join(os.getcwd(), file_name)))

# airfoil = asb.Airfoil("dae51")  # Geometry will be automatically pulled from UIUC database (local).

analysis = asb.XFoil(
    airfoil=airfoil,
    Re=1.3e6,
    xfoil_command="xfoil",
    # If XFOIL is not on your PATH, then set xfoil_command to the filepath to your XFOIL executable.
)

sweep_analysis = analysis.alpha(
    alpha=np.linspace(0, 15, 16)
)
print("\nSweep analysis:")
pprint(sweep_analysis)

analysis = analysis.alpha(
    alpha=5.01
)
print("\nanalysis:")
pprint(analysis)

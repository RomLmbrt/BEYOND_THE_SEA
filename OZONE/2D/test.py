###
# %% Import
###

import os
from datetime import datetime
from time import time

import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import aerosandbox.tools.pretty_plots as p

import casadi as ca
import aerosandbox as asb
import aerosandbox.numpy as np
from aerosandbox.tools.pretty_plots import plt, show_plot, set_ticks  # sets some nice defaults

from Change_airfoil import(
     make_ellipse_leading_edge,
     move_apex2,
     move_apex_lower_surface,
     upper_edge_separation
)

from Get_airfoil_data import get_apex_x_over_c

########################################################################################################################
################################################## Data extractions ####################################################
########################################################################################################################

# %% Import airfoil from .dat file
# file_name = "R1 V5 Satori 3.dat"
file_name = "R1 V5 Satori 3.dat"

airfoil = asb.Airfoil(coordinates = (os.path.join(os.getcwd(), "Airfoils", file_name)))
kulfan_airfoil = airfoil.to_kulfan_airfoil()

print(f'data extracted from : {file_name}\n')
print("________\n")

CL_multipoint_targets = np.array([ 
    asb.XFoil(airfoil=airfoil, Re=1.3e6, xfoil_command="xfoil").alpha(0.0)['CL'][0],
    asb.XFoil(airfoil=airfoil, Re=1.3e6, xfoil_command="xfoil").alpha(2.5)['CL'][0],
    asb.XFoil(airfoil=airfoil, Re=1.3e6, xfoil_command="xfoil").alpha(5.01)['CL'][0],
    asb.XFoil(airfoil=airfoil, Re=1.3e6, xfoil_command="xfoil").alpha(7.5)['CL'][0],
    asb.XFoil(airfoil=airfoil, Re=1.3e6, xfoil_command="xfoil").alpha(10)['CL'][0],
    asb.XFoil(airfoil=airfoil, Re=1.3e6, xfoil_command="xfoil").alpha(12.5)['CL'][0],
    asb.XFoil(airfoil=airfoil, Re=1.3e6, xfoil_command="xfoil").alpha(15)['CL'][0]
])
print(CL_multipoint_targets)
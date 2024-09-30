import aerosandbox.numpy as np
import aerosandbox as asb
import aerosandbox.numpy as np

def get_apex_x_over_c(kulfan_airfoil: asb.KulfanAirfoil) -> float:
    c = kulfan_airfoil.coordinates[0][0]
    i = 0
    while kulfan_airfoil.coordinates[i][1] <= kulfan_airfoil.coordinates[i+1][1]:
        i+=1
    x = kulfan_airfoil.coordinates[i][0]   
    return x/c
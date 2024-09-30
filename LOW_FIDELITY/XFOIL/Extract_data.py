import aerosandbox.numpy as np

def data_extraction(file_name: str,) -> list:

    with open(file_name, 'r') as file:
        content = file.readlines()

        coordinates = []

        for line in content:
            try:
                coordinates.append([float(line.strip().split("   ")[0]), float(line.strip().split("   ")[1])])
            except ValueError:
                print()  # Ignore lines that are useless (exple : the airfoil name)

    return(coordinates)
    
#################################################

def surface_separation(coordinates: list) -> list:

    N=len(coordinates)

    upper_surface = [[1.0, 0.0]]
    lower_surface = []

    for i in range(N):
        if coordinates[i][1] > 0:
            upper_surface.append(coordinates[i])
        elif coordinates[i][1] < 0 :
            lower_surface.append(coordinates[i])
    
    lower_surface.append([1.0, 0.0])
    upper_surface.append([0.0, 0.0])
    
    return([upper_surface, lower_surface])

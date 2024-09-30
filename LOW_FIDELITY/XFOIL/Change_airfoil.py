import aerosandbox.numpy as np
import aerosandbox as asb
import aerosandbox.numpy as np
import os

def upper_edge_separation(coordinates: np.ndarray) -> list[np.ndarray]:
    
    N = coordinates.shape[0]

    i = 0
    while coordinates[i][1] <= coordinates[i+1][1] : # trailing edge part
        if i ==N-2 :
            print("edge separation reached the end of the surface without finding an apex")
            exit()
        if coordinates[i][1] < 0 :
            print("edge separation works only for upper surface")
            exit()
        i+=1

    trailing_edge = coordinates[:i]
    leading_edge = coordinates[i:]
    
    return([leading_edge, trailing_edge])
                
####################################################################

def lower_edge_separation(coordinates: np.ndarray) -> list[np.ndarray]:
    
    N = coordinates.shape[0]

    i = 0
    while coordinates[i][1] >= coordinates[i+1][1] : # trailing edge part
        if i ==N-2 :
            print("edge separation reached the end of the surface without finding an apex")
            exit()
        if coordinates[i][1] > 0 :
            print("lower_edge_separation works only for lower surface")
            exit()
        i+=1

    leading_edge = coordinates[:i]
    trailing_edge = coordinates[i:]
    
    return([leading_edge, trailing_edge])

####################################################################

def make_ellipse_leading_edge(airfoil: asb.Airfoil) -> asb.Airfoil:
    # %% Extract airfoil data
    upper_surface = airfoil.upper_coordinates()
    lower_surface = airfoil.lower_coordinates()

    upper_leading_edge, upper_trailing_edge = upper_edge_separation(upper_surface)

    # %% Make the upper leading edge elliptic
    a = upper_leading_edge[0][0]
    b = upper_leading_edge[0][1]
    x0 = upper_leading_edge[0][0]
    y0 = 0

    N = upper_leading_edge.shape[0]
    new_upper_leading_edge =np.zeros((N, 2))

    for i in range(N):
        new_upper_leading_edge[i] = [ upper_leading_edge[i][0], b*np.sqrt(1-((upper_leading_edge[i][0] - x0)/a)**2) + y0]
    
    # %% Create the new Airfoil
    new_upper_surface = np.concatenate((upper_trailing_edge, new_upper_leading_edge), axis=0)
    new_coords = np.concatenate((new_upper_surface, lower_surface), axis=0)

    x_coords, y_coords = zip(*new_coords) # to get the right format for creating an Airfoil
    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)

    new_airfoil = asb.Airfoil(
        name=f'Elliptic law',
        coordinates=np.column_stack((x_coords, y_coords))
    )

    return(new_airfoil)

####################################################################

def move_apex_lower_surface(airfoil: asb.Airfoil, change: float) -> asb.Airfoil:

    # %% Extract airfoil data
    upper_surface = airfoil.upper_coordinates()
    lower_surface = airfoil.lower_coordinates()

    lower_leading_edge, lower_trailing_edge = lower_edge_separation(lower_surface)

    # # %% Check that abs(change) < 1
    # if abs(change) > 1 :
    #     print(" change must be inferior to 1 and superior to -1 ")
    #     exit()

    Nl = lower_leading_edge.shape[0]
    Nt = lower_trailing_edge.shape[0]
    chord = upper_surface[0][0] 
    
    new_lower_leading_edge = np.zeros((Nl-1, 2)) # To Avoid adding (0,0) twice when merging upper/lower surfaces
    new_lower_trailing_edge = np.zeros((Nt, 2))

    # %% Move the apex
    for i in range(Nl-1): 
        new_lower_leading_edge[i] = [lower_leading_edge[i+1][0]*(1+change*chord), lower_leading_edge[i+1][1]]

    coef = (chord - new_lower_leading_edge[Nl-2][0])/(chord-lower_leading_edge[Nl-1][0])
    for i in range(Nt):
        new_lower_trailing_edge[i] = [chord - (chord - lower_trailing_edge[i][0]) * coef, lower_trailing_edge[i][1]]

    # %% Create the new Airfoil
    new_lower_surface = np.concatenate((new_lower_leading_edge, new_lower_trailing_edge), axis=0)
    new_coords = np.concatenate((upper_surface, new_lower_surface), axis=0)

    x_coords, y_coords = zip(*new_coords) # to get the right format for creating an Airfoil
    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)

    new_airfoil = asb.Airfoil(
        name=f'Apex lower surface moved of : {change}',
        coordinates=np.column_stack((x_coords, y_coords))
    )

    return(new_airfoil)

####################################################################

def move_apex(airfoil: asb.Airfoil, change: float) -> asb.Airfoil:

    # %% Extract airfoil data
    upper_leading_edge, upper_trailing_edge = upper_edge_separation(airfoil.upper_coordinates())

    Nl = upper_leading_edge.shape[0]
    Nt = upper_trailing_edge.shape[0]

    chord = airfoil.coordinates[0][0] 
    new_airfoil = airfoil.deepcopy()

    # %% Move the apex
    coef = (chord - airfoil.coordinates[Nt][0]*(1+change*chord))/(chord-airfoil.coordinates[Nt][0])
    for i in range(Nt):
        new_airfoil.coordinates[i][0] = chord - (chord - airfoil.coordinates[i][0]) * coef

    for i in range(Nt, Nt+Nl-1): 
        new_airfoil.coordinates[i][0] = airfoil.coordinates[i][0]*(1+change*chord)

    new_airfoil.name = f'Apex moved of : {change}'

    return(new_airfoil)

####################################################################

def move_apex2(airfoil: asb.Airfoil, change: float) -> asb.Airfoil:

    # %% Extract airfoil data
    upper_leading_edge, upper_trailing_edge = upper_edge_separation(airfoil.upper_coordinates())

    Nl = upper_leading_edge.shape[0]
    Nt = upper_trailing_edge.shape[0]

    chord = airfoil.coordinates[0][0] 

    # %% Move the apex
    coef = (chord - airfoil.coordinates[Nt][0]*(1+change*chord))/(chord-airfoil.coordinates[Nt][0])
    for i in range(Nt):
        airfoil.coordinates[i][0] = chord - (chord - airfoil.coordinates[i][0]) * coef
        print(f'coef : {type(coef)}')
        print(f'bordel : {type(chord - (chord - airfoil.coordinates[i][0]) * coef)}')
        print(f'airfoil : {type(airfoil.coordinates[i][0])}')
    for i in range(Nt, Nt+Nl-1): 
        airfoil.coordinates[i][0] = airfoil.coordinates[i][0]*(1+change*chord)

    airfoil.name = f'Apex moved of : {change}'

    return(airfoil)
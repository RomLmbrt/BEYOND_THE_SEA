import numpy as np
from Kite3d import Kite
from view import plot_data

def rotate_points(points):
    # Rotation matrix for pi/2 around Y-axis
    Ry = np.array([
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0]
    ])

    # Rotation matrix for pi/2 around Z-axis
    Rz = np.array([
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ])

    # Combined rotation matrix
    R = np.dot(Rz, Ry)

    # Rotate points
    rotated_points = [np.dot(R, point) for point in points]

    return rotated_points

def main():
    # Initialize Kite instance
    kite = Kite()
    
    # Read the data from the file
    filename = 'test_cases/default_kite/default_kite_3d.txt'
    #filename = 'test_cases/Seakite50_VH/SK50-VH_3d.txt'
    kite.read_from_txt(filename)
    kite.ribs[0].read_dat_file('test_cases/default_kite/profiles/prof_1.dat')
    
    # Plot the data
    plot_data(kite.ribs, kite.le_tube, kite.struts, kite.bridle)

if __name__ == "__main__":
    main()

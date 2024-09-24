import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Function to parse the file and extract LE tube and struts data
def parse_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    ref_point = []
    rib_data = []
    le_tube_data = []
    struts_data = []
    strut = []
    bridle_data = []

    rib_section_found = False    
    le_tube_section_found = False
    struts_section_found = False
    bridle_section_found = False
    
    for line in lines:
        line = line.strip()

        if line == "3d rib positions":
            rib_section_found = True
            continue
        if line == "LE tube":
            le_tube_section_found = True
            continue
        if line.startswith("Strut"):
            struts_section_found = True
            continue
        elif line == "3d Bridle":
            bridle_section_found = True
            continue
        
        if rib_section_found:
            if not line:
                rib_section_found = False
                continue  # End of rib section
            if line.isdigit() or not any(char.isdigit() for char in line):
                continue  # Skip the line with the number of entries
            else :
                values = line.split(';')
                pointsLE = [float(value.replace(',', '.')) for value in values[:3]]  # Only take X, Y, Z
                pointsTE = [float(value.replace(',', '.')) for value in values[3:6]]  # Only take X, Y, Z
                pointsVUP = [float(value.replace(',', '.')) for value in values[6:9]]  # Only take X, Y, Z
                rib_data.append(np.array([pointsLE, pointsTE, pointsVUP], dtype=float))
                #rib_data.append(np.array([pointsLE], dtype=float))
                if line.startswith('0,000000;'): #extract the reference point
                    ref_point = pointsLE

        if le_tube_section_found:
            if not line:
                le_tube_section_found = False
                continue  # End of LE tube section
            if line.isdigit() or not any(char.isdigit() for char in line):
                continue  # Skip the line with the number of entries
            else :
                values = line.split(';')
                points = [float(value.replace(',', '.')) for value in values[:3]]  # Only take X, Y, Z
                le_tube_data.append(points)
        
        if struts_section_found:
            if not line:
                if strut :  
                    struts_data.append(np.array(strut, dtype=float))
                    strut = [] # Clear strut list for the next set of struts
                struts_section_found = False
                continue  # End of struts section
            if line.isdigit() or not any(char.isdigit() for char in line):
                continue  # Skip the line with the number of entries
            else:
                values = line.split(';')
                points = [float(value.replace(',', '.')) for value in values[:3]]  # Only take X, Y, Z
                strut.append(points)
        
        if bridle_section_found:
            if not line:
                bridle_section_found = False
                continue  # End of bridle section
            if line.isdigit() or not any(char.isdigit() for char in line):
                continue  # Skip the line with the number of entries
            else :
                values = line.split(';')
                pointsTop = [float(value.replace(',', '.')) for value in values[:3]]  # Only take X, Y, Z
                pointsBottom = [float(value.replace(',', '.')) for value in values[3:6]]  # Only take X, Y, Z
                bridle_data.append([pointsTop, pointsBottom])

    if strut:
        struts_data.append(np.array(strut, dtype=float))

    return ref_point, rib_data, np.array(le_tube_data, dtype=float), struts_data, bridle_data


#Function to parse the avl file and extract the positions of sections 
def parse_avl_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    avl_section_data = []
    section_found = False

    for line in lines:
        line = line.strip()
        #if line.startswith('#') or line == '' or not any(char.isdigit() for char in line):
        #    continue  # Skip comments, empty lines, and lines without numbers

        if line.startswith('SECTION'):
            section_found = True
            continue

        if section_found :
            # Split the line at the pipe symbol to isolate the coordinate data
            data_part = line.split('|')[0].strip()
            values = data_part.split()

            if len(values) >= 3:
                try:
                    # Parse the first three values as floats and append as a point
                    x, y, z = float(values[0]), float(values[1]), float(values[2])
                    avl_section_data.append(np.array((x, y, z), dtype=float))
                except ValueError:
                    # If conversion to float fails, skip this line
                    continue
            section_found=False
    
    return avl_section_data

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

# Function to plot the LE tube and struts data
def plot_data(rib_data, le_tube_data, struts_data, bridle_data, avl_section_data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if len(rib_data) == 0 and le_tube_data.size == 0 and len(struts_data) == 0 and len(bridle_data) == 0:
        print("No data to plot.")
        return

    first_rib = True
    for rib in rib_data:
        label = 'ribs' if first_rib else ''
        ax.scatter(rib[:, 0], rib[:, 1], rib[:, 2], c='c', label=label, marker='.')
        first_rib = False

    if le_tube_data.size != 0:
        ax.scatter(le_tube_data[:, 0], le_tube_data[:, 1], le_tube_data[:, 2], c='g', label='LE tube', marker='^')

    first_strut = True
    for strut in struts_data:
        label = 'Struts' if first_strut else ''
        ax.scatter(strut[:, 0], strut[:, 1], strut[:, 2], c='b', label=label, marker='o')
        first_strut = False
    
    first_bridle = True
    for bridle in bridle_data:
        label = '3d bridle' if first_bridle else ''
        bridle = np.array(bridle)
        ax.plot([bridle[0][0], bridle[1][0]], [bridle[0][1], bridle[1][1]], [bridle[0][2], bridle[1][2]], c='r', label=label)
        first_bridle = False
    
    first_section = True
    for section in avl_section_data:
        label = 'avl section' if first_section else ''
        ax.scatter(section[0], section[1], section[2], c='m', label=label, marker='o')
        first_section = False
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_aspect('equal', adjustable='box')
    ax.legend()
    plt.show()

# Main script
filename = 'test_cases/default_kite/default_kite_3d.txt'
filename = 'test_cases/Seakite50_VH/SK50-VH_3d.txt'
ref_point, rib_data, le_tube_data, struts_data, bridle_data = parse_data(filename)
filename_avl = 'test_cases/default_kite/profiles/default_kite_3d.avl'
avl_section_data = parse_avl_file(filename_avl)
rotated_avl_section_data = rotate_points(avl_section_data)

print(ref_point)
translated_avl_data = [section + ref_point for section in rotated_avl_section_data] # translate points
#plot_data(rib_data, le_tube_data, struts_data, bridle_data, rotated_avl_section_data)
plot_data(rib_data, le_tube_data, struts_data, bridle_data, translated_avl_data)

for i in range(len(rotated_avl_section_data)):
    print(np.linalg.norm(translated_avl_data[i] - rib_data[8+i][0]))


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_data(rib_data, le_tube_data, struts_data, bridle_data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if len(rib_data) == 0 and le_tube_data.size == 0 and len(struts_data) == 0 and len(bridle_data) == 0:
        print("No data to plot.")
        return

    first_rib = True
    for rib in rib_data:
        label = 'ribs' if first_rib else ''
        ax.scatter(rib.LE[0], rib.LE[1], rib.LE[2], c='c', label=label, marker='.')
        ax.scatter(rib.TE[0], rib.TE[1], rib.TE[2], c='c', marker='.')
        ax.scatter(rib.VUP[0], rib.VUP[1], rib.VUP[2], c='c', marker='.')
        first_rib = False

    first_le_section = True
    for le_section in le_tube_data:
        label = 'LE Tube' if first_le_section else ''
        ax.scatter(le_section.centre[0], le_section.centre[1], le_section.centre[2], c='g', label=label, marker='^')
        first_le_section = False

    first_strut = True
    for strut in struts_data:
        for section in strut.sections:
            label = 'Struts' if first_strut else ''
            ax.scatter(section.centre[0], section.centre[1], section.centre[2], c='b', label=label, marker='o')
            first_strut = False
    
    first_bridle = True
    for bridle in bridle_data:
        label = '3d bridle' if first_bridle else ''
        ax.plot([bridle.top[0], bridle.bottom[0]], [bridle.top[1], bridle.bottom[1]], [bridle.top[2], bridle.bottom[2]], c='r', label=label)
        first_bridle = False

    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_aspect('equal', adjustable='box')
    ax.legend()
    plt.show()
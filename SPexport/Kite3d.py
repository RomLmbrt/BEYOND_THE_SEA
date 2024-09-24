import numpy as np

class Rib:
    def __init__(self):
        self.LE = []    #LE 3d coordinate
        self.TE = []    #TE 3d coordinate
        self.VUP = []   #
        self.profile3d = []
    
    def __init__(self, LE, TE, VUP):
        self.LE = LE
        self.TE = TE
        self.VUP = VUP
        self.profile3d = []
    
    #read the .dat file of the 2d profile and switch it into 3d in the kite reference
    def read_dat_file(self, dat_filename):
        points2d = []

        #read .dat file
        with open(dat_filename, 'r') as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith('prof'): #name of the profile
                print('skip line')
                continue
            else  :
                values = line.split()
                if len(values) == 2:
                    try:
                        x, y = float(values[0]), float(values[1])
                        xy = np.array([x, y, 0], dtype=float)
                        print(xy)
                        points2d.append(xy)
                    except ValueError:
                        print(f"Skipping invalid line: {line}")
        
        #Project 2d profile into the 3d reference of the kite
        # Compute the first basis vector (x-axis in the plane)
        x_basis = self.TE - self.LE
        x_basis = x_basis / np.linalg.norm(x_basis)
        print('x norm =', np.linalg.norm(x_basis))
        # Compute the second basis vector (y-axis in the plane)
        y_basis = self.VUP / np.linalg.norm(self.VUP)
        print('y norm =', np.linalg.norm(y_basis))
        # Calculate the normal vector of the plane containing the profile by taking the cross product of LE_to_TE and VUP
        normal_vector = np.cross(x_basis , y_basis )
        # Ensure normal vector is a unit vector
        print(np.linalg.norm(normal_vector))
        # Create the transformation matrix
        transformation_matrix = np.vstack([x_basis, y_basis, normal_vector]).T
        # Project 2d profile points in 3d frame
        points3d = [self.LE + np.dot(transformation_matrix, point2d) for point2d in points2d]             
        self.profile3d = points3d
                        

    
    def print(self):
        print(f"Leading Edge (LE): {self.LE}")
        print(f"Trailing Edge (TE): {self.TE}")
        print(f"Up vector (VUP): {self.VUP}")

class LETubeSection:
    def __init__(self, centre, diam):
        self.centre = centre
        self.diam = diam

    def print(self):
        print(f"Centre: {self.centre}")
        print(f"Diameter: {self.diam}")

class StrutSection:
    def __init__(self, centre, diam):
        self.centre = centre
        self.diam = diam

    def print(self):
        print(f"Centre: {self.centre}")
        print(f"Diameter: {self.diam}")

class Strut:
    def __init__(self):
        self.sections = []

    #def __init__(self, strut_sections):
    #    self.sections = strut_sections

    def add_section(self, section):
        self.sections.append(section)
    
    def print(self):
        for section in self.sections:
            section.print()

class Bridle:
    def __init__(self, top, bottom, name, length, material):
        self.top = top
        self.bottom = bottom
        self.name = name
        self.length = length
        self.material = material

    def print(self):
        print(f"Top: {self.top}")
        print(f"Bottom: {self.bottom}")
        print(f"Name: {self.name}")
        print(f"Length: {self.length}")
        print(f"Material: {self.material}")

class Kite:
    def __init__(self):
        self.ribs = []
        self.le_tube = []
        self.struts = []
        self.bridle = []

    def read_from_txt(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        section = None
        current_strut = Strut()

        for line in lines:
            line = line.strip()
            if line.startswith('3d rib positions'):
                section = 'ribs'
                continue
            elif line.startswith('LE tube'):
                section = 'le_tube'
                continue
            elif line.startswith('Strut'):
                section = 'strut'
                continue
            elif line.startswith('3d Bridle'):
                section = 'bridle'
                continue
            #Read kite ribs
            if section == 'ribs':
                if not line or line.isdigit() or not any(char.isdigit() for char in line):
                    continue  # Skip empty or comments lines
                values = list(map(float, line.replace(',', '.').split(';')))
                if len(values) == 9:
                    le = np.array(values[0:3])
                    te = np.array(values[3:6])
                    vup = np.array(values[6:9])
                    self.ribs.append(Rib(le, te, vup))
            #Read Kite LE tube
            elif section == 'le_tube':
                if not line or line.isdigit() or not any(char.isdigit() for char in line):
                    continue  # Skip empty or comments lines
                values = list(map(float, line.replace(',', '.').split(';')))
                if len(values) == 4:
                    centre = np.array(values[0:3])
                    diam = values[3]
                    self.le_tube.append(LETubeSection(centre, diam))
            #Read Struts
            elif section == 'strut':
                if not line: #end of the strut section
                    self.struts.append(current_strut) #add the strut to the struts list of the kite
                    current_strut = Strut()
                    continue
                if line.isdigit() or not any(char.isdigit() for char in line):
                    continue  # Skip comments lines
                values = list(map(float, line.replace(',', '.').split(';')))
                if len(values) == 4:
                    centre = np.array(values[0:3])
                    diam = values[3]
                    strut_section = StrutSection(centre, diam)
                    current_strut.add_section(strut_section)

            #Read Bridle
            elif section == 'bridle':
                if not line or line.isdigit() or not any(char.isdigit() for char in line):
                    continue  # Skip empty or comments lines
                parts = line.replace(',', '.').split(';')
                top = np.array(list(map(float, parts[0:3])))
                bottom = np.array(list(map(float, parts[3:6])))
                name = parts[6]
                length = float(parts[7].replace(',', '.'))
                material = parts[8] if len(parts) > 8 else ""
                self.bridle.append(Bridle(top, bottom, name, length, material))




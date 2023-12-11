import os
from pathlib import Path
import numpy as np

class FileInput:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.printed_matrix = np.zeros((300, 200), dtype=bool)
        self.start_x = 0
        self.start_y = 0

    def process_file(self):
        new_file_path = self.file_path.with_name(f"{self.file_path.stem}_nougat.gcode")
        current_tool = 'T0'

        with self.file_path.open('r') as original_file, new_file_path.open('w') as new_file:
            for line in original_file:
                

                if line.startswith(';LAYER:'):
                    if line == ';LAYER:0\n' or line == ';LAYER:1\n' or line == ';LAYER:2\n':
                        continue
                    else : self.handle_layer_change(line, new_file, current_tool) 
                    current_tool = 'T1' if current_tool == 'T0' else 'T0'
                elif line.startswith('G1'):
                    ziel_x_y = self.extract_coordinates(line)
                    if ziel_x_y != (self.start_x, self.start_y):
                        f = self.calculate_fucntion(ziel_x_y)
                        self.mark_printed(f, ziel_x_y)
                elif line.startswith('G0'):
                    self.start_x, self.start_y = self.extract_coordinates(line)
                new_file.write(line)
            

        print(f"Datei verarbeitet und gespeichert als: {new_file_path}")
        print(f"Bedruckte Matrix: \n{self.printed_matrix}")
        # Speichern des Arrays mit booleschen Werten in einer Datei
        # Speichern des Arrays in einer Datei
        with open('array_output.txt', 'w') as f:
            np.savetxt(f, self.printed_matrix, fmt='%d')



    def handle_layer_change(self, line, new_file, current_tool):
        commands = [
            "G1 E-6 F300\n",  # Fügen Sie einen Zeilenumbruch am Ende hinzu
            'G0 f100 X-14\t;park left extruder\n' if current_tool == 'T0' else 'G0 f500 X342\t;park right extruder\n',  
            f'{self.get_next_tool(current_tool)}\n',  
        ]

        new_file.writelines(commands)
    @staticmethod
    def get_next_tool(current_tool):
        return 'T1' if current_tool == 'T0' else 'T0'

    def extract_coordinates(self, line):
        coords = line.split(' ')
        x = self.start_x  # Standardwert, falls X nicht in der Zeile ist
        y = self.start_y  # Standardwert, falls Y nicht in der Zeile ist

        for coord in coords:
            if coord.startswith('X'):
                x = float(coord[1:])
            elif coord.startswith('Y'):
                y = float(coord[1:])
            elif coord.startswith('Z'):
                break
            elif coord.startswith(';'):
                break

        return (x, y)
    
    def calculate_fucntion(self, ziel_x_y):
        x, y = ziel_x_y
        x = int(round(x))
        y = int(round(y))
        
        x_diff = x - self.start_x
        y_diff = y - self.start_y

        if x_diff == 0:
            return lambda y: self.start_x
        elif y_diff == 0:
            return lambda x: self.start_y
        else:
            m = y_diff / x_diff
            b = y - m * x
            f = lambda x: m * x + b
            return f
    
    
        
    def mark_printed(self, f, ziel_x_y):
        x, y = ziel_x_y
        x = int(round(x))
        y = int(round(y))

        if x < 0 or x >= 300 or y < 0 or y >= 200:
            return

        x_range = range(int(round(self.start_x)), x + 1) if x >= self.start_x else range(x, int(round(self.start_x)) + 1)
        y_range = range(int(round(self.start_y)), y + 1) if y >= self.start_y else range(y, int(round(self.start_y)) + 1)

        if self.start_x == x:
            for y_koordinate in y_range:
                self.printed_matrix[x][y_koordinate] = True
        elif self.start_y == y:
            for x_koordinate in x_range:
                self.printed_matrix[x_koordinate][y] = True
        else:
            for x_koordinate in x_range:
                y_koordinate = int(round(f(x_koordinate)))
                if 0 <= y_koordinate < 200:
                    self.printed_matrix[x_koordinate][y_koordinate] = True

        self.start_x = x
        self.start_y = y


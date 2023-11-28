import os

class FileInput:
    def __init__(self, file_path):
        self.file_path = file_path

    def process_file(self):
        dir_name, file_name = os.path.split(self.file_path)
        name, _ = os.path.splitext(file_name)
        new_file_name = f"{name}_veraendert.gcode"
        new_file_path = os.path.join(dir_name, new_file_name)

        with open(self.file_path, 'r') as original_file, open(new_file_path, 'w') as new_file:
            current_tool = 'T0'  # Start mit dem ersten Werkzeug

            for line in original_file:
                new_file.write(line)

                # Überprüfen, ob es sich um eine Layer-Wechselzeile handelt
                if line.startswith(';LAYER:'):

                    if line.startswith(';LAYER:0'):
                        # Startpunkt
                        new_file.write("M104 S205 T0\n")
                        new_file.write("M104 S205 T1\n")
                        continue

                    # Werkzeug wechseln
                    next_tool = 'T1' if current_tool == 'T0' else 'T0'

                    # Parkbefehl für das aktuelle Werkzeug
                    if current_tool == 'T0':
                        park_command = 'G0 f500 X-14\t;park left extruder\n'
                    else:
                        park_command = 'G0 f500 X342\t;park right extruder\n'
                    new_file.write(park_command)
                    # G1 F600 E-6 ;retract filament
                    new_file.write('G1 F600 E-6\n')

                    # Neues Werkzeug aktivieren
                    tool_change_command = f'{next_tool}\n'
                    new_file.write(tool_change_command)
                    
                    new_extruder_command = f'M900 {next_tool} K0.054\n'
                    new_filament_command = f'G1 F600 E5.5\n'
                    new_fan_command = f'M106 S255\n'
                    new_file.write(new_extruder_command)
                    new_file.write(new_filament_command)
                    new_file.write(new_fan_command)

                    # Update current_tool
                    current_tool = next_tool

        print(f"Datei verarbeitet und gespeichert als: {new_file_path}")

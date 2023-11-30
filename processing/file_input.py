import os
from pathlib import Path

class FileInput:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def process_file(self):
        new_file_path = self.file_path.with_name(f"{self.file_path.stem}_nougat.gcode")
        current_tool = 'T0'

        with self.file_path.open('r') as original_file, new_file_path.open('w') as new_file:
            for line in original_file:
                new_file.write(line)
                if line.startswith(';LAYER:'):
                    if line == ';LAYER:0\n':  # Verwenden Sie '==' anstelle von '.equals()'
                        continue
                    if line == ';LAYER:1\n':
                        continue
                    if line == ';LAYER:2\n':
                        continue
                    self.handle_layer_change(line, new_file, current_tool)
                    current_tool = 'T1' if current_tool == 'T0' else 'T0'

        print(f"Datei verarbeitet und gespeichert als: {new_file_path}")

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

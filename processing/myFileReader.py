import os
from pathlib import Path
import numpy as np
import processOptions
from processing.reRoutingTravel import reRoutingTravel
from processing.findOuterPoints import findOuterPoints
from processOptions import ProcessOptions


class myFileReader:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.printed_matrix = np.zeros((300, 300), dtype=bool)
        self.current_tool = 'T0'
        self.layerACounter = 0
        self.layerBCounter = 0
        self.currentFilament = 0
        self.gradientlevel = 0
        self.start_x = 0
        self.start_y = 0
        self.currentExtrusionT0 = 0
        self.currentExtrusionT1 = 0
        self.boolGradientCollectCircumference = False
        self.boolGradientLayerToSkip = False
        self.gradientOuterLinedict = {}

    def process_file(self, options: processOptions):
        schichtwechsel = options.schichtwechsel
        modell_Option = options.modell_Option
        verhältnis_A = options.verhältnis_A
        verhältnis_B = options.verhältnis_B
        numberRepitions = options.numberRepitions
        travelOutside = options.travelOutside
        gradienten = options.gradienten
        gradientGrundflächeLayer = options.gradientGrundflächeLayer
        gradientStartHöhe = options.gradientStartHöhe
        gradientenLineStartHöhe = options.gradientenLineStartHöhe
        gradientenLineEndHöhe = options.gradientenLineEndHöhe
        gradientenFlowRate = options.gradientenFlowRate
        gradientenFlowRateFactor = options.gradientenFlowRateFactor
        gradientenLayers = options.gradientenLayers
        gradientenTemperatur = options.gradientenTemperatur
        minTravelDistance = options.minTravelDistance
        gradientenSpeed = options.gradientenSpeed
        new_file_path = self.file_path.with_name(f"{self.file_path.stem}_nougat.gcode")

        with self.file_path.open('r') as original_file, new_file_path.open('w') as new_file:
            
            for line in original_file:
                if line.startswith(';LAYER:'):
                    print(line)
                    if schichtwechsel:
                        self.handle_layer_change(line, new_file, verhältnis_A, verhältnis_B, numberRepitions, modell_Option)
                        #set Hotende temperature
                        
                    if gradienten and int(line[7:]) >= gradientGrundflächeLayer:
                        self.boolGradientCollectCircumference = True
                if line.startswith('G1'):
                    self.mark_printed(line)
                    if self.boolGradientCollectCircumference:
                        self.createGradientCircumference(line)
                if line.startswith('G0'):
                    if (travelOutside == True):
                        if self.needNewTravel(line, minTravelDistance):
                            print("ReRouting" + line)
                            # Finden von Start und Ziel für den A* Algorithmus auserhalb des gedruckten Bereichs
                            ziel_x_y = self.extract_coordinates(line)
                            startCoordinates = findOuterPoints.findPointOnLimit(self.start_x, self.start_y, self.printed_matrix)
                            endCoordinates = findOuterPoints.findPointOnLimit(ziel_x_y[0], ziel_x_y[1], self.printed_matrix)
                            start_x_out = startCoordinates[0]
                            start_y_out = startCoordinates[1]
                            ziel_x_out = endCoordinates[0]
                            ziel_y_out = endCoordinates[1]
                            reRouting = reRoutingTravel((start_x_out, start_y_out), (ziel_x_out, ziel_y_out), self.printed_matrix)
                            # reRouting = reRoutingTravel((round(self.start_x), round(self.start_y)), (round(ziel_x_y[0]), round(ziel_x_y[1])), self.printed_matrix)  
                            newCommands = reRouting.findPathWithA()  # Aufrufen des A* Algorithmus für die Reiseroute

                            new_file.write(f'G0 X{start_x_out} Y{start_y_out} F1800\n')
                            # Erster und letzter command soll ausgelassen werden
                            updated_commands = [f'G0 X{command[0]} Y{command[1]} F1800\n' for command in newCommands[1:-1]]
                            new_file.writelines(updated_commands)
                            
                            new_file.write(f'G0 X{ziel_x_out} Y{ziel_y_out} F1800\n')    
                if line.startswith(";TYPE:WALL-INNER"):
                    if self.boolGradientCollectCircumference:
                        self.boolGradientCollectCircumference = False
                        self.boolGradientLayerToSkip = True
                        self.createGradient(new_file, gradientStartHöhe, gradientenLineStartHöhe, gradientenLineEndHöhe, gradientenFlowRate, gradientenFlowRateFactor, gradientenLayers, gradientenTemperatur, gradientenSpeed)
                        # reset dict
                        self.gradientOuterLinedict = {}
                if self.line_contains_coordinates(line):
                    self.updateStartCoordinates(line)   
                if self.boolGradientLayerToSkip or self.boolGradientCollectCircumference:
                    continue  
                new_file.write(line)
        print(f"Saved new file to {new_file_path.name}.")

    def line_contains_coordinates(self, line):
        if line.startswith('G0') or line.startswith('G1'):
            if 'X' in line and 'Y' in line:
                return True
        return False

    def updateStartCoordinates(self, line):
        ziel_x_y = self.extract_coordinates(line)
        self.start_x = ziel_x_y[0]
        self.start_y = ziel_x_y[1]

    def handle_layer_change(self, line, new_file, verhältnis_A, verhältnis_B, numberRepitions, modell_Option):

        commands = []
        # Modell Option B
        if modell_Option == "Vollschichten Modell":
            if self.currentFilament == 0:
                if self.layerACounter < verhältnis_A:
                    self.layerACounter += 1
                else:
                    self.currentFilament = 1
                    self.layerACounter = 1
                    commands = [f'G0 X{self.start_x + 50} Y{self.start_y + 50}\n' ,f'{self.get_next_tool()}\n', f'M104 S220 T0\n', f'M104 S205 T1\n']
                    self.current_tool = 'T1' if self.current_tool == 'T0' else 'T0'
                    
                    
            else:
                if self.layerBCounter < verhältnis_B:
                    self.layerBCounter += 1
                else:
                    self.currentFilament = 0
                    self.layerBCounter = 1
                    commands = [f'G0 X{self.start_x + 50} Y{self.start_y + 50}\n' ,f'{self.get_next_tool()}\n', f'M104 S220 T0\n', f'M104 S205 T1\n']
                    self.current_tool = 'T1' if self.current_tool == 'T0' else 'T0'

        # Modell Option A
        #else: 
        #    commands = [
        #    'G0 f100 X-14\t;park left extruder\n' if self.current_tool == 'T0' else 'G0 f500 X342\t;park right extruder\n',  
        #    f'{self.get_next_tool()}\n',  
        #]
            
        new_file.writelines(commands)
        
    def get_next_tool(self):
        print("Im in get_next_tool and the current tool is: " + self.current_tool)
        return 'T1' if self.current_tool == 'T0' else 'T0'

    def extract_coordinates(self, line):
        line = line.replace('\t', ' ')
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
             
    def mark_printed(self, line):
        ziel_x_y = self.extract_coordinates(line)
        if ziel_x_y != (self.start_x, self.start_y):
            line_function = self.calculate_fucntion(ziel_x_y)
        else:
            return
        
        x, y = ziel_x_y
        x = int(round(x))
        y = int(round(y))

        if x < 0 or x >= 300 or y < 0 or y >= 300:
            return

        x_range = range(int(round(self.start_x)), x + 1) if x >= self.start_x else range(x, int(round(self.start_x)) + 1)
        y_range = range(int(round(self.start_y)), y + 1) if y >= self.start_y else range(y, int(round(self.start_y)) + 1)

        if round(self.start_x) == x:
            for y_koordinate in y_range:
                self.printed_matrix[x][y_koordinate] = True
        elif (self.start_y) == y:
            for x_koordinate in x_range:
                self.printed_matrix[x_koordinate][y] = True
        else:
            for x_koordinate in x_range:
                y_koordinate = int(round(line_function(x_koordinate)))
                if 0 <= y_koordinate < 200:
                    self.printed_matrix[x_koordinate][y_koordinate] = True
        # write to file
        #¶np.savetxt('printed_matrix.txt', self.printed_matrix, fmt='%d')

    def needNewTravel(self, line, minTravelDistance):
        ziel_x_y = self.extract_coordinates(line)
        x, y = ziel_x_y
        #euklidische distanz von start zu ziel
        distance = ((x - self.start_x) ** 2 + (y - self.start_y) ** 2) ** 0.5
        #wenn distanz kleiner als 10 ist, muss nicht neu gereist werden
        if x < 0 or x >= 300:
            return False
        elif distance > minTravelDistance:
            return True
        else:
            return False
        
    def createGradientCircumference(self, line):
        if self.line_contains_coordinates(line) is False:
            return
        if self.gradientlevel not in self.gradientOuterLinedict:
            self.gradientOuterLinedict[self.gradientlevel] = []

        new_object = {
            "start_x": self.start_x,
            "start_y": self.start_y,
            "ziel_x": self.extract_coordinates(line)[0],
            "ziel_y": self.extract_coordinates(line)[1],
            "distance": ((self.extract_coordinates(line)[0] - self.start_x) ** 2 + (self.extract_coordinates(line)[1] - self.start_y) ** 2) ** 0.5,
            "line_function": self.calculate_fucntion(self.extract_coordinates(line)),
        }
        self.gradientOuterLinedict[self.gradientlevel].append(new_object)
        print(new_object)
    
    def createGradient(self, new_file, gradientStartHöhe, gradientenLineStartHöhe, gradientenLineEndHöhe, gradientenFlowRate, gradientenFlowRateFactor, gradientenLayers, gradientenTemperatur, gradientenSpeed):
        # Finde die linkere untere Ecke im dict für key = 0
        lowest_x, lowest_y = self.findLowestXYPoint(self.gradientOuterLinedict[0])

        #Finde die Linie die in der linkeren unteren Ecke startet
        startLine = self.findStartLine(self.gradientOuterLinedict[0], lowest_x, lowest_y)
        #Finde die Linie die in der linkeren unteren Ecke endet
        endLine = self.findEndLine(self.gradientOuterLinedict[0], lowest_x, lowest_y)

        # Die Travelline ist die längere der beiden Linien und die andere ist die offsetline
        zSteps = (gradientenLineEndHöhe - gradientenLineStartHöhe) / 0.01
        travelLine = startLine if startLine["distance"] > endLine["distance"] else endLine
        offsetLine = startLine if startLine["distance"] < endLine["distance"] else endLine
        travelVector = (travelLine["ziel_x"] - travelLine["start_x"], travelLine["ziel_y"] - travelLine["start_y"])
        travelVectorZStep = (travelVector[0] / zSteps, travelVector[1] / zSteps, 0.01)
        travelVectorLengthXY = (travelVector[0] ** 2 + travelVector[1] ** 2) ** 0.5
        travelVectornormiert = (travelVector[0] / travelVectorLengthXY, travelVector[1] / travelVectorLengthXY)
        offsetVector = (abs(offsetLine["ziel_x"] - offsetLine["start_x"]), abs(offsetLine["ziel_y"] - offsetLine["start_y"]))
        offsetVectorLength = (offsetVector[0] ** 2 + offsetVector[1] ** 2) ** 0.5
        offsetVectornormiert = (offsetVector[0] / offsetVectorLength, offsetVector[1] / offsetVectorLength)
        # todo offset muss immer 0.4 sein von der letzen linie
        offsetVectorStep = (offsetVectornormiert[0] * 0.4, offsetVectornormiert[1] * 0.4)

        for j in range (1, gradientenLayers + 1):

            neededLines = offsetVectorLength / 0.4
            new_file.write(f'G0 X{travelLine["start_x"]} Y{travelLine["start_y"]} \n')
            new_file.write(f'G92 E0 \n')
            new_file.write(f'M104 S{gradientenTemperatur} \n')
            self.currentExtrusionT0 = 0
            layerStartHeight = gradientStartHöhe + gradientenLineStartHöhe * j
            new_file.write(f'G0 Z{layerStartHeight} \n')
            new_file.write(";Gradienten" "\n")

            for i in range(int(neededLines) + 1):
                line_x_start, line_y_start, line_z_start = lowest_x + (i * offsetVectorStep[0]), lowest_y + (i * offsetVectorStep[1]), layerStartHeight
                new_file.write(f'G0 X{line_x_start} Y{line_y_start} Z{line_z_start} \n')
                self.createGradientLineZsteps(new_file, (line_x_start, line_y_start, line_z_start), zSteps, travelVectorZStep, gradientenLineStartHöhe, gradientenFlowRate, gradientenFlowRateFactor, j, gradientenSpeed)
                #self.createGradientLine(new_file, (line_x_start, line_y_start, line_z_start), travelVectornormiert, travelVectorLengthXY , gradientenLineStartHöhe, gradientenLineEndHöhe)   
                #endpartLength = travelVectorLengthXY - (int(travelVectorLengthXY - 1) )
                #endpartExtrusion = self.currentExtrusionT0 + self.filamentVolumeToMM(0.4 * endpartLength * gradientenLineEndHöhe)
                #new_file.write(f'G1 X{line_x_start + travelVector[0] } Y{line_y_start + travelVector[1]} Z{gradientStartHöhe + gradientenLineEndHöhe} E{endpartExtrusion} \n') 
                #self.currentExtrusionT0 = endpartExtrusion

    def findStartLine(self, gradientOuterLinedict, lowest_x, lowest_y):
        for line in gradientOuterLinedict:
            if line["start_x"] == lowest_x and line["start_y"] == lowest_y:
                return line
    
    def findEndLine(self, gradientOuterLinedict, lowest_x, lowest_y):
        for line in gradientOuterLinedict:
            if line["ziel_x"] == lowest_x and line["ziel_y"] == lowest_y:
                return line
            
    def findLowestXYPoint(self, gradientOuterLinedict):
        lowest_x = 300
        lowest_y = 200
        for line in gradientOuterLinedict:
            if line["start_x"] < lowest_x and line["start_y"] < lowest_y:
                lowest_x = line["start_x"]
                lowest_y = line["start_y"]
        return lowest_x, lowest_y

    def createGradientLine(self, new_file, start, travelVectornormiert, travelVectorLengthXY, gradientenLineStartHöhe, gradientenLineEndHöhe):
        travelVectorStepmmXYZ = (travelVectornormiert[0], travelVectornormiert[1], (gradientenLineEndHöhe - gradientenLineStartHöhe) / travelVectorLengthXY)
        for i in range(int(travelVectorLengthXY)) :
            newExtrusion = self.currentExtrusionT0 + self.filamentVolumeToMM((0.4 * (i * travelVectorStepmmXYZ[2])))
            ziel = (start[0] + (i * travelVectorStepmmXYZ[0]), start[1] + (i * travelVectorStepmmXYZ[1]), start[2] + (i * travelVectorStepmmXYZ[2]))

            new_file.write(f'G1 X{round(ziel[0],3)} Y{round(ziel[1],3)} Z{round(ziel[2],3)} E{newExtrusion} \n')
            self.currentExtrusionT0 = newExtrusion
    
    def filamentVolumeToMM(self, volume, gradientenFlowRate):
        diameter = 1.75
        flowrate = gradientenFlowRate
        radius = diameter / 2
        return volume / (radius * radius * 3.14159) * flowrate
    
    def createGradientLineZsteps(self, new_file, start, zSteps, travelVectorZStep, gradientenLineStartHöhe, gradientenFlowRate, gradientenFlowRateFactor, currentgradienenLayer = 1, gradientenSpeed = 1500):
        for i in range(1, int(zSteps) + 1):
            distance = (travelVectorZStep[0] ** 2 + travelVectorZStep[1] ** 2) ** 0.5
            layerHeight = (i) * 0.01 + gradientenLineStartHöhe
            extrusionWidth = 0.4
            
            newExtrusion = self.currentExtrusionT0 + self.filamentVolumeToMM(extrusionWidth * distance * layerHeight, gradientenFlowRate * (gradientenFlowRateFactor ** i))
            ziel = (start[0] + (i * travelVectorZStep[0]), start[1] + (i * travelVectorZStep[1]), start[2] + (i * travelVectorZStep[2] * currentgradienenLayer))
            new_file.write(f'G1 F{gradientenSpeed} X{round(ziel[0],3)} Y{round(ziel[1],3)} Z{round(ziel[2],3)} E{newExtrusion} \n')
            self.currentExtrusionT0 = newExtrusion

        
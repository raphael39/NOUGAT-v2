import sys
from PyQt6.QtWidgets import QRadioButton, QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QLineEdit, QHBoxLayout
from PyQt6.QtWidgets import QGroupBox
import PyQt6.QtCore as QtCore
from processOptions import ProcessOptions
from processing.myFileReader import myFileReader



class FilePicker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selected_file_path = None  # Speichern des ausgewählten Dateipfads

    def initUI(self):
        self.setWindowTitle('NOUGAT')
        mainlayoutVB = QVBoxLayout()
        self.setLayout(mainlayoutVB)

        self.initSchichtwechselGroup()
        self.initReiserouteGroup()
        self.initGradientenGroup()
        self.initDateiauswahlGroup()
        
        # Hinzufügen der Gruppen zur Hauptlayout
        mainlayoutVB.addWidget(self.groupSchichtwechsel)
        mainlayoutVB.addWidget(self.groupReiseroute)
        mainlayoutVB.addWidget(self.groupGradienten)
        # Hinzufügen der Buttons zur Hauptlayout
        mainlayoutVB.addWidget(self.openButton)
        mainlayoutVB.addWidget(self.processButton)
        mainlayoutVB.addWidget(self.filePathLabel)

    # Methode zum Aktivieren/Deaktivieren der Schichtwechsel-Option
    def on_radioButtonSchichtwechsel_toggled(self, checked):
        self.ModellMenü.setEnabled(checked)
        self.onComboBoxChanged(self.ModellMenü.currentIndex())
        self.ratioLineA.setEnabled(checked)
        self.ratioLineB.setEnabled(checked)
        self.NumberRepitions.setEnabled(checked)

    # Methode zum Initialisieren der Schichtwechsel-Gruppe
    def initSchichtwechselGroup(self):
        self.groupSchichtwechsel = QGroupBox("Schichtwechsel", self)
        layoutSchichtwechsel = QVBoxLayout()
        self.groupSchichtwechsel.setLayout(layoutSchichtwechsel)

        # RadioButton für die Option des Schichtwechsels
        self.radioButtonSchichtwechsel = QRadioButton("Schichtwechsel aktivieren", self)
        layoutSchichtwechsel.addWidget(self.radioButtonSchichtwechsel)
        self.radioButtonSchichtwechsel.toggled.connect(self.on_radioButtonSchichtwechsel_toggled)

        # ComboBox für das Modell
        self.ModellMenü = QComboBox(self)
        self.ModellMenü.addItem("2 Schichten Modell")
        self.ModellMenü.addItem("Vollschichten Modell")
        self.ModellMenü.currentIndexChanged.connect(self.onComboBoxChanged)
        layoutSchichtwechsel.addWidget(self.ModellMenü)

        # Label und Textfelder für das Verhältnis der abwechselnden Schichten
        self.LabelVerhätnis = QLabel("Verhältnis der abwechselnden Schichten", self)
        layoutSchichtwechsel.addWidget(self.LabelVerhätnis)
    
        self.verhältnisLayoutHB = QHBoxLayout()
        self.ratioLineA = QLineEdit(self)
        self.ratioLineA.setPlaceholderText("1")
        self.ratioLineB = QLineEdit(self)
        self.ratioLineB.setPlaceholderText("3")
        self.ratioColonLabel = QLabel(":", self)
        self.verhältnisLayoutHB.addWidget(self.ratioLineA)
        self.verhältnisLayoutHB.addWidget(self.ratioColonLabel)
        self.verhältnisLayoutHB.addWidget(self.ratioLineB)
        layoutSchichtwechsel.addLayout(self.verhältnisLayoutHB)

        # Label und Textfeld für die Anzahl der Wiederholungen
        self.numberRepitionsLabel = QLabel("Anzahl Wiederholungen", self)
        layoutSchichtwechsel.addWidget(self.numberRepitionsLabel)
        self.NumberRepitions = QLineEdit(self)
        self.NumberRepitions.setPlaceholderText("125")
        layoutSchichtwechsel.addWidget(self.NumberRepitions)

        self.on_radioButtonSchichtwechsel_toggled(self.radioButtonSchichtwechsel.isChecked())
    
    # Methode zum Initialisieren der Reiseroute-Gruppe
    def initReiserouteGroup(self):
        self.groupReiseroute = QGroupBox("Reiseroute", self)
        layoutReiseroute = QVBoxLayout()
        self.groupReiseroute.setLayout(layoutReiseroute)

        # RadioButton für die Option der Reiseroute
        self.radioButtonTravelOutside = QRadioButton("Reiseroute nicht über das Bauteil", self)
        layoutReiseroute.addWidget(self.radioButtonTravelOutside)

    # Methode aktiviert/deaktiviert die Gradienten-Option  
    def on_radioButtonGradienten_toggled(self, checked):
        self.gradientenGrundflächeLayer.setEnabled(checked)
        self.gradientStartHöhe.setEnabled(checked)
        self.gradientenLineStartHöhe.setEnabled(checked)
        self.gradientenLineEndHöhe.setEnabled(checked)
        self.gradientenFlowRate.setEnabled(checked)
        self.gradientenFlowRateFactor.setEnabled(checked)
        self.gradientenAnzahl.setEnabled(checked)

    # Methode zum Initialisieren der Gradienten-Gruppe
    def initGradientenGroup(self):
        self.groupGradienten = QGroupBox("Gradienten", self)
        layoutGradienten = QVBoxLayout()
        self.groupGradienten.setLayout(layoutGradienten)

        # RadioButton für die Option der Gradienten
        self.radioButtonGradienten = QRadioButton("Gradienten aktivieren", self)
        layoutGradienten.addWidget(self.radioButtonGradienten)
        self.radioButtonGradienten.toggled.connect(self.on_radioButtonGradienten_toggled)

        # Label und Textfelder für die Gradientengrundflächen
        self.gradientenLabel = QLabel("Gradientengrundflächen von zu findendem Layer zu platzierender StartHöhe", self)
        layoutGradienten.addWidget(self.gradientenLabel)
    
        self.gradientenGrundlächeLayoutHB = QHBoxLayout()
        self.gradientenGrundFlächeFindenLabel = QLabel("Finden:", self)
        self.gradientenGrundflächeLayer = QLineEdit(self)
        self.gradientenGrundflächeLayer.setPlaceholderText("z.B. Layer 250 ")
        self.gradientenGrundflächePlatzierenLabel = QLabel("Platzieren:", self)
        self.gradientStartHöhe = QLineEdit(self)
        self.gradientStartHöhe.setPlaceholderText("auf Höhe 0.390mm ")
        self.gradientenGrundlächeLayoutHB.addWidget(self.gradientenGrundFlächeFindenLabel)
        self.gradientenGrundlächeLayoutHB.addWidget(self.gradientenGrundflächeLayer)
        self.gradientenGrundlächeLayoutHB.addWidget(self.gradientenGrundflächePlatzierenLabel)
        self.gradientenGrundlächeLayoutHB.addWidget(self.gradientStartHöhe)
        layoutGradienten.addLayout(self.gradientenGrundlächeLayoutHB)

        # Label und Textfelder für die Gradientenanfangs- und -endhöhe
        self.gradientenStartLabel = QLabel("Gradientenanfangshöhe und -endhöhe", self)
        layoutGradienten.addWidget(self.gradientenStartLabel)
    
        self.gradientenStartEndLayoutHB = QHBoxLayout()
        self.gradientenLineStartHöhe = QLineEdit(self)
        self.gradientenLineStartHöhe.setPlaceholderText("z.B. 0.05mm Schichthöhe")
        self.gradientenLineStartHöheLabel = QLabel("mm", self)
        self.gradientenLineEndHöhe = QLineEdit(self)
        self.gradientenLineEndHöhe.setPlaceholderText("z.B. bis auf 0.2mm Schichthöhe")
        self.gradientenLineEndHöheLabel = QLabel("mm", self)
        self.gradientenStartEndLayoutHB.addWidget(self.gradientenLineStartHöhe)
        self.gradientenStartEndLayoutHB.addWidget(self.gradientenLineStartHöheLabel)
        self.gradientenStartEndLayoutHB.addWidget(self.gradientenLineEndHöhe)
        self.gradientenStartEndLayoutHB.addWidget(self.gradientenLineEndHöheLabel)
        layoutGradienten.addLayout(self.gradientenStartEndLayoutHB)

        self.gradientenFlowRateLayoutHB = QHBoxLayout()
        self.gradientenFlowRateLabel = QLabel("Gradientenflowrate", self)
        self.gradientenFlowRate = QLineEdit(self)
        self.gradientenFlowRate.setPlaceholderText("z.B. 120%")
        self.gradientenFlowRateFactorLabel = QLabel("GradientdescendingFactor", self)
        self.gradientenFlowRateFactor = QLineEdit(self)
        self.gradientenFlowRateFactor.setPlaceholderText("z.B 0.9")
        self.gradientenFlowRateLayoutHB.addWidget(self.gradientenFlowRateLabel)
        self.gradientenFlowRateLayoutHB.addWidget(self.gradientenFlowRate)
        self.gradientenFlowRateLayoutHB.addWidget(self.gradientenFlowRateFactorLabel)
        self.gradientenFlowRateLayoutHB.addWidget(self.gradientenFlowRateFactor)
        layoutGradienten.addLayout(self.gradientenFlowRateLayoutHB)

        self.gradientenAnzahlLayoutHB = QHBoxLayout()
        self.gradientenAnzahlLabel = QLabel("Anzahl der Gradienten", self)
        self.gradientenAnzahl = QLineEdit(self)
        self.gradientenAnzahl.setPlaceholderText("z.B. 5")
        self.gradientenAnzahlLayoutHB.addWidget(self.gradientenAnzahlLabel)
        self.gradientenAnzahlLayoutHB.addWidget(self.gradientenAnzahl)
        layoutGradienten.addLayout(self.gradientenAnzahlLayoutHB)



        self.on_radioButtonGradienten_toggled(self.radioButtonGradienten.isChecked())

    # Methode zum Initialisieren der Dateiauswahl-Gruppe
    def initDateiauswahlGroup(self):
        # Button zum Öffnen des Dateiauswahldialogs
        self.openButton = QPushButton('Datei auswählen', self)
        self.openButton.clicked.connect(self.showFileDialog)
    
        # Button zum Verarbeiten der Datei
        self.processButton = QPushButton('Datei verarbeiten', self)
        self.processButton.clicked.connect(self.processFile)
    
        # Label für den Pfad der ausgewählten Datei
        self.filePathLabel = QLabel(self)

    # Methode zum Anzeigen oder Verbergen der Textfelder basierend auf der Auswahl
    def onComboBoxChanged(self, index):
        # Zeigen oder Verbergen der Textfelder basierend auf der Auswahl
        if self.ModellMenü.currentText() == "2 Schichten Modell":
            self.LabelVerhätnis.show()
            self.verhältnisLayoutHB.itemAt(0).widget().show()
            self.verhältnisLayoutHB.itemAt(1).widget().show()
            self.verhältnisLayoutHB.itemAt(2).widget().show()
            self.numberRepitionsLabel.show()
            self.NumberRepitions.show()
        elif self.ModellMenü.currentText() == "Vollschichten Modell":
            self.LabelVerhätnis.show()
            self.verhältnisLayoutHB.itemAt(0).widget().show()
            self.verhältnisLayoutHB.itemAt(1).widget().show()
            self.verhältnisLayoutHB.itemAt(2).widget().show()
            self.numberRepitionsLabel.hide()
            self.NumberRepitions.hide()       
        else:
            self.LabelVerhätnis.hide()
            self.verhältnisLayoutHB.itemAt(0).widget().hide()
            self.verhältnisLayoutHB.itemAt(1).widget().hide()
            self.verhältnisLayoutHB.itemAt(2).widget().hide()

    # Methode zum Öffnen des Dateiauswahldialogs
    def showFileDialog(self):
        try:
            fileName, _ = QFileDialog.getOpenFileName(self, "Datei auswählen", "", "Alle Dateien (*)")
            if fileName:
                self.filePathLabel.setText(fileName)
                self.selected_file_path = fileName  # Speichern des ausgewählten Dateipfads
        except Exception as e:
            print(f"Fehler beim Öffnen des Dialogs: {e}")

    # Methode zum Konvertieren eines Strings in einen Float
    def get_float_from_text(self, text, default_value=0.0):
        try:
            return float(text)
        except ValueError:
            return default_value
        
    # Methode zum Verarbeiten der Datei mit der FileInput Klasse
    def processFile(self):
        if self.selected_file_path:
            try:
                options = ProcessOptions(
                    schichtwechsel=self.radioButtonSchichtwechsel.isChecked(),
                    modell_Option=self.ModellMenü.currentText(),
                    verhältnis_A=self.get_float_from_text(self.ratioLineA.text()),
                    verhältnis_B=self.get_float_from_text(self.ratioLineB.text()),
                    numberRepitions=int(self.NumberRepitions.text()) if self.NumberRepitions.text().isdigit() else 0,
                    travelOutside=self.radioButtonTravelOutside.isChecked(),
                    gradienten=self.radioButtonGradienten.isChecked(),
                    gradientGrundflächeLayer=self.get_float_from_text(self.gradientenGrundflächeLayer.text()),
                    gradientStartHöhe=self.get_float_from_text(self.gradientStartHöhe.text()),
                    gradientenLineStartHöhe=self.get_float_from_text(self.gradientenLineStartHöhe.text()),
                    gradientenLineEndHöhe=self.get_float_from_text(self.gradientenLineEndHöhe.text()),
                    gradientenFlowRate=self.get_float_from_text(self.gradientenFlowRate.text()),
                    gradientenFlowRateFactor=self.get_float_from_text(self.gradientenFlowRateFactor.text()),
                    gradientenLayers=int(self.get_float_from_text(self.gradientenAnzahl.text()))
                )
            except ValueError as e:
                print(f"Ungültige Eingabe: {e}")
                return  # Frühzeitiger Rückkehr bei fehlerhafter Eingabe

            file_processor = myFileReader(self.selected_file_path)
            file_processor.process_file(options)
        else:
            print("Keine Datei ausgewählt")

# Methode zum Starten der Anwendung
def main():
    app = QApplication(sys.argv)
    ex = FilePicker()
    ex.show()
    sys.exit(app.exec())


# Starten der Anwendung mit der main Methode als Einstiegspunkt
if __name__ == '__main__':
    main()

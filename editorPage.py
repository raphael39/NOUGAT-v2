import sys
from PyQt6.QtWidgets import QRadioButton, QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QLineEdit, QHBoxLayout
from processing.file_input import FileInput  # Importieren der FileInput Klasse

class FilePicker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selected_file_path = None  # Speichern des ausgewählten Dateipfads

    def initUI(self):
        self.setWindowTitle('NOUGAT')

        

        mainlayoutVB = QVBoxLayout()
        self.setLayout(mainlayoutVB)

        ##### Auswahlkästchen für die Typ des Modells (ComboBox) hinzufügen
        self.ModellMenü = QComboBox(self)
        self.ModellMenü.addItem("2 Schichten Modell")  # Erster Menüpunkt
        self.ModellMenü.addItem("Vollschichten Modell")  # Zweiter Menüpunkt
        mainlayoutVB.addWidget(self.ModellMenü)
        self.ModellMenü.currentIndexChanged.connect(self.onComboBoxChanged)

        ##### Description for the ratio of alternating layers
        self.LabelVerhätnis = QLabel("Verhältnis der abwechselnden Schichten", self)
        mainlayoutVB.addWidget(self.LabelVerhätnis)

        #Textfelder für die Eingabe des Verhältnisses bei der Auswahl des 2 Schichten Modells hinzufügen
        self.verhältnisLayoutHB = QHBoxLayout()
        
        self.ratioLineA = QLineEdit(self)
        self.ratioLineB = QLineEdit(self)
        self.ratioColonLabel = QLabel(":", self)

        self.verhältnisLayoutHB.addWidget(self.ratioLineA)
        self.verhältnisLayoutHB.addWidget(self.ratioColonLabel)
        self.verhältnisLayoutHB.addWidget(self.ratioLineB)

        mainlayoutVB.addLayout(self.verhältnisLayoutHB)

        ##### Description for the number of repetitions
        self.numberRepitionsLabel = QLabel("Anzahl Wiederholungen", self)
        mainlayoutVB.addWidget(self.numberRepitionsLabel)
        #Textfeld für die Eingabe der Wiederholungsanzahl
        self.NumberRepitions = QLineEdit(self)
        mainlayoutVB.addWidget(self.NumberRepitions)

        ##### Radio Button für die Option der Reiseroute hinzufügen
        self.radioButtonTravelOutside = QRadioButton("Reiseroute nicht über das Bauteil", self)
        mainlayoutVB.addWidget(self.radioButtonTravelOutside)

        # Button zum Öffnen des Dateiauswahldialogs hinzufügen
        self.openButton = QPushButton('Datei auswählen', self)
        self.openButton.clicked.connect(self.showFileDialog)
        mainlayoutVB.addWidget(self.openButton)

        # Button zum Verarbeiten der Datei hinzufügen
        self.processButton = QPushButton('Datei verarbeiten', self)  # Neuer Button zum Verarbeiten
        self.processButton.clicked.connect(self.processFile)  # Verbinden des Buttons mit der Verarbeitungsmethode
        mainlayoutVB.addWidget(self.processButton)

        self.filePathLabel = QLabel(self)
        mainlayoutVB.addWidget(self.filePathLabel)

        # Anfangsstatus der Textfelder (deaktiviert)
        self.verhältnisLayoutHB.itemAt(0).widget().show()
        self.verhältnisLayoutHB.itemAt(1).widget().show()
        self.verhältnisLayoutHB.itemAt(2).widget().show()

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

    # Methode zum Verarbeiten der Datei mit der FileInput Klasse
    def processFile(self):
        if self.selected_file_path:
            modell_Option = self.ModellMenü.currentText()
            verhältnis_A = self.ratioLineA.text()
            verhältnis_B = self.ratioLineB.text()
            numberRepitions = self.NumberRepitions.text()
            travelOutside = self.radioButtonTravelOutside.isChecked()
            file_processor = FileInput(self.selected_file_path)  # Erstellen einer Instanz von FileInput
            file_processor.process_file(modell_Option, verhältnis_A, verhältnis_B, numberRepitions, travelOutside )  # Aufrufen der Verarbeitungsmethode mit den ausgewählten Optionen
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

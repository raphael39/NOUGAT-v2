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

        # Minimale und maximale Fenstergröße festlegen
        self.setMinimumSize(400, 300)  # Mindestgröße auf 400x300 Pixel setzen
        self.setMaximumSize(800, 600)  # Maximalgröße auf 800x600 Pixel setzen

        layout = QVBoxLayout()
        self.setLayout(layout)

         # Auswahlkästchen für die Typ des Modells (ComboBox) hinzufügen
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("2 Schichten Modell")  # Erster Menüpunkt
        self.comboBox.addItem("Vollschichten Modell")  # Zweiter Menüpunkt
        layout.addWidget(self.comboBox)
        self.comboBox.currentIndexChanged.connect(self.onComboBoxChanged)

        #Textfelder für die Eingabe des Verhältnisses bei der Auswahl des 2 Schichten Modells hinzufügen
        self.ratioLayout = QHBoxLayout()
        
        self.ratioLineEdit1 = QLineEdit(self)
        self.ratioLineEdit2 = QLineEdit(self)
        self.ratioLabel = QLabel(":", self)

        self.ratioLayout.addWidget(self.ratioLineEdit1)
        self.ratioLayout.addWidget(self.ratioLabel)
        self.ratioLayout.addWidget(self.ratioLineEdit2)

        layout.addLayout(self.ratioLayout)

        #Radio Button für die Option der Reiseroute hinzufügen
        self.radioButton1 = QRadioButton("Reiseroute nicht über das Bauteil", self)
        layout.addWidget(self.radioButton1)

        # Button zum Öffnen des Dateiauswahldialogs hinzufügen
        self.openButton = QPushButton('Datei auswählen', self)
        self.openButton.clicked.connect(self.showFileDialog)
        layout.addWidget(self.openButton)

        # Button zum Verarbeiten der Datei hinzufügen
        self.processButton = QPushButton('Datei verarbeiten', self)  # Neuer Button zum Verarbeiten
        self.processButton.clicked.connect(self.processFile)  # Verbinden des Buttons mit der Verarbeitungsmethode
        layout.addWidget(self.processButton)

        self.filePathLabel = QLabel(self)
        layout.addWidget(self.filePathLabel)

        # Anfangsstatus der Textfelder (deaktiviert)
        self.ratioLayout.itemAt(0).widget().show()
        self.ratioLayout.itemAt(1).widget().show()
        self.ratioLayout.itemAt(2).widget().show()

    # Methode zum Anzeigen oder Verbergen der Textfelder basierend auf der Auswahl
    def onComboBoxChanged(self, index):
        # Zeigen oder Verbergen der Textfelder basierend auf der Auswahl
        if self.comboBox.currentText() == "2 Schichten Modell":
            self.ratioLayout.itemAt(0).widget().show()
            self.ratioLayout.itemAt(1).widget().show()
            self.ratioLayout.itemAt(2).widget().show()
        else:
            self.ratioLayout.itemAt(0).widget().hide()
            self.ratioLayout.itemAt(1).widget().hide()
            self.ratioLayout.itemAt(2).widget().hide()

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
            selected_Option = self.comboBox.currentText()
            file_processor = FileInput(self.selected_file_path)  # Erstellen einer Instanz von FileInput
            file_processor.process_file(selected_Option)  # Aufrufen der Verarbeitungsmethode
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

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from processing.file_input import FileInput  # Importieren der FileInput Klasse

class FilePicker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selected_file_path = None  # Speichern des ausgewählten Dateipfads

    def initUI(self):
        self.setWindowTitle('NOUGAT')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.openButton = QPushButton('Datei auswählen', self)
        self.openButton.clicked.connect(self.showFileDialog)
        layout.addWidget(self.openButton)

        self.processButton = QPushButton('Datei verarbeiten', self)  # Neuer Button zum Verarbeiten
        self.processButton.clicked.connect(self.processFile)  # Verbinden des Buttons mit der Verarbeitungsmethode
        layout.addWidget(self.processButton)

        self.filePathLabel = QLabel(self)
        layout.addWidget(self.filePathLabel)

    def showFileDialog(self):
        try:
            fileName, _ = QFileDialog.getOpenFileName(self, "Datei auswählen", "", "Alle Dateien (*)")
            if fileName:
                self.filePathLabel.setText(fileName)
                self.selected_file_path = fileName  # Speichern des ausgewählten Dateipfads
        except Exception as e:
            print(f"Fehler beim Öffnen des Dialogs: {e}")

    def processFile(self):
        if self.selected_file_path:
            file_processor = FileInput(self.selected_file_path)  # Erstellen einer Instanz von FileInput
            file_processor.process_file()  # Aufrufen der Verarbeitungsmethode
        else:
            print("Keine Datei ausgewählt")

def main():
    app = QApplication(sys.argv)
    ex = FilePicker()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

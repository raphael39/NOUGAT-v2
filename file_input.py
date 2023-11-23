import os
import shutil

class FileInput:
    def __init__(self, file_path):
        self.file_path = file_path

    def process_file(self):
        # Logik zur Verarbeitung der Datei
        # ...

        # Neuen Dateinamen erstellen
        dir_name, file_name = os.path.split(self.file_path)
        name, ext = os.path.splitext(file_name)
        new_file_name = f"{name}_veraendert{ext}"
        new_file_path = os.path.join(dir_name, new_file_name)

        # Hier fügen Sie Ihre Logik ein, um die Datei zu verändern
        # Zum Beispiel: Lesen Sie die Originaldatei und schreiben Sie den veränderten Inhalt in die neue Datei
        # ...

        # Fürs Beispiel kopieren wir einfach die Datei
        shutil.copy(self.file_path, new_file_path)

        print(f"Datei verarbeitet und gespeichert als: {new_file_path}")

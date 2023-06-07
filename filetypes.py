import os


def find_file_types(dir_path):
    # Dateitypen sammeln
    file_types = set()

    # Durchlaufen des Verzeichnisbaums
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # Extrahieren des Dateityps
            _, extension = os.path.splitext(file)

            # Fügen Sie den Dateityp zur Menge hinzu
            file_types.add(extension)

    return file_types


# Pfad zum durchsuchenden Verzeichnis
dir_path = 'C:/Users/nicol/OneDrive/Playlist'  # Ändern Sie dies in den Pfad, den Sie durchsuchen möchten

file_types = find_file_types(dir_path)

# Ausgeben der gefundenen Dateitypen
for file_type in file_types:
    print(f'Gefundener Dateityp: {file_type}')

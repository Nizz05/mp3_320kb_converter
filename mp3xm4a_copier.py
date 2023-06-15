import os
import shutil
from pathlib import Path

def kopiere_dateien(input_ordner, output_ordner, datei_endungen):
    # Stelle sicher, dass der Output-Ordner existiert
    os.makedirs(output_ordner, exist_ok=True)

    input_ordner_path = Path(input_ordner)

    for wurzel, ordner, dateien in os.walk(input_ordner):
        for datei in dateien:
            if datei.endswith(datei_endungen):
                pfad_zu_datei = Path(wurzel) / datei
                # Erstelle das Unterverzeichnis im Output-Ordner, das dem relativen Pfad im Input-Ordner entspricht
                rel_pfad = pfad_zu_datei.relative_to(input_ordner_path)
                output_pfad = Path(output_ordner) / rel_pfad
                output_pfad.parent.mkdir(parents=True, exist_ok=True)

                shutil.copy2(pfad_zu_datei, output_pfad)

def main():
    input_ordner = 'C:\\Users\\nicol\\OneDrive\\Playlist'
    output_ordner = 'G:\\Test1'
    datei_endungen = ('.aiff', '.aif', '.wav')

    kopiere_dateien(input_ordner, output_ordner, datei_endungen)


if __name__ == '__main__':
    main()

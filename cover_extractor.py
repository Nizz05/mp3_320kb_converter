import os
from mutagen import File, MutagenError

input_dir = 'C:/Users/nicol/OneDrive/Playlist'  # Pfad zu den Quelldateien
output_dir = 'C:/Users/nicol/Desktop/outpout'  # Pfad zum Ausgabeordner

for dirpath, dirnames, filenames in os.walk(input_dir):
    for filename in filenames:
        # Der vollständige Pfad zur Quelldatei
        file_path = os.path.join(dirpath, filename)
        # Die Ausgabedatei, die auf den gleichen Namen wie die Quelle gesetzt ist, aber mit einer .png-Erweiterung
        output_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.png')

        try:
            # Öffnen Sie die Datei mit mutagen
            audio = File(file_path)

            # Wenn die Datei ein Wave-Format hat, überspringen wir sie
            if file_path.lower().endswith('.wav'):
                continue

            # Wenn das Audio-Objekt Bilder hat
            if hasattr(audio, 'pictures') and audio.pictures:
                # Nehmen Sie das erste Bild (dies könnte angepasst werden, wenn Sie ein bestimmtes Bild wollen)
                picture = audio.pictures[0]
                # Schreiben Sie das Bild in die Ausgabedatei
                with open(output_file_path, 'wb') as img:
                    img.write(picture.data)
        except MutagenError:
            print(f"Datei {file_path} wurde nicht gefunden, sie wird übersprungen.")
            continue

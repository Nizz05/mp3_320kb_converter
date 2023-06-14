import os
# cover_importer.py
import os
import eyed3
import glob


def import_cover(music_directory, cover_directory):
    # Durchlaufen aller Dateien im Musikverzeichnis
    for root, dirs, files in os.walk(music_directory):
        for file in files:
            # Prüfen ob die Datei eine mp3-Datei ist
            if file.endswith(".mp3"):
                # Pfad zur mp3-Datei
                mp3_path = os.path.join(root, file)

                # Name der mp3-Datei ohne Erweiterung
                mp3_name = os.path.splitext(file)[0]

                # Pfad zur möglichen png-Datei
                png_path = os.path.join(cover_directory, mp3_name + ".png")

                # Wenn die png-Datei existiert, dann füge sie der mp3-Datei hinzu
                if os.path.exists(png_path):
                    # Laden der mp3-Datei
                    audio_file = eyed3.load(mp3_path)
                    if audio_file.tag is None:
                        # Erstelle einen Tag, falls keiner existiert
                        audio_file.initTag()

                    # Bild hinzufügen
                    audio_file.tag.images.set(3, open(png_path, 'rb').read(), 'image/png')

                    # Änderungen speichern
                    audio_file.tag.save()


def delete_png_files(directory):
    # Generiere einen Pfad für jede .png Datei im angegebenen Ordner
    png_files = glob.glob(os.path.join(directory, "*.png"))

    # Gehe durch jede png-Datei und lösche sie
    for png_file in png_files:
        try:
            os.remove(png_file)
        except OSError:
            print(f"Datei {png_file} konnte nicht gelöscht werden.")
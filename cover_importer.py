import os
import eyed3
# Pfade zu den Verzeichnissen
music_directory = "C:/Users/nicol/OneDrive/playlist_mp3_iphonefriendly"
cover_directory = "C:/Users/nicol/Desktop/outpout"

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

import os
import shutil


def kopieren_dateien(quell_ordner, ziel_ordner, erlaubte_formate):
    for wurzel, ordner, dateien in os.walk(quell_ordner):
        for datei in dateien:
            if datei.split('.')[-1] in erlaubte_formate:
                quell_datei = os.path.join(wurzel, datei)
                ziel_datei = os.path.join(ziel_ordner, os.path.relpath(quell_datei, quell_ordner))

                os.makedirs(os.path.dirname(ziel_datei), exist_ok=True)

                if os.path.exists(ziel_datei):
                    print(f"Die Datei {ziel_datei} existiert bereits, Überspringen")
                    continue

                print(f"Kopiere Datei {quell_datei} nach {ziel_datei}")  # Zeigt, welche Dateien kopiert werden

                shutil.copy2(quell_datei, ziel_datei)


if __name__ == "__main__":
    quell_ordner = "C:/Users/nicol/OneDrive/Playlist"  # Pfad zu Ihrem Quellordner
    ziel_ordner = "C:/Users/nicol/OneDrive/playlist_wav_aiff_wma"  # Pfad zu Ihrem Zielordner

    erlaubte_formate = {'wav', 'aiff', 'aif', 'wma'}  # Erlaubte Dateiformate

    kopieren_dateien(quell_ordner, ziel_ordner, erlaubte_formate)

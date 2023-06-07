import os
import shutil
import concurrent.futures
from pydub import AudioSegment


def process_file(file_path, target_path):
    # Wenn die Ausgabedatei bereits existiert, überspringe die Verarbeitung
    if os.path.exists(target_path):
        print(f"Überspringe {file_path}, da bereits konvertiert.")
        return

    # Konvertiere oder kopiere die Datei, abhängig vom Dateityp
    if file_path.lower().endswith('.mp3'):
        print(f"Kopiere {file_path}...")
        shutil.copy(file_path, target_path)
    else:
        print(f"Konvertiere {file_path}...")
        try:
            audio = AudioSegment.from_file(file_path)
            audio.export(target_path, format='mp3', bitrate='320k')
        except Exception as e:
            print(f"Konnte {file_path} nicht konvertieren: {e}")


def scan_folders(input_folder, output_folder):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for path, subdirs, files in os.walk(input_folder):
            for name in files:
                file_path = os.path.join(path, name)
                relative_path = os.path.relpath(path, input_folder)
                output_path = os.path.join(output_folder, relative_path)
                os.makedirs(output_path, exist_ok=True)
                target_path = os.path.join(output_path, os.path.splitext(name)[0] + '.mp3')
                executor.submit(process_file, file_path, target_path)


# Startpunkt ist der Pfad zu Ihrem Ordner
input_folder_path = "C:/Users/nicol/OneDrive/Playlist"
output_folder_path = "C:/Users/nicol/Desktop/outpout"
scan_folders(input_folder_path, output_folder_path)

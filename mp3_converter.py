import os
import shutil
import concurrent.futures
from pydub import AudioSegment

def process_file(file_path, target_path):
    # Wenn die Ausgabedatei bereits existiert, überspringe die Verarbeitung
    if os.path.exists(target_path):
        print(f"Überspringe {file_path}, da bereits verarbeitet.")
        return

    # Konvertiere oder kopiere die Datei, abhängig vom Dateityp
    if file_path.lower().endswith(('.flac', '.wma',)):
        print(f"Konvertiere {file_path}...")
        try:
            audio = AudioSegment.from_file(file_path)
            audio.export(target_path, format='mp3', bitrate='320k')
        except Exception as e:
            print(f"Konnte {file_path} nicht konvertieren: {e}")
    else:
        print(f"Kopiere Nicht-Audiodatei {file_path}...")
        shutil.copy(file_path, target_path)

def scan_folders(input_folder, output_folder):
    total_files = 0
    for path, subdirs, files in os.walk(input_folder):
        for name in files:
            if name.lower().endswith(('.flac', '.wma')):
                total_files += 1

    converted_files = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for path, subdirs, files in os.walk(input_folder):
            for name in files:
                file_path = os.path.join(path, name)
                relative_path = os.path.relpath(path, input_folder)
                output_path = os.path.join(output_folder, relative_path)
                os.makedirs(output_path, exist_ok=True)

                if file_path.lower().endswith(('.flac', '.wma')):
                    target_path = os.path.join(output_path, os.path.splitext(name)[0] + '.mp3')
                    future = executor.submit(process_file, file_path, target_path)
                    futures.append(future)
                else:
                    target_path = os.path.join(output_path, name)
                    executor.submit(process_file, file_path, target_path)

        for future in concurrent.futures.as_completed(futures):
            if future.exception() is None:
                converted_files += 1
            progress = (converted_files / total_files) * 100
            yield progress  # Hier wird der aktuelle Fortschritt zurückgegeben


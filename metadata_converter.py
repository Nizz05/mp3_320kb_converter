import os
from tinytag import TinyTag
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TRCK, TDRC, APIC


def copy_metadata_and_cover(original_file, converted_file):
    try:
        # Get metadata from the original file
        original_metadata = TinyTag.get(original_file)

        # Load or create ID3 tag in the converted file
        mp3_file = MP3(converted_file, ID3=ID3)

        # Copy metadata
        if original_metadata.title:
            mp3_file.tags.add(TIT2(encoding=3, text=original_metadata.title))
        if original_metadata.artist:
            mp3_file.tags.add(TPE1(encoding=3, text=original_metadata.artist))
        if original_metadata.album:
            mp3_file.tags.add(TALB(encoding=3, text=original_metadata.album))
        if original_metadata.genre:
            mp3_file.tags.add(TCON(encoding=3, text=original_metadata.genre))
        if original_metadata.track:
            mp3_file.tags.add(TRCK(encoding=3, text=str(original_metadata.track)))
        if original_metadata.year:
            mp3_file.tags.add(TDRC(encoding=3, text=str(original_metadata.year)))

        mp3_file.save()

        # Load both files with mutagen
        original_file_tags = File(original_file)
        mp3_file = MP3(converted_file, ID3=ID3)

        # Copy cover art
        if 'APIC:' in original_file_tags.keys():
            artwork = original_file_tags['APIC:']
            mp3_file.tags.add(
                APIC(
                    encoding=artwork.encoding,
                    mime=artwork.mime,
                    type=artwork.type,
                    desc=artwork.desc,
                    data=artwork.data
                )
            )
            mp3_file.save()
    except Exception as e:
        print(f"Could not copy metadata and/or cover from {original_file} to {converted_file}: {e}")


def copy_metadata_and_cover_in_folder(input_folder, output_folder):
    for path, subdirs, files in os.walk(input_folder):
        for name in files:
            if name.lower().endswith(('.flac', '.wav', '.m4a', '.wma', '.aif', '.aiff')):
                original_file_path = os.path.join(path, name)
                relative_path = os.path.relpath(path, input_folder)
                converted_file_path = os.path.join(output_folder, relative_path, os.path.splitext(name)[0] + '.mp3')
                if os.path.exists(converted_file_path):
                    copy_metadata_and_cover(original_file_path, converted_file_path)


# Replace these paths with your actual paths
input_folder_path = "C:/Users/nicol/Desktop/input"
output_folder_path = "C:/Users/nicol/Desktop/outpout"
copy_metadata_and_cover_in_folder(input_folder_path, output_folder_path)

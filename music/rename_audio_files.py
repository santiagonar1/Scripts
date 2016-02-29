#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Este sript permite renombrar archivos de audio para que tengar el
formato '{artist} - {title}.mp3'
"""
try:
    import pytag
except ImportError:
    raise ImportError("La libreria pytag debe estar instalada. pip install pytag")
import argparse
import mimetypes
import os

def get_audio_files(files):
    """Retorna solamente los archivos de musica"""
    music_files = []
    for f in files:
        #if mimetypes.guess_type(f)[0] == "audio/mpeg":
        if "audio/" in mimetypes.guess_type(f)[0]:
            music_files.append(f)
    return music_files


def get_info(afile):
    """Retorna el titulo y album de la canción"""
    try:
        if afile[-4:] == ".mp3":
            tags = pytag.AudioReader(afile).get_tags()
        elif afile[-4:] == ".ogg":
            tags = pytag.formats.OggVorbisReader(afile).get_tags()
        return tags.get("artist", None), tags.get("title", None)
    except pytag.FormatNotSupportedError:
        print("FormatNotSupportedError: El archivo << {0} >> no es soportado".format(afile))
        return None, None
    except ValueError:
        print("ValueError: << {0} >> no ha podido ser procesado".format(afile))
        return None, None

def get_path(filepath):
    """Retorna el path del archivo: ej /home/p.py --> /home/"""
    path, filename = os.path.split(filepath)
    return path + "/" if path != "" else path

def rename_file(old_name, new_name):
    os.rename(old_name, "{0}{1}".format(get_path(old_name), new_name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='+',
                help="mp3 files to be renamed")

    args = parser.parse_args()
    for af in get_audio_files(args.files):
        artist, title = get_info(af)
        if artist and title:
            rename_file(af, "{0} - {1}.mp3".format(artist, title))

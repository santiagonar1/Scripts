#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para sincronizar los subtitulos de una pelicula

Ejemplo:
    python3 sync_subtitles.py input.srt -t HH:MM:SS,mmm [-f] [-o output.srt]
            [-s HH:MM:SS,mmm]

Autor: Santiago Narvaez
Fecha: 26.feb.2016
"""

import custom_time as ctime
import argparse
import os

# The lines with the times have the format: HH:MM:SS,mmm --> HH:MM:SS,mmm
SEARCH = "-->"
MESSAGES = {1:"The time format must be HH:MM:SS,mmm (ej.: 02:21:00,032)"}


def read(filename):
    """
    Reads and returns the filename's content
    """
    # We need to set encoding to latin-1 because the subtitles are in spanish
    with open(filename, "r", encoding="latin-1") as f:
        return f.read()


def get_times(string):
    """
    Takes a string with the format HH:MM:SS,mmm --> HH:MM:SS,mmm and returns
    a tuple with both times
    """
    return [ctime.string_to_time(s) for s in string.replace(" ", "").split(SEARCH)]


def main():
    parser = argparse.ArgumentParser(description="Helps to syncronize the subtitles")
    # Opciones que no pueden ser usadas al mismo tiempo:
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("input_file",
                       help="Path to file in which the subtitles are stored")
    parser.add_argument("-t", "--time",
                       help="Format HH:MM:SS,mmm to forward or delay the subtitles",
                       default="00:00:00,000")
    parser.add_argument("-f", "--forward",
                    help="By default the program delays the subtitles, but if this option is selected it will forward them",
                    action="store_true")
    group.add_argument("-o", "--output",
                       help="Output file",
                       default="new.srt")
    group.add_argument("-r", "--replace",
                        help="Replace the original file",
                        action="store_true")
    parser.add_argument("-s", "--since",
                       help="Format HH:MM:SS,mmm, sync the subtitles since this timestamp",
                       default="00:00:00,000")
    args = parser.parse_args()

    if not ctime.validate_string(args.time):
        print(MESSAGES[1])
        return -1

    mtime = ctime.string_to_time(args.time)
    stime = ctime.string_to_time(args.since)
    with open(args.output, "w", encoding="latin-1") as output:
        for line in read(args.input_file).split("\n"):
            if SEARCH in line:
                time1, time2 = get_times(line)
                if (time1 > stime) and args.forward:
                    time1 = ctime.milliseconds_to_time(mtime + time1)
                    time2 = ctime.milliseconds_to_time(mtime + time2)
                elif time1 > stime:
                    time1 = ctime.milliseconds_to_time(time1 - mtime)
                    time2 = ctime.milliseconds_to_time(time2 - mtime)
                line = "{0} {1} {2}".format(time1, SEARCH, time2)
            output.write(line + "\n")
    # If neccesary replace the original file
    if args.replace:
        os.remove(args.input_file)
        os.rename(args.output, args.input_file)


if __name__ == "__main__":
    main()




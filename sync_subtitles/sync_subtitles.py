#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import custom_time as ctime
import argparse

# The lines with the times have the format: HH:MM:SS,mmm --> HH:MM:SS,mmm
SEARCH = "-->"
MESSAGES = {1:"The time format must be HH:MM:SS,mmm (ej.: 02:21:00,032)"}


def read(filename):
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
    parser.add_argument("input_file",
                       help="Path to file in which the subtitles are stored")
    parser.add_argument("-t", "--time",
                       help="Format HH:MM:SS,mmm to forward or delay the subtitles",
                       default="00:00:00,000")
    parser.add_argument("-f", "--forward",
                    help="By default the program delays the subtitles, but if this option is selected it will forward them",
                    action="store_true")
    parser.add_argument("-o", "--output",
                       help="Output file",
                       default="new.srt")
    args = parser.parse_args()

    if not ctime.validate_string(args.time):
        print(MESSAGES[1])
        return -1

    mtime = ctime.string_to_time(args.time)
    with open(args.output, "w") as output:
        for line in read(args.input_file).split("\n"):
            if SEARCH in line:
                time1, time2 = [ctime.milliseconds_to_time(t + mtime)
                                if args.forward
                                else ctime.milliseconds_to_time(t - mtime)
                                for t in get_times(line)]
                line = "{0} {1} {2}".format(time1, SEARCH, time2)
            output.write(line + "\n")


if __name__ == "__main__":
    main()




#!/usr/bin/env python3
# -*- # -*- coding: utf-8 -*-

"""
Script para remplazar tabs con espacios

Ejemplo:
    python3 replace_tabs.py filename.py [-n number_spaces_per_tab]
            [-r replace_original_file]

Autor: Santiago Narvaez
Fecha: 26.feb.2016
"""

import argparse
import os

def read(filename):
    """
    Reads and returns the filename's content
    """
    # We need to set encoding to latin-1 because the subtitles are in spanish
    with open(filename, "r", encoding="latin-1") as f:
        return f.read()

def write(filename, content):
    """
    Writes content to filename. If there is alreade content in the file
    it does not erase it
    """
    with open(filename, "a") as f:
        f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace tabs with spaces")
    parser.add_argument("input_file",
                       help="Path to file in which the tabs are going to be replaced")
    parser.add_argument("-n", "--nspaces",
                       help="Number of spaces in a tab. By default 4",
                       type=int,
                       default=4)
    parser.add_argument("-r", "--replace",
                        help="Replace the original document",
                        action="store_true")

    args = parser.parse_args()
    for line in read(args.input_file).split("\n"):
        line = line.replace("\t", " "*args.nspaces)
        write(args.input_file+".new" , line+"\n")

    if(args.replace):
        os.remove(args.input_file)
        os.rename(args.input_file+".new", args.input_file)

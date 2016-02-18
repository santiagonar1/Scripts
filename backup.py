#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
ruta_usuario = "/home/santiago" #Modificar según ruta de usuario
ruta_volumen = "/run/media/santiago/SANTIAGO" #Modificar según nombre de disco externo
directorio_destino = ruta_volumen + "/" + "Backup"

try:
    if not os.path.exists(directorio_destino):
        os.mkdir(directorio_destino, mode=0o755)

    directorios_origen=[]
    rutas_directorios_origen=[]

    #Se añaden los directorios para sincronizar
    directorios_origen.append("Documents")
    directorios_origen.append("Pictures")
    directorios_origen.append("Music")
    directorios_origen.append("Programacion/C")
    directorios_origen.append("Programacion/C++")
    directorios_origen.append("Programacion/Java")
    directorios_origen.append("Programacion/Octave")
    directorios_origen.append("Programacion/Python")
    directorios_origen.append("Videos")

    for rutas in directorios_origen:
        rutas_directorios_origen.append(ruta_usuario + "/" + rutas)

    for rutas in rutas_directorios_origen:
        print("Sincronizando " + rutas + " con " + directorio_destino)
        os.system("rsync -ahv --progress" + " " + rutas + " " + directorio_destino)
    print("Proceso terminado")

except OSError:
    print("Ha ocurrido un error ¿está el disco externo listo?")

except:
    print("Ha ocurrido un error")

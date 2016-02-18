#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import time

from gi.repository import Notify as notify

# ID del indicador. Debe ser unico
APPINDICATOR_ID = 'batteryindicator'
# Path al archivo que muestra en el sistema el porcentaje de carga de la batería
CAPACITY_INDICATOR = '/sys/class/power_supply/BAT0/capacity'
# Path al archivo que muestra en el sistema el status de la batería [Charging, Discharging, Full]
STATUS_INDICATOR = '/sys/class/power_supply/BAT0/status'
# Máxima carga deseada antes de notificar
MAX_BATTERY = 90
# Mínima carga antes de notificar
MIN_BATTERY = 30
# Cada cuantos segundos revisa el estado de la bateria
CHECK_INTERVAL = 240


"""
Retorna el porcentaje de carga de la batería

Return: int, porcentaje de carga de la batería
"""
def get_capacity():
	with open(CAPACITY_INDICATOR, 'r') as f:
		capacity = int(f.read())
	return capacity

"""
Retorna el estado de la batería

Return: string, estado de la batería -> [Charging, Discharging, Full] 
"""
def get_status():
	with open(STATUS_INDICATOR, 'r') as f:
		status = f.read().replace('\n', '')
	return status

"""
Determina si la batería a) ya esta cargada, b) esta por descargarse, o c) esta bien.
Si a) o b), entonces genera la notificación pertinente.

capacity: int, porcentaje de carga de la batería.
status: string, estado de la batería -> [Charging, Discharging, Full]
"""
def check_battery(capacity, status):
	#Los iconos son tomados de /usr/share/notify-osd/icons/Humanity/scalable/status
	if capacity <= MIN_BATTERY and status == 'Discharging':
		make_notification("Power Critically Low", 
			"The battery is below the critical level and this computer will power-off when the battery becomes completely empty.", 
			"notification-battery-low")
	elif capacity >= MAX_BATTERY and (status == 'Charging' or status == 'Full'):
		make_notification("Battery Charged", 
			"Your laptop battery is now fully charged.", 
			"notification-battery-100-plugged")

"""
Genera una notificación.

title: string, Título de la notificación
body: string, Cuerpo de la notificación
icon: Path to an icon image, or the name of a stock icon
"""
def make_notification(title, body, icon):
	notify.init(APPINDICATOR_ID)
	notify.Notification.new(title, body, icon).show()
	# NOTA: Ubuntu al parecer no soporta el sonido para las notificaciones. Para comprobarlo se podría hacer:
	# 				for c in notify.get_server_caps(): print(c)
	# Si las soportara, sería posible (creo) reproducir un sonido mediante el siguiente codigo:
	# 				n.set_hint('sound-file', glib.Variant("s", PATH_TO_SOUND))
	# Se necesitaría el siguiente import:
	#				from gi.repository import GLib as glib
	#
	# Para mayor información: 	https://people.gnome.org/~gcampagna/docs/GLib-2.0/GLib.Variant.html
	#							https://people.gnome.org/~gcampagna/docs/GLib-2.0/GLib.VariantType.html
	#							http://dbus.freedesktop.org/doc/dbus-specification.html
	#							https://notify2.readthedocs.org/en/latest/
	#							https://people.gnome.org/~mccann/docs/notification-spec/notification-spec-latest.html#hints
	#							https://people.gnome.org/~mccann/docs/notification-spec/notification-spec-latest.html#commands


def main():
	while True:
		check_battery(get_capacity(), get_status())
		time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
	# Lo siguiente permite usar Ctrl + c para cancelar el script
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main()
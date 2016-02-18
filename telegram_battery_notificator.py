#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import telegram  # ver: https://pypi.python.org/pypi/python-telegram-bot
import signal
import time
import sys
import os

try:
	from urllib.error import URLError
except ImportError:
	from urllib2 import URLError  # python 2

# Token del Bot de Telegram
BOT_TOKEN = "156396267:AAH21YrqwJ_MF1Ljffvk5LJEqj5y8AzpFbQ"
# ID del chat en telegram
CHAT_ID = "165076928"
# Path al archivo que muestra en el sistema el porcentaje de carga de la batería
CAPACITY_INDICATOR = '/sys/class/power_supply/BAT0/capacity'
# Path al archivo que muestra en el sistema el status de la batería [Charging, Discharging, Full]
STATUS_INDICATOR = '/sys/class/power_supply/BAT0/status'
# Máxima carga deseada antes de notificar
MAX_BATTERY = 92
# Mínima carga antes de notificar
MIN_BATTERY = 20
# Cada cuantos segundos revisa el estado de la bateria
CHECK_INTERVAL = 30
# Lista de commandos aceptados
COMMANDS = ["Ok, thank you bot", "I'm bussy, don't interrupt me", "Wtf! ... shut down my machine"]

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
def check_battery(capacity, status, bot):
	#Los iconos son tomados de /usr/share/notify-osd/icons/Humanity/scalable/status
	if capacity <= MIN_BATTERY and status == 'Discharging':
		send_message("Power Critically Low",
			"The battery is below the critical level and the computer will power-off when the battery becomes completely empty.",
			bot)
	elif capacity >= MAX_BATTERY and (status == 'Charging' or status == 'Full'):
		send_message("Battery Charged",
			"Your laptop battery is now fully charged.",
			bot)

"""
Envia un mensaje a telegram

title : string, titulo del mensaje
body : string, cuerpo del mensaje
bot : telegram.Bot, es el bot usado para enviar el mensaje
"""
def send_message(title, body, bot):
	print "Enviando mensaje..."
	custom_keyboard = [ [c] for c in COMMANDS]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	bot.sendMessage(chat_id=CHAT_ID,
		text="*" + title.upper() + "*\n" + body,
		parse_mode=telegram.ParseMode.MARKDOWN,
		reply_markup=reply_markup)

"""
Retorna el update_id que DEBERÍA ser usado como offset para recuperar SOLAMENTE los mensajes
nuevos
"""
def get_update_id(bot):
	try:
		update_id = bot.getUpdates()[-1].update_id + 1
	except IndexError:
		update_id = None
	return update_id

"""
Revisa si el usuario ha enviado nuevos mensajes al bot

update_id: id del ultimo mensaje + 1
bot: bot usado para leer y, si es el caso, enviar mensajes

return: update_id actualizado, mensajes nuevos
"""
def get_new_messages(bot, update_id):
	new_messages = []
	# Request updates after the last update_id
	for update in bot.getUpdates(offset=update_id, timeout=0):
		update_id = update.update_id + 1
		new_messages.append(update.message.text)

	return update_id, new_messages

"""
Toma acciones de acuerdo a los mensajes recibidos, en orden de prioridad:

	1. Si ha recibido el COMMANDS[0], no hace nada
	2. Si ha recibido el COMMANDS[1], detiene el script
	3. Si ha recibido el COMMANDS[2], apaga el computador

Solamente realiza una de las anteriores acciones (p. ej., si hace el (1), no hace el (3) así halla
recibido COMMANDS[2])
"""
def answer_messages(messages, bot):
	if COMMANDS[0] in messages:
		send_message("You're welcome",
			"If just all the people were like you " + telegram.Emoji.SMILING_FACE_WITH_OPEN_MOUTH_AND_SMILING_EYES,
			bot)
	elif COMMANDS[1] in messages:
		send_message("Message received",
			"Don't worry, I'm not going to disturb you any more " + telegram.Emoji.LOUDLY_CRYING_FACE,
			bot)
		sys.exit (1)
	elif COMMANDS[2] in messages:
		send_message("Turning your computer off",
			"I'm turning your computer off, I hope you that you had saved all your work " + telegram.Emoji.PENSIVE_FACE,
			bot)
		os.system("systemctl poweroff")

def main():
	print "Iniciando el script..."
	bot = telegram.Bot(token = BOT_TOKEN)
	update_id = get_update_id(bot)
	while True:
		try:
			update_id, new_messages = get_new_messages(bot, update_id)
			answer_messages(new_messages, bot)
			time.sleep(CHECK_INTERVAL / 2.0)
			check_battery(get_capacity(), get_status(), bot)
			time.sleep(CHECK_INTERVAL / 2.0)
		except telegram.TelegramError as e:
			# These are network problems with Telegram.
			if e.message in ("Bad Gateway", "Timed out"):
				time.sleep(1)
			elif e.message == "Unauthorized":
				# The user has removed or blocked the bot.
				update_id += 1
			else:
				raise e
		except URLError as e:
			# These are network problems on our end.
			time.sleep(1)

if __name__ == "__main__":
	# Lo siguiente permite usar Ctrl + c para cancelar el script
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main()

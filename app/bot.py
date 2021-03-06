import tweepy
import logging
import time
import random
import datetime

from config import create_api

# Usamos la fecha y hora como semilla para las funciones random, porque sino
# cada vez que se inicia el bot, genera los mismos números aleatorios.
random.seed(datetime.datetime.now())

# Activamos un logging básico.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Esta es la función que manda fruta
def mandar_fruta(usuario):
	frases = ["¡Satisface!", "¡Resuena!", "¡Te elijo!", "¡Gran caricia!",
	"¡Enorme caricia!", "¡Siéntete libre!", "¡Te recomiendo!",
	"¡Adelante!", "¡Apoyo!", "¡Sincero aliento!", "¡Importante valor!"]
	random.shuffle(frases)
	return frases[0].replace("!", f" a @{usuario}!") + " " + frases[1] + " " + frases[2] + " #CariciaSignificativa"

# Esta es la función que cada N segundos busca menciones en Twitter.
# Usa la variable since_id, que es la mención más reciente que ya respondió,
# así no responde dos veces a la misma mención.
def check_mentions(api, since_id):
	logger.info(f"Buscando menciones desde {since_id}...")

	# Crea una variable temporal para ir guardando las IDs de los tweets que
	# vamos respondiendo.
	tmp_since_id = since_id

	# Buscamos menciones en Twitter.
	for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
		tmp_since_id = max(tweet.id, tmp_since_id)

		# Si el tweet es una respuesta, lo ignoramos.
		if tweet.in_reply_to_status_id is not None:
			continue

		logger.info(f"Respondiendo la mención de {tweet.user.name}.")

		# Si no estamos siguiendo al usuario, lo seguimos, total es gratis.
		if not tweet.user.following:
			tweet.user.follow()

		# Le mandamos fruta.
		try:
			api.update_status(mandar_fruta(tweet.user.screen_name))
		except Exception:
			logger.exception("Error al responder.")

	# Devolvemos la since_id más reciente
	return tmp_since_id

def main():
	# Generamos el objeto para interactuar con Twitter.
	# create_api() está definido en el archivo config.py
	api = create_api()

	# Cargamos el último tweet respondido desde la descripción del usuario
	# (esto es un hack súper grasa, pero Heroku no tiene persistencia
	# de datos, y son las 2 AM).
	try:
		since_id = int(api.me().description)
	except Exception:
		since_id = 1

	last_saved_since_id = since_id

	# Loop infinito.
	while True:
		# Buscamos menciones.
		since_id = check_mentions(api, since_id)
		
		# Guardamos el último tweet respondido como descripción del usuario
		if last_saved_since_id != since_id:
			try:
				api.update_profile(description=since_id)
				last_saved_since_id = since_id
			except Exception:
				logger.exception("Error al guardar la descripción.")
		
		# Esperamos 30 segundos
		logger.info("Esperando 30 segundos.")
		time.sleep(30)

if __name__ == "__main__":
	main()

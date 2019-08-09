import tweepy
import logging
import os

logger = logging.getLogger()

def create_api():
	# Cargamos los datos secretos desde las variables de entorno
	consumer_key = os.getenv("CONSUMER_KEY")
	consumer_secret = os.getenv("CONSUMER_SECRET")
	access_token = os.getenv("ACCESS_TOKEN")
	access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

	# Nos autenticamos con los datos secretos
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Creamos el objeto para interactuar con la API
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	# Verificamos si las credenciales son válidas
	try:
		api.verify_credentials()
	except Exception as e:
		logger.error("Las credenciales no son correctas.", exc_info=True)
		raise e

	logger.info("Credenciales correctas.")
	return api

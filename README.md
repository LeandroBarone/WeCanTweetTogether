# WeCanTweetTogether
Twitter bot en Python con Tweepy. Responde las menciones de otros usuarios con palabras de ánimo.

## Instalación

Este proyecto está preparado para correr en un dyno gratuito de Heroku, que es un sistema de virtualización de aplicaciones en la nube.

1) Clonar todo a un repo de GitHub.

2) Crear una cuenta de Twitter, solicitar acceso de desarrollador y generar las credenciales de acceso.

3) Crear una cuenta de Heroku (es gratis), crear una app y configurarla para que use el repo de arriba.

4) Crear estas cuatro variables de entorno con las credenciales que generamos arriba:

- CONSUMER_KEY
- CONSUMER_SECRET
- ACCESS_TOKEN
- ACCESS_TOKEN_SECRET

5) Activar el worker.

## Explicación de cada archivo:

**requirements.txt** le dice al administrador de paquetes de Python (pip) qué paquetes requiere este proyecto. Heroku lo usa para instalar los paquetes automáticamente.

**Procfile** le dice a Heroku qué procesos tienen que estar corriendo en este proyecto. En este caso, es uno solo worker: app/bot.py

**app/config.py** inicializa una conexión con Twitter usando la librería Tweepy. Nuestro bot necesita esto para interactuar con Twitter.

**app/bot.py** revisa cada 30 segundos la lista de tweets que mencionan al bot y le responde al autor con palabras de ánimo.

## Probando el proyecto en local desde Windows

Como el proyecto espera cuatro variables de entorno, es necesario especificarlas para poder probar el proyecto. Hacer esto desde Windows es muy fácil: hay que crear un archivo batch (por ejemplo, run.bat) con los siguientes comandos (reemplazando los puntos por las credenciales de nuestra cuenta de Twitter, sin comillas ni nada):

    set CONSUMER_KEY=...
    set CONSUMER_SECRET=...
    set ACCESS_TOKEN=...
    set ACCESS_TOKEN_SECRET=...
    python app/bot.py

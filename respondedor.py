#!/usr/bin/env python
# tweepy-bots/bots/followfollowers.py
from os import listdir
from os.path import isfile, join
import os
import tweepy
import logging
import random
from tweepy import TweepError

from config import create_api
import time

# habra varias reacciones.
# cada reaccion tendra su lista de nombre de fotos.
# la reaccion es la palabra clave que le sigue al !
# ejemplo: !susto


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# reacciones = ['gracioso', 'triste', 'aburrido', 'entretenido', 'random', '', ' ']

debug = True
##printea varias cosas como para saber que esta funcionandotodo ok
reaccionesDict = {
    'gracioso': 'src/gracioso/',
    'triste': 'src/triste/',
    'aburrido': 'src/aburrido/',
    'ansiedad': 'src/ansiedad/',
    'depresion': 'src/depresion/',
    'drogado': 'src/drogado/',
    'entretenido': 'src/entretenido/',
    'feliz': 'src/feliz/',
    'furioso': 'src/furioso/',
    'histeria': 'src/histeria/',
    'hot': 'src/hot/',
    'locura': 'src/locura/',
    'malardo': 'src/malardo/',
    'nerd': 'src/nerd/',
    'paranoia': 'src/paranoia/',
    'pete': 'src/pete/',
    'wtf': 'src/wtf/'
}



numero = 9




def crearCarpetas(diccionario):

    for value in diccionario:
        try:
            os.mkdir(diccionario[value])
            if debug: logger.info("se creo la carpeta {}".format(value))
        except FileExistsError:
            print("")




def buscarMencion(api, keywords, since_id):
    logger.info("Buscando menciones")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)

        if tweet.in_reply_to_status_id is not None:  ########estamos viendo si cambia algo
            continue
        #if any(palabraClave in tweet.text.lower() for palabraClave in keywords.keys()):
        for keyword in keywords.keys():
            if keyword in tweet.text.lower():

                #logger.info("hay tweets con palabras clave de {} cuyos ID son: {}".format( tweet.user.name, tweet.id))

                ##probando si asi funciona al menos y si funciona hago el chequeo de la palabra clave adentro
                if not estaFaveado(api, tweet):

                    if debug: logger.info(f"Respondiendo a {tweet.user.name}")
                    # responderMeme(api, tweet.text.lower(), tweet, buscarFoto(darRandom(4), keywords.keys(), reaccionesDict))

                    if not isEmpty(darUbicacionCarpeta(reaccionesDict, keyword)):

                        responderMeme(
                            api,
                            tweet,
                            darFoto(darRandom(
                                len(crearListaFotos(darUbicacionCarpeta(reaccionesDict, keyword)))),
                                darUbicacionCarpeta(reaccionesDict, keyword),
                                crearListaFotos(darUbicacionCarpeta(reaccionesDict, keyword)))
                        )
                        favear(api,tweet)
                    else: logger.info("El directorio de esa reaccion esta actualmente vacio.\n Por lo tanto se procede a no responder nada.")

            #if "cambiar nombre" in tweet.text.lower():
                #logger.info("me voy a cambiar el nombre..")
                #print(tweet.text.lower().split('cambiar nombre ', 1))
                #try:
                    #api.update_profile('@' + str(tweet.text.lower().split('cambiar nombre ', 1)))
                #except Exception as e:
                    #print(e)

    return new_since_id


def estaFaveado(api, tweet):
    for favorits in api.favorites():
        if tweet.id == favorits.id:
            if debug: logger.info("El tweet {} ya fue faveado, no deberia intentar favearse xd".format(favorits.id))
            return True
    return False
    #vamos a probar si faveandolo nos da  error y si da error asumimos que respondimos
#####podraimos ver de chequear si esta respondido por nosotros el hilo


def isEmpty(path):
    if len(os.listdir(path)) == 0:
        return True
    else: return False


def favear(api, tweet):
    try:
        api.create_favorite(tweet.id)
        if debug: logger.info("se faveo el tweet.")
    except Exception as e:
        if debug: print(e)


def rt(api, tweet):
    try:
        api.retweet(tweet.id)
        if debug: logger.info("Se retweeteo el TW.")
    except Exception as e:
        if debug: print(e)


def seguirLista (api, listaNombres):
    if listaNombres is not None:
        for gente in listaNombres:

            try:
                nombreA_Seguir = gente.replace('@', '')
                api.create_friendship(screen_name = nombreA_Seguir)
                if debug: logger.info("Se Siguio al usuario especificado")
            except Exception as e:
                if debug: print(e)


def seguirCuentaPorTweet(api, tweet):
    try:
        api.create_friendship(tweet.user.screen_name)
        if debug: logger.info("Se siguio al usuario.")
    except Exception as e:
        if debug: print(e)


def darRandom(limite):
    return random.randint(0, limite - 1)


def darUbicacionCarpeta(diccionario, reaccion):
    return diccionario.get(reaccion)



def responderTW (api, tweet, texto):
    try:
        api.update_status(texto, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        if debug: logger.info("Se contesto el Twit correctamente.")
    except Exception as e:
        if debug: print(e)



def crearListaFotos(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


def darFoto(rnd, path, listaFotos):
    return path + listaFotos[rnd]


def responderMeme(api, tweet, src):
    logger.info("se procede a responder con meme")
    #api.create_favorite(tweet.id)

    try:
        api.update_with_media(filename=src, status=" jdsjadja {}".format(numero),
                              in_reply_to_status_id=tweet.id,
                              auto_populate_reply_metadata=True)
        logger.info("----------------------- TWEET ENVIADO -----------------------")



        # api.update_status("@{} chupala ultimo ".format(tweet.user.screen_name), in_reply_to_status_id = tweet.id)
    except Exception as e:
        print(e)
        logger.info("###################### ALGO ANDA RE MAL SI ESTO ESTA PASANDO ######################")

def buscarHashtags(api, query, diccionario):
    logger.info("Buscando hashtags")
    for tweet in api.search(q=query):
        for keyword in diccionario.keys():
            if keyword in tweet.text.lower():
                if not estaFaveado(api, tweet):

                    logger.info(f"Respondiendo HASHTAG a  {tweet.user.name}")
                    # responderMeme(api, tweet.text.lower(), tweet, buscarFoto(darRandom(4), keywords.keys(), reaccionesDict))

                    if not isEmpty(darUbicacionCarpeta(reaccionesDict, keyword)):

                        responderMeme(
                            api,
                            tweet,
                            darFoto(darRandom(
                                len(crearListaFotos(darUbicacionCarpeta(reaccionesDict, keyword)))),
                                darUbicacionCarpeta(reaccionesDict, keyword),
                                crearListaFotos(darUbicacionCarpeta(reaccionesDict, keyword)))
                        )

                        favear(api, tweet)

                    else: logger.info("El directorio de esa reaccion esta actualmente vacio.\n Por lo tanto se procede a no responder nada.")






def main():
    api = create_api()
    for friend in tweepy.Cursor(api.friends).items():
        # Process the friend here
        print(friend.screen_name)
    #print(crearListaFotos(darUbicacionCarpeta(reaccionesDict, "hot")))
    ### esto nos retorna una foto que hay, en teoria elegida al azar.
    #print(darFoto(darRandom(len(crearListaFotos(darUbicacionCarpeta(reaccionesDict, "hot")))),
      #            darUbicacionCarpeta(reaccionesDict, "hot"),
       #           crearListaFotos(darUbicacionCarpeta(reaccionesDict, "hot"))))

    #crearCarpetas(reaccionesDict)

    since_id = 1
    while True:
        print("por ahora hay {} tweets faveados".format(len(api.favorites())))
        #print("por ahora me llamo {}".format(api.me().name))
        since_id = buscarMencion(api, reaccionesDict, since_id)
        buscarHashtags(api, reaccionesDict)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()

#    def follow_followers(api):
#        logger.info("Retrieving and following followers")
#        for follower in tweepy.Cursor(api.followers).items():
#            if not follower.following:
#                logger.info(f"Following {follower.name}")
#                follower.follow()

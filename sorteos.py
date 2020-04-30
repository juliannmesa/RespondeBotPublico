import substring
from respondedor import *
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# devuelve un cursor con los top 'n' tweets que saltaron en la busquda del query
#

listaArrobados = ['@julianmesa5 ', '@BotVieja ']
stringArrobados = ''.join(listaArrobados)

def buscarSorteos (api, query):
    logger.info("Buscando sorteos")
    print(len(api.search(q=query, result_type='recent', count=20)))
    for tweet in api.search(q=query,result_type='recent', count=20):

        if not estaFaveado(api, tweet):
            favear(api, tweet)
            rt(api, tweet)
            seguirCuentaPorTweet(api, tweet)
            arrobarGente(api, tweet, stringArrobados)
            seguirLista(api, genteA_Seguir( tweet))
            time.sleep(40)




def probarFuncionGenteA_Seguir (api, ids):
    for tweet in api.statuses_lookup(ids):
        if debug: print("se encontro un tw con este id")
        #seguirLista(api, genteA_Seguir(api, tweet))
        print(genteA_Seguir(tweet))




def arrobarGente (api, tweet, gente):
        responderTW(api, tweet, gente)

def encontrarCaracter (string, caracter):
    for char in string:
        if char == caracter:
            return True
    return False


##todavia no se como resolverlo
def genteA_Seguir (tweet):
    gente = []
    #no se como lo logre pero funciona asique..
    try:
        palabras = tweet.text.split(' ')
        for palabra in palabras:
            if encontrarCaracter(palabra, '@') and not encontrarCaracter(palabra, ':'):
                logger.info("la palabra {} tiene @".format(palabra))
                gente.append(palabra)

        if debug: logger.info("Gente que se seguira: {}".format(gente))
        #podria pasar los nombres sin @ pero creo q me sirve para mas adelante
        return gente ## es la ListaA_Seguir del tweet
    except Exception as e:
        if debug: print(e)






##no funciuona como espero y al final ya lo solucione
def contarGenteA_Seguir ( tweet):
    countar = 0

    for word in tweet.text:
        if word == '@':
            countar += 1
    return countar





def main():
    api = create_api()


    while True:

        print("Por ahora sigo {} usuarios.".format(len(api.friends_ids(id=api.me().id))))
        buscarSorteos(api, "#CSGOGiveaway")
        #probarFuncionGenteA_Seguir(api, [1251559175387320321, 1251318846146908165, 1251467412362399746, 1252286162804322309, 1252554089814282241])

        print("Durmiendo")
        #time.sleep(120)

        #cuando este listo lo dejo corriendo cada una hora

        time.sleep(3600)

if  __name__  ==  "__main__":
    main()

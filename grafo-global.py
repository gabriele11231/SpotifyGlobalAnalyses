#per lavorare con le api di spotify in python serve installare una libreria
#che si chiama spotipy si installa con questo comando: 
#pip install spotipy --upgrade
#link github libreria: https://github.com/plamere/spotipy

#mail: wohit36816@tourcc.com username: wohit
#password: Ciao123! 
#questo è il profilo creato appositamente per usare le api di spotify
#per lavorare con le api di spotify abbiamo bisogno di due codici
#che otteniamo creando una app dal nostro profilo nell'area sviluppatori

from traceback import print_tb
import networkx as nx
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#----INIZIO----API-SPOTIFY----INIZIO----

#ID della mia applicazione su account spotify
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="afff80ae387b42f8836ae2d2d138343c",client_secret="350216c50b194805b52cb62369d8f136"))

#apro il file playlist che contiene il nome dell'utente e il link alla sua playlist
#metto i dati nella lista people
people = list()
with open('global.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        people.append(row)

#questo è il mio dataset a ogni indice corrisponde una lista di codici ISRC (30 per playlist tranne in rari casi)
dataset = list()

#prendo il link della playlist dalla lista people creata prima
#dal link estraggo l'id della playlist
#dall'id della playlist estraggo tutti i brani da ogni brano estraggo il codice ISRC
for person in people:

    #prendo il link della playlist da person 
    playlist = spotify.playlist(person["Link"])
    #dal link estraggo l'id della playlist
    songs = spotify.playlist_items(playlist["id"]) 

    #insieme ausiliario in cui metto tutti gli ISRC di una singola playlist
    aux = set()

    #estraggo da ogni canzone il codice ISRC e lo inserisco nell'insieme aux
    for i in range (len(songs["items"])):
        aux.add(songs["items"][i]["track"]["external_ids"]["isrc"])
    
    #appendo al mio dataset gli ISRC estratti per ogni playlist
    #indice 0 avrò codici ISRC della playlist dell'utente 0 che in realtà è gia 
    #relazionato con il suo nome
    dataset.append(aux)

#----FINE----API-SPOTIFY----FINE----

#n risulta uguale alla lunghezza del nostro dataset quindi al numero di utenti
#per il quali siamo andati ad estrarre le canzoni dalla playlist
n = len(dataset)

centrality = {}
for x in range (1,n) : 
        affinity = len(dataset[0].intersection(dataset[x]))
        centrality[people[x]["Name"]] = affinity

#print(centrality)

centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)

header = ['Paese', 'Centralità']
with open('global-centrality.csv', 'w+', newline='', encoding='utf-16') as file:
    #writer = csv.DictWriter(file,fieldnames=["Paese","Centralità"])
    writer = csv.writer(file)
    #scrive Paese Centralità nel file csv come intestazione
    writer.writerow(header)
    #scrive id affiancato da nome nel file
    for i in range (len(centrality)) :
        writer.writerow(centrality[i])

grafo = nx.Graph()

for i in range (1,len(people)) :
        #writer.writerow({"Id":i,"Label":people[i]["Name"]})
        grafo.add_node(i,label=people[i]["Name"],latitudine=float(people[i]["latitudine"]),longitudine=float(people[i]["longitudine"]))

#dato che trattiamo le canzoni estratte come insiemi a coppie di utenti
#intersechiamo questi insiemi ed estraiamo il numero di elementi
#ovvero le canzoni che hanno in comune ovvero il loro grado di affinità
for x in range (1,n) : 
    for y in range (x+1,n) :
        #intersezione degli insiemi di canzoni tra utenti
        affinity = len(dataset[x].intersection(dataset[y]))

        #se l'intersezione non è vuota vuol dire che ho un link valido
        #pertanto aggiungo gli id degli utenti e il numero di canzoni
        #che hanno in comune
        if affinity :
            grafo.add_edge(x,y,weight=affinity)
            #edges.append({"Source":x, "Target":y, "Weight":affinity})

nx.write_gexf(grafo,'global.gexf')
nx.write_gpickle(grafo,'global.pkl')










  
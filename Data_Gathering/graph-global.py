#In order to work with Spotify API in Python you have to install a library
#called spotipy, you can install it with this command:
#pip install spotipy --upgrade
#link github for the library: https://github.com/plamere/spotipy

from traceback import print_tb
import networkx as nx
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#----START----API-SPOTIFY----START----

#In order to work with the Spotify API we need two codes (client_id, client_secret)
#we can obtain this codes by creating an application from our spotify
#profile in the developer area
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="",client_secret=""))

#I read the file called global.csv that contains the name of the country(in italian) 
#the link for the Global country playlist on Spotify and the latitute and longitude of the capital city
#the latitude and longitude are useful for the graph visualization in gephi
countries = list()
with open('global.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        countries.append(row)

#This is my dataset, at avery index i have a list of ISRC (50 per playlist except for some less populated countries)
dataset = list()

#I take the link of the playlist from countries
#from the link i will extract the id of the playlist
#from the id i will extract for each song its ISRC
for country in countries:

    playlist = spotify.playlist(country["Link"])
    songs = spotify.playlist_items(playlist["id"]) 

    #aux is a auxiliary set where i put the ISRC from a single playlist
    aux = set()

    for i in range (len(songs["items"])):
        aux.add(songs["items"][i]["track"]["external_ids"]["isrc"])
    
    dataset.append(aux)

#----END----API-SPOTIFY----END----

#The lenght of n is the same of our dataset so the same of the number of countries
n = len(dataset)

#centrality contains how many songs a country have in common with the top 50 global 
#this is called global-centrality (i created it)
centrality = {}
for x in range (1,n) : 
        affinity = len(dataset[0].intersection(dataset[x]))
        centrality[countries[x]["Name"]] = affinity

centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)

header = ['Country', 'Centrality']
with open('global-centrality.csv', 'w+', newline='', encoding='utf-16') as file:

    writer = csv.writer(file)
    writer.writerow(header)
    for i in range (len(centrality)) :
        writer.writerow(centrality[i])

#This is the graph with the affinity of the countries
#so the songs they have in common
#TODO: Use a decente color for the graph visualization also for colorblind
graph = nx.Graph()

for i in range (1,len(countries)) :
        graph.add_node(i,label=countries[i]["Name"],latitudine=float(countries[i]["latitudine"]),longitudine=float(countries[i]["longitudine"]))

for x in range (1,n) : 
    for y in range (x+1,n) :
        affinity = len(dataset[x].intersection(dataset[y]))

        if affinity :
            graph.add_edge(x,y,weight=affinity)

nx.write_gexf(graph,'global.gexf')
nx.write_gpickle(graph,'global.pkl')










  
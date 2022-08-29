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

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="",client_secret=""))

#From global.csv extract the link for the Global country playlist
countries = list()
with open('global.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        countries.append(row)

#Delete the link of the top 50 global
del countries[0]

dataset = list()

#j is just a visual content to understand the progress
j = 0

aux = {}
for country in countries:

    id_playlist = spotify.playlist(country["Link"])["id"]
    songs = spotify.playlist_items(id_playlist)["items"]
    
    #Extract data from the songs
    for i in range (len(songs)):
        print(j)
        isrc = songs[i]["track"]["external_ids"]["isrc"]
        track_uri = songs[i]["track"]["uri"]
        artist_uri = songs[i]["track"]["artists"][0]["uri"]
        genres = spotify.artist(artist_uri)["genres"]

        #Put some data to 0 if Spotify can't provide for a number
        danceability = 0
        try:
            danceability = spotify.audio_features(track_uri)[0]['danceability']
        except:
            pass

        energy = 0
        try:
            energy = spotify.audio_features(track_uri)[0]['energy']
        except:
            pass

        specchiness = 0
        try:
            speechiness = spotify.audio_features(track_uri)[0]['speechiness']
        except:
            pass

        acousticness = 0
        try:
            acousticness = spotify.audio_features(track_uri)[0]['acousticness']
        except:
            pass

        instrumentalness = 0
        try:
            instrumentalness = spotify.audio_features(track_uri)[0]['instrumentalness']
        except:
            pass

        valence = 0
        try:
            valence = spotify.audio_features(track_uri)[0]['valence']
        except:
            pass

        tempo = 0
        try:
            tempo = spotify.audio_features(track_uri)[0]['tempo']
        except:
            pass

        aux[j] = {"country": country["Name"],"isrc":isrc,"uri":track_uri,"genres":genres,"danceability":danceability,"energy":energy,"speechiness":speechiness,"acousticness":acousticness,"instrumentalness":instrumentalness,"valence":valence,"tempo":tempo}
        j = j+1

#Save result
with open('machine-global.csv', 'w+', newline='', encoding='utf-16') as file:
    writer = csv.DictWriter(file,fieldnames=["country","isrc","uri","genres","danceability","energy","speechiness","acousticness","instrumentalness","valence","tempo"])
    writer.writeheader()

    for i in range (j) :
        print(i)
        writer.writerow(aux[i])
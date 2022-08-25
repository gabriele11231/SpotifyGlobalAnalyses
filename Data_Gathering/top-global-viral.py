#In order to work with Spotify API in Python you have to install a library
#called spotipy, you can install it with this command:
#pip install spotipy --upgrade
#link github for the library: https://github.com/plamere/spotipy

from traceback import print_tb
import networkx as nx
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#----INIZIO----API-SPOTIFY----INIZIO----

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="",client_secret=""))

#global.csv and viral.csv contains the name of the country(in italian),
#the link for the Global/Viral country playlist on Spotify and the latitute and longitude of the capital city
#the latitude and longitude are useful for the graph visualization in gephi
countriesg = list()
with open('global.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        countriesg.append(row)
        break

countriesv = list()
with open('viral.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        countriesv.append(row)
        break

auxg = {}
auxv = {}

#----FIRST-TEN-SONGS-FROM-TOP-50-GLOBAL----

id_playlist = spotify.playlist(countriesg[0]["Link"])["id"]
songs = spotify.playlist_items(id_playlist)["items"]

for i in range (10):
    isrc = songs[i]["track"]["external_ids"]["isrc"]

    track_uri = songs[i]["track"]["uri"]
    track_name = songs[i]["track"]["name"]

    artist_name = songs[i]["track"]["artists"][0]["name"]

    album = spotify.album(songs[i]["track"]["album"]["external_urls"]["spotify"])
    data = album["release_date"]
    
    auxg[i] = {"isrc":isrc,"uri":track_uri,"title":track_name,"artist":artist_name,"release-date":data}


#----FIRST-TEN-SONGS-FROM-TOP-50-VIRAL----

id_playlist = spotify.playlist(countriesv[0]["Link"])["id"]
songs = spotify.playlist_items(id_playlist)["items"]
    
for i in range (10):
    isrc = songs[i]["track"]["external_ids"]["isrc"]

    track_uri = songs[i]["track"]["uri"]
    track_name = songs[i]["track"]["name"]

    artist_name = songs[i]["track"]["artists"][0]["name"]

    album = spotify.album(songs[i]["track"]["album"]["external_urls"]["spotify"])
    data = album["release_date"]
    
    auxv[i] = {"isrc":isrc,"uri":track_uri,"title":track_name,"artist":artist_name,"release-date":data}


#----SAVE-RESULT----

with open('10-global.csv', 'w+', newline='', encoding='utf-16') as file:
    writer = csv.DictWriter(file,fieldnames=["isrc","uri","title","artist","release-date"])
    writer.writeheader()

    for i in range (10) :
        writer.writerow(auxg[i])


with open('10-viral.csv', 'w+', newline='', encoding='utf-16') as file:
    writer = csv.DictWriter(file,fieldnames=["isrc","uri","title","artist","release-date"])
    writer.writeheader()

    for i in range (10) :
        writer.writerow(auxv[i])











  
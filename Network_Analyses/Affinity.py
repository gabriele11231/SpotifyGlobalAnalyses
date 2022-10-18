import warnings
warnings.filterwarnings("ignore")

import networkx as nx
import numpy as np
import pandas as pd
import pathlib
import csv
import json
from Geographic_zone import fast_geographic_zone
from PIL import ImageColor

#Number of day for which the data has been collected
day = 15

affinity = dict()
for z in range(1, day+1):

    data_path = pathlib.Path(__file__).parent.absolute().parent
    graph = pd.read_pickle(data_path.joinpath(f'Dataset/global-pkl/global{z}.pkl'))     

    edges = list(graph.edges.data("weight"))

    #Summarize of all affinity day per day
    for i in (edges):
        key = str(i[0])+" "+str(i[1])

        try:   
            affinity[key] = affinity[key] + i[2]
        except:
            affinity[key] = 0

    #Ricreate the edge list, the weight is the total affinity
    edges = list()
    mean_affinity = 0
    for i in affinity:
      vertex = i.split(" ")
      mean_affinity = mean_affinity + affinity[i]
      aux = int(vertex[0]),int(vertex[1]),affinity[i]
      edges.append(aux)


#----CREATE-THE-AFFINITY-GRAPH-TOP----
graph = nx.Graph()
graph_min = nx.Graph()
countries = list()
mean_affinity = mean_affinity / len(edges)

data_path = pathlib.Path(__file__).parent.absolute().parent
with open(data_path.joinpath('Data_Gathering/global.csv'), 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        countries.append(row)

zone = fast_geographic_zone()

for i in range (1,len(countries)) :
    rgb = zone.color_zone(zone.find_zone(countries[i]["Name"]))
    graph.add_node(i,label=countries[i]["Name"],latitudine=float(countries[i]["latitudine"]),longitudine=float(countries[i]["longitudine"]),color=rgb)
    graph_min.add_node(i,label=countries[i]["Name"],latitudine=float(countries[i]["latitudine"]),longitudine=float(countries[i]["longitudine"]),color=rgb)


for x in (edges):
    if x[2] > mean_affinity:
        graph.add_edge(x[0],x[1],weight=x[2])

edges_min = (sorted(edges, key=lambda x:x[2]))[:100]
for x in(edges_min):
    graph_min.add_edge(x[0],x[1],weight=(day*50)-x[2])

data_path = pathlib.Path(__file__).parent.absolute().parent
nx.write_gexf(graph,data_path.joinpath('Network_Analyses/top_affinity.gexf'))
nx.write_gexf(graph_min,data_path.joinpath('Network_Analyses/top_min_affinity.gexf'))


affinity = dict()
for z in range(1, day+1):

    data_path = pathlib.Path(__file__).parent.absolute().parent
    graph = pd.read_pickle(data_path.joinpath(f'Dataset/viral-pkl/viral{z}.pkl'))     

    edges = list(graph.edges.data("weight"))

    #Summarize of all affinity day per day
    for i in (edges):
        key = str(i[0])+" "+str(i[1])

        try:   
            affinity[key] = affinity[key] + i[2]
        except:
            affinity[key] = 0

    #Ricreate the edge list, the weight is the total affinity
    edges = list()
    mean_affinity = 0
    for i in affinity:
      vertex = i.split(" ")
      mean_affinity = mean_affinity + affinity[i]
      aux = int(vertex[0]),int(vertex[1]),affinity[i]
      edges.append(aux)


#----CREATE-THE-AFFINITY-GRAPH-VIRAL----
graph = nx.Graph()
graph_min = nx.Graph()
countries = list()
mean_affinity = mean_affinity / len(edges)

data_path = pathlib.Path(__file__).parent.absolute().parent
with open(data_path.joinpath('Data_Gathering/viral.csv'), 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        countries.append(row)

zone = fast_geographic_zone()

for i in range (1,len(countries)) :
    print(countries[i]["Name"])
    rgb = zone.color_zone(zone.find_zone(countries[i]["Name"]))
    graph.add_node(i,label=countries[i]["Name"],latitudine=float(countries[i]["latitudine"]),longitudine=float(countries[i]["longitudine"]),color=rgb)
    graph_min.add_node(i,label=countries[i]["Name"],latitudine=float(countries[i]["latitudine"]),longitudine=float(countries[i]["longitudine"]),color=rgb)

for x in (edges):
    if x[2] > mean_affinity:
        graph.add_edge(x[0],x[1],weight=x[2])

edges_min = (sorted(edges, key=lambda x:x[2]))[:100]
for x in(edges_min):
    graph_min.add_edge(x[0],x[1],weight=(day*50)-x[2])

data_path = pathlib.Path(__file__).parent.absolute().parent
nx.write_gexf(graph,data_path.joinpath('Network_Analyses/viral_affinity.gexf'))
nx.write_gexf(graph_min,data_path.joinpath('Network_Analyses/viral_min_affinity.gexf'))


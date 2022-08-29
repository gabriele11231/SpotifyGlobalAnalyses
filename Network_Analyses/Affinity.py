import networkx as nx
import numpy as np
import pandas as pd
import pathlib
import csv
import json
from Geographic_zone import fast_geographic_zone

affinity = dict()
for z in range(1, 16):

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
    for i in affinity:
      vertex = i.split(" ")
      aux = int(vertex[0]),int(vertex[1]),affinity[i]
      edges.append(aux)


#----CREATE-THE-AFFINITY-GRAPH----
graph = nx.Graph()
countries = list()
data_path = pathlib.Path(__file__).parent.absolute().parent

with open(data_path.joinpath('Data_Gathering/global.csv'), 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        countries.append(row)

zone = fast_geographic_zone()

for i in range (1,len(countries)) :
    graph.add_node(i,label=countries[i]["Name"],latitudine=float(countries[i]["latitudine"]),longitudine=float(countries[i]["longitudine"]),color=zone.color_zone(zone.find_zone(countries[i]["Name"])))

for x in (edges):
        graph.add_edge(x[0],x[1],weight=x[2])

data_path = pathlib.Path(__file__).parent.absolute().parent
nx.write_gexf(graph,data_path.joinpath('Network_Analyses/global_affinity.gefx'))

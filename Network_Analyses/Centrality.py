from turtle import color
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


countries = list()
data_path = pathlib.Path(__file__).parent.absolute().parent
with open(data_path.joinpath('Data_Gathering/global.csv'), 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        countries.append(row)


#Number of day for which the data has been collected
day = 15

#----EIGEN-TOP----
eigen = dict()
j = 0
for z in range(1, day+1):

    data_path = pathlib.Path(__file__).parent.absolute().parent
    graph = pd.read_pickle(data_path.joinpath(f'Dataset/global-pkl/global{z}.pkl'))     

    eigen_con_pesi = nx.eigenvector_centrality(graph, weight='weight')

    if z == 1:
        for i in eigen_con_pesi:
            eigen[i] = eigen_con_pesi[i]
    else:
        for i in eigen_con_pesi:
            eigen[i] = eigen_con_pesi[i] + eigen[i]

eigen = dict(sorted(eigen.items(), key=lambda item: item[1] ,reverse=True))
j = 0

print("TOP")
for i in eigen:
    j = j + 1
    if (j >= 1 and j <= 5):
        print("MAX ",countries[i]["Name"]," ",(eigen[i])/(day))
    if (j >= 68):
        print("MIN ",countries[i]["Name"]," ",(eigen[i])/(day))


#----EIGEN-VIRAL----
eigen = dict()
j = 0
for z in range(1, day+1):

    data_path = pathlib.Path(__file__).parent.absolute().parent
    graph = pd.read_pickle(data_path.joinpath(f'Dataset/viral-pkl/viral{z}.pkl'))     

    eigen_con_pesi = nx.eigenvector_centrality(graph, weight='weight')

    if z == 1:
        for i in eigen_con_pesi:
            eigen[i] = eigen_con_pesi[i]
    else:
        for i in eigen_con_pesi:
            eigen[i] = eigen_con_pesi[i] + eigen[i]

eigen = dict(sorted(eigen.items(), key=lambda item: item[1] ,reverse=True))
j = 0

print("\nVIRAL")
for i in eigen:
    j = j + 1
    if (j >= 1 and j <= 5):
        print("MAX ",countries[i]["Name"]," ",(eigen[i])/(day))
    if (j >= 68):
        print("MIN ",countries[i]["Name"]," ",(eigen[i])/(day))
import networkx as nx
import numpy as np
import pandas as pd
from pathlib import Path, PureWindowsPath

#----DEGREE-ANALYSES-VIRAL----
viral_dict = dict()
mean_degree_l = list()
max_country_l = list()
max_degree_l = list()
min_country_l = list()
min_degree_l = list()
for z in range(1, 16):

    data_path = f'Dataset/viral-pkl/viral{z}.pkl'
    grafo = pd.read_pickle(Path(data_path))

    degree = dict(grafo.degree(weight='weight'))
    campione_grado = list(degree.values())
    mean_degree_l.append(np.mean(list(degree.values())))

    max_degree = max(degree.values())
    max_country = ''
    for k, v in grafo.degree(weight='weight'):
        if v == max_degree:
            max_country = k
            break
    max_country_l.append(grafo.nodes.data("label")[max_country])
    max_degree_l.append(max_degree)


    min_degree = min(degree.values())
    min_country = ''
    for k, v in grafo.degree(weight='weight'):
        if v == min_degree:
            min_country = k
            break
    min_country_l.append(grafo.nodes.data("label")[min_country])
    min_degree_l.append(min_degree)

viral_dict['mean_degree'] = mean_degree_l
viral_dict['max_country'] = max_country_l
viral_dict['max_degree'] = max_degree_l
viral_dict['min_country'] = min_country_l
viral_dict['min_degree'] = min_degree_l


#----DEGREE-ANALYSES-GLOBAL----
global_dict = dict()
mean_degree_l = list()
max_country_l = list()
max_degree_l = list()
min_country_l = list()
min_degree_l = list()
for z in range(1, 16):

    data_path = f'Dataset/global-pkl/global{z}.pkl'
    grafo = pd.read_pickle(Path(data_path))

    degree = dict(grafo.degree(weight='weight'))
    campione_grado = list(degree.values())
    mean_degree_l.append(np.mean(list(degree.values())))

    max_degree = max(degree.values())
    max_country = ''
    for k, v in grafo.degree(weight='weight'):
        if v == max_degree:
            max_country = k
            break
    max_country_l.append(grafo.nodes.data("label")[max_country])
    max_degree_l.append(max_degree)

    min_degree = min(degree.values())
    min_country = ''
    for k, v in grafo.degree(weight='weight'):
        if v == min_degree:
            min_country = k
            break
    min_country_l.append(grafo.nodes.data("label")[min_country])
    min_degree_l.append(min_degree)

global_dict['mean_degree'] = mean_degree_l
global_dict['max_country'] = max_country_l
global_dict['max_degree'] = max_degree_l
global_dict['min_country'] = min_country_l
global_dict['min_degree'] = min_degree_l

print(viral_dict)
print(global_dict)
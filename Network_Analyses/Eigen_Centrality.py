from unicodedata import name
import networkx as nx
import pandas as pd
import pathlib
import csv
import plotly.express as px
import pycountry


countries = list()
data_path = pathlib.Path(__file__).parent.absolute().parent
with open(data_path.joinpath('Data_Gathering/global.csv'), 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        countries.append(row)


#Number of day for which the data has been collected
day = 15

df = pd.DataFrame(data=[country['Name'] for country in countries][1:],columns=['Name'])
countr = {}
for country in pycountry.countries:
    countr[country.name.split(',')[0]] = country.alpha_3
df['iso'] = [countr[country] for country in df['Name']]

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

eigen_top = dict(sorted(eigen.items(), key=lambda item: item[1] ,reverse=False)).values()
df['eigen_top'] = eigen_top
fig_top = px.choropleth(
    df, 
    locations='iso', 
    color='eigen_top',
    projection='natural earth'
    
)
fig_top.update_geos(
    visible=False, 
    resolution=50,
    showcountries=True, 
    countrycolor="White",
    bgcolor='#191414'   
)
fig_top.show()
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


eigen_viral = dict(sorted(eigen.items(), key=lambda item: item[0] ,reverse=False)).values()
df['eigen_viral'] = eigen_viral
fig_viral = px.choropleth(
    df, 
    locations='iso', 
    color='eigen_viral',#eigenvector == autovettore
    projection='natural earth'
    
)
fig_viral.update_geos(
    visible=False, 
    resolution=50,
    showcountries=True, 
    countrycolor="White",
    bgcolor='#191414'   
)
fig_viral.write_image("eigen_viral.png")
fig_viral.show()
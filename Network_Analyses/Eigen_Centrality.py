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

eigen_top = eigen.values()
df['eigen_top'] = eigen_top
fig_top = px.choropleth(
    df, 
    locations='iso', 
    color='eigen_top',
    projection='natural earth',
    color_continuous_scale=['#ffffd9','#edf8b1','#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8','#253494','#081d58'] ,
    scope = 'world',
    labels= {'eigen_top':'Valore eigenvector centrality Top'}
)


fig_top.update_geos(
    visible=False, 
    resolution=50,
    showcountries=True, 
    countrycolor="White",
    bgcolor='#1c1e21',   
)
fig_top.update_layout(
    font_size = 18,
    font_color = 'White',
    paper_bgcolor = "#1c1e21",
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


eigen_viral = eigen.values()
df['eigen_viral'] = eigen_viral
fig_viral = px.choropleth(
    df, 
    locations='iso', 
    color='eigen_viral',#eigenvector == autovettore,
    color_continuous_scale=['#ffffd9','#edf8b1','#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8','#253494','#081d58'] ,
    projection='natural earth',
    scope = 'world',
    labels= {'eigen_viral':'Valore eigenvector centrality Viral'}
    
)
fig_viral.update_geos(
    visible=False, 
    resolution=50,
    showcountries=True, 
    countrycolor="White",
    bgcolor='#1c1e21',
)
fig_viral.update_layout(
    font_size = 18,
    font_color = 'White',   
    paper_bgcolor = "#1c1e21",

)

fig_viral.show()
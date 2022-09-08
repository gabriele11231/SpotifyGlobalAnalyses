import csv
import pathlib
import pycountry
import pandas as pd
import plotly.express as px
#https://extendsclass.com/merge-csv.html
#use this file in order to merge all the global-centrality file


centrality = dict()
data_path = pathlib.Path(__file__).parent.absolute().parent
with open(data_path.joinpath('Data_Gathering/global.csv'), 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['Name'] != "Global":
            centrality[row['Name']] = 0


#----TOP----

with open(data_path.joinpath(f'Dataset/global-centrality/global-centrality-merged.csv'), 'r', encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        centrality[row['Country']] = centrality[row['Country']] + int(row['Centrality'])

#global-centrality of top
centrality_top = centrality.values()
countries = list()
data_path = pathlib.Path(__file__).parent.absolute().parent
with open(data_path.joinpath('Data_Gathering/global.csv'), 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        countries.append(row)
df = pd.DataFrame(data=[country['Name'] for country in countries][1:],columns=['Name'])
countr = {}
for country in pycountry.countries:
    countr[country.name.split(',')[0]] = country.alpha_3
df['iso'] = [countr[country] for country in df['Name']]
df['centrality_top'] = centrality_top

fig_top = px.choropleth(
    df, 
    locations='iso', 
    color='centrality_top',
    projection='natural earth',
    color_continuous_scale=['#ffffd9','#edf8b1','#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8','#253494','#081d58'] ,
    scope = 'world',
    labels= {'centrality_top':'Global Centrality Top'}
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


#----VIRAL----
for x in centrality:
    centrality[x] = 0

with open(data_path.joinpath(f'Dataset/viral-centrality/viral-centrality-merged.csv'), 'r', encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        centrality[row['Country']] = centrality[row['Country']] + int(row['Centrality'])

#global-centrality of viral
centrality_viral = centrality.values()
df['centrality_viral'] = centrality_viral


fig_viral = px.choropleth(
    df, 
    locations='iso', 
    color='centrality_viral',
    projection='natural earth',
    color_continuous_scale=['#ffffd9','#edf8b1','#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8','#253494','#081d58'] ,
    scope = 'world',
    labels= {'centrality_viral':'Global Centrality Viral'}
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

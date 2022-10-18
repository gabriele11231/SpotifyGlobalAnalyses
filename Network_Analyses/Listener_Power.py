from babel import Locale
import pycountry
import babel.languages as bl
import pathlib
import pandas as pd
import csv
import plotly.express as px



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
    countr[country.name.split(',')[0]] = country.alpha_2
df['iso'] = [countr[country] for country in df['Name']]
df['centrality_top'] = centrality_top
temp = dict()




for i in range(len(df)):
    j = 0 
    try:
        Locale(bl.get_official_languages(df['iso'].loc[i],de_facto=True)[0]).english_name
    except:
        j = 1
    if temp.get(Locale(bl.get_official_languages(df['iso'].loc[i],de_facto=True)[j]).english_name) == None:
        temp[Locale(bl.get_official_languages(df['iso'].loc[i],de_facto=True)[j]).english_name] = df.loc[i]['centrality_top']
    else:
        temp[Locale(bl.get_official_languages(df['iso'].loc[i],de_facto=True)[j]).english_name] = temp.get(Locale(bl.get_official_languages(df.loc[i]['iso'],de_facto=True)[j]).english_name) + df.loc[i]['centrality_top']
centrality_lang = {k:[v] for k,v in temp.items()}
del(temp)
df_lang = pd.DataFrame.from_dict(
    centrality_lang,orient='index',
    columns=['Centrality'],
)

print(df_lang)

fig = px.bar(
    df_lang,
    x=df_lang.index,
    y= df_lang.columns,
    color=df_lang.index,
    labels={
        "index": "Contries",
        "value": "Centrality",
    },
    color_discrete_sequence= ['#8aa023','#5eeed8','#2b9ce1','#ed9500','#c77de9','#d7edb5','#1421a1','#e05a77','#c977c5','#bcc1d4','#cd39d8','#5562d9','#e87eb2','#ab2072','#e1b752'],
)
fig.update_layout( 
    xaxis={'categoryorder':'total descending'},
    showlegend = False,
)

fig.show()
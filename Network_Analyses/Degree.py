import networkx as nx
import numpy as np
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pathlib
from Geographic_zone import fast_geographic_zone

#In order to use plotly you have to install it with the command pip install plotly

#----DEGREE-ANALYSES-VIRAL----
viral_dict = dict()
mean_degree_l = list()
max_country_l = list()
max_degree_l = list()
min_country_l = list()
min_degree_l = list()
for z in range(1, 16):

    data_path = pathlib.Path(__file__).parent.absolute().parent
    grafo = pd.read_pickle(data_path.joinpath(f'Dataset/viral-pkl/viral{z}.pkl'))

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
    
    data_path = pathlib.Path(__file__).parent.absolute().parent
    grafo = pd.read_pickle(data_path.joinpath(f'Dataset/global-pkl/global{z}.pkl'))
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

df  = pd.DataFrame.from_dict(global_dict)


fig_global = go.Figure()


#creation of the graphic,is divided in l and for creating a dotted line
#fig is composed with the mean,maximum and mininum plot combined
#color palette can be found here 
#https://davidmathlogic.com/colorblind/#%23E66100-%235D3A9B-%2343a28e-%23b1606a-%23ccac51-%234933d4-%23df454f-%23960bd5-%23178e18-%23d1802f-%23aabfc2-%23a24af3-%235b8110-%231552dd-%23252852-%23a5a1e8-%238aa023-%235eeed8-%232b9ce1-%23ed9500-%23c77de9-%23d7edb5-%231421a1-%23e05a77-%23c977c5-%23bcc1d4-%23cd39d8-%235562d9-%23e87eb2-%23ab2072-%23e1b752-%231fa5c0
fig_s_max = px.scatter(
    df,
    x=[i+1 for i in range(15)],
    y="max_degree",
    color= "max_country",
    color_discrete_sequence = ['#e66100','#5d3a9b','#43a28e','#b1606a','#ccac51','#4933d4','#df454f','#960bd5','#178e18','#d1802f','#aabfc2','#a24af3','#5b8110','#1552dd','#a5a1e8']
)

fig_l_max = (px.line(
        df,
        x=[i+1 for i in range(15)],
        y="max_degree"
    )
)

fig_s_min = px.scatter(
    df,
    x=[i+1 for i in range(15)],
    y="min_degree",
    color= "min_country",
    color_discrete_sequence = ['#8aa023','#5eeed8','#2b9ce1','#ed9500','#c77de9','#d7edb5','#1421a1','#e05a77','#c977c5','#bcc1d4','#cd39d8','#5562d9','#e87eb2','#ab2072','#e1b752']
)

fig_l_min = (px.line(
        df,
        x=[i+1 for i in range(15)],
        y="min_degree"
    )
)

fig_s_mean = px.scatter(
    df,
    x=[i+1 for i in range(15)],
    y="mean_degree",
    color_discrete_sequence=['#1fa5c0']
)

fig_s_mean.update_traces(
    selector=dict(mode='markers'),
)    

fig_l_mean = (px.line(
        df,
        x=[i+1 for i in range(15)],
        y="mean_degree",
    )
)

fig_s_mean['data'][0]['showlegend']=True  # type: ignore
fig_s_mean['data'][0]['name']='Media'  # type: ignore

fig_global = go.Figure(data = fig_l_min.data + fig_s_min.data  + fig_l_max.data + fig_s_max.data + fig_l_mean.data + fig_s_mean.data)  # type: ignore

fig_global.update_layout(
    xaxis_title = 'Days',
    title_font_family="Times New Roman",
    plot_bgcolor = 'white'
)

fig_global.update_traces(
    marker=dict(
        size = 15
    )
)


fig_global.update_xaxes(
    showgrid=False,
    dtick = 1,
)

fig_global.update_yaxes(
    showgrid=True,
    dtick = 50,
    gridwidth=1, 
    gridcolor= '#e0e0e0',
    zeroline = True,
    zerolinecolor = '#e0e0e0',
    zerolinewidth  = 1
)

fig_global.update_traces(line_color='#252852', line_width=1)
fig_global.update_layout(
    width = 2160,
    height = 1080,
)
fig_global.write_image("global.svg")

fig_global.show()




fig_viral = go.Figure()
df_viral  = pd.DataFrame.from_dict(viral_dict)


#creation of the graphic,is divided in l and for creating a dotted line
#fig is composed with the mean,maximum and mininum plot combined
#color palette can be found here 
#https://davidmathlogic.com/colorblind/#%23E66100-%235D3A9B-%2343a28e-%23b1606a-%23ccac51-%234933d4-%23df454f-%23960bd5-%23178e18-%23d1802f-%23aabfc2-%23a24af3-%235b8110-%231552dd-%23252852-%23a5a1e8-%238aa023-%235eeed8-%232b9ce1-%23ed9500-%23c77de9-%23d7edb5-%231421a1-%23e05a77-%23c977c5-%23bcc1d4-%23cd39d8-%235562d9-%23e87eb2-%23ab2072-%23e1b752-%231fa5c0
fig_s_max = px.scatter(
    df_viral,
    x=[i+1 for i in range(15)],
    y="max_degree",
    color= "max_country",
    color_discrete_sequence = ['#e66100','#5d3a9b','#43a28e','#b1606a','#ccac51','#4933d4','#df454f','#960bd5','#178e18','#d1802f','#aabfc2','#a24af3','#5b8110','#1552dd','#a5a1e8']
)

fig_l_max = (px.line(
        df_viral,
        x=[i+1 for i in range(15)],
        y="max_degree"
    )
)

fig_s_min = px.scatter(
    df_viral,
    x=[i+1 for i in range(15)],
    y="min_degree",
    color= "min_country",
    color_discrete_sequence = ['#8aa023','#5eeed8','#2b9ce1','#ed9500','#c77de9','#d7edb5','#1421a1','#e05a77','#c977c5','#bcc1d4','#cd39d8','#5562d9','#e87eb2','#ab2072','#e1b752']
)

fig_l_min = (px.line(
        df_viral,
        x=[i+1 for i in range(15)],
        y="min_degree"
    )
)

fig_s_mean = px.scatter(
    df_viral,
    x=[i+1 for i in range(15)],
    y="mean_degree",
    color_discrete_sequence=['#1fa5c0']
)

fig_s_mean.update_traces(
    selector=dict(mode='markers'),
)    

fig_l_mean = (px.line(
        df_viral,
        x=[i+1 for i in range(15)],
        y="mean_degree",
    )
)

fig_s_mean['data'][0]['showlegend']=True  # type: ignore
fig_s_mean['data'][0]['name']='Media'  # type: ignore

fig_viral = go.Figure(data = fig_l_min.data + fig_s_min.data  + fig_l_max.data + fig_s_max.data + fig_l_mean.data + fig_s_mean.data)  # type: ignore

fig_viral.update_layout(
    xaxis_title = 'Days',
    title_font_family="Times New Roman",
    plot_bgcolor = 'white'
)

fig_viral.update_traces(
    marker=dict(
        size = 15
    )
)

fig_viral.update_xaxes(
    showgrid=False,
    dtick = 1,
)

fig_viral.update_yaxes(
    showgrid=True,
    dtick = 50,
    gridwidth=1, 
    gridcolor= '#e0e0e0',
    zeroline = True,
    zerolinecolor = '#e0e0e0',
    zerolinewidth  = 1
)

fig_viral.update_traces(line_color='#252852', line_width=1)
fig_viral.update_layout(
    width = 2160,
    height = 1080,
)
fig_viral.write_image("viral.svg")

fig_viral.show()



#by continents
fast = fast_geographic_zone()
fig_global_zone = go.Figure()


print(df['max_country'])

for i in range(len(df)):
    df.at[i,'max_country'] = fast.find_zone(df.at[i,'max_country'])
    df.at[i,'min_country'] = fast.find_zone(df.at[i,'min_country'])


print(df['max_country'])

color_max = []
color_min = []
for i in range(len(df)):
    if not color_max.__contains__(fast.color_zone(df.at[i,'max_country'])):
        color_max.append(fast.color_zone(df.at[i,'max_country']))
    if not color_min.__contains__(fast.color_zone(df.at[i,'min_country'])):
        color_min.append(fast.color_zone(df.at[i,'min_country']))


fig_s_max = px.scatter(
    df,
    x=[i+1 for i in range(15)],
    y="max_degree",
    color= "max_country",
    color_discrete_sequence = color_max,
)

fig_l_max = (px.line(
        df,
        x=[i+1 for i in range(15)],
        y="max_degree"
    )
)

fig_s_min = px.scatter(
    df,
    x=[i+1 for i in range(15)],
    y="min_degree",
    color= "min_country",
    color_discrete_sequence = color_min
)

fig_l_min = (px.line(
        df,
        x=[i+1 for i in range(15)],
        y="min_degree"
    )
)



fig_s_mean = px.scatter(
    df,
    x=[i+1 for i in range(15)],
    y="mean_degree",
    color_discrete_sequence=['#1fa5c0']
)

fig_s_mean.update_traces(
    selector=dict(mode='markers'),
)    

fig_l_mean = (px.line(
        df,
        x=[i+1 for i in range(15)],
        y="mean_degree",
    )
)

fig_s_mean['data'][0]['showlegend']=True  # type: ignore
fig_s_mean['data'][0]['name']='Media'  # type: ignore

fig_global_zone = go.Figure(data = fig_l_min.data + fig_s_min.data  + fig_l_max.data + fig_s_max.data + fig_l_mean.data + fig_s_mean.data)  # type: ignore

fig_global_zone.update_layout(
    xaxis_title = 'Days',
    title_font_family="Times New Roman",
    plot_bgcolor = 'white'
)

fig_global_zone.update_traces(
    marker=dict(
        size = 15
    )
)


fig_global_zone.update_xaxes(
    showgrid=False,
    dtick = 1,
)

fig_global_zone.update_yaxes(
    showgrid=True,
    dtick = 50,
    gridwidth=1, 
    gridcolor= '#e0e0e0',
    zeroline = True,
    zerolinecolor = '#e0e0e0',
    zerolinewidth  = 1
)

fig_global_zone.update_traces(line_color='#252852', line_width=1)

already = []
for trace in fig_global_zone['data']:
    if(already.__contains__(trace['name'])):  # type: ignore
        trace['showlegend'] = False  # type: ignore
    else:
        already.append(trace['name'])  # type: ignore

fig_global_zone.update_layout(
    width = 2160,
    height = 1080,
)
fig_global_zone.write_image("global_zone.svg")

fig_global_zone.show()


fig_viral_zone = go.Figure()
df_viral  = pd.DataFrame.from_dict(viral_dict)

for i in range(len(df)):
    df_viral.at[i,'max_country'] = fast.find_zone(df_viral.at[i,'max_country'])
    df_viral.at[i,'min_country'] = fast.find_zone(df_viral.at[i,'min_country'])



color_max_viral = []
color_min_viral = []
for i in range(len(df['max_country'])):
    if not color_max_viral.__contains__(fast.color_zone(df_viral.at[i,'max_country'])):
        color_max_viral.append(fast.color_zone(df_viral.at[i,'max_country']))
    if not color_min_viral.__contains__(fast.color_zone(df_viral.at[i,'min_country'])):
        color_min_viral.append(fast.color_zone(df_viral.at[i,'min_country']))

fig_s_max = px.scatter(
    df_viral,
    x=[i+1 for i in range(15)],
    y="max_degree",
    color= "max_country",
    color_discrete_sequence = color_max_viral,
)


fig_l_max.update_layout(legend_title_text='Trend')

fig_l_max = (px.line(
        df_viral,
        x=[i+1 for i in range(15)],
        y="max_degree"
    )
)

fig_s_min = px.scatter(
    df_viral,
    x=[i+1 for i in range(15)],
    y="min_degree",
    color= "min_country",
    color_discrete_sequence = color_min_viral,

)



fig_l_min = (px.line(
        df_viral,
        x=[i+1 for i in range(15)],
        y="min_degree"
    )
)

fig_s_mean = px.scatter(
    df_viral,
    x=[i+1 for i in range(15)],
    y="mean_degree",
    color_discrete_sequence=['#1fa5c0']
)

fig_s_mean.update_traces(
    selector=dict(mode='markers'),
)    

fig_l_mean = (px.line(
        df_viral,
        x=[i+1 for i in range(15)],
        y="mean_degree",
    )
)

fig_s_mean['data'][0]['showlegend']=True  # type: ignore
fig_s_mean['data'][0]['name']='Media'  # type: ignore

fig_viral_zone = go.Figure(data = fig_l_min.data + fig_s_min.data  + fig_l_max.data + fig_s_max.data + fig_l_mean.data + fig_s_mean.data)  # type: ignore
fig_viral_zone.update_layout(
    xaxis_title = 'Days',
    title_font_family="Times New Roman",
    plot_bgcolor = 'white'
)

fig_viral_zone.update_traces(
    marker=dict(
        size = 15
    )
)

fig_viral_zone.update_xaxes(
    showgrid=False,
    dtick = 1,
)

fig_viral_zone.update_yaxes(
    showgrid=True,
    dtick = 50,
    gridwidth=1, 
    gridcolor= '#e0e0e0',
    zeroline = True,
    zerolinecolor = '#e0e0e0',
    zerolinewidth  = 1
)

already = []
for trace in fig_viral_zone['data']:
    if(already.__contains__(trace['name'])):  # type: ignore
        trace['showlegend'] = False  # type: ignore
    else:
        already.append(trace['name'])  # type: ignore
fig_viral_zone.update_layout(
    width = 2160,
    height = 1080,
)
fig_viral_zone.update_traces(line_color='#252852', line_width=1)
fig_viral_zone.write_image("viral_zone.svg")

fig_viral_zone.show()

fig_line_max_viral = px.bar(
    df_viral,
    x = [x+1 for x in range(15)],
    y = df_viral['max_degree'],
    color_discrete_sequence=['#998ec3'],
)
fig_line_max_viral['data'][0]['showlegend']=True  # type: ignore
fig_line_max_viral['data'][0]['name']='Grado Massimo Viral'  # type: ignore

fig_line_max_global = px.bar(
    df,
    x = [x+1 for x in range(15)],
    y = df['max_degree'],
    color_discrete_sequence=['#f1a340'],
)
fig_line_max_global['data'][0]['showlegend']=True  # type: ignore
fig_line_max_global['data'][0]['name']='Grado Massimo Top'  # type: ignore




fig_line = go.Figure(fig_line_max_viral.data+fig_line_max_global.data)  # type: ignore
fig_line.update_xaxes(
    showgrid=False,
    dtick = 1,
)

fig_line.update_yaxes(
    showgrid=True,
    dtick = 50,
    gridwidth=1, 
    gridcolor= '#e0e0e0',
    zeroline = True,
    zerolinecolor = '#e0e0e0',
    zerolinewidth  = 1
)

fig_line.update_layout(
    barmode = 'overlay'
)
fig_line.show()

fig_line_min_viral = px.bar(
    df_viral,
    x = [x+1 for x in range(15)],
    y = df_viral['min_degree'],
    color_discrete_sequence=['#998ec3'],
)
fig_line_min_viral['data'][0]['showlegend']=True  # type: ignore
fig_line_min_viral['data'][0]['name']='Grado Minimo Viral'  # type: ignore

fig_line_min_global = px.bar(
    df,
    x = [x+1 for x in range(15)],
    y = df['min_degree'],
    color_discrete_sequence=['#f1a340'],
)
fig_line_min_global['data'][0]['showlegend']=True  # type: ignore
fig_line_min_global['data'][0]['name']='Grado Minimo Top'  # type: ignore


fig_line = go.Figure(fig_line_min_viral.data+fig_line_min_global.data)  # type: ignore
fig_line.update_xaxes(
    showgrid=False,
    dtick = 1,
)

fig_line.update_yaxes(
    showgrid=True,
    dtick = 50,
    gridwidth=1, 
    gridcolor= '#e0e0e0',
    zeroline = True,
    zerolinecolor = '#e0e0e0',
    zerolinewidth  = 1
)

fig_line.update_layout(
    barmode = 'overlay'
)
fig_line.show()

fig_line_mean_viral = px.bar(
    df_viral,
    x = [x+1 for x in range(15)],
    y = df_viral['mean_degree'],
    color_discrete_sequence=['#998ec3'],
)


fig_line_mean_viral['data'][0]['showlegend']=True  # type: ignore
fig_line_mean_viral['data'][0]['name']='Grado Medio Viral'  # type: ignore

fig_line_mean_global = px.bar(
    df,
    x = [x+1 for x in range(15)],
    y = df['mean_degree'],
    color_discrete_sequence=['#f1a340'],
) 
fig_line_mean_global['data'][0]['showlegend']=True  # type: ignore
fig_line_mean_global['data'][0]['name']='Grado Medio Top'  # type: ignore


fig_line = go.Figure(fig_line_mean_viral.data+fig_line_mean_global.data)  # type: ignore
fig_line.update_xaxes(
    showgrid=False,
    dtick = 1,
)

fig_line.update_yaxes(
    showgrid=True,
    dtick = 50,
    gridwidth=1, 
    gridcolor= '#e0e0e0',
    zeroline = True,
    zerolinecolor = '#e0e0e0',
    zerolinewidth  = 1
)

fig_line.update_layout(
    barmode = 'overlay'
)
fig_line.show()


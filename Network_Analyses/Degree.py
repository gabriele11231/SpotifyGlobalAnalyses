from cProfile import label
import networkx as nx
import numpy as np
import pandas as pd
from pathlib import Path, PureWindowsPath
import plotly.graph_objects as go
import plotly.express as px
import pathlib

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

fig_s_mean['data'][0]['showlegend']=True
fig_s_mean['data'][0]['name']='Mean'

fig_global = go.Figure(data = fig_l_min.data + fig_s_min.data  + fig_l_max.data + fig_s_max.data + fig_l_mean.data + fig_s_mean.data)

fig_global.update_layout(
    xaxis_title = 'Days',
    title_font_family="Times New Roman",
    plot_bgcolor = 'white'
)

fig_global.update_traces(
    marker=dict(
        size = 13
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

fig_global.update_traces(line_color='#252852', line_width=5)

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

fig_s_mean['data'][0]['showlegend']=True
fig_s_mean['data'][0]['name']='Mean'

fig_viral = go.Figure(data = fig_l_min.data + fig_s_min.data  + fig_l_max.data + fig_s_max.data + fig_l_mean.data + fig_s_mean.data)

fig_viral.update_layout(
    xaxis_title = 'Days',
    title_font_family="Times New Roman",
    plot_bgcolor = 'white'
)

fig_viral.update_traces(
    marker=dict(
        size = 13
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

fig_viral.update_traces(line_color='#252852', line_width=5)

fig_viral.show()

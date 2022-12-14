import networkx as nx
import numpy as np
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pathlib
from Geographic_zone import fast_geographic_zone

def singleScatter(df,degree,colors):

    fig_s = px.scatter(
        df,
        x=[i+1 for i in range(15)],
        y= degree + "_degree",

        color = degree + "_country",
        color_discrete_sequence = colors
    )

    fig_l = (px.line(
            df,
            x=[i+1 for i in range(15)],
            y= degree  + "_degree"
        )
    )

        
    return go.Figure(data = fig_l.data + fig_s.data)

def singleScatterMean(df):
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
    return go.Figure(fig_s_mean. data + fig_l_mean.data)



def scatterPlot(df):


    fig_max = singleScatter(df,'max',['#e66100','#5d3a9b','#43a28e','#b1606a','#ccac51','#4933d4','#df454f','#960bd5','#178e18','#d1802f','#aabfc2','#a24af3','#5b8110','#1552dd','#a5a1e8'])
    fig_min = singleScatter(df,'min',['#8aa023','#5eeed8','#2b9ce1','#ed9500','#c77de9','#d7edb5','#1421a1','#e05a77','#c977c5','#bcc1d4','#cd39d8','#5562d9','#e87eb2','#ab2072','#e1b752'])

    fig_mean = singleScatterMean(df)

    fig = go.Figure(data = fig_min.data  + fig_max.data + fig_mean.data)  # type: ignore

    fig.update_layout(
        xaxis_title = 'Days',
        title_font_family="Times New Roman",
        plot_bgcolor = 'white'
    )

    fig.update_traces(
        marker=dict(
            size = 15
        )
    )


    fig.update_xaxes(
        showgrid=False,
        dtick = 1,
    )

    fig.update_yaxes(
        showgrid=True,
        dtick = 50,
        gridwidth=1, 
        gridcolor= '#e0e0e0',
        zeroline = True,
        zerolinecolor = '#e0e0e0',
        zerolinewidth  = 1
    )

    fig.update_traces(line_color='#252852', line_width=1)
    fig.update_layout(
        width = 2160,
        height = 1080,
    )
    
    return fig


def scatterPlotZone(df):
    fast = fast_geographic_zone()
    fig_zone = go.Figure()

    for i in range(len(df)):
        df.at[i,'max_country'] = fast.find_zone(df.at[i,'max_country'])
        df.at[i,'min_country'] = fast.find_zone(df.at[i,'min_country'])



    color_max = []
    color_min = []
    for i in range(len(df)):
        if not color_max.__contains__(fast.color_zone(df.at[i,'max_country'])):
            color_max.append(fast.color_zone(df.at[i,'max_country']))
        if not color_min.__contains__(fast.color_zone(df.at[i,'min_country'])):
            color_min.append(fast.color_zone(df.at[i,'min_country']))

    fig_max = singleScatter(df,'max',color_max)
    fig_min = singleScatter(df,'min',color_min)
    fig_mean =singleScatterMean(df)


    fig_zone = go.Figure(data = fig_min.data+ fig_max.data + fig_mean.data )  # type: ignore

    fig_zone.update_layout(
        xaxis_title = 'Days',
        title_font_family="Times New Roman",
        plot_bgcolor = 'white'
    )

    fig_zone.update_traces(
        marker=dict(
            size = 15
        )
    )


    fig_zone.update_xaxes(
        showgrid=False,
        dtick = 1,
    )

    fig_zone.update_yaxes(
        showgrid=True,
        dtick = 50,
        gridwidth=1, 
        gridcolor= '#e0e0e0',
        zeroline = True,
        zerolinecolor = '#e0e0e0',
        zerolinewidth  = 1
    )

    fig_zone.update_traces(line_color='#252852', line_width=1)

    already = []
    for trace in fig_zone['data']:
        if(already.__contains__(trace['name'])):  # type: ignore
            trace['showlegend'] = False  # type: ignore
        else:
            already.append(trace['name'])  # type: ignore

    fig_zone.update_layout(
        width = 2160,
        height = 1080,
    )

    return fig_zone

def bar(df,df_viral,degree,name):
    fig_line_viral = px.bar(
        df_viral,
        x = [x+1 for x in range(15)],
        y = df_viral[degree],
        color_discrete_sequence=['#998ec3'],
    )
    fig_line_viral['data'][0]['showlegend']=True  # type: ignore
    fig_line_viral['data'][0]['name']='Grado ' +  name +' Viral'  # type: ignore

    fig_line_global = px.bar(
        df,
        x = [x+1 for x in range(15)],
        y = df[degree],
        color_discrete_sequence=['#f1a340'],
    )
    fig_line_global['data'][0]['showlegend']=True  # type: ignore
    fig_line_global['data'][0]['name']='Grado ' +  name +' Top'  # type: ignore
    

    fig_line = go.Figure(fig_line_viral.data+fig_line_global.data)  # type: ignore
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

    return fig_line

def createDataFrame(name):
    dic = dict()
    mean_degree_l = list()
    max_country_l = list()
    max_degree_l = list()
    min_country_l = list()
    min_degree_l = list()
    for z in range(1, 16):

        data_path = pathlib.Path(__file__).parent.absolute().parent
        grafo = pd.read_pickle(data_path.joinpath('Dataset/'+ name +'-pkl/'+ name + str(z) + '.pkl'))

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

    dic['mean_degree'] = mean_degree_l
    dic['max_country'] = max_country_l
    dic['max_degree'] = max_degree_l
    dic['min_country'] = min_country_l
    dic['min_degree'] = min_degree_l

    return pd.DataFrame.from_dict(dic)


#----DEGREE-ANALYSES
df  = createDataFrame('global')
df_viral  = createDataFrame('viral')
#----SCATTER--------
scatterPlot(df).show()
scatterPlot(df_viral).show()
scatterPlotZone(df).show()
scatterPlotZone(df_viral).show()
#----SCATTER--------
bar(df,df_viral,"max_degree","Massimo").show()
bar(df,df_viral,"mean_degree","Medio").show()
bar(df,df_viral,"min_degree","Minimo").show()



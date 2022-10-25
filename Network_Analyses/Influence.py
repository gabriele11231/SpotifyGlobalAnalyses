import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import plotly.express as px

def main():
    data = data_gathering("global")
    data_viral = data_gathering("viral")
    create_treemap_plotly(data).show()
    create_treemap_plotly(data_viral).show()



def data_gathering(name):
    data_path = pathlib.Path(__file__).parent.absolute().parent

    df = pd.DataFrame()
    for z in range(1,16):
        entry_path = data_path.joinpath('Dataset/10-'+name+'/10-' + name + str(z)  +'.csv')
        with open(entry_path,newline='',encoding='utf-16') as file:
            df = pd.concat([df,pd.read_csv(file).iloc[:5]],ignore_index=True)


    for i in range(len(df['pubblicazione'])):
        df['pubblicazione'].at[i] = df['pubblicazione'].at[i].split("-")[0]


    return df

def create_treemap_plotly(data):
    values = data.groupby('titolo')['isrc'].count().to_dict()
    data = data.drop_duplicates(subset = 'titolo')
    fig = px.treemap(
        data,
        path=['titolo'],
        values = [values.get(title) for title in data['titolo']],
    )

    fig.data[0]['labels'] = create_label(data.sort_values(by='titolo'))

    fig.update_layout(
        treemapcolorway = ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#f7f7f7','#d1e5f0','#92c5de','#4393c3','#2166ac','#053061',], #defines the colors in the treemap
        margin = dict(t=50, l=25, r=25, b=25),
        width = 2160,
        height = 1080,    
    )
    return fig

def create_label(data):
    return [row[3] + "<br>" + row[4] + " - " + row[5] for row in data.itertuples()]
    
    


main()

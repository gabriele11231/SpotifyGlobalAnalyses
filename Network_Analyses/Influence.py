import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import plotly.express as px

def main():
    data = data_gathering()

    create_treemap_plotly(data)

def data_gathering():
    data_path = pathlib.Path(__file__).parent.absolute().parent

    df = pd.DataFrame()
    for z in range(1,16):
        entry_path = data_path.joinpath(f'Dataset/10-viral/10-viral{z}.csv')
        with open(entry_path,newline='',encoding='utf-16') as file:
            df = pd.concat([df,pd.read_csv(file)],ignore_index=True)


    for i in range(len(df['pubblicazione'])):
        df['pubblicazione'].at[i] = df['pubblicazione'].at[i].split("-")[0]


    return df

def create_treemap_plotly(data):

    fig = px.treemap(
        data,
        path=['titolo'],
        values = [1 for i in range(150)],
    )

    fig.data[0]['labels'] = create_label(data.drop_duplicates().reset_index())

    fig.update_layout(
        treemapcolorway = ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#f7f7f7','#d1e5f0','#92c5de','#4393c3','#2166ac','#053061',], #defines the colors in the treemap
        margin = dict(t=50, l=25, r=25, b=25),
        width = 2160,
        height = 1080,    
    )
    fig.show()
    fig.write_image("Influence.jpg")

def create_label(data):
    return [row[4] + "<br>" + row[5] + " - " + row[6] for row in data.itertuples()]
    
    


main()

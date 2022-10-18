import time
import numpy
import pandas as pd
import pathlib
import plotly.graph_objects as go

data_path = pathlib.Path(__file__).parent.absolute().parent
current_year = time.gmtime().tm_year 

influence = list(dict())
for z in range(1,16):
    entry_path = data_path.joinpath(f'Dataset/10-viral/10-viral{z}.csv')
    with open(entry_path,newline='',encoding='utf-16') as file:
        entry = pd.read_csv(file)
        temp_dict = dict()
        for row in entry['pubblicazione']:
            year_of_release = current_year - int(row.split('-')[0])
            value = 0
            if temp_dict.get(year_of_release) != None:
                value = temp_dict.get(year_of_release)
            temp_dict[year_of_release] = value + 1  # type: ignore
        influence.append(temp_dict)
        del temp_dict
     

df = pd.DataFrame(influence)
df = df.reindex(sorted(df.columns), axis=1)



figure = go.Figure()
for i in range(len(df.index)) :
    size = list()
    for element in df.iloc[i]:
        if numpy.isnan(element) :
            size.append(0)
        else:
            size.append(element)
    print(size)
    figure.add_trace(
        go.Scatter(
            x = [i+1 for x in range(len(df.iloc[i]))],
            y = df.columns.to_list(),
            mode='markers',
            marker_size = [element*5 for element in size],
            showlegend= False,
        )
    )

figure.update_xaxes(
    title = dict(
        text = 'Settembre',
    ),
    dtick = 1,
    tick0 = -1
)
figure.update_yaxes(
    title = dict(
        text = "anni dall'uscita",
    ),
    tick0 = -1
)   
figure.update_layout(
    width = 2160,
    height = 1080,
)
figure.write_image("Influence.svg")
figure.show()
import csv
import pathlib
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
with open(f'Dataset/global-centrality/global-centrality-merged.csv', 'r', encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        centrality[row['Country']] = centrality[row['Country']] + int(row['Centrality'])

#global-centrality of top
centrality_top = dict(sorted(centrality.items(), key=lambda item: item[1] ,reverse=True))


#----VIRAL----
for x in centrality:
    centrality[x] = 0

with open(f'Dataset/viral-centrality/viral-centrality-merged.csv', 'r', encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        centrality[row['Country']] = centrality[row['Country']] + int(row['Centrality'])

#global-centrality of viral
centrality_viral = dict(sorted(centrality.items(), key=lambda item: item[1] ,reverse=True))

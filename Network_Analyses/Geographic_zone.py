from csv import DictReader
from pathlib import Path
import json

#Group countries in zone of interest using the coordinates of the capital city
data_path = Path(__file__).parent.absolute().parent
countries_geographic_zone = dict()
countries_geographic_zone['Europa'] = list()
countries_geographic_zone['Globale'] = list()
countries_geographic_zone['Africa'] = list()
countries_geographic_zone['Nord_America'] = list()
countries_geographic_zone['America_centro_sud'] = list()
countries_geographic_zone['Asia'] = list()
countries_geographic_zone['Oceania'] = list()
countries_geographic_zone['Medio_Oriente'] = list()

with open(data_path.joinpath('Data_Gathering/global.csv'), 'r') as file:
    reader = DictReader(file)
    test = []
    for row in reader:
        if (37 <= float(row['latitudine'])and  -24 <= float(row['longitudine']) <= 32):
            countries_geographic_zone['Europa'].append(row['Name'])
        elif row['Name'] == 'Globale':
            countries_geographic_zone['Globale'].append('Globale')
        elif  float(row['latitudine']) < 36 and -7 < float(row['longitudine'] ) < 35:
            countries_geographic_zone['Africa'].append(row['Name'])
        elif  38 < float(row['latitudine']) < 51 and -79 < float(row['longitudine'] ) < -73:
            countries_geographic_zone['Nord_America'].append(row['Name'])
        elif  float(row['latitudine']) < 37 and -100 < float(row['longitudine'] ) < -45:
            countries_geographic_zone['America_centro_sud'].append(row['Name'])
        elif -31 < float(row['latitudine']) < 52 and 70 < float(row['longitudine'] ):
            countries_geographic_zone['Asia'].append(row['Name'])
        elif float(row['latitudine']) < -33 and 102 < float(row['longitudine'] ):
            countries_geographic_zone['Oceania'].append(row['Name'])
        else:
            countries_geographic_zone['Medio_Oriente'].append(row['Name'])

#Save result
'''with open(data_path.joinpath('Network_Analyses/Countries_geographic_zone.json'), 'w') as outfile:
    json.dump(countries_geographic_zone, outfile)
'''
#Class useful to find quickly the geographic zone given a country
class fast_geographic_zone:
    def __init__(self):
        self.complete = list()
        self.name = list()
        self.array = list()
        with open(data_path.joinpath('Network_Analyses/Countries_geographic_zone.json')) as json_file:
            geographic_zone = json.load(json_file)

        for row in geographic_zone:
            self.name.append(row)
            self.array.append(geographic_zone[row])
            for key in geographic_zone[row]:
                self.complete.append(key)
            self.complete.sort()

    def find_zone(self,country):
        for i in range(len(self.name)):
            if country in self.array[i]:
                return self.name[i]

    def color_zone(self,zone):
        color = dict()
        color['Europa'] = "#2d004b"
        color['Globale'] = "#f7f7f7"
        color['Africa'] = "#7f3b08"
        color['Nord_America'] = "#8073ac"
        color['America_centro_sud'] = "#fdb863"
        color['Asia'] = "#fee0b6"
        color['Oceania'] = "#b2abd2"
        color['Medio_Oriente'] = "#e08214"
        #other colors if you need: #b35806 #d8daeb #542788
        return color[zone]
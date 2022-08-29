from csv import DictReader
from pathlib import Path
import json

#Group countries in zone of interest using the coordinates of the capital city
data_path = Path(__file__).parent.absolute().parent
countries_geographic_zone = dict()
countries_geographic_zone['Europe'] = list()
countries_geographic_zone['Global'] = list()
countries_geographic_zone['Africa'] = list()
countries_geographic_zone['North_America'] = list()
countries_geographic_zone['South_Central_America'] = list()
countries_geographic_zone['Asia'] = list()
countries_geographic_zone['Australia'] = list()
countries_geographic_zone['Middle_east'] = list()

with open(data_path.joinpath('Data_Gathering/global.csv'), 'r') as file:
    reader = DictReader(file)
    test = []
    for row in reader:
        if (37 <= float(row['latitudine'])and  -24 <= float(row['longitudine']) <= 32):
            countries_geographic_zone['Europe'].append(row['Name'])
        elif row['Name'] == 'Global':
            countries_geographic_zone['Global'].append('Global')
        elif  float(row['latitudine']) < 36 and -7 < float(row['longitudine'] ) < 35:
            countries_geographic_zone['Africa'].append(row['Name'])
        elif  38 < float(row['latitudine']) < 51 and -79 < float(row['longitudine'] ) < -73:
            countries_geographic_zone['North_America'].append(row['Name'])
        elif  float(row['latitudine']) < 37 and -100 < float(row['longitudine'] ) < -45:
            countries_geographic_zone['South_Central_America'].append(row['Name'])
        elif -31 < float(row['latitudine']) < 52 and 70 < float(row['longitudine'] ):
            countries_geographic_zone['Asia'].append(row['Name'])
        elif float(row['latitudine']) < -33 and 102 < float(row['longitudine'] ):
            countries_geographic_zone['Australia'].append(row['Name'])
        else:
            countries_geographic_zone['Middle_east'].append(row['Name'])

#Save result
with open(data_path.joinpath('Network_Analyses/Countries_geographic_zone.json'), 'w') as outfile:
    json.dump(countries_geographic_zone, outfile)

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
        color['Europe'] = "#2d004b"
        color['Global'] = "#f7f7f7"
        color['Africa'] = "#7f3b08"
        color['North_America'] = "#8073ac"
        color['South_Central_America'] = "#fdb863"
        color['Asia'] = "#fee0b6"
        color['Australia'] = "#b2abd2"
        color['Middle_east'] = "#e08214"
        #other colors if you need: #b35806 #d8daeb #542788
        return color[zone]

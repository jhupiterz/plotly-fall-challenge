import json
from urllib.request import urlopen

def read_json_data(json_file):
    with open(json_file, 'r') as myfile:
        data=myfile.read()
    research = json.loads(data)
    return research

def load_counties():
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    return counties
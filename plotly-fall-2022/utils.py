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

def get_category_options(df):
    categories = df['category_name'].unique().tolist()
    categories.insert(0, 'All')
    return categories

def get_metric_labels(metric):
    if metric == 'invoice_and_item_number':
        return 'Total invoices'
    elif metric == 'sale_dollars':
        return 'Sales ($)'
    else:
        return 'Volume (L)'

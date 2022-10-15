import pandas as pd
import utils

global df
df = pd.DataFrame(utils.read_json_data('data.json'))
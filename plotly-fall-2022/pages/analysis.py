import dash
from dash import dcc, html, Input, Output

dash.register_page(__name__, path='/analysis')

layout = html.Div([html.H4('This will be the in-depth analytics page')])
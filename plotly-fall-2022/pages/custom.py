import dash
from dash import dcc, html, Input, Output

dash.register_page(__name__, path='/custom')

layout = html.Div([html.H4('This will be the make-you-own dashboard page')])
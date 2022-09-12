import pandas as pd
import utils, plots

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__, suppress_callback_exceptions = True, use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1", 'charSet':'“UTF-8”'}])

app.title = "Iowa Liquor Sales"
map_center = [42.036, -93.46505]

sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src="assets/bottle_logo.png", style={"width": "5.5rem", 'margin-left': '-1.2vw'}),
                html.H2("Cheers!", style={'margin-left': '0.5vw'}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("Overview")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-pie-chart me-2"),
                        html.Span("In-depth"),
                    ],
                    href="/analysis",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-magic me-2"),
                        html.Span("Make your own"),
                    ],
                    href="/custom",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-info-circle me-2"),
                        html.Span("Info"),
                    ],
                    n_clicks=0,
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar", style = {'margin-right': '2rem'}
)

app.layout = html.Div([
    dcc.Store(id='store-data', data = utils.read_json_data('../raw_data/data.json'), storage_type = 'memory'),
    dcc.Store(id='store-counties', data = utils.load_counties(), storage_type = 'memory'),
    sidebar,
    dash.page_container,
    ])

# Runs the app ------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
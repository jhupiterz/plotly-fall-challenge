import utils

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__, suppress_callback_exceptions = True, use_pages=True,
    external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"],
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1", 'charSet':'“UTF-8”'}])

app.title = "Iowa Liquor Sales"
map_center = [42.036, -93.46505]

sidebar = html.Div(
    [
        html.Div(
            [
                html.Img(src="assets/bottle_logo.png", style={"width": "5.8rem", 'margin-left': '-1.5vw'}),
                html.H2("Cheers!", style={'margin-left': '-0.5vw'}),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.I(className="fas fa-eye me-2", **{'aria-hidden': 'true'}, style = {'margin-right': '0.2vw'}),
                        html.Span("Counties overview")
                    ],
                    href="/",
                    active="exact"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-usd me-2"),
                        html.Span("Cumulative sales"),
                    ],
                    href="/sales",
                    active="exact"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-thermometer-half me-2"),
                        html.Span("Profit and Loss"),
                    ],
                    href="/profits",
                    active="exact"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa fa-bar-chart me-2"),
                        html.Span("Time series"),
                    ],
                    href="/timeseries",
                    active="exact"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-info-circle me-2"),
                        html.Span("Info")
                    ],
                    href="/info",
                    active="exact"
                )
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar", style = {'margin-right': '2rem'}
)

app.layout = html.Div([
    dcc.Store(id='store-data', data = utils.read_json_data('/raw_data/data.json'), storage_type = 'memory'),
    dcc.Store(id='store-counties', data = utils.load_counties(), storage_type = 'memory'),
    sidebar,
    dash.page_container,
    ])

# Runs the app ------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=True)
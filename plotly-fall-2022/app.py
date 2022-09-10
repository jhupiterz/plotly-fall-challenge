import pandas as pd
import utils, plots

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__, suppress_callback_exceptions = True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1", 'charSet':'“UTF-8”'}])

app.title = "Iowa Liquor Sales"
map_center = [42.036, -93.46505]
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src=PLOTLY_LOGO, style={"width": "3rem"}),
                html.H2("Sidebar"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("Home")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-calendar-alt me-2"),
                        html.Span("Calendar"),
                    ],
                    href="/calendar",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-envelope-open-text me-2"),
                        html.Span("Messages"),
                    ],
                    href="/messages",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar", style = {'order': 1, 'margin-right': '2rem'}
)

app.layout = html.Div([
    dcc.Store(id='store-data', data = utils.read_json_data('../raw_data/data.json'), storage_type = 'memory'),
    dcc.Store(id='store-counties', data = utils.load_counties(), storage_type = 'memory'),
    html.Div([
        sidebar,
        html.Div([dcc.Graph(id='map')], style = {'order': 2, 'border-radius': '5px', 'width': '810px', 'height': '510px', 'backgroundColor': 'white', 'padding': '5px'}),
    ], style = {'width': '100vw', 'height': '100vh', 'margin-left': '2rem', 'margin': 'auto', 'backgroundColor': 'grey', 'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', 'justifyContent': 'space-around', 'alignItems': 'center', 'alignContent': 'center'}),
])

@app.callback(Output('map', 'figure'),
              Input('store-data', 'data'),
              Input('store-counties', 'data'))
def update_map(data, counties):
    df = pd.DataFrame(data)
    grouped_df = df.groupby(['full_fips', 'county'], as_index=False).count()[['full_fips', 'county', 'invoice_and_item_number']]
    #print(f"COUNTIES: {counties}")
    #print(df.head())
    fig = plots.choropleth_map(grouped_df, counties, map_center)
    return fig

# Runs the app ------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
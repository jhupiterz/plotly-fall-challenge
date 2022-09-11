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
                        html.Span("Predictions"),
                    ],
                    href="/predictions",
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
    html.Div([
        html.Div([
            dcc.Dropdown(id = 'category', placeholder = 'Filter by alcohol category', value = 'All', style = {'width': '30vw', 'margin-top': '2rem', 'margin-right': '1rem'}),
            dcc.Dropdown(id = 'metric', placeholder = 'Select metric', options = [{'label': 'Total invoices', 'value': 'invoice_and_item_number'},
                                                                                  {'label': 'Total sales', 'value': 'sale_dollars'},
                                                                                  {'label': 'Total volume', 'value': 'volume_sold_liters'}],
                         value = 'invoice_and_item_number', style = {'width': '21.5vw', 'margin-top': '2rem'}),
        ], style = {'order': '2', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-between'}),
        dcc.Graph(id='map', style = {'order':'3', 'border-radius': '5px', 'width': '810px', 'height': '510px', 'backgroundColor': 'white', 'padding': '5px', 'margin-top': '2rem'}),
        html.H1(['Iowa Liquor Sales',html.Br(),'2021 Analytics Overview'], style = {'order':'1', 'color': '#a4e57a', 'margin-top': '2rem', 'text-align': 'left'})
    ], style = {'order':'1', 'height': '80vh', 'width': '50vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-left': '7rem'}),
    
    html.Div([
        html.H2(id = 'county_name', style = {'order': '1', 'color': '#a4e57a', 'margin-bottom': '2rem'}),
        html.Div(id = 'hover-bar-chart', children = [], style = {'order': '1'})],
        #html.Div(id = 'hover-pie-chart', children = [], style = {'order': '2'})],
        style = {'order':'2', 'height': '80vh', 'width': '50vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'margin-top': '8vh'})

], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': '#5e17eb', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

@app.callback(Output('map', 'figure'),
              Input('store-data', 'data'),
              Input('store-counties', 'data'),
              Input('category', 'value'),
              Input('metric', 'value'))
def update_map(data, counties, category, metric):
    df = pd.DataFrame(data)
    df = df[df['category_name'] == category] if category != 'All' else df
    if metric == 'invoice_and_item_number':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).count()[['full_fips', 'county', 'invoice_and_item_number']]
    elif metric == 'sale_dollars':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'sale_dollars']]
    elif metric == 'volume_sold_liters':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'volume_sold_liters']]
    fig = plots.choropleth_map(grouped_df, counties, map_center, metric)
    return fig

@app.callback(Output('category', 'options'),
              Input('store-data', 'data'))
def update_category_options(data):
    df = pd.DataFrame(data)
    return utils.get_category_options(df)

@app.callback(
    Output('hover-bar-chart', 'children'),
    Input('map', 'hoverData'),
    Input('store-data', 'data')
)
def create_bar_chart(hoverData, data):
    if hoverData:
        print(hoverData)
        df = pd.DataFrame(data)
        FIPS = hoverData['points'][0]['location']
        df_to_plot = df[df['full_fips'] == FIPS].groupby('category_name', as_index=False).sum()[['category_name', 'sale_dollars', 'volume_sold_liters']].sort_values('sale_dollars', ascending=False).head(5)
        fig = plots.bar_chart(df_to_plot)
        return dcc.Graph(figure=fig, style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '410px', 'height': '260px', 'padding': '5px'})

@app.callback(
    Output('county_name', 'children'),
    Input('map', 'hoverData')
)
def update_county_name(hoverData):
    if hoverData:
        return hoverData['points'][0]['customdata'][0].capitalize()

# Runs the app ------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
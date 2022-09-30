import dash
from dash import dcc, html, Input, Output, callback, clientside_callback, ClientsideFunction
import dash_bootstrap_components as dbc
import pandas as pd
import plots

dash.register_page(__name__, path='/timeseries')

add_trace_button = dbc.Button("add trace", id = 'trace-button', className="me-1", n_clicks=0, style = {'border-radius': '20px', 'width': '7vw', 'margin-left':'81vw', 'margin-top':'-8.8vh', 'margin-bottom': 0})

add_trace_dropdown = dcc.Dropdown(
    id = 'add-trace-dropdown',
    placeholder= "Add traces (max. 3)",
    style = {'width': '25vw', 'margin-left':'31.5vw', 'margin-top':'-4.5vh', 'margin-bottom': 0},
    multi=True
)

layout_3 = html.Div([
        dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle("🎨 Add traces 🎨"), style = {'margin': 'auto'}),
                    dbc.ModalBody(children=[
                        html.Div([
                            html.Div([
                                html.P("Choose up to 3 counties"),
                                add_trace_dropdown,
                            ], style = {'order': '1'}),
                            dbc.Button("Add traces", id = 'add-trace-button-modal', className="me-1", n_clicks=0, style = {'order':'2', 'z-index': '10000'}),
                        ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'flex-end', 'justify-content': 'space-between', 'z-index': '1000'}),
                    ])
                ],
                id = 'add-trace-modal',
                size = 'md',
                is_open = False,
                style={'color': 'black', 'font-family': 'Arial, sans-serif', 'font-size': '1.5vw'}),
        html.H1(['Iowa Liquor Sales',html.Br(),'2021 Time series'], style = {'order':'1', 'color': 'black', 'margin-left': '7vw', 'margin-top': '2rem', 'text-align': 'left'}),
        html.Div(id = 'timeseries-container', children = [
            html.Div(id = 'drag-container-3', className = 'container', children = [
                dbc.Card([
                    dbc.CardHeader(children = ["🌀  Number of invoices", add_trace_dropdown], style = {'font-size': '24px', 'height': '6vh'}),
                    dbc.CardBody(
                        dcc.Loading(dcc.Graph(id='line_l3', style = {'width': '89vw', 'height': '280px', 'padding': '5px', 'margin-top': '-1rem'})),
                    ),
                ], style = {'height': '320px', 'width': '90vw', 'margin-top': '2vh'})
            ], style = {'display': 'flex', 'flex-direction': 'column'}),
            html.Div(id = 'drag-container-4', className = 'container', children = [
                dbc.Card([
                    dbc.CardHeader(children = ["🌀  Monthly waterfalls"], style = {'font-size': '24px'}),
                    dbc.CardBody(
                        dcc.Loading(dcc.Graph(id='waterfall_l3', style = {'width': '90vw', 'height': '250px', 'padding': '5px', 'margin-top': '0.5rem', 'margin-left': '-1vw'})),
                    ),
                ], style = {'height': '320px', 'width': '90vw', 'margin-top': '2vh'}),
            ], style = {'height': '80vh', 'width': '85vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start'}),
        ], style = {'order':'2', 'display': 'flex', 'flex-direction': 'column', 'margin-right': '2.5vw', 'margin-top': '2vh'})
    ], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': 'rgba(94, 23, 235, 0.2)',
                'display': 'flex', 'flex-direction': 'column'})

layout = layout_3
        
### LAYOUT 3 ###
@callback(Output('waterfall_l3', 'figure'),
              Input('store-data', 'data'))
def create_monthly_waterfall(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    fig = plots.monthly_waterfall(df)
    return fig

@callback(
    Output('add-trace-modal', 'is_open'),
    Input('trace-button', 'n_clicks'),
)
def add_trace_to_line_plot(n_clicks):
    if n_clicks > 0:
        return True

@callback(
    Output('add-trace-dropdown', 'options'),
    Input('store-data', 'data')
)
def generate_dropdown(data):
    df = pd.DataFrame(data)
    county_options = [{'label': i, 'value': i} for i in df['county'].unique()]
    return county_options

@callback(
    Output('line_l3', 'figure'),
    Input('add-trace-dropdown', 'value'),
    Input('add-trace-button-modal', 'n_clicks'),
    Input('store-data', 'data')
)
def add_trace_to_line_plot(counties, n_clicks, data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    if n_clicks == 0:
        fig = plots.line_chart_invoices(df, counties)
        return fig
    elif n_clicks > 0:
        fig = plots.line_chart_invoices(df, counties)
        return fig

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output('timeseries-container', "data-drag"),
    [Input("drag-container-3", "id"), Input("drag-container-4", "id")],
)
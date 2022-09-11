import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/analysis')

layout = html.Div([

    html.Div([
        html.H1(['Iowa Liquor Sales',html.Br(),'2021 Store Analytics'], style = {'order':'1', 'color': '#a4e57a', 'margin-top': '2rem', 'text-align': 'left'}),
        dbc.Card(
            [
                dbc.CardHeader(
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Top stores in Iowa", tab_id="iowa"),
                            dbc.Tab(label="Top stores in county", tab_id="county"),
                            dbc.Tab(label="Search for specific store", tab_id="specific"),
                        ],
                        style = {'margin-top': '0.5vh', 'margin-left': '0.1vw'},
                        id="card-tabs",
                        active_tab="iowa",
                    )
                ),
                dbc.CardBody(html.P(id="card-content", className= "card-text")),
            ], style = {'order':'2', 'margin-top': '2rem'})
        ], style = {'order':'1', 'height': '80vh', 'width': '50vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-left': '7rem'}),
    
    ], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': '#5e17eb', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

@callback(Output('card-content', 'children'),
          Input('card-tabs', 'active_tab'))
def render_tab_content(tab_value):
    if tab_value == 'iowa':
        return html.Div([
            html.H2('Top stores in Iowa')
            ])
    elif tab_value == 'county':
        return html.Div([
            html.H2('Top stores in county')
            ])
    else:
        return html.Div([
            html.H2('Search for specific store')
            ])
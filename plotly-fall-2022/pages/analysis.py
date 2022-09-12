import pandas as pd
import plots
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/analysis')

radioitems = html.Div(
    [
        dbc.Label("Time period"),
        dbc.RadioItems(
            options=[
                {"label": "2021", "value": 2021},
                {"label": "Q1", "value": 'Q1'},
                {"label": "Q2", "value": 'Q2'},
                {"label": "Q3", "value": 'Q3'},
                {"label": "Q4", "value": 'Q4'}
            ],
            value=2021,
            inline=True,
            id="radioitems-input",
        ),
    ], style = {'margin-left': '1rem', 'order': '3'}
)

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
            ], style = {'order':'2', 'margin-top': '2rem', 'padding': '0px'})
        ], style = {'order':'1', 'height': '80vh', 'width': '50vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-left': '7rem', 'padding': '0px'}),
    
    ], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': '#5e17eb', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

@callback(Output('card-content', 'children'),
          Input('card-tabs', 'active_tab'))
def render_tab_content(tab_value):
    if tab_value == 'iowa':
        return html.Div([
            html.Div(id = 'iowa-store', style = {'width': '88vw', 'height': '67vh', 'backgroundColor': 'rgba(164, 229, 122, 0.5)', 'border-radius': '5px'})
            ])
    elif tab_value == 'county':
        return html.Div([
            html.Div(id = 'county-store', style = {'width': '88vw', 'height': '67vh', 'backgroundColor': 'white', 'border-radius': '5px'})
            ])
    else:
        return html.Div([
            html.Div(id = 'specific-store', style = {'width': '88vw', 'height': '67vh', 'backgroundColor': 'white', 'border-radius': '5px'})
            ])

@callback(Output('iowa-store', 'children'),
          Input('card-tabs', 'active_tab'),
          Input('store-data', 'data')
)
def render_iowa_store(tab, data):
    if tab == 'iowa':
        df = pd.DataFrame(data)
        iowa_store = df.groupby(['store_number', 'store_name'], as_index=False).sum()[['store_number', 'store_name', 'benefit']].sort_values(by = 'benefit', ascending = False).head(2)
        store_name_1 = iowa_store.iloc[0]['store_name']
        store_number_1 = iowa_store.iloc[0]['store_number']
        store_name_2 = iowa_store.iloc[1]['store_name']
        store_number_2 = iowa_store.iloc[1]['store_number']
        return html.Div([
            dcc.Store(id = 'store-infos', data = {'store_name_1': store_name_1, 'store_number_1': store_number_1, 'store_name_2': store_name_2, 'store_number_2': store_number_2}),
            html.Div([
                html.Div([
                    html.Div([
                        html.H3(f'{store_name_1}', style = {'order':'1', 'color': 'black', 'text-align': 'left', 'margin-top': '1rem', 'margin-left': '1rem'}),
                        html.H5(f'Store number: {store_number_1}', style = {'order':'2', 'color': 'black', 'text-align': 'left', 'margin-top': '0.5rem', 'margin-left': '1rem'}),
                        radioitems,
                    ], style = {'order':'1', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'width': '22vw', 'height': '20vh', 'margin-right': '2rem'}),
                    dcc.Graph(id = 'dist-plot-1', style = {'order': '2', 'margin-bottom': '1rem', 'margin-right': '1rem'})
                ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'width': '42vw', 'height': '20vh'}),
                dcc.Graph(id = 'iowa-store-1-cum', style = {'margin-left': '1rem', 'margin-top': '1rem'})
                ], style = {'order': '1', 'width': '42vw', 'height': '65vh', 'margin': 'auto',
                            'backgroundColor': 'white', 'border-radius': '5px', 'margin-top': '0.5rem'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.H3(f'{store_name_2}', style = {'order':'1', 'color': 'black', 'text-align': 'left', 'margin-top': '1rem', 'margin-left': '1rem'}),
                        html.H5(f'Store number: {store_number_2}', style = {'order':'2', 'color': 'black', 'text-align': 'left', 'margin-top': '0.5rem', 'margin-left': '1rem'}),
                        radioitems,
                    ], style = {'order':'1', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'width': '22vw', 'height': '20vh', 'margin-right': '2rem'}),
                    dcc.Graph(id = 'dist-plot-2', style = {'order': '2', 'margin-bottom': '1rem', 'margin-right': '1rem'})
                ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'width': '42vw', 'height': '20vh'}),
                dcc.Graph(id = 'iowa-store-2-cum', style = {'margin-left': '1rem', 'margin-top': '1rem'})
            ], style = {'order': '2', 'width': '42vw', 'height': '65vh', 'margin': 'auto',
                        'backgroundColor': 'white', 'border-radius': '5px', 'margin-top': '0.5rem'})
            ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                        'justify-content': 'space-between', 'width': '88vw', 'height': '65vh'})

@callback(Output('iowa-store-1-cum', 'figure'),
          Input('store-data', 'data'),
            Input('store-infos', 'data')
)
def render_cum_graph(data, store_data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['store_number'] == store_data['store_number_1']].sort_values('date', ascending=True).set_index('date')
    daily_sales = df.groupby(pd.Grouper(freq="D")).sum()[['benefit', 'cost', 'profit']]
    daily_sales['cum_sum_benefit'] = daily_sales['benefit'].cumsum()
    daily_sales['cum_sum_cost'] = daily_sales['cost'].cumsum()
    daily_sales['cum_sum_profit'] = daily_sales['profit'].cumsum()
    daily_sales = daily_sales.reset_index()
    fig = plots.cum_sales(daily_sales)
    return fig

@callback(Output('iowa-store-2-cum', 'figure'),
          Input('store-data', 'data'),
            Input('store-infos', 'data')
)
def render_cum_graph(data, store_data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['store_number'] == store_data['store_number_2']].sort_values('date', ascending=True).set_index('date')
    daily_sales = df.groupby(pd.Grouper(freq="D")).sum()[['benefit', 'cost', 'profit']]
    daily_sales['cum_sum_benefit'] = daily_sales['benefit'].cumsum()
    daily_sales['cum_sum_cost'] = daily_sales['cost'].cumsum()
    daily_sales['cum_sum_profit'] = daily_sales['profit'].cumsum()
    daily_sales = daily_sales.reset_index()
    fig = plots.cum_sales(daily_sales)
    return fig

@callback(Output('dist-plot-1', 'figure'),
          Input('store-data', 'data'),
            Input('store-infos', 'data')
)
def render_cum_graph(data, store_data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df_ = df.groupby(['store_number', 'store_name'], as_index=False).sum()[['store_number', 'store_name', 'profit']]
    store_profit = df_[df_['store_number'] == store_data['store_number_1']]['profit'].values[0]
    fig = plots.dist_plot(df_, store_profit)
    return fig

@callback(Output('dist-plot-2', 'figure'),
          Input('store-data', 'data'),
            Input('store-infos', 'data')
)
def render_cum_graph(data, store_data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df_ = df.groupby(['store_number', 'store_name'], as_index=False).sum()[['store_number', 'store_name', 'profit']]
    store_profit = df_[df_['store_number'] == store_data['store_number_2']]['profit'].values[0]
    fig = plots.dist_plot(df_, store_profit)
    return fig
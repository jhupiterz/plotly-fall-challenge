import pandas as pd
import plots
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/sales')

layout = html.Div([

    html.Div([
        html.H1(['Iowa Liquor Sales',html.Br(),'2021 Cumulative Sales'], style = {'order':'1', 'color': 'black', 'margin-top': '2rem', 'text-align': 'left'}),
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
    
    ], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': 'rgba(94, 23, 235, 0.2)', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

@callback(Output('card-content', 'children'),
          Input('card-tabs', 'active_tab'),
          Input('store-data', 'data'),
    )
def render_tab_content(tab_value, data):
    df = pd.DataFrame(data)
    county_options = [{'label': i, 'value': i} for i in df['county'].unique()]
    store_options = [{'label': i, 'value': i} for i in df['store_number'].unique()]
    if tab_value == 'iowa':
        return dcc.Loading(html.Div([
            html.Div(id = 'iowa-store', style = {'width': '88vw', 'height': '67vh', 'border-radius': '5px'})
            ]))
    elif tab_value == 'county':
        return dcc.Loading(html.Div([
            html.Div(id = 'county-store', children = [
                html.Div([
                    html.Div(id = 'county-store-1', children = [
                        dcc.Dropdown(id = 'county-dropdown-1', options = county_options, value = county_options[0]['value'], style = {'order':'1', 'width': '20vw', 'margin-left': '0.8rem', 'margin-top': '0.5rem'}),
                        html.Div(id = 'county-store-1-content', style = {'order':'2', 'width': '41vw', 'height': '57vh', 'border-radius': '5px', 'margin-left': '0.5rem', 'margin-top': '0.5rem'})
                    ],
                    style = {'order': '1', 'width': '42vw', 'height': '65vh', 'margin': 'auto',
                             'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start',
                             'backgroundColor': 'white', 'border-radius': '5px', 'margin-top': '0.5rem'}),
                    html.Div(id = 'county-store-2', children = [
                        dcc.Dropdown(id = 'county-dropdown-2', options = county_options, value = county_options[1]['value'], style = {'width': '20vw', 'margin-left': '0.8rem', 'margin-top': '0.5rem', 'z-index': '1000'}),
                        html.Div(id = 'county-store-2-content', style = {'order':'2', 'width': '41vw', 'height': '57vh', 'border-radius': '5px', 'margin-left': '0.5rem', 'margin-top': '0.5rem', 'z-index': '1'})
                    ],
                    style = {'order': '2', 'width': '42vw', 'height': '65vh', 'margin': 'auto',
                             'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start',
                             'backgroundColor': 'white', 'border-radius': '5px', 'margin-top': '0.5rem'})
                    ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                                'justify-content': 'space-between', 'width': '88vw', 'height': '65vh'})
            ],
            style = {'width': '88vw', 'height': '67vh', 'border-radius': '5px'})
            ]))
    else:
        return dcc.Loading(html.Div([
            html.Div(id = 'specific-store', children = [
                html.Div([
                    html.Div(id = 'specific-store-1', children = [
                        dcc.Dropdown(id = 'specific-dropdown-1', options = store_options, value = store_options[0]['value'], style = {'order':'1', 'width': '30vw', 'margin-left': '0.8rem', 'margin-top': '0.5rem'}),
                        html.Div(id = 'specific-store-1-content', style = {'order':'2', 'width': '41vw', 'height': '57vh', 'border-radius': '5px', 'margin-left': '0.5rem', 'margin-top': '0.5rem'})
                    ],
                    style = {'order': '1', 'width': '42vw', 'height': '65vh', 'margin': 'auto',
                             'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start',
                             'backgroundColor': 'white', 'border-radius': '5px', 'margin-top': '0.5rem'}),
                    html.Div(id = 'specific-store-2', children = [
                        dcc.Dropdown(id = 'specific-dropdown-2', options = store_options, value = store_options[0]['value'], style = {'width': '30vw', 'margin-left': '0.8rem', 'margin-top': '0.5rem', 'z-index': '1000'}),
                        html.Div(id = 'specific-store-2-content', style = {'order':'2', 'width': '41vw', 'height': '57vh', 'border-radius': '5px', 'margin-left': '0.5rem', 'margin-top': '0.5rem', 'z-index': '1'})
                    ],
                    style = {'order': '2', 'width': '42vw', 'height': '65vh', 'margin': 'auto',
                             'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start',
                             'backgroundColor': 'white', 'border-radius': '5px', 'margin-top': '0.5rem'})
                    ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                                'justify-content': 'space-between', 'width': '88vw', 'height': '65vh'})
            ], style = {'width': '88vw', 'height': '67vh', 'border-radius': '5px'})
            ]))

@callback(Output('iowa-store', 'children'),
          Input('card-tabs', 'active_tab'),
          Input('store-data', 'data')
)
def render_iowa_store(tab, data):
    if tab == 'iowa':
        df = pd.DataFrame(data)
        iowa_store = df.groupby(['store_number', 'store_name'], as_index=False).sum()[['store_number', 'store_name', 'profit']].sort_values(by = 'profit', ascending = False).head(2)
        store_name_1 = iowa_store.iloc[0]['store_name']
        store_number_1 = iowa_store.iloc[0]['store_number']
        store_name_2 = iowa_store.iloc[1]['store_name']
        store_number_2 = iowa_store.iloc[1]['store_number']
        return dcc.Loading(html.Div([
            dcc.Store(id = 'store-infos', data = {'store_name_1': store_name_1, 'store_number_1': store_number_1, 'store_name_2': store_name_2, 'store_number_2': store_number_2}),
            html.Div([
                html.Div([
                    html.Div([
                        html.H3(f'{store_name_1}', style = {'order':'1', 'color': 'black', 'text-align': 'left', 'margin-top': '1rem', 'margin-left': '1rem'}),
                        html.H5(f'Store number: {store_number_1}', style = {'order':'2', 'color': 'black', 'text-align': 'left', 'margin-top': '0.5rem', 'margin-left': '1rem'}),
                        #radioitems,
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
                        #radioitems,
                    ], style = {'order':'1', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'width': '22vw', 'height': '20vh', 'margin-right': '2rem'}),
                    dcc.Graph(id = 'dist-plot-2', style = {'order': '2', 'margin-bottom': '1rem', 'margin-right': '1rem'})
                ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'width': '42vw', 'height': '20vh'}),
                dcc.Graph(id = 'iowa-store-2-cum', style = {'margin-left': '1rem', 'margin-top': '1rem'})
            ], style = {'order': '2', 'width': '42vw', 'height': '65vh', 'margin': 'auto',
                        'backgroundColor': 'white', 'border-radius': '5px', 'margin-top': '0.5rem'})
            ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin': 'auto',
                        'justify-content': 'space-between', 'width': '88vw', 'height': '65vh'}))

@callback(Output('county-store-1-content', 'children'),
         Input('county-dropdown-1', 'value'),
         Input('store-data', 'data')
)
def render_county_store_1(county1, data):
    df = pd.DataFrame(data)
    df_1 = df[df['county'] == county1].groupby(['store_number', 'store_name'], as_index=False).sum()[['store_number', 'store_name', 'profit']].sort_values(by = 'profit', ascending = False).head(1)
    store_name_1 = df_1.iloc[0]['store_name']
    store_number_1 = df_1.iloc[0]['store_number']
    return html.Div([
            dcc.Store(id = 'county-infos-1', data = {'store_name_1': store_name_1, 'store_number_1': store_number_1}),
            html.Div([
                html.Div([
                    html.Div([
                        html.H3(f'{store_name_1}', style = {'order':'1', 'color': 'black', 'text-align': 'left', 'margin-top': '1rem', 'margin-left': '1rem'}),
                        html.H5(f'Store number: {store_number_1}', style = {'order':'2', 'color': 'black', 'text-align': 'left', 'margin-top': '0.5rem', 'margin-left': '1rem'}),
                        #radioitems,
                    ], style = {'order':'1', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'width': '22vw', 'height': '20vh', 'margin-right': '2rem'}),
                    dcc.Graph(id = 'dist-plot-3', style = {'order': '2', 'margin-right': '1rem'})
                ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'width': '42vw', 'height': '20vh', 'margin-left': '0rem'}),
                dcc.Graph(id = 'county-store-1-cum', style = {'margin-left': '1rem', 'margin-top': '-0.5rem'})
                ], style = {'order': '1', 'width': '42vw', 'height': '60vh', 'margin': 'auto', 'margin-left': '0rem',
                            'border-radius': '5px', 'margin-top': '0rem'})])

@callback(Output('county-store-2-content', 'children'),
         Input('county-dropdown-2', 'value'),
         Input('store-data', 'data')
)
def render_county_store_2(county2, data):
    df = pd.DataFrame(data)
    df_2 = df[df['county'] == county2].groupby(['store_number', 'store_name'], as_index=False).sum()[['store_number', 'store_name', 'profit']].sort_values(by = 'profit', ascending = False).head(1)
    store_name_2 = df_2.iloc[0]['store_name']
    store_number_2 = df_2.iloc[0]['store_number']
    return html.Div([
                dcc.Store(id = 'county-infos-2', data = {'store_name_2': store_name_2, 'store_number_2': store_number_2}),
                html.Div([
                    html.Div([
                        html.H3(f'{store_name_2}', style = {'order':'1', 'color': 'black', 'text-align': 'left', 'margin-top': '1rem', 'margin-left': '1rem'}),
                        html.H5(f'Store number: {store_number_2}', style = {'order':'2', 'color': 'black', 'text-align': 'left', 'margin-top': '0.5rem', 'margin-left': '1rem'}),
                        #radioitems,
                    ], style = {'order':'1', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'width': '22vw', 'height': '20vh', 'margin-right': '2rem', 'z-index': '1000'}),
                    dcc.Graph(id = 'dist-plot-4', style = {'order': '2', 'margin-right': '1rem'})
                ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'width': '42vw', 'height': '20vh', 'margin-left': '0rem'}),
                dcc.Graph(id = 'county-store-2-cum', style = {'margin-left': '1rem', 'margin-top': '-0.5rem'})
            ], style = {'order': '2', 'width': '42vw', 'height': '60vh', 'margin': 'auto', 'margin-left': '0rem',
                        'border-radius': '5px', 'margin-top': '0rem'})

@callback(Output('specific-store-1-content', 'children'),
         Input('specific-dropdown-1', 'value'),
         Input('store-data', 'data')
)
def render_county_store_1(store1, data):
    df = pd.DataFrame(data)
    store_name_1 = df[df['store_number']== store1]['store_name'].unique()[0]
    return html.Div([
            dcc.Store(id = 'specific-store-infos-1', data = {'store_name_1': store_name_1, 'store_number_1': store1}),
            html.Div([
                html.Div([
                    html.Div([
                        html.H3(f'{store_name_1}', style = {'order':'1', 'color': 'black', 'text-align': 'left', 'margin-top': '1rem', 'margin-left': '1rem'}),
                        html.H5(f'Store number: {store1}', style = {'order':'2', 'color': 'black', 'text-align': 'left', 'margin-top': '0.5rem', 'margin-left': '1rem'}),
                        #radioitems,
                    ], style = {'order':'1', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'width': '22vw', 'height': '20vh', 'margin-right': '2rem'}),
                    dcc.Graph(id = 'dist-plot-5', style = {'order': '2', 'margin-bottom': '0.5rem', 'margin-right': '1rem'})
                ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'width': '42vw', 'height': '20vh', 'margin-left': '0rem'}),
                dcc.Graph(id = 'specific-1-cum', style = {'margin-left': '1rem'})
                ], style = {'order': '1', 'width': '42vw', 'height': '60vh', 'margin': 'auto', 'margin-left': '0rem',
                            'border-radius': '5px', 'margin-top': '-0.5rem'})])

@callback(Output('specific-store-2-content', 'children'),
         Input('specific-dropdown-2', 'value'),
         Input('store-data', 'data')
)
def render_county_store_1(store2, data):
    df = pd.DataFrame(data)
    store_name_2 = df[df['store_number']== store2]['store_name'].unique()[0]
    return html.Div([
            dcc.Store(id = 'specific-store-infos-2', data = {'store_name_2': store_name_2, 'store_number_2': store2}),
                html.Div([
                    html.Div([
                        html.H3(f'{store_name_2}', style = {'order':'1', 'color': 'black', 'text-align': 'left', 'margin-top': '1rem', 'margin-left': '1rem'}),
                        html.H5(f'Store number: {store2}', style = {'order':'2', 'color': 'black', 'text-align': 'left', 'margin-top': '0.5rem', 'margin-left': '1rem'}),
                        #radioitems,
                    ], style = {'order':'1', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'width': '22vw', 'height': '20vh', 'margin-right': '2rem', 'z-index': '1000'}),
                    dcc.Graph(id = 'dist-plot-6', style = {'order': '2', 'margin-bottom': '0.5rem', 'margin-right': '1rem'})
                ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'width': '42vw', 'height': '20vh', 'margin-left': '0rem'}),
                dcc.Graph(id = 'specific-2-cum', style = {'margin-left': '1rem'})
            ], style = {'order': '2', 'width': '42vw', 'height': '60vh', 'margin': 'auto', 'margin-left': '0rem',
                        'border-radius': '5px', 'margin-top': '-0.5rem'})

@callback(Output('county-store-1-cum', 'figure'),
          Input('county-dropdown-1', 'value'),
          Input('store-data', 'data'),
          Input('county-infos-1', 'data')
)
def render_cum_graph(county, data, store_data):
    df = pd.DataFrame(data)
    df = df[df['county']==county]
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['store_number'] == store_data['store_number_1']].sort_values('date', ascending=True).set_index('date')
    daily_sales = df.groupby(pd.Grouper(freq="D")).sum()[['benefit', 'cost', 'profit']]
    daily_sales['cum_sum_benefit'] = daily_sales['benefit'].cumsum()
    daily_sales['cum_sum_cost'] = daily_sales['cost'].cumsum()
    daily_sales['cum_sum_profit'] = daily_sales['profit'].cumsum()
    daily_sales = daily_sales.reset_index()
    fig = plots.cum_sales(daily_sales, county=True)
    return fig

@callback(Output('county-store-2-cum', 'figure'),
          Input('county-dropdown-2', 'value'),
          Input('store-data', 'data'),
          Input('county-infos-2', 'data')
)
def render_cum_graph(county, data, store_data):
    df = pd.DataFrame(data)
    df = df[df['county'] == county]
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['store_number'] == store_data['store_number_2']].sort_values('date', ascending=True).set_index('date')
    daily_sales = df.groupby(pd.Grouper(freq="D")).sum()[['benefit', 'cost', 'profit']]
    daily_sales['cum_sum_benefit'] = daily_sales['benefit'].cumsum()
    daily_sales['cum_sum_cost'] = daily_sales['cost'].cumsum()
    daily_sales['cum_sum_profit'] = daily_sales['profit'].cumsum()
    daily_sales = daily_sales.reset_index()
    fig = plots.cum_sales(daily_sales, county=True)
    return fig

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

@callback(Output('specific-1-cum', 'figure'),
          Input('store-data', 'data'),
          Input('specific-dropdown-1', 'value')
)
def render_cum_graph(data, store_number):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['store_number'] == store_number].sort_values('date', ascending=True).set_index('date')
    daily_sales = df.groupby(pd.Grouper(freq="D")).sum()[['benefit', 'cost', 'profit']]
    daily_sales['cum_sum_benefit'] = daily_sales['benefit'].cumsum()
    daily_sales['cum_sum_cost'] = daily_sales['cost'].cumsum()
    daily_sales['cum_sum_profit'] = daily_sales['profit'].cumsum()
    daily_sales = daily_sales.reset_index()
    fig = plots.cum_sales(daily_sales, county=True)
    return fig

@callback(Output('specific-2-cum', 'figure'),
          Input('store-data', 'data'),
          Input('specific-dropdown-2', 'value')
)
def render_cum_graph(data, store_number):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['store_number'] == store_number].sort_values('date', ascending=True).set_index('date')
    daily_sales = df.groupby(pd.Grouper(freq="D")).sum()[['benefit', 'cost', 'profit']]
    daily_sales['cum_sum_benefit'] = daily_sales['benefit'].cumsum()
    daily_sales['cum_sum_cost'] = daily_sales['cost'].cumsum()
    daily_sales['cum_sum_profit'] = daily_sales['profit'].cumsum()
    daily_sales = daily_sales.reset_index()
    fig = plots.cum_sales(daily_sales, county=True)
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

@callback(Output('dist-plot-3', 'figure'),
          Input('county-dropdown-1', 'value'),
          Input('store-data', 'data'),
          Input('county-infos-1', 'data')
)
def render_cum_graph(county, data, store_data):
    df = pd.DataFrame(data)
    df = df[df['county'] == county]
    df['date'] = pd.to_datetime(df['date'])
    df_ = df.groupby(['store_number', 'store_name'], as_index=False).sum()[['store_number', 'store_name', 'profit']]
    store_profit = df_[df_['store_number'] == store_data['store_number_1']]['profit'].values[0]
    fig = plots.dist_plot(df_, store_profit)
    return fig

@callback(Output('dist-plot-4', 'figure'),
          Input('county-dropdown-2', 'value'),
          Input('store-data', 'data'),
          Input('county-infos-2', 'data')
)
def render_cum_graph(county, data, store_data):
    df = pd.DataFrame(data)
    df = df[df['county'] == county]
    df['date'] = pd.to_datetime(df['date'])
    df_ = df.groupby(['store_number', 'store_name'], as_index=False).sum()[['store_number', 'store_name', 'profit']]
    store_profit = df_[df_['store_number'] == store_data['store_number_2']]['profit'].values[0]
    fig = plots.dist_plot(df_, store_profit)
    return fig

@callback(Output('dist-plot-5', 'figure'),
          Input('specific-dropdown-1', 'value'),
          Input('store-data', 'data')
)
def render_cum_graph(store, data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df_ = df.groupby(['store_number', 'store_name'], as_index=False).sum()[['store_number', 'store_name', 'profit']]
    store_profit = df_[df_['store_number'] == store]['profit'].sum()
    fig = plots.dist_plot(df_, store_profit)
    return fig

@callback(Output('dist-plot-6', 'figure'),
          Input('specific-dropdown-2', 'value'),
          Input('store-data', 'data')
)
def render_cum_graph(store, data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df_ = df.groupby(['store_number', 'store_name'], as_index=False).sum()[['store_number', 'store_name', 'profit']]
    store_profit = df_[df_['store_number'] == store]['profit'].sum()
    fig = plots.dist_plot(df_, store_profit)
    return fig
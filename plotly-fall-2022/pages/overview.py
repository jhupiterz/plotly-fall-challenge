import pandas as pd
import utils, plots

import dash
from dash import dcc, html, Input, Output, callback

dash.register_page(__name__, path='/')


map_center = [42.036, -93.46505]

layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(id = 'category', placeholder = 'Filter by alcohol category', value = 'All', style = {'width': '30vw', 'margin-top': '2rem', 'margin-right': '1rem'}),
            dcc.Dropdown(id = 'metric', placeholder = 'Select metric', options = [{'label': 'Total invoices', 'value': 'invoice_and_item_number'},
                                                                                  {'label': 'Total sales', 'value': 'benefit'},
                                                                                  {'label': 'Total volume', 'value': 'volume_sold_liters'}],
                         value = 'invoice_and_item_number', style = {'width': '21.5vw', 'margin-top': '2rem'}),
        ], style = {'order': '2', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-between'}),
        dcc.Graph(id='map', style = {'order':'3', 'border-radius': '5px', 'width': '810px', 'height': '510px', 'backgroundColor': 'white', 'padding': '5px', 'margin-top': '2rem'}),
        html.H1(['Iowa Liquor Sales',html.Br(),'2021 Analytics Overview'], style = {'order':'1', 'color': '#a4e57a', 'margin-top': '2rem', 'text-align': 'left'})
    ], style = {'order':'1', 'height': '80vh', 'width': '50vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-left': '7rem'}),
    
    html.Div([
        html.H2(id = 'county_name', style = {'order': '1', 'color': '#a4e57a', 'margin-bottom': '2rem'}),
        html.Div(id = 'top-buyer', style = {'order': '2', 'margin-bottom': '2rem', 'backgroundColor': 'white', 'border-radius': '5px', 'width': '540px'}),
        html.Div(id = 'top-vendor', style = {'order': '3', 'margin-bottom': '2rem', 'backgroundColor': 'white', 'border-radius': '5px', 'width': '540px'}),
        html.Div(id = 'top-item', style = {'order': '4', 'margin-bottom': '2rem', 'backgroundColor': 'white', 'border-radius': '5px', 'width': '540px'}),
        html.Div(id = 'hover-bar-chart', children = [], style = {'order': '6'})],
        #html.Div(id = 'hover-pie-chart', children = [], style = {'order': '2'})],
        style = {'order':'2', 'height': '80vh', 'width': '35vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'flex-end', 'margin-right': '2.3rem', 'margin-top': '8.6vh'})

], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': '#5e17eb', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

@callback(Output('map', 'figure'),
              Input('store-data', 'data'),
              Input('store-counties', 'data'),
              Input('category', 'value'),
              Input('metric', 'value'))
def update_map(data, counties, category, metric):
    df = pd.DataFrame(data)
    df = df[df['category_name'] == category] if category != 'All' else df
    if metric == 'invoice_and_item_number':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).count()[['full_fips', 'county', 'invoice_and_item_number']]
    elif metric == 'benefit':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'benefit']]
    elif metric == 'volume_sold_liters':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'volume_sold_liters']]
    fig = plots.choropleth_map(grouped_df, counties, map_center, metric, 'viridis')
    return fig

@callback(Output('category', 'options'),
              Input('store-data', 'data'))
def update_category_options(data):
    df = pd.DataFrame(data)
    return utils.get_category_options(df)

@callback(
    Output('hover-bar-chart', 'children'),
    Input('map', 'hoverData'),
    Input('store-data', 'data')
)
def create_bar_chart(hoverData, data):
    if hoverData:
        df = pd.DataFrame(data)
        FIPS = hoverData['points'][0]['location']
        df_to_plot = df[df['full_fips'] == FIPS].groupby('category_name', as_index=False).sum()[['category_name', 'benefit', 'volume_sold_liters']].sort_values('benefit', ascending=False).head(6)
        fig = plots.bar_chart(df_to_plot)
        return html.Div([
            html.H2('Top categories', style = {'order': '5', 'color': '#a4e57a', 'margin-bottom': '1rem'}),
            dcc.Graph(figure=fig, style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '540px', 'height': '310px', 'padding': '5px'})
        ])

@callback(
    Output('county_name', 'children'),
    Input('map', 'hoverData')
)
def update_county_name(hoverData):
    if hoverData:
        return f"County: {hoverData['points'][0]['customdata'][0].capitalize()}"

@callback(
    Output('top-buyer', 'children'),
    Input('map', 'hoverData'),
    Input('store-data', 'data')
)
def update_top_store(hoverData, data):
    if hoverData:
        df = pd.DataFrame(data)
        FIPS = hoverData['points'][0]['location']
        temp_ = df[df['full_fips'] == FIPS].groupby(['store_number', 'store_name'], as_index=False).sum()[['store_number', 'store_name', 'benefit']].sort_values('benefit', ascending=False).head(1).reset_index()
        store_name = temp_['store_name'][0].split(' ')[0].capitalize()
        return html.H4(f'💸  #1 buyer:    {store_name} -- USD {int(temp_["benefit"][0])}', style = {'text-align':'left', 'color': '#ba1e7f', 'margin-left': '0.3rem', 'margin-right': '0.2rem', 'margin-top': '5px'})

@callback(
    Output('top-vendor', 'children'),
    Input('map', 'hoverData'),
    Input('store-data', 'data')
)
def update_top_store(hoverData, data):
    if hoverData:
        df = pd.DataFrame(data)
        FIPS = hoverData['points'][0]['location']
        temp_ = df[df['full_fips'] == FIPS].groupby(['vendor_number', 'vendor_name'], as_index=False).sum()[['vendor_number', 'vendor_name', 'benefit']].sort_values('benefit', ascending=False).head(1).reset_index()
        vendor_name = temp_['vendor_name'][0].split(' ')[0].capitalize()
        return html.H4(f'💸  #1 vendor:   {vendor_name} -- USD {int(temp_["benefit"][0])}', style = {'text-align':'left', 'color': '#ba1e7f', 'margin-left': '0.3rem', 'margin-right': '0.2rem', 'margin-top': '5px'})

@callback(
    Output('top-item', 'children'),
    Input('map', 'hoverData'),
    Input('store-data', 'data')
)
def update_top_store(hoverData, data):
    if hoverData:
        df = pd.DataFrame(data)
        FIPS = hoverData['points'][0]['location']
        temp_ = df[df['full_fips'] == FIPS].groupby(['item_number', 'item_description'], as_index=False).sum()[['item_number', 'item_description', 'benefit']].sort_values('benefit', ascending=False).head(1).reset_index()
        item_name = temp_['item_description'][0]
        return html.H4(f'🍻  #1 item: {item_name}', style = {'text-align':'left', 'color': '#ba1e7f', 'margin-left': '0.3rem', 'margin-right': '0.2rem', 'margin-top': '5px'})

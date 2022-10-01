import pandas as pd
import utils, plots

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, clientside_callback, ClientsideFunction

dash.register_page(__name__, path='/')

map_center = [42.036, -93.46505]

global df
df = pd.DataFrame(utils.read_json_data('data.json'))
print(df)

layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(id = 'category', placeholder = 'Filter by alcohol category', options = utils.get_category_options(df) ,value = 'All', style = {'width': '30vw', 'margin-top': '2rem', 'margin-right': '1rem'}),
            dcc.Dropdown(id = 'metric', placeholder = 'Select metric', options = [{'label': 'Total invoices', 'value': 'invoice_and_item_number'},
                                                                                  {'label': 'Total sales', 'value': 'benefit'},
                                                                                  {'label': 'Total volume', 'value': 'volume_sold_liters'}],
                         value = 'invoice_and_item_number', style = {'width': '21.5vw', 'margin-top': '2rem'}),
        ], style = {'order': '2', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-between'}),
        dcc.Graph(id='map', style = {'order':'3', 'border-radius': '5px', 'width': '810px', 'height': '510px', 'backgroundColor': 'white', 'padding': '5px', 'margin-top': '2rem'}),
        html.H1(['Iowa Liquor Sales',html.Br(),'2021 Counties Overview'], style = {'order':'1', 'color': 'black', 'margin-top': '2rem', 'text-align': 'left'})
    ], style = {'order':'1', 'height': '80vh', 'width': '50vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-left': '7rem'}),
    
    html.Div([
        html.H2(id = 'county_name', style = {'order': '1', 'color': 'black', 'margin-bottom': '2rem'}),
        html.Div(id = 'top-buyer', style = {'order': '2', 'margin-bottom': '2rem', 'backgroundColor': 'white', 'border-radius': '5px', 'width': '540px'}),
        html.Div(id = 'top-vendor', style = {'order': '3', 'margin-bottom': '2rem', 'backgroundColor': 'white', 'border-radius': '5px', 'width': '540px'}),
        html.Div(id = 'top-item', style = {'order': '4', 'margin-bottom': '2rem', 'backgroundColor': 'white', 'border-radius': '5px', 'width': '540px'}),
        html.Div(id = 'hover-bar-chart', children = [], style = {'order': '6', 'display': 'flex', 'flex-direction': 'row'})],
        style = {'order':'2', 'height': '80vh', 'width': '35vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'flex-end', 'margin-right': '2.3rem', 'margin-top': '8.6vh'})

], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': 'rgba(94, 23, 235, 0.2)', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

@callback(Output('map', 'figure'),
              #Input('store-data', 'data'),
              Input('store-counties', 'data'),
              Input('category', 'value'),
              Input('metric', 'value'))
def update_map(counties, category, metric):
    #df = pd.DataFrame(data)
    df_ = df[df['category_name'] == category] if category != 'All' else df
    if metric == 'invoice_and_item_number':
        grouped_df = df_.groupby(['full_fips', 'county'], as_index=False).count()[['full_fips', 'county', 'invoice_and_item_number']]
    elif metric == 'benefit':
        grouped_df = df_.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'benefit']]
    elif metric == 'volume_sold_liters':
        grouped_df = df_.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'volume_sold_liters']]
    fig = plots.choropleth_map(grouped_df, counties, map_center, metric, 'viridis')
    return fig

@callback(
    Output('hover-bar-chart', 'children'),
    Input('map', 'clickData')
)
def create_bar_chart(hoverData):
    if hoverData:
        #df = pd.DataFrame(data)
        FIPS = hoverData['points'][0]['location']
        df['date'] = pd.to_datetime(df['date'])
        fig_2 = plots.month_pie_chart(df)
        df_to_plot = df[df['full_fips'] == FIPS].groupby('category_name', as_index=False).sum()[['category_name', 'benefit', 'volume_sold_liters']].sort_values('benefit', ascending=False).head(3)
        fig_1 = plots.bar_chart(df_to_plot)
        return html.Div(id = 'drag-container-1', className = 'container',  children = [
                html.Div(id = 'drag-container-2', className = 'container',  children = [
                    dbc.Card([
                        dbc.CardHeader("🌀  Top Categories ($)", style = {'font-size': '24px'}),
                        dbc.CardBody(
                            dcc.Graph(figure=fig_1, style = {'width': '10vw', 'height': '15vh', 'margin-left': '-1vw', 'margin-top': '-5vh'})
                        ),
                    ], style = {'height': '40vh', 'width': '18vw', 'margin-right': '0.5vw', 'margin-left': '0.5vw'}),
                    dbc.Card([
                        dbc.CardHeader("🌀  Sales per month", style = {'font-size': '24px'}),
                        dbc.CardBody(
                            dcc.Graph(figure=fig_2, style = {'width': '15vw', 'height': '30vh', 'margin-top': 0})
                        ),
                    ], style = {'height': '40vh', 'width': '18vw', 'margin-right': '0.5vw', 'margin-left': '0.5vw'}),
                    ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'width': '38vw', 'height': '40vh', 'margin-right': '1.5vw'}),
                ], style = {'order': '2', 'display': 'flex', 'flex-direction': 'row', 'width': '38vw', 'height': '40vh', 'margin-right': '1.5vw'})
            
@callback(
    Output('county_name', 'children'),
    Input('map', 'clickData')
)
def update_county_name(hoverData):
    if hoverData:
        return f"County: {hoverData['points'][0]['customdata'][0].capitalize()}"
    else:
        return html.P(children = ["Click on a county on the map", html.Br(), "to display more data"], style = {'text-align':'center', 'color': 'white', 'font-size': '28px', 'margin-bottom': '25vh'})


@callback(
    Output('top-buyer', 'children'),
    Input('map', 'clickData')
)
def update_top_store(hoverData):
    if hoverData:
        #df = pd.DataFrame(data)
        FIPS = hoverData['points'][0]['location']
        temp_ = df[df['full_fips'] == FIPS].groupby(['store_number', 'store_name'], as_index=False).sum()[['store_number', 'store_name', 'benefit']].sort_values('benefit', ascending=False).head(1).reset_index()
        store_name = temp_['store_name'][0].split(' ')[0].capitalize()
        return html.P(children = [
                        html.H4(f'#1 buyer: {store_name} ', style = {'text-align': 'left', 'order': '1', 'height' : '1.6vh'}),
                        html.H4(f'USD {int(temp_["benefit"][0])}', style = {'text-align': 'right', 'order': '2', 'height' : '1.6vh'})],
                        style = {'display':'flex', 'flex-direction':'row', 'align-items':'center', 'justify-content': 'space-between',
                                 'color': 'black', 'margin-left': '0.3rem', 'margin-right': '0.2rem', 'margin-top': '5px'})

@callback(
    Output('top-vendor', 'children'),
    Input('map', 'clickData')
)
def update_top_store(hoverData):
    if hoverData:
        #df = pd.DataFrame(data)
        FIPS = hoverData['points'][0]['location']
        temp_ = df[df['full_fips'] == FIPS].groupby(['vendor_number', 'vendor_name'], as_index=False).sum()[['vendor_number', 'vendor_name', 'benefit']].sort_values('benefit', ascending=False).head(1).reset_index()
        vendor_name = temp_['vendor_name'][0].split(' ')[0].capitalize()
        return html.P(children = [
                        html.H4(f'#1 vendor: {vendor_name} ', style = {'text-align': 'left', 'order': '1', 'height' : '1.6vh'}),
                        html.H4(f'USD {int(temp_["benefit"][0])}', style = {'text-align': 'right', 'order': '2', 'height' : '1.6vh'})],
                        style = {'display':'flex', 'flex-direction':'row', 'align-items':'center', 'justify-content': 'space-between',
                                 'color': 'black', 'margin-left': '0.3rem', 'margin-right': '0.2rem', 'margin-top': '5px'})

@callback(
    Output('top-item', 'children'),
    Input('map', 'clickData')
)
def update_top_store(hoverData):
    if hoverData:
        #df = pd.DataFrame(data)
        FIPS = hoverData['points'][0]['location']
        temp_ = df[df['full_fips'] == FIPS].groupby(['item_number', 'item_description'], as_index=False).sum()[['item_number', 'item_description', 'benefit']].sort_values('benefit', ascending=False).head(1).reset_index()
        item_name = temp_['item_description'][0]
        if len(item_name) > 35:
            item_name = item_name[:35] + '...'
        return html.P(children = [
                        html.H4(f'#1 item: {item_name} ', style = {'text-align': 'left', 'order': '1', 'height' : '1.6vh'})],
                        style = {'display':'flex', 'flex-direction':'row', 'align-items':'center', 'justify-content': 'space-between',
                                 'color': 'black', 'margin-left': '0.3rem', 'margin-right': '0.2rem', 'margin-top': '5px'})

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output("hover-bar-chart", "data-drag"),
    [Input("drag-container-1", "id"), Input("drag-container-2", "id")],
)

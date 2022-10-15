import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import utils, plots
import plotly.express as px
from variables import df

dash.register_page(__name__, path='/profits')

df['date'] = pd.to_datetime(df['date'])

add_trace_button = dbc.Button("add trace", id = 'trace-button', className="me-1", n_clicks=0, style = {'order':'2', 'border-radius': '20px', 'width': '7vw', 'margin-left': '83vw'})

add_trace_dropdown = dcc.Dropdown(
    id = 'add-trace-dropdown',
    style = {'width': '20vw'},
    multi=True
)

map_center = [42.036, -93.46505]

fig_1 = plots.waterfall_chart(df)
waterfall_children = html.Div([
        html.H2('Profits and loss statement 2021', style = {'order': '5', 'color': 'black', 'margin-bottom': '0.5rem'}),
        dcc.Graph(figure=fig_1, style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '540px', 'height': '310px', 'padding': '5px'})
    ])

fig_2 = plots.weekday_pie_chart(df)
most_profitable_items = plots.get_mos_profitable_items(df)
upper_plots_children = html.Div([
            html.Div([
                html.H2('Profits per weekday', style = {'color': 'black', 'margin-bottom': '0.5rem', 'font-size': '26px', 'margin-left': '1.7vw'}),
                dcc.Graph(figure=fig_2, style = {'width': '260px', 'height': '310px', 'padding': '5px'})
            ], style = {'order': '2', 'margin-left': '0.5vw'}),
            html.Div([
                html.H2('Most profitable items', style = {'color': 'black', 'margin-bottom': '0.5rem', 'font-size': '26px'}),
                html.P(children = [html.H5("#1", style = {'margin-bottom': '-1.9vh'}), html.Br(), f"{most_profitable_items[0]['item']}", html.Br(), f"Margin: {most_profitable_items[0]['margin']} %"], style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '280px', 'height': '87px', 'padding': '5px'}),
                html.P(children = [html.H5("#2", style = {'margin-bottom': '-1.9vh'}), html.Br(), f"{most_profitable_items[1]['item']}", html.Br(), f"Margin: {most_profitable_items[1]['margin']} %"], style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '280px', 'height': '87px', 'padding': '5px'}),
                html.P(children = [html.H5("#3", style = {'margin-bottom': '-1.9vh'}), html.Br(), f"{most_profitable_items[2]['item']}", html.Br(), f"Margin: {most_profitable_items[2]['margin']} %"], style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '280px', 'height': '87px', 'padding': '5px'})
            ], style = {'order': '1'})
     ], style = {'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'align-items': 'center', 'margin-bottom': '1rem'})

layout_2 = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(id = 'category_l2', options = utils.get_category_options(df) , placeholder = 'Filter by alcohol category', value = 'All', style = {'width': '21vw', 'margin-top': '2rem', 'margin-right': '1rem'}),
            dcc.Dropdown(id = 'metric_l2', placeholder = 'Select metric', options = [{'label': 'Total invoices', 'value': 'invoice_and_item_number'},
                                                                                  {'label': 'Total sales', 'value': 'benefit'},
                                                                                  {'label': 'Total volume', 'value': 'volume_sold_liters'},
                                                                                  {'label': 'Total profits', 'value': 'profit'}],
                         value = 'profit', style = {'width': '15vw', 'margin-top': '2rem', 'margin-right': '1rem'}),
            dcc.Dropdown(id= 'map-color-l2', options=px.colors.named_colorscales(), value='viridis', style = {'width': '15vw', 'margin-top': '2rem'})
        ], style = {'order': '3', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-between', 'margin-top': '5vh'}),
        dcc.Graph(id='map_l2', style = {'order':'4', 'border-radius': '5px', 'width': '810px', 'height': '510px', 'backgroundColor': 'white', 'padding': '5px', 'margin-top': '2rem'}),
        html.H1(['Iowa Liquor Sales',html.Br(),'2021 Profits Statement'], style = {'order':'1', 'color': 'black', 'margin-top': '2rem', 'text-align': 'left'}),
    ], style = {'order':'1', 'height': '80vh', 'width': '50vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-left': '7rem'}),
    
    html.Div([
        html.Div(id = 'upper-plots-l2', children = [upper_plots_children], style = {'order': '1'}),
        html.Div(id = 'waterfall-chart_l2', children = [waterfall_children], style = {'order': '2'})],
        style = {'order':'2', 'height': '80vh', 'width': '35vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'flex-end', 'margin-right': '2.3rem', 'margin-top': '13.6vh'})

], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': 'rgba(94, 23, 235, 0.2)', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

layout = html.Div([
            layout_2
        ], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': 'rgba(94, 23, 235, 0.2)', 'display': 'flex',
                    'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

### LAYOUT 2 ###
@callback(Output('map_l2', 'figure'),
              Input('store-counties', 'data'),
              Input('category_l2', 'value'),
              Input('metric_l2', 'value'),
              Input('map-color-l2', 'value'))
def update_map(counties, category, metric, color_scale):
    #df = pd.DataFrame(data)
    df_ = df[df['category_name'] == category] if category != 'All' else df
    if metric == 'invoice_and_item_number':
        grouped_df = df_.groupby(['full_fips', 'county'], as_index=False).count()[['full_fips', 'county', 'invoice_and_item_number']]
    elif metric == 'benefit':
        grouped_df = df_.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'benefit']]
    elif metric == 'volume_sold_liters':
        grouped_df = df_.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'volume_sold_liters']]
    elif metric == 'profit':
        grouped_df = df_.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'profit']]
    fig = plots.choropleth_map(grouped_df, counties, map_center, metric, color_scale)
    return fig
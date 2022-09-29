import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import pandas as pd
import utils, plots
import plotly.express as px

dash.register_page(__name__, path='/profits')

add_trace_button = dbc.Button("add trace", id = 'trace-button', className="me-1", n_clicks=0, style = {'order':'2', 'border-radius': '20px', 'width': '7vw', 'margin-left': '83vw'})

add_trace_dropdown = dcc.Dropdown(
    id = 'add-trace-dropdown',
    style = {'width': '20vw'},
    multi=True
)

map_center = [42.036, -93.46505]

# inline_radioitems = html.Div(
#     [
#         dbc.Label("Choose a dashboard to display:", style = {'font-size': '20px'}),
#         dbc.RadioItems(
#             options=[
#                 {"label": "Profit and loss statements", "value": 1},
#                 {"label": "Time series", "value": 2}
#             ],
#             value=1,
#             id="radioitems-inline-input",
#             inline=True,
#             style = {'margin-top': '-0.5rem', 'font-size': '20px'}
#         ),
#     ], style = {'order':'1', 'margin-bottom': '1rem', 'z-index': '1000'}
# )

# def create_card(image_name, title, margin_right='0px'):
#     return dbc.Card(
#                 [
#                     html.H4(title, style = {'text-align': 'left', 'margin-top': '0.5rem'}),
#                     dbc.CardImg(src=f"assets/{image_name}.png", top=True, style = {"width":"26rem", "height": "26rem", 'margin': 'auto', 'margin-top': '-6.7rem', 'margin-left': '-2.1rem'})
#                 ],
#                 style={"width": "24rem", 'height': '18rem', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'margin-right': margin_right, 'backgroundColor': 'lightgrey'},
#             )

layout_2 = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(id = 'category_l2', placeholder = 'Filter by alcohol category', value = 'All', style = {'width': '21vw', 'margin-top': '2rem', 'margin-right': '1rem'}),
            dcc.Dropdown(id = 'metric_l2', placeholder = 'Select metric', options = [{'label': 'Total invoices', 'value': 'invoice_and_item_number'},
                                                                                  {'label': 'Total sales', 'value': 'benefit'},
                                                                                  {'label': 'Total volume', 'value': 'volume_sold_liters'},
                                                                                  {'label': 'Total profits', 'value': 'profit'}],
                         value = 'profit', style = {'width': '15vw', 'margin-top': '2rem', 'margin-right': '1rem'}),
            dcc.Dropdown(id= 'map-color-l2', options=px.colors.named_colorscales(), value='viridis', style = {'width': '15vw', 'margin-top': '2rem'})
        ], style = {'order': '3', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-between', 'margin-top': '0.2vh'}),
        dcc.Graph(id='map_l2', style = {'order':'4', 'border-radius': '5px', 'width': '810px', 'height': '510px', 'backgroundColor': 'white', 'padding': '5px', 'margin-top': '2rem'}),
        html.H1(['Iowa Liquor Sales',html.Br(),'2021 Profits Statement'], style = {'order':'1', 'color': 'black', 'margin-top': '2rem', 'text-align': 'left'}),
    ], style = {'order':'1', 'height': '80vh', 'width': '50vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-left': '7rem'}),
    
    html.Div([
        html.Div(id = 'upper-plots-l2', children = [], style = {'order': '1'}),
        html.Div(id = 'waterfall-chart_l2', children = [], style = {'order': '2'})],
        style = {'order':'2', 'height': '80vh', 'width': '35vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'flex-end', 'margin-right': '2.3rem', 'margin-top': '13.6vh'})

], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': 'rgba(94, 23, 235, 0.2)', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

# layout_3 = html.Div([
#     dbc.Modal([
#                 dbc.ModalHeader(dbc.ModalTitle("🎨 Add traces 🎨"), style = {'margin': 'auto'}),
#                 dbc.ModalBody(children=[
#                     html.Div([
#                         html.Div([
#                             html.P("Choose up to 3 counties"),
#                             add_trace_dropdown,
#                         ], style = {'order': '1'}),
#                         dbc.Button("Add traces", id = 'add-trace-button-modal', className="me-1", n_clicks=0, style = {'order':'2', 'z-index': '10000'}),
#                     ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'flex-end', 'justify-content': 'space-between', 'z-index': '1000'}),
#                 ])
#             ],
#             id = 'add-trace-modal',
#             size = 'md',
#             is_open = False,
#             style={'color': 'black', 'font-family': 'Arial, sans-serif', 'font-size': '1.5vw'}),
#     html.Div([
#         add_trace_button,
#         dcc.Graph(id='line_l3', style = {'order':'3', 'border-radius': '5px', 'width': '90vw', 'height': '500px', 'backgroundColor': 'white', 'padding': '5px', 'margin-top': '0.5rem'}),
#         dcc.Graph(id='waterfall_l3', style = {'order':'4', 'border-radius': '5px', 'width': '90vw', 'height': '500px', 'backgroundColor': 'white', 'padding': '5px', 'margin-top': '2rem'}),
#         html.H1(['Iowa Liquor Sales',html.Br(),'2021 Time series'], style = {'order':'1', 'color': 'black', 'margin-top': '2rem', 'text-align': 'left'}),
#         dbc.Button("New dashboard", id = 'new-button', className="me-1", n_clicks=0, style = {'order':'1', 'margin-top': '1vh'}),
#     ], style = {'order':'1', 'height': '80vh', 'width': '85vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-left': '7rem'}),
# ], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': 'rgba(94, 23, 235, 0.2)', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})


layout = html.Div([
            layout_2
            # dbc.Modal([
            #     dbc.ModalHeader(dbc.ModalTitle("🎨 Explore other dashboards! 🎨"), style = {'margin': 'auto'}),
            #     dbc.ModalBody(children=[
            #         html.Div([
            #             inline_radioitems,
            #             dbc.Button("Submit", id = 'submit-button', className="me-1", n_clicks=0, style = {'order':'2', 'z-index': '10000'}),
            #         ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-between', 'z-index': '1000'}),
            #         html.Div(id = 'layouts', children = [
            #             html.Div(children = [create_card('layout1', 'Profit and Loss', '4rem'), create_card('layout2', 'Time Series')], style = {'order': '1', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around', 'margin-bottom': '1rem', 'z-index': '0'})
            #         ], style = {'display': 'flex', 'flex-direction': 'column', 'z-index': '0'})
            #     ])
            # ],
            # id = 'layout-choice-modal',
            # size = 'lg',
            # is_open = True,
            # style={'color': 'black', 'font-family': 'Arial, sans-serif', 'font-size': '1.5vw'})
        ], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': 'rgba(94, 23, 235, 0.2)', 'display': 'flex',
                    'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

# @callback(Output('layout-choice-modal', 'is_open'),
#           Input('radioitems-inline-input', 'value'),
#           Input('submit-button', 'n_clicks'),
#           Input('new-button', 'n_clicks'))
# def update_layout_choice(layout, n_clicks_submit, n_clicks_new):
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if n_clicks_new > 0:
#         return True
#     elif layout is not None:
#         if n_clicks_submit > 0:
#             return False
#         else:
#             return True

# @callback(Output('custom-page-content', 'children'),
#           Input('radioitems-inline-input', 'value'),
#           Input('submit-button', 'n_clicks'))
# def update_custome_page_content(layout, n_clicks):
#     if n_clicks > 0:
#         if layout == 1:
#             return layout_2
#         elif layout == 2:
#             return layout_3

### LAYOUT 2 ###
@callback(Output('map_l2', 'figure'),
              Input('store-data', 'data'),
              Input('store-counties', 'data'),
              Input('category_l2', 'value'),
              Input('metric_l2', 'value'),
              Input('map-color-l2', 'value'))
def update_map(data, counties, category, metric, color_scale):
    df = pd.DataFrame(data)
    df = df[df['category_name'] == category] if category != 'All' else df
    if metric == 'invoice_and_item_number':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).count()[['full_fips', 'county', 'invoice_and_item_number']]
    elif metric == 'benefit':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'benefit']]
    elif metric == 'volume_sold_liters':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'volume_sold_liters']]
    elif metric == 'profit':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'profit']]
    fig = plots.choropleth_map(grouped_df, counties, map_center, metric, color_scale)
    return fig

@callback(Output('category_l2', 'options'),
              Input('store-data', 'data'))
def update_category_options(data):
    df = pd.DataFrame(data)
    return utils.get_category_options(df)

@callback(
    Output('waterfall-chart_l2', 'children'),
    Input('store-data', 'data')
)
def create_waterfall_chart(data):
    df = pd.DataFrame(data)
    fig = plots.waterfall_chart(df)
    return html.Div([
        html.H2('Profits and loss statement 2021', style = {'order': '5', 'color': 'black', 'margin-bottom': '0.5rem'}),
        dcc.Graph(figure=fig, style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '540px', 'height': '310px', 'padding': '5px'})
    ])

@callback(
    Output('upper-plots-l2', 'children'),
    Input('store-data', 'data')
)
def create_donut_chart(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    fig = plots.weekday_pie_chart(df)
    most_profitable_items = plots.get_mos_profitable_items(df)
    return html.Div([
            html.Div([
                html.H2('Profits per weekday', style = {'color': 'black', 'margin-bottom': '0.5rem', 'font-size': '26px', 'margin-left': '1.7vw'}),
                dcc.Graph(figure=fig, style = {'width': '260px', 'height': '310px', 'padding': '5px'})
            ], style = {'order': '2', 'margin-left': '0.5vw'}),
            html.Div([
                html.H2('Most profitable items', style = {'color': 'black', 'margin-bottom': '0.5rem', 'font-size': '26px'}),
                html.P(children = [html.H5("#1", style = {'margin-bottom': '-1.9vh'}), html.Br(), f"{most_profitable_items[0]['item']}", html.Br(), f"Margin: {most_profitable_items[0]['margin']} %"], style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '280px', 'height': '87px', 'padding': '5px'}),
                html.P(children = [html.H5("#2", style = {'margin-bottom': '-1.9vh'}), html.Br(), f"{most_profitable_items[1]['item']}", html.Br(), f"Margin: {most_profitable_items[1]['margin']} %"], style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '280px', 'height': '87px', 'padding': '5px'}),
                html.P(children = [html.H5("#3", style = {'margin-bottom': '-1.9vh'}), html.Br(), f"{most_profitable_items[2]['item']}", html.Br(), f"Margin: {most_profitable_items[2]['margin']} %"], style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '280px', 'height': '87px', 'padding': '5px'})
            ], style = {'order': '1'})
     ], style = {'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'align-items': 'center', 'margin-bottom': '1rem'})

# ### LAYOUT 3 ###
# @callback(Output('waterfall_l3', 'figure'),
#               Input('store-data', 'data'))
# def create_monthly_waterfall(data):
#     df = pd.DataFrame(data)
#     df['date'] = pd.to_datetime(df['date'])
#     fig = plots.monthly_waterfall(df)
#     return fig

# # @callback(Output('line_l3', 'figure'),
# #               Input('store-data', 'data'))
# # def create_monthly_waterfall(data):
# #     df = pd.DataFrame(data)
# #     df['date'] = pd.to_datetime(df['date'])
# #     fig = plots.line_chart_invoices(df)
# #     return fig

# @callback(Output('category_l3', 'options'),
#               Input('store-data', 'data'))
# def update_category_options(data):
#     df = pd.DataFrame(data)
#     return utils.get_category_options(df)

# @callback(
#     Output('waterfall-chart_l3', 'children'),
#     Input('store-data', 'data')
# )
# def create_waterfall_chart(data):
#     df = pd.DataFrame(data)
#     fig = plots.waterfall_chart(df)
#     return html.Div([
#         html.H2('Profits and loss statement 2021', style = {'order': '5', 'color': 'black', 'margin-bottom': '0.5rem'}),
#         dcc.Graph(figure=fig, style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '540px', 'height': '310px', 'padding': '5px'})
#     ])

# @callback(
#     Output('upper-plots-l3', 'children'),
#     Input('store-data', 'data')
# )
# def create_donut_chart(data):
#     df = pd.DataFrame(data)
#     df['date'] = pd.to_datetime(df['date'])
#     fig = plots.weekday_pie_chart(df)
#     most_profitable_items = plots.get_mos_profitable_items(df)
#     return html.Div([
#             html.Div([
#                 html.H2('Sales per weekday', style = {'color': 'black', 'margin-bottom': '0.5rem', 'font-size': '26px', 'margin-left': '1.7vw'}),
#                 dcc.Graph(figure=fig, style = {'width': '260px', 'height': '310px', 'padding': '5px'})
#             ], style = {'order': '2', 'margin-left': '0.5vw'}),
#             html.Div([
#                 html.H2('Most profitable items', style = {'color': 'black', 'margin-bottom': '0.5rem', 'font-size': '26px'}),
#                 html.P(children = [html.H5("#1", style = {'margin-bottom': '-1.9vh'}), html.Br(), f"{most_profitable_items[0]['item']}", html.Br(), f"Margin: {most_profitable_items[0]['margin']} %"], style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '280px', 'height': '87px', 'padding': '5px'}),
#                 html.P(children = [html.H5("#2", style = {'margin-bottom': '-1.9vh'}), html.Br(), f"{most_profitable_items[1]['item']}", html.Br(), f"Margin: {most_profitable_items[1]['margin']} %"], style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '280px', 'height': '87px', 'padding': '5px'}),
#                 html.P(children = [html.H5("#3", style = {'margin-bottom': '-1.9vh'}), html.Br(), f"{most_profitable_items[2]['item']}", html.Br(), f"Margin: {most_profitable_items[2]['margin']} %"], style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '280px', 'height': '87px', 'padding': '5px'})
#             ], style = {'order': '1'})
#      ], style = {'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'align-items': 'center', 'margin-bottom': '1rem'})

# @callback(
#     Output('add-trace-modal', 'is_open'),
#     Input('trace-button', 'n_clicks'),
# )
# def add_trace_to_line_plot(n_clicks):
#     if n_clicks > 0:
#         return True

# @callback(
#     Output('add-trace-dropdown', 'options'),
#     Input('store-data', 'data')
# )
# def generate_dropdown(data):
#     df = pd.DataFrame(data)
#     county_options = [{'label': i, 'value': i} for i in df['county'].unique()]
#     return county_options

# @callback(
#     Output('line_l3', 'figure'),
#     Input('add-trace-dropdown', 'value'),
#     Input('add-trace-button-modal', 'n_clicks'),
#     Input('store-data', 'data')
# )
# def add_trace_to_line_plot(counties, n_clicks, data):
#     df = pd.DataFrame(data)
#     df['date'] = pd.to_datetime(df['date'])
#     if n_clicks == 0:
#         fig = plots.line_chart_invoices(df, counties)
#         return fig
#     elif n_clicks > 0:
#         fig = plots.line_chart_invoices(df, counties)
#         return fig
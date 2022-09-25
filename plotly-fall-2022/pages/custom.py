import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import pandas as pd
import utils, plots
import plotly.express as px

dash.register_page(__name__, path='/custom')

inline_radioitems = html.Div(
    [
        dbc.Label("Choose a layout (max. 1)", style = {'font-size': '20px'}),
        dbc.RadioItems(
            options=[
                {"label": "Layout 1", "value": 1},
                {"label": "Layout 2", "value": 2},
                {"label": "Layout 3", "value": 3},
                {"label": "Layout 4", "value": 4},
            ],
            value=1,
            id="radioitems-inline-input",
            inline=True,
            style = {'margin-top': '-0.5rem', 'font-size': '20px'}
        ),
    ], style = {'order':'1', 'margin-bottom': '1rem', 'z-index': '1000'}
)

def create_card(image_name, title, margin_right='0px'):
    return dbc.Card(
                [
                    html.H4(title, style = {'text-align': 'left', 'margin-top': '0.5rem'}),
                    dbc.CardImg(src=f"assets/{image_name}.png", top=True, style = {"width":"26rem", "height": "26rem", 'margin': 'auto', 'margin-top': '-6.7rem', 'margin-left': '-2.1rem'})
                ],
                style={"width": "24rem", 'height': '18rem', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'margin-right': margin_right, 'backgroundColor': 'lightgrey'},
            )

map_center = [42.036, -93.46505]

layout_1 = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(id = 'category_l1', placeholder = 'Filter by alcohol category', value = 'All', style = {'width': '21vw', 'margin-top': '2rem', 'margin-right': '1rem'}),
            dcc.Dropdown(id = 'metric_l1', placeholder = 'Select metric', options = [{'label': 'Total invoices', 'value': 'invoice_and_item_number'},
                                                                                  {'label': 'Total sales', 'value': 'benefit'},
                                                                                  {'label': 'Total volume', 'value': 'volume_sold_liters'}],
                         value = 'invoice_and_item_number', style = {'width': '15vw', 'margin-top': '2rem', 'margin-right': '1rem'}),
            dcc.Dropdown(id= 'map-color', options=px.colors.named_colorscales(), value='viridis', style = {'width': '15vw', 'margin-top': '2rem'})
        ], style = {'order': '3', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-between', 'margin-top': '0.2vh'}),
        dcc.Graph(id='map_l1', style = {'order':'4', 'border-radius': '5px', 'width': '810px', 'height': '510px', 'backgroundColor': 'white', 'padding': '5px', 'margin-top': '2rem'}),
        html.H1(['2021 Iowa Liquor Sales',html.Br(),'Custom dashboard'], style = {'order':'1', 'color': '#a4e57a', 'margin-top': '2rem', 'text-align': 'left'}),
        dbc.Button("New dashboard", id = 'new-button', className="me-1", n_clicks=0, style = {'order':'2', 'margin-top': '1vh'}),
    ], style = {'order':'1', 'height': '80vh', 'width': '50vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-left': '7rem'}),
    
    html.Div([
        html.Div(id = 'cum-plot_l1', children = [], style = {'order': '1'}),
        html.Div(id = 'bar-chart_l1', children = [], style = {'order': '2'})],
        style = {'order':'2', 'height': '80vh', 'width': '35vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'flex-end', 'margin-right': '2.3rem', 'margin-top': '13.6vh'})

], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': '#5e17eb', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

layout = html.Div([
            dcc.Store(id='chosen-layout'),
            html.Div(id='custom-page-content'),
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("🎨 Create your own dashboard! 🎨"), style = {'margin': 'auto'}),
                dbc.ModalBody(children=[
                    html.Div([
                        inline_radioitems,
                        dbc.Button("Submit", id = 'submit-button', className="me-1", n_clicks=0, style = {'order':'2', 'z-index': '10000'}),
                    ], style = {'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-between', 'z-index': '1000'}),
                    html.Div(id = 'layouts', children = [
                        html.Div(children = [create_card('layout1', 'Layout 1', '4rem'), create_card('layout2', 'Layout 2')], style = {'order': '1', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around', 'margin-bottom': '1rem', 'z-index': '0'}),
                        html.Div(children = [create_card('layout3', 'Layout 3', '4rem'), create_card('layout4', 'Layout 4')], style = {'order': '2', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around', 'margin-bottom': '1rem', 'z-index': '0'}),
                    ], style = {'display': 'flex', 'flex-direction': 'column', 'z-index': '0'})
                ])
            ],
            id = 'layout-choice-modal',
            size = 'lg',
            is_open = True,
            style={'color': 'black', 'font-family': 'Arial, sans-serif', 'font-size': '1.5vw'})
        ], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': '#5e17eb', 'display': 'flex',
                    'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

@callback(Output('layout-choice-modal', 'is_open'),
          Input('radioitems-inline-input', 'value'),
          Input('submit-button', 'n_clicks'),
          Input('new-button', 'n_clicks'))
def update_layout_choice(layout, n_clicks_submit, n_clicks_new):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if n_clicks_new > 0:
        return True
    elif layout is not None:
        if n_clicks_submit > 0:
            return False
        else:
            return True

@callback(Output('custom-page-content', 'children'),
          Input('radioitems-inline-input', 'value'),
          Input('submit-button', 'n_clicks'))
def update_custome_page_content(layout, n_clicks):
    if n_clicks > 0:
        if layout == 1:
            return layout_1
        elif layout == 2:
            return html.H1('Layout 2', style = {'margin': 'auto'})
        elif layout == 3:
            return html.H1('Layout 3', style = {'margin': 'auto'})
        elif layout == 4:
            return html.H1('Layout 4', style = {'margin': 'auto'})

### LAYOUT 1 ###
@callback(Output('map_l1', 'figure'),
              Input('store-data', 'data'),
              Input('store-counties', 'data'),
              Input('category_l1', 'value'),
              Input('metric_l1', 'value'),
              Input('map-color', 'value'))
def update_map(data, counties, category, metric, color_scale):
    df = pd.DataFrame(data)
    df = df[df['category_name'] == category] if category != 'All' else df
    if metric == 'invoice_and_item_number':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).count()[['full_fips', 'county', 'invoice_and_item_number']]
    elif metric == 'benefit':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'benefit']]
    elif metric == 'volume_sold_liters':
        grouped_df = df.groupby(['full_fips', 'county'], as_index=False).sum()[['full_fips', 'county', 'volume_sold_liters']]
    fig = plots.choropleth_map(grouped_df, counties, map_center, metric, color_scale)
    return fig

@callback(Output('category_l1', 'options'),
              Input('store-data', 'data'))
def update_category_options(data):
    df = pd.DataFrame(data)
    return utils.get_category_options(df)

@callback(
    Output('bar-chart_l1', 'children'),
    Input('store-data', 'data')
)
def create_bar_chart(data):
    df = pd.DataFrame(data)
    df_to_plot = df.groupby('category_name', as_index=False).sum()[['category_name', 'benefit', 'volume_sold_liters']].sort_values('benefit', ascending=False).head(6)
    fig = plots.bar_chart(df_to_plot)
    return html.Div([
        html.H2('Top categories', style = {'order': '5', 'color': '#a4e57a', 'margin-bottom': '0.5rem'}),
        dcc.Graph(figure=fig, style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '540px', 'height': '310px', 'padding': '5px'})
    ])

@callback(
    Output('cum-plot_l1', 'children'),
    Input('store-data', 'data')
)
def create_bar_chart(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date', ascending=True).set_index('date')
    daily_sales = df.groupby(pd.Grouper(freq="D")).sum()[['benefit', 'cost', 'profit']]
    daily_sales['cum_sum_benefit'] = daily_sales['benefit'].cumsum()
    daily_sales['cum_sum_cost'] = daily_sales['cost'].cumsum()
    daily_sales['cum_sum_profit'] = daily_sales['profit'].cumsum()
    daily_sales = daily_sales.reset_index()
    fig = plots.cum_sales(daily_sales, county=True, custom=True)
    return html.Div([
        html.H2('Cumulative sales', style = {'order': '5', 'color': '#a4e57a', 'margin-bottom': '0.5rem'}),
        dcc.Graph(figure=fig, style = {'backgroundColor': 'white', 'border-radius': '5px', 'width': '540px', 'height': '310px', 'padding': '5px'})
    ])
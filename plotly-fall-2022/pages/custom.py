import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/custom')

switches = html.Div(
    [
        dbc.Checklist(
            options=[
                {"label": "Metric 1", "value": 1},
                {"label": "Metric 2", "value": 2},
                {"label": "Metric 3", "value": 3},
                {"label": "Metric 4", "value": 4},
                {"label": "Metric 5", "value": 5},
                {"label": "Metric 6", "value": 6},
                {"label": "Metric 7", "value": 7},
                {"label": "Metric 8", "value": 8},
            ],
            value=[1],
            id="switches-input",
            switch=True,
        ),
    ]
)

def create_card(image_name, title, margin_right='0px'):
    return dbc.Card(
                [
                    dbc.CardImg(src=f"assets/{image_name}.png", top=True, style = {"width":"26rem", "height": "26rem", 'margin': 'auto', 'margin-top': '-5.5rem', 'margin-left': '-2.1rem'}),
                    dbc.CardBody(
                        [
                            dbc.Checklist(options=[{"label": title, "value": True}],
                                        id ='include-pie-chart', switch=True,
                                        style = {'font-size': '18px', 'width': '10rem', 'margin': 'auto', 'padding': '0.1rem',
                                                 'padding-bottom':'-0.2rem', 'margin-top':'-6.2rem', 'margin-left': '-10.4rem'}),
                        ]
                    ),
                ],
                style={"width": "24rem", 'height': '18rem', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'margin-right': margin_right, 'backgroundColor': 'lightgrey'},
            )

layout = html.Div([

    html.Div([
        html.H1(['Iowa Liquor Sales',html.Br(),'Make your own dashboard!'], style = {'order':'1', 'color': '#a4e57a', 'margin-top': '2rem', 'text-align': 'left'}),
        dbc.Button("New dashboard", id = 'new-dash-button', size = 'lg', className="me-1", style={'order': '2'}, n_clicks=0)
        ], style = {'order':'1', 'height': '80vh', 'width': '50vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-left': '7rem', 'padding': '0px'}),

        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Choose a layout (max. 1)"), style = {'margin': 'auto'}),
            dbc.ModalBody(children=[
                html.Div(id = 'layouts', children = [
                    html.Div(children = [create_card('layout1', 'Layout 1', '4rem'), create_card('layout2', 'Layout 2')], style = {'order': '1', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around', 'margin-bottom': '1rem', 'z-index': '1000'}),
                    html.Div(children = [create_card('layout3', 'Layout 3', '4rem'), create_card('layout4', 'Layout 4')], style = {'order': '2', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around', 'margin-bottom': '1rem'}),
                ], style = {'display': 'flex', 'flex-direction': 'column'}),
                dbc.Button("Let's go!", size ='lg', className="me-1", style={'margin-top': '0.5rem'})
            ])
        ],
        id = 'layout-choice-modal',
        size = 'lg',
        is_open = False,
        style={'color': 'black', 'font-family': 'Arial, sans-serif', 'font-size': '1.5vw'})
        # dbc.Modal(
        #     [
        #         dbc.ModalHeader(dbc.ModalTitle("What do you wish to visualize?"), style={'margin': 'auto'}),
        #         dbc.ModalBody(children=[
        #             html.Div(id = 'metrics', children = [
        #                 html.H5('Step 1: pick your metrics (max. 4)', style = {'margin-top': '0.5rem', 'text-align': 'center', 'margin-bottom': '3rem'}),
        #                 switches,
        #                 dbc.Button("Submit choices", size ='lg', className="me-1", style={'margin-top': '3.2rem'})
        #             ], style = {'order':'1', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'width': '35vw', 'height':'60vh', 'backgroundColor': '#a4e57a', 'justify-content': 'flex-start', 'border-radius': '5px 0px 0px 5px'}),
        #             html.Div(id = 'graphs', children = [
        #                 html.H5('Step 2: pick your graphs (max. 4)', style = {'order':'1', 'margin-top': '0.5rem', 'margin-bottom': '1.5rem', 'text-align': 'center'}),
        #                 html.Div(children = [create_card('pie_chart', 'Pie chart', '4rem'), create_card('bar_chart', 'Bar chart')], style = {'order': '2', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around', 'margin-bottom': '1rem'}),
        #                 html.Div(children = [create_card('line_chart', 'Line chart', '4rem'), create_card('iowa', 'Iowa map')], style = {'order': '3', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around', 'margin-bottom': '1rem'}),
        #                 html.Div(children = [create_card('waterfall', 'Waterfall')], style = {'order': '4', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around'}),
        #             ], style = {'order':'2', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'width': '35vw', 'height':'60vh', 'backgroundColor': '#a4e57a', 'border-radius': '0px 5px 5px 0px'}),
        #         ], style = {'display':'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around'}),
        #     ],
        #     id="enter-custom-choices",
        #     size="lg",
        #     style={'color': 'black', 'font-family': 'Arial, sans-serif', 'font-size': '1.5vw'},
        #     is_open=False,
        # ),
    
    ], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': '#5e17eb', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})

@callback(Output('layout-choice-modal', 'is_open'),
          Input('new-dash-button', 'n_clicks'))
def update_modal(n_clicks):
    if n_clicks > 0:
        return True
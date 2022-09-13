import dash
from dash import dcc, html, Input, Output
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

def create_card(image_name, title):
    return dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src=f"assets/{image_name}.png",
                            className="img-fluid rounded-start",
                            style = {'margin-right': '-0.1rem'}
                        ),
                        className="col-md-4",
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H4(title, className="card-title", style={'font-size': '16px', 'margin-left': '-0.1rem'}),
                            ]
                        ),
                        className="col-md-8",
                    ),
                ],
                className="g-0 d-flex align-items-center",
            )
        ],
        className="mb-3",
        style={"maxWidth": "10rem", 'padding': '0.1rem'},
    )

layout = html.Div([

    html.Div([
        html.H1(['Iowa Liquor Sales',html.Br(),'Make your own dashboard!'], style = {'order':'1', 'color': '#a4e57a', 'margin-top': '2rem', 'text-align': 'left'}),
        ], style = {'order':'1', 'height': '80vh', 'width': '50vw', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'margin-left': '7rem', 'padding': '0px'}),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("What do you wish to visualize?"), style={'margin': 'auto'}),
                dbc.ModalBody(children=[
                    html.Div(id = 'metrics', children = [
                        html.H4('Step 1: pick your metrics (max. 4)', style = {'margin-top': '0.5rem', 'text-align': 'center', 'margin-bottom': '2rem'}),
                        switches
                    ], style = {'order':'1', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'width': '35vw', 'height':'60vh', 'backgroundColor': 'grey', 'justify-content': 'flex-start'}),
                    html.Div(id = 'graphs', children = [
                        html.H4('Step 2: pick your graphs (max. 4)', style = {'order':'1', 'margin-top': '0.5rem', 'text-align': 'center'}),
                        create_card('pie_chart', 'Pie chart'),
                        create_card('bar_chart', 'Bar chart'),
                        create_card('line_chart', 'Line chart'),
                        create_card('iowa', 'Iowa map'),
                        create_card('waterfall', 'Waterfall'),
                    ], style = {'order':'2', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'width': '35vw', 'height':'60vh', 'backgroundColor': 'grey'}),
                ], style = {'display':'flex', 'flex-direction': 'row', 'align-items': 'center', 'justify-content': 'space-around'}),
            ],
            id="enter-custom-choices",
            size="xl",
            style={'color': 'black', 'font-family': 'Arial, sans-serif', 'font-size': '1.5vw'},
            is_open=True,
        ),
    
    ], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': '#5e17eb', 'display': 'flex',
                'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})
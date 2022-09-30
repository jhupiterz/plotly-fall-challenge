import dash
from dash import html

dash.register_page(__name__, path='/info')

layout = html.Div([
    html.Div(children = [
        html.H1(['Information about the app'], style = {'order':'1', 'color': 'black', 'margin-top': '2rem', 'text-align': 'left'}),
        html.Br(),
        html.Br(),
        html.P(["🙋 This app was built for the purpose of ", html.A(href = "https://community.plotly.com/t/autumn-community-app-challenge/66996", children = ["Plotly's Autumn App Challenge"])," and does not aim to promote the consumption of alcohol."], style = {'font-size': '22px'}),
        html.P(["💽 The 2021 Iowa Liquor Sales dataset was obtained from Kaggle at ", html.A(href = "https://www.kaggle.com/datasets/residentmario/iowa-liquor-sales", children = ["this link"]), "."], style = {'font-size': '22px'}),
        html.P("Cards with this symbol 🌀 can be dragged and dropped to different positions on the page.", style = {'font-size': '22px'}),
        html.P(["💻 The full code for this app is available on GitHub at ", html.A(href = "https://github.com/jhupiterz/plotly-fall-challenge", children = ["this link"]), "."], style = {'font-size': '22px'}),
        html.P("🙏 Huge thanks to the following libraries: Dash, Dragula, and Bootstrap.", style = {'font-size': '22px'}),
        html.H2("Enjoy the different dashboards!"),
    ], style = {'margin-left': '7rem'}),
], style = {'width': '100vw', 'height': '100vh', 'backgroundColor': 'rgba(94, 23, 235, 0.2)', 'display': 'flex', 'flex-direction': 'row', 'align-items': 'flex-start', 'justify-content': 'space-between'})
from turtle import width
import plotly.express as px
import plotly.graph_objects as go
import utils

def choropleth_map(df, geojson, center, metric, color_scale):
    fig = px.choropleth_mapbox(df, geojson=geojson, locations='full_fips', color=metric,
                            color_continuous_scale=color_scale,
                            range_color=(0, df[metric].max()),
                            mapbox_style='stamen-toner',
                            zoom=6, center = {"lat": center[0], "lon": center[1]},
                            opacity=0.4,
                            hover_data= ['county', metric],
                            labels={metric: utils.get_metric_labels(metric), 'full_fips': 'FIPS'},
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height = 500, width = 800)
    return fig

def bar_chart(df):
    fig = px.bar(df, x='category_name', y='benefit', width = 520, height = 320)
    fig.update_yaxes(visible=False)
    fig.update_xaxes(title='')
    fig.update_layout(
        margin=dict(l=1, r=1, t=30, b=0),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        legend={'title_text':''},
        plot_bgcolor='rgba(0, 0, 0, 0)',
        title_text= '',
        title_x = 0.5)
    return fig

def cum_sales(df, county=False, custom=False):
    if county == False:
        width = 610
        height = 360
    elif custom == True:
        width = 500
        height = 250
    else: 
        width = 590
        height = 340
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.date, y=df.cum_sum_benefit,
                        mode='lines+markers',
                        name='cum. benefits'))
    fig.add_trace(go.Scatter(x=df.date, y=df.cum_sum_cost,
                        mode='lines+markers',
                        name='cum. costs'))
    fig.add_trace(go.Scatter(x=df.date, y=df.cum_sum_profit,
                        mode='lines+markers',
                        name='cum. profits'))
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    fig.update_layout(
        width = width,
        height = height,
        hovermode="x unified",
        title_x=0.5,
        margin=dict(l=1, r=1, t=30, b=0),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        legend={'title_text':''},
        plot_bgcolor='rgba(0, 0, 0, 0)')
    return fig

def dist_plot(df, profit):
    fig = px.violin(df, x='profit', log_x=True, width=300, height=200)
    fig.update_xaxes(range=[0, 5.5])
    fig.add_vline(x=profit, line_width=2, line_dash="dash", line_color="#ba1e7f")
    fig.update_layout(
            title_x=0.5,
            margin=dict(l=1, r=1, t=30, b=0),
            paper_bgcolor='rgba(0, 0, 0, 0)')
    return fig
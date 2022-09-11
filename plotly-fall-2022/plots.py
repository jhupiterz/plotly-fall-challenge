from queue import Full
import plotly.express as px
import utils

def choropleth_map(df, geojson, center, metric):
    fig = px.choropleth_mapbox(df, geojson=geojson, locations='full_fips', color=metric,
                            color_continuous_scale="Viridis",
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
    fig = px.bar(df, x='category_name', y='sale_dollars', width = 530, height = 300)
    fig.update_yaxes(visible=False)
    fig.update_xaxes(title='')
    fig.update_layout(
        margin=dict(l=1, r=1, t=30, b=0),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        legend={'title_text':''},
        plot_bgcolor='rgba(0, 0, 0, 0)',
        title_text= 'Top categories ($)',
        title_x = 0.5)
    return fig
import plotly.express as px

def choropleth_map(df, geojson, center):
    fig = px.choropleth_mapbox(df, geojson=geojson, locations='full_fips', color='invoice_and_item_number',
                            color_continuous_scale="Viridis",
                            range_color=(0, df.invoice_and_item_number.max()),
                            mapbox_style="stamen-toner",
                            zoom=6, center = {"lat": center[0], "lon": center[1]},
                            opacity=0.4,
                            labels={'invoice_and_item_number':'total invoices'}
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height = 500, width = 800)
    # fig = px.choropleth(
    #     df, geojson=geojson, color='invoice_and_item_number',
    #     locations="county", featureidkey="properties.county",
    #     center= center,
    #     projection="mercator", range_color=[0, df.invoice_and_item_number.max()])
    # fig.update_geos(fitbounds="locations", visible=False)
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
from turtle import title, width
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import utils

def map_weekdays(x):
    if x == 0:
        return "Monday"
    elif x == 1:
        return "Tuesday"
    elif x == 2:
        return "Wednesday"
    elif x == 3:
        return "Thursday"
    elif x == 4:
        return "Friday"
    elif x == 5:
        return "Saturday"
    return "Sunday"

def map_months(x):
    if x == 1:
        return "January"
    elif x == 2:
        return "February"
    elif x == 3:
        return "March"
    elif x == 4:
        return "April"
    elif x == 5:
        return "May"
    elif x == 6:
        return "June"
    elif x == 7:
        return "July"
    elif x == 8:
        return "August"
    elif x == 9:
        return "September"
    elif x == 10:
        return "October"
    elif x == 11:
        return "November"
    return "December"

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
    fig = px.bar(df, x='category_name', y='benefit', text= 'benefit', width = 250, height = 340)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
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
        height = 340
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
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_text=''
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)')
    return fig

def dist_plot(df, profit):
    fig = px.violin(df, x='profit', log_x=True, width=300, height=180)
    fig.update_xaxes(range=[0, 5.5])
    fig.add_vline(x=profit, line_width=2, line_dash="dash", line_color="#ba1e7f")
    fig.update_layout(
            title_x=0.5,
            margin=dict(l=1, r=1, t=30, b=0),
            paper_bgcolor='rgba(0, 0, 0, 0)')
    return fig

def waterfall_chart(df):
    fig = go.Figure(go.Waterfall(
        orientation = "v",
        measure = ["relative", "relative", "total"],
        x = ["Revenues", "Costs", "Profits"],
        textposition = "outside",
        text = [utils.human_format(round(df.benefit.sum(),1)), utils.human_format(round(-1*df.cost.sum(),1)), utils.human_format(round(df.profit.sum(),1))],
        y = [df.benefit.sum(), -1*df.cost.sum(), df.profit.sum()],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
            width = 530,
            height = 300,
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            showlegend = False,
            margin=dict(l=0, r=0, t=0, b=0),
            yaxis_range=[0,round(df.benefit.sum(),1)+1000000]
    )
    return fig

def weekday_pie_chart(df):
    df['weekday'] = [x.weekday() for x in df.date]
    df['weekday'] = df['weekday'].apply(map_weekdays)
    df_to_pie = df.groupby('weekday', as_index=False).sum()[['weekday', 'profit']]
    fig = px.pie(df_to_pie, values='profit', names='weekday', hole=0.5)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        width = 200,
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        showlegend = False,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

def month_pie_chart(df):
    df['month'] = df.date.dt.month
    df['month'] = df['month'].apply(map_months)
    df_to_pie = df.groupby('month', as_index=False).count()[['month', 'invoice_and_item_number']]
    fig = px.pie(df_to_pie, values='invoice_and_item_number', names='month', hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        width = 200,
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        showlegend = False,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig

def get_mos_profitable_items(df):
    most_profitable_items = df[['item_description', 'state_bottle_cost', 'state_bottle_retail']]
    most_profitable_items['margin_%'] = round((most_profitable_items.state_bottle_retail-df.state_bottle_cost)/df.state_bottle_retail*100,1)
    df_items = most_profitable_items.sort_values('margin_%', ascending=False).head(10).drop_duplicates().reset_index(drop=True).drop([1,2]).reset_index(drop=True)
    return [{'item': df_items['item_description'][0], 'margin': df_items['margin_%'][0]},
            {'item': df_items['item_description'][1], 'margin': df_items['margin_%'][1]},
            {'item': df_items['item_description'][2], 'margin': df_items['margin_%'][2]}
            ]

def monthly_waterfall(df):
    df = df.sort_values('date', ascending=True).set_index('date')
    df = df.groupby(pd.Grouper(freq="M")).sum()[['benefit', 'cost', 'profit']]
    measure = ['relative', 'relative', 'total']*12
    x = ["Dec. 2020 (Rev.)", "Dec. 2020 (Cost)", "Dec. 2020 (Profit)", "Jan. 2021 (Rev.)","Jan. 2021 (Cost)","Jan. 2021 (Profit)", "Feb. 2021 (Rev.)","Feb. 2021 (Cost)","Feb. 2021 (Profit)",
        "Mar. 2021 (Rev.)","Mar. 2021 (Cost)","Mar. 2021 (Profit)", "Apr. 2021 (Rev.)","Apr. 2021 (Cost)","Apr. 2021 (Profit)",
        "May 2021 (Rev.)","May 2021 (Cost)","May 2021 (Profit)", "Jun. 2021 (Rev.)", "Jun. 2021 (Cost)", "Jun. 2021 (Profit)", "Jul. 2021 (Rev.)","Jul. 2021 (Cost)","Jul. 2021 (Profit)",
        "Aug. 2021 (Rev.)","Aug. 2021 (Cost)","Aug. 2021 (Profit)", "Sep. 2021 (Rev.)","Sep. 2021 (Cost)","Sep. 2021 (Profit)",
        "Oct. 2021 (Rev.)","Oct. 2021 (Cost)","Oct. 2021 (Profit)", "Nov. 2021 (Rev.)","Nov. 2021 (Cost)","Nov. 2021 (Profit)"]
    y_list = []
    for index, row in df.iterrows():
        y_list.append(row.benefit)
        y_list.append(row.cost*-1)
        y_list.append(row.profit)
    fig = go.Figure(go.Waterfall(
                        orientation = "v",
                        measure = measure,
                        x = x,
                        y = y_list,
                        connector = {"line":{"color":"rgb(63, 63, 63)"}},
                    ))
    fig.update_layout(
        width = 1350,
        height = 280,
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        showlegend = False,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    for v_line in [2.5, 5.5, 8.5, 11.5, 14.5, 17.5, 20.5, 23.5, 26.5, 29.5, 32.5]:
        fig.add_vline(x=v_line, line_width=1, line_dash="dash", line_color="black")
    fig.update_xaxes(tickvals=[1.25, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34],
                    ticktext=["Dec. 2020", "Jan. 2021", "Feb. 2021", "Mar. 2021",
                            "Apr. 2021", "May. 2021", "Jun. 2021", "Jul. 2021",
                            "Aug. 2021", "Sep. 2021", "Oct. 2021", "Nov. 2021"])
    fig.update_yaxes(title_text="USD")
    return fig

def line_chart_invoices(df, counties):
    df = df.sort_values('date', ascending=True).set_index('date')
    df_sorted = df.groupby(pd.Grouper(freq="D")).count()[['invoice_and_item_number']]
    df_sorted['invoice_mean'] = df_sorted.invoice_and_item_number/df.county.nunique()
    df_sorted = df_sorted.reset_index()
    df_sorted['weekday'] = [x.weekday() for x in df_sorted.date]
    df_to_plot = df_sorted[(df_sorted['weekday'] != 5) & (df_sorted['weekday'] != 6)]
    v_lines = ["2020-12-31","2021-01-31","2021-02-28","2021-03-31","2021-04-30","2021-05-31",
               "2021-06-30","2021-07-31","2021-08-31","2021-09-30","2021-10-31","2021-11-30"]
    tick_vals = ["2020-12-15","2021-01-15","2021-02-15","2021-03-15","2021-04-15","2021-05-15",
                 "2021-06-15","2021-07-15","2021-08-15","2021-09-15","2021-10-15","2021-11-15"]
    fig = px.line(df_to_plot, x='date', y='invoice_mean',
              labels=dict(date="", invoice_and_item_number="Number of invoices"))
    if counties:
        for county in counties:
            df_county_sorted = df[df['county'] == county].groupby(pd.Grouper(freq="D")).count()[['invoice_and_item_number']]
            df_county_sorted = df_county_sorted.reset_index()
            df_county_sorted['weekday'] = [x.weekday() for x in df_county_sorted.date]
            df_county_to_plot = df_county_sorted[(df_county_sorted['weekday'] != 5) & (df_county_sorted['weekday'] != 6)]
            fig.add_trace(go.Scatter(x=df_county_to_plot["date"],
                                     y=df_county_to_plot["invoice_and_item_number"],
                                     name= county, mode='lines'))
    for v_line in v_lines:
        fig.add_vline(x=v_line, line_width=1, line_dash="dash", line_color="black")
    fig.update_xaxes(tickvals=tick_vals,
                    ticktext=["Dec. 2020", "Jan. 2021", "Feb. 2021", "Mar. 2021",
                            "Apr. 2021", "May. 2021", "Jun. 2021", "Jul. 2021",
                            "Aug. 2021", "Sep. 2021", "Oct. 2021", "Nov. 2021"])
    fig.update_yaxes(title_text="Number of invoices")
    fig.update_layout(
        width = 1350,
        height = 280,
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Rockwell"
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        showlegend = True,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig
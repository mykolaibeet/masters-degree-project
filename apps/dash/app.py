from dash import Dash, callback
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dash_table
import requests
import re
import pandas as pd
import requests
import statistics

CHART_THEME = 'plotly_white'  # others examples: seaborn, ggplot2, plotly_dark
chart_ptfvalue = go.Figure()  # generating a figure that will be updated in the following lines
chart_ptfvalue.add_trace(go.Scatter(x=[0], y=[0],
                                    mode='lines',  # you can also use "lines+markers", or just "markers"
                                    name='Global Value'))
chart_ptfvalue.layout.template = CHART_THEME
chart_ptfvalue.layout.height=500
chart_ptfvalue.update_layout(margin = dict(t=50, b=50, l=25, r=25))  # this will help you optimize the chart space
chart_ptfvalue.update_layout(
    #     title='Global Portfolio Value (USD $)',
    xaxis_tickfont_size=12,
    yaxis=dict(
        title='Value: $ USD',
        titlefont_size=14,
        tickfont_size=12,
    ))


indicators_ptf = go.Figure()
indicators_ptf.layout.template = CHART_THEME
indicators_ptf.add_trace(go.Indicator(
    mode = "number+delta",
    value = 0,
    number = {'suffix': " %"},
    title = {"text": "<br><span style='font-size:0.7em;color:gray'>1 Changes</span>"},
    delta = {'position': "bottom", 'reference': 0, 'relative': False},
    domain = {'row': 0, 'column': 0}))

indicators_ptf.add_trace(go.Indicator(
    mode = "number+delta",
    value = 0,
    number = {'suffix': " %"},
    title = {"text": "<span style='font-size:0.7em;color:gray'>5 Changes</span>"},
    delta = {'position': "bottom", 'reference': 0, 'relative': False},
    domain = {'row': 1, 'column': 0}))

indicators_ptf.add_trace(go.Indicator(
    mode = "number+delta",
    value = 0,
    number = {'suffix': " %"},
    title = {"text": "<span style='font-size:0.7em;color:gray'>10 Changes</span>"},
    delta = {'position': "bottom", 'reference': 0, 'relative': False},
    domain = {'row': 2, 'column': 0}))

indicators_ptf.add_trace(go.Indicator(
    mode = "number+delta",
    value = 0,
    number = {'suffix': " %"},
    title = {"text": "<span style='font-size:0.7em;color:gray'>30 Changes</span>"},
    delta = {'position': "bottom", 'reference': 0, 'relative': False},
    domain = {'row': 3, 'column': 1}))

indicators_ptf.update_layout(
    grid = {'rows': 4, 'columns': 1, 'pattern': "independent"},
    margin=dict(l=50, r=50, t=30, b=30)
)


indicators_social_media = go.Figure()
indicators_social_media.layout.template = CHART_THEME
indicators_social_media.add_trace(go.Indicator(
    mode = "number",
    value = 0,
    title = {"text": "<br><span style='font-size:0.7em;color:gray'>Discord</span>"},
    domain = {'row': 0, 'column': 0}))

indicators_social_media.add_trace(go.Indicator(
    mode = "number",
    value = 0,
    title = {"text": "<span style='font-size:0.7em;color:gray'>Twitter</span>"},
    domain = {'row': 1, 'column': 0}))

indicators_social_media.add_trace(go.Indicator(
    mode = "number",
    value = 0,
    title = {"text": "<span style='font-size:0.7em;color:gray'>Website</span>"},
    domain = {'row': 2, 'column': 0}))

indicators_social_media.add_trace(go.Indicator(
    mode = "number",
    value = 0,
    title = {"text": "<span style='font-size:0.7em;color:gray'>Badges</span>"},
    domain = {'row': 3, 'column': 1}))

indicators_social_media.update_layout(
    grid = {'rows': 4, 'columns': 1, 'pattern': "independent"},
    margin=dict(l=50, r=50, t=30, b=30)
)


fig_growth2 = go.Figure()
fig_growth2.layout.template = CHART_THEME
fig_growth2.add_trace(go.Bar(
    x=[0],
    y=[0],
    name='Portfolio'
))
fig_growth2.add_trace(go.Bar(
    x=[0],
    y=[0],
    name='S&P 500',
))
fig_growth2.update_layout(barmode='group')
fig_growth2.layout.height=300
fig_growth2.update_layout(margin = dict(t=50, b=50, l=25, r=25))
fig_growth2.update_layout(
    xaxis_tickfont_size=12,
    yaxis=dict(
        title='% change',
        titlefont_size=13,
        tickfont_size=12,
    ))

fig_growth2.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=0.99))


donut_top = go.Figure()
donut_top.layout.template = CHART_THEME
donut_top.add_trace(go.Indicator(mode = "gauge+number+delta",
                                 title = {'text': "Score"},
                                 value = 0,
                                 gauge = {'axis': {'range': [None, 10]},
                                          'steps' : [
                                              {'range': [0, 2], 'color': "#e03030"},
                                              {'range': [2, 4], 'color': "#aa5500"},
                                              {'range': [4, 6], 'color': "#746100"},
                                              {'range': [6, 8], 'color': "#48601c"},
                                              {'range': [8, 10], 'color': "#2a5838"}],
                                          'bar': {'color': "#d6d1d1"}}))
#donut_top.update_traces(hole=.4, hoverinfo="label+value+percent")
#donut_top.update_traces(textposition='outside', textinfo='label+value')
donut_top.update_layout(showlegend=False)
donut_top.update_layout(margin = dict(t=50, b=50, l=25, r=25))

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H2('NFT Analyzer', className='text-center text-primary, mb-3'))),

        dbc.Row(dbc.Col(dcc.Input(
            id="nft_url",
            placeholder="NFT URL",
            className='text-center text-primary, mb-3',
            style={'width':950}
        ))),  # header row

        dbc.Row([  # start of second row
            dbc.Col([  # first column on second row
            html.Iframe(id="nft_render", height=575, width=950),
            html.Hr(),
            ], width={'size': 8, 'offset': 0, 'order': 1}),  # width first column on second row
            dbc.Col([  # second column on second row
            html.H5('Changes', className='text-center'),
            dcc.Graph(id='indicators-ptf',
                      figure=indicators_ptf,
                      style={'height':550}),
            html.Hr()
            ], width={'size': 2, 'offset': 0, 'order': 2}),  # width second column on second row
            dbc.Col([  # third column on second row
            html.H5('Social media', className='text-center'),
            dcc.Graph(id='indicators-sm',
                      figure=indicators_social_media,
                      style={'height':550}),
            html.Hr()
            ], width={'size': 2, 'offset': 0, 'order': 3}),  # width third column on second row
        ]),  # end of second row

        dbc.Row([  # start of third row
            dbc.Col([  # first column on second row
                html.H5('History price', className='text-center'),
                dcc.Graph(id='chrt-portfolio-main',
                          figure=chart_ptfvalue,
                          style={'height':550}),
                html.Hr(),
            ], width={'size': 8, 'offset': 0, 'order': 1}),  # width first column on second row
            dbc.Col([  # second column on third row
                html.H5('Score', className='text-center'),
                dcc.Graph(id='pie-top15',
                      figure = donut_top,
                      style={'height':380}),
            ], width={'size': 4, 'offset': 0, 'order': 2}),  # width second column on second row
        ])  # end of third row

    ], fluid=True)

def json_rpc_call(method, params):
    url = "http://solana-processor:5000"

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }
    response = requests.post(url, json=payload)
    return response.json()

@callback(
    Output("nft_render", "src"),
    Input("nft_url", "value"),
    prevent_initial_call=True
)
def renderer(url):
    return url

@callback(
    Output("chrt-portfolio-main", "figure"),
    Input("nft_url", "value"),
    prevent_initial_call=True
)
def history(url):

    data = json_rpc_call("process", {"url": url})

    data = data['result']

    chart_ptfvalue = go.Figure()  # generating a figure that will be updated in the following lines
    chart_ptfvalue.add_trace(go.Scatter(x=data['dates'], y=data['prices'],
                                        mode='lines',  # you can also use "lines+markers", or just "markers"
                                        name='Global Value'))
    chart_ptfvalue.layout.template = CHART_THEME
    chart_ptfvalue.layout.height=500
    chart_ptfvalue.update_layout(margin = dict(t=50, b=50, l=25, r=25))  # this will help you optimize the chart space
    chart_ptfvalue.update_layout(
        #     title='Global Portfolio Value (USD $)',
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Price for NFT',
            titlefont_size=14,
            tickfont_size=12,
        ))

    return chart_ptfvalue

@callback(
    Output("pie-top15", "figure"),
    Input("nft_url", "value"),
    prevent_initial_call=True
)
def score(url):

    data = json_rpc_call("process", {"url": url})

    data = data['result']

    price_median_weight = 0.01
    offer_weight = 0.01
    discord_weight = 1.5
    website_weight = 2.0
    twitter_weight = 1.5
    badge_weight = 3.0

    price_median = statistics.median(data['prices'])
    price_max = max(data['prices'])
    price_min = min(data['prices'])
    price_score = min(100, ((price_median * price_max) / 100)) * price_median_weight
    #
    # offer_score = min(100, (data['last_offer'] * price_max) / 100) * offer_weight
    #
    # discord_score = data['isDiscord'] * discord_weight
    #
    # website_score = data['isSite'] * website_weight
    #
    # twitter_score = data['isTwitter'] * twitter_weight
    #
    # badge_score = data['isBadget'] * badge_weight

    score = price_score # + offer_score + discord_score + website_score + twitter_score + badge_score

    donut_top = go.Figure()
    donut_top.layout.template = CHART_THEME
    donut_top.add_trace(go.Indicator(mode = "gauge+number+delta",
                                     title = {'text': "Score"},
                                     value = score,
                                     gauge = {'axis': {'range': [None, 10]},
                                              'steps' : [
                                                  {'range': [0, 2], 'color': "#e03030"},
                                                  {'range': [2, 4], 'color': "#aa5500"},
                                                  {'range': [4, 6], 'color': "#746100"},
                                                  {'range': [6, 8], 'color': "#48601c"},
                                                  {'range': [8, 10], 'color': "#2a5838"}],
                                              'bar': {'color': "#d6d1d1"}}))
    #donut_top.update_traces(hole=.4, hoverinfo="label+value+percent")
    #donut_top.update_traces(textposition='outside', textinfo='label+value')
    donut_top.update_layout(showlegend=False)
    donut_top.update_layout(margin = dict(t=50, b=50, l=25, r=25))

    return donut_top

# @callback(
#     Output("indicators-ptf", "figure"),
#     Input("nft_url", "value"),
#     prevent_initial_call=True
# )
# def indicator_1(url):
#
#     data = json_rpc_call("process", {"url": url})
#
#     data = data['result']
#
#     indicators_ptf = go.Figure()
#     indicators_ptf.layout.template = CHART_THEME
#     indicators_ptf.add_trace(go.Indicator(
#         mode = "number+delta",
#         value = data['prices'][-1],
#         number = {'suffix': " "},
#         title = {"text": "<br><span style='font-size:0.7em;color:gray'>1 Changes</span>"},
#         delta = {'position': "bottom", 'reference': data['prices'][-1], 'relative': False},
#         domain = {'row': 0, 'column': 0}))
#
#     indicators_ptf.add_trace(go.Indicator(
#         mode = "number+delta",
#         value = 0,
#         number = {'suffix': " %"},
#         title = {"text": "<span style='font-size:0.7em;color:gray'>5 Changes</span>"},
#         delta = {'position': "bottom", 'reference': data['prices'][-1], 'relative': False},
#         domain = {'row': 1, 'column': 0}))
#
#     indicators_ptf.add_trace(go.Indicator(
#         mode = "number+delta",
#         value = 0,
#         number = {'suffix': " %"},
#         title = {"text": "<span style='font-size:0.7em;color:gray'>10 Changes</span>"},
#         delta = {'position': "bottom", 'reference': data['prices'][-1], 'relative': False},
#         domain = {'row': 2, 'column': 0}))
#
#     indicators_ptf.add_trace(go.Indicator(
#         mode = "number+delta",
#         value = 0,
#         number = {'suffix': " %"},
#         title = {"text": "<span style='font-size:0.7em;color:gray'>30 Changes</span>"},
#         delta = {'position': "bottom", 'reference': data['prices'][-1], 'relative': False},
#         domain = {'row': 3, 'column': 1}))
#
#     indicators_ptf.update_layout(
#         grid = {'rows': 4, 'columns': 1, 'pattern': "independent"},
#         margin=dict(l=50, r=50, t=30, b=30)
#     )
#
#     return indicators_ptf
#
# @callback(
#     Output("indicators-sm", "figure"),
#     Input("nft_url", "value"),
#     prevent_initial_call=True
# )
# def indicator_2(url):
#
#     data = json_rpc_call("process", {"url": url})
#
#     data = data['result']
#
#     indicators_social_media = go.Figure()
#     indicators_social_media.layout.template = CHART_THEME
#     indicators_social_media.add_trace(go.Indicator(
#         mode = "number",
#         value = data['isDiscord'],
#         title = {"text": "<br><span style='font-size:0.7em;color:gray'>Discord</span>"},
#         domain = {'row': 0, 'column': 0}))
#
#     indicators_social_media.add_trace(go.Indicator(
#         mode = "number",
#         value = data['isTwitter'],
#         title = {"text": "<span style='font-size:0.7em;color:gray'>Twitter</span>"},
#         domain = {'row': 1, 'column': 0}))
#
#     indicators_social_media.add_trace(go.Indicator(
#         mode = "number",
#         value = data['isSite'],
#         title = {"text": "<span style='font-size:0.7em;color:gray'>Website</span>"},
#         domain = {'row': 2, 'column': 0}))
#
#     indicators_social_media.add_trace(go.Indicator(
#         mode = "number",
#         value = data['isBadget'],
#         title = {"text": "<span style='font-size:0.7em;color:gray'>Badges</span>"},
#         domain = {'row': 3, 'column': 1}))
#
#     indicators_social_media.update_layout(
#         grid = {'rows': 4, 'columns': 1, 'pattern': "independent"},
#         margin=dict(l=50, r=50, t=30, b=30)
#     )
#
#     return indicators_social_media

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050, use_reloader=True)


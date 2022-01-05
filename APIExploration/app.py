import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from connection import one_day_curve, infos
import dash_bootstrap_components as dbc
import dash_table
import json


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = html.Div(children=[
    html.H1(children='Crypto currency dashboard'),

    html.Div([
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='currency',
                options=[
                    {'label': 'ETH', 'value': 'ETHUSDT'},
                    {'label': 'BNB', 'value': 'BNBUSDT'},
                    {'label': 'XRP', 'value': 'XRPUSDT'},
                    {'label': 'XRP', 'value': 'XRPUSDT'},
                    {'label': 'LTC', 'value': 'LTCUSDT'},
                    {'label': 'DOT', 'value': 'DOTUSDT'},
                    {'label': 'VET', 'value': 'VETUSDT'},
                    {'label': 'BTC', 'value': 'BTCUSDT'},
                    {'label': 'FET', 'value': 'FETUSDT'}
                ],
                value='BTCUSDT'
            )),
            dbc.Col(dcc.Dropdown(
                id='time',
                options=[
                    {'label':'minutes', 'value':'15 minutes ago UTC'},
                    {'label':'hour', 'value':'1 hour ago UTC'},
                    {'label':'day', 'value':'1 day ago UTC'},
                    {'label':'week', 'value':'1 week ago UTC'},
                    {'label':'month', 'value':'1 month ago UTC'},
                ],
                value='1 day ago UTC'
            ))
        ])
    ]),
    
    html.Br(),

    html.Div([
        dbc.Row([
            dbc.Col(html.Div(id='one_day')),
            dbc.Col(html.Div(id='infos'))
        ])
    ]),

    
])

@app.callback(
    Output(component_id='one_day', component_property='children'),
    [Input(component_id='currency', component_property='value'),
    (Input(component_id='time', component_property='value'))]
)
def update_graph_one_day(value, time):
    return dcc.Graph(figure=one_day_curve(value, time))

@app.callback(
    Output(component_id='infos', component_property='children'),
    Input(component_id='currency', component_property='value')
)
def info(value):

    df = pd.DataFrame.from_dict(json.loads(infos(value)), orient='index').transpose()
    df = df[['baseAsset','status', 'orderTypes','permissions']]
    return [dash_table.DataTable(
            style_cell={
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0
            },
            style_header={
                'backgroundColor':'blue',
                'fontWeight':'bold'
            },
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
            ],
            tooltip_delay=0,
            tooltip_duration=None,
            data=df.to_dict('rows'),
            columns=[{"name": i, "id": i,} for i in (df.columns)]
            )]


if __name__ == '__main__':
    app.run_server(debug=True, port=8001)
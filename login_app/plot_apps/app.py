from django_plotly_dash import DjangoDash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from login_app.models import *
import sqlite3
import dash

app = DjangoDash('SimpleExample')   # replaces dash.Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cnx = sqlite3.connect('db.sqlite3')

df = pd.read_sql_query("SELECT * FROM login_app_city", cnx)

app.layout = html.Div([
    dcc.Graph(
        id='temp-vs-airpollution',
        figure={
            'data': [
                dict(
                    x=df['temp'],
                    y=df['aqi'],
                    text=df['city_name'],
                    mode='markers',
                    opacity=0.7,
                    markers={
                        'size': 40,
                        'color' : 'rgba(135, 206, 250, 0.5)',
                        'line': {'width': 0.5,}
                    },
                    name=i
                ) for i in df.city_name.unique()
            ],
            'layout': dict(
                xaxis={'type': 'scatter', 'title': 'Temperature', 'range': [0,75]},
                yaxis={'title': 'Air Quality Index', 'range': [0,75]},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
from django_plotly_dash import DjangoDash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from login_app.models import *
import sqlite3

app = DjangoDash('SimpleExample')   # replaces dash.Dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
print('IM UPDATING PLOT FROM THE PY FILE')

cnx = sqlite3.connect('db.sqlite3')
<<<<<<< HEAD


=======
>>>>>>> c44eb343dbbceb55cae2862fed4f6a387fc401de
df = pd.read_sql_query("SELECT * FROM login_app_city", cnx)

app.layout = html.Div([
    dcc.Graph(
        id='temp-vs-airpollution',
        figure={
            'data': [
                dict(
                    x=df[df['impact'] == i]['temp'],
                    y=df[df['impact'] == i]['aqi'],
                    text=df[df['impact'] == i]['city_name'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.impact.unique()
            ],
            'layout': dict(
                xaxis={'type': 'scatter', 'title': 'Temperature', 'range': [0,150]},
                yaxis={'title': 'Air Quality Index', 'range': [0,150]},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

print("JUST RAN THE APP.PY FILE")
print(df)

if __name__ == '__main__':
<<<<<<< HEAD
    print('hello')
    app.run_server(debug=True)
=======
    app.run_server(debug=True)
>>>>>>> c44eb343dbbceb55cae2862fed4f6a387fc401de

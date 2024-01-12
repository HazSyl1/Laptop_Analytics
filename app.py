import dash
from dash import dcc,html
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px 
import plotly.graph_objects as go
from dash.dependencies import Input,Output

server=Flask(__name__)
app=dash.Dash(__name__ , server=server,external_stylesheets=[dbc.themes.UNITED,dbc.icons.BOOTSTRAP])

df=pd.read_csv('Cleaned_Laptop_data.csv')


Header_component=html.H1("Laptop Analysis (Amazon)",style={'color':'darkred','text-align':'center','font-size':72})


barfig=go.FigureWidget(
    data=[
        go.Bar(
            x= df['brand'].value_counts().keys().tolist(),
            y= df['brand'].value_counts().tolist(),
            marker_color="skyblue",
            textposition='auto'
        )
    ]
)
barfig.update_layout(
    title='LAPTOP BRAND DISTRIBUTION'
)


app.layout =html.Div(
    [
        dbc.Row(Header_component),
        dbc.Row(
            [dbc.Col(
                [dcc.Graph(figure=barfig)]
                ),dbc.Col()]
        ),
        dbc.Row(
            [dbc.Col(),dbc.Col(),dbc.Col()]
        ),
    ]
)

app.run_server(debug=True)
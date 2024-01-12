import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input ,Output
import plotly.express as px

external_stylesheets=[
    {
        'href':"https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" ,
        'rel': 'stylesheet',
        'integrity':"sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T",
        'crossorigin': 'anonymous'
    }
]


df=pd.read_csv("Cleaned_Laptop_data.csv")
brand_noms=df['brand'].unique().shape[0]
price_range=f"{df['latest_price'].max():,}-{df['latest_price'].min():,} " 
models=df['model'].unique().shape[0]
os=df['os'].unique().shape[0]
options=[
    {'label': 'All','value':'All'},
    {'label': 'ASUS', 'value': 'ASUS'}, {'label': 'DELL', 'value': 'DELL'}, {'label': 'Lenovo', 'value': 'Lenovo'}, {'label': 'HP', 'value': 'HP'}, {'label': 'acer', 'value': 'acer'}, {'label': 'MSI', 'value': 'MSI'}, {'label': 'APPLE', 'value': 'APPLE'}, {'label': 'Avita', 'value': 'Avita'}, {'label': 'Vaio', 'value': 'Vaio'}, {'label': 'LG', 'value': 'LG'}, {'label': 'ALIENWARE', 'value': 'ALIENWARE'}, {'label': 'realme', 'value': 'realme'}, {'label': 'Nokia', 'value': 'Nokia'}, {'label': 'lenovo', 'value': 'lenovo'}, {'label': 'Smartron', 'value': 'Smartron'}, {'label': 'MICROSOFT', 'value': 'MICROSOFT'}, {'label': 'Infinix', 'value': 'Infinix'}, {'label': 'RedmiBook', 'value': 'RedmiBook'}, {'label': 'Mi', 'value': 'Mi'}, {'label': 'iball', 'value': 'iball'}, {'label': 'SAMSUNG', 'value': 'SAMSUNG'}
    
]

app= dash.Dash(__name__, external_stylesheets=external_stylesheets)


piep=go.Figure(data=[go.Pie(labels=df['brand'].unique() , values=df['brand'].value_counts().tolist())])

app.layout=html.Div([
    html.H1("Laptop Analysis",style={'color': 'rgb(255, 255, 255)', 'text-align': 'center'}),
    html.Br(),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Brands",className="text-light"),
                    html.H4(brand_noms,className="text-light")
                    ],className='card-body')
                ],className='card bg-info')
            ],className='col-md-3'),
        html.Div([html.Div([
                html.Div([
                    html.H3("Price Range",className="text-light"),
                    html.H4(price_range,className="text-light")
                    ],className='card-body')
                ],className='card bg-success')],className='col-md-3'), 
        html.Div([html.Div([
                html.Div([
                    html.H3("Operating Systems",className="text-light"),
                    html.H4(os,className="text-light")
                    ],className='card-body')
                ],className='card bg-primary')],className='col-md-4'),
        html.Div([html.Div([
                html.Div([
                    html.H3("Models",className="text-light"),
                    html.H4(models,className="text-light")
                    ],className='card-body')
                ],className='card bg-warning')],className='col-md-2')
        ],className='row'),
    
    html.Div([
       html.Div([
           
           ],className='col-md-8'),
       html.Div([
           dcc.Graph(figure=piep)
           ],className='col-md-4'),
       
        ],className='row'),
    html.Div([
        
        html.Div([
            html.Div([
                html.Div([
                    # DROPDOWN
                    dcc.Dropdown(id='picker',options=options ,value='All'),
                    dcc.Graph(id='bar')
                    
                    ],className='card-body')
                ],className='card')
            ],className='col-md-12'),
        
        ],className='row')
    ],className='container')


@app.callback(Output('bar','figure'),[Input('picker','value')])
def update_graph(type):
    
    if type=='All':    
        return {'data':[
            go.Bar(x=df['brand'].value_counts().keys().tolist(), y=df['brand'].value_counts().tolist())
            ],
                'layout':go.Layout(title='Stats')}
    else:
        units=df[df['brand']==type].shape[0]
        model=df[df['brand']==type].model.unique().shape[0]
        proc=df[df['brand']==type].processor_name.unique().shape[0]
        gpu=df[df['brand']==type].graphic_card_gb.unique().shape[0]
        ram=df[df['brand']==type].ram_gb.unique().shape[0]
        ssd=(df[df['brand']==type].ssd != "0 GB").sum()
        hdd=(df[df['brand']==type].hdd != "0 GB").sum()
        hdd_and_ssd=df[(df['brand'] == type) & (df['ssd'] != "0 GB") & (df['hdd'] != "0 GB")].shape[0]
        titles=['Units','Model Options','Processors Options', 'GPU Options' ,'RAM Options','SSD','HDD','SSD and HDD']
        vals=[units,model,proc,gpu,ram,ssd,hdd,hdd_and_ssd]
        
        return {'data':[
            go.Bar(x=titles, y=vals)
            ],
                'layout':go.Layout(title='Brand Stats')}
        

        
        
        
        
        

if __name__ == '__main__':
    app.run_server(debug=True)
    
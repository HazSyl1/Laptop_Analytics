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
price_range=f"{df['latest_price'].min():,} - {df['latest_price'].max():,}" 
models=df['model'].unique().shape[0]
os=df['os'].unique().shape[0]
brands=df['brand'].unique()
avg_ratings=[round(df[df['brand']==x]['star_rating'].mean()) for x in brands]
avg_prices=[round(df[df['brand']==x]['latest_price'].mean()) for x in brands]

options=[
    {'label': 'All','value':'All'},
    {'label': 'ASUS', 'value': 'ASUS'}, {'label': 'DELL', 'value': 'DELL'}, {'label': 'Lenovo', 'value': 'Lenovo'}, {'label': 'HP', 'value': 'HP'}, {'label': 'acer', 'value': 'acer'}, {'label': 'MSI', 'value': 'MSI'}, {'label': 'APPLE', 'value': 'APPLE'}, {'label': 'Avita', 'value': 'Avita'}, {'label': 'Vaio', 'value': 'Vaio'}, {'label': 'LG', 'value': 'LG'}, {'label': 'ALIENWARE', 'value': 'ALIENWARE'}, {'label': 'realme', 'value': 'realme'}, {'label': 'Nokia', 'value': 'Nokia'}, {'label': 'lenovo', 'value': 'lenovo'}, {'label': 'Smartron', 'value': 'Smartron'}, {'label': 'MICROSOFT', 'value': 'MICROSOFT'}, {'label': 'Infinix', 'value': 'Infinix'}, {'label': 'RedmiBook', 'value': 'RedmiBook'}, {'label': 'Mi', 'value': 'Mi'}, {'label': 'iball', 'value': 'iball'}, {'label': 'SAMSUNG', 'value': 'SAMSUNG'}
    
]

app= dash.Dash(__name__, external_stylesheets=external_stylesheets,title="Laptop Analysis")
server=app.server

#piep=go.Figure(data=[go.Pie(labels=df['brand'].unique() , values=df['brand'].value_counts().tolist())])
piep=px.pie(labels=df['brand'].unique() , values=df['brand'].value_counts().tolist(),title="Porportion of Market",hole=0.2,names=df['brand'].unique())
# piep.update_traces(hoverinfo='label+value',textinfo='')
piep.update_traces(textposition='inside')
piep.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
piep.update_layout(paper_bgcolor='rgba(0,0,0,0)')

three_plot=fig = px.scatter_3d( x=brands, y=avg_prices, z=avg_ratings,color=brands , size_max=12, opacity=0.8,text=['Brand','Avg Price','Avg Rating (5)'])
three_plot.update_layout(paper_bgcolor='rgba(0,0,0,0)')

app.layout=html.Div([
    html.Br(),
    html.H1("Laptop Analysis",style={'color': 'rgb(255, 255, 255)', 'text-align': 'center' , 'font-family': 'Georgia,serif'}),
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
    html.Br(),
    #PIECHART (MIDDLE ROW)
    html.Div([
       html.Div([
           dcc.Graph(figure=three_plot,
                     style={ 'border-radius':'15px', 'background-color':'white'}),
           
           ],className='col-md-8'),
       html.Div([
           dcc.Graph(figure=piep,style={ 'border-radius':'15px', 'background-color':'white'})
           ],className='col-md-4'),
       
        ],className='row'),
    html.Br(),
    html.Div([
        
        html.Div([
            html.Div([
                html.Div([
                    # DROPDOWN
                    dcc.Dropdown(id='picker',options=options ,value='All'),
                    dcc.Graph(id='bar',style={ 'border-radius':'15px', 'background-color':'white'})
                    
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
                'layout':go.Layout(title='Stats',paper_bgcolor='rgba(0,0,0,0)')}
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
                'layout':go.Layout(title='Brand Stats',paper_bgcolor='rgba(0,0,0,0)' )}
        

        
        
        
        
        

if __name__ == '__main__':
    app.run_server(debug=True)
    

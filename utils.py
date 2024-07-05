import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

# Connect to the database
connection = create_engine('mysql+pymysql://root:{}@121.43.63.51/sdm'.format(os.getenv('MYSQL_ROOT_PASSWORD')))
princess = pd.read_sql_table('princess_plus_sales', connection)
dwarf = pd.read_sql_table('dwarf_plus_sales', connection)
superman = pd.read_sql_table('superman', connection)
superman_plus = pd.read_sql_table('superman_plus_channels', connection)

regions = ['AMR', 'Europe', 'PAC']
toys = ['Dwarf', 'Princess', 'Superman (Predicted)']
superman_models = ['Superman', 'Superman Plus', 'Superman Mini']
superman_plus_channels = ['Online Store', 'Retail Store', 'Reseller Partners-AMR', 'Reseller Partners-Europe', 'Reseller Partners-PAC']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

shared_weeks = dwarf['week'][dwarf['week'].isin(princess['week'])].values
princess_shared = princess[princess['week'].isin(shared_weeks)]
dwarf_shared = dwarf[dwarf['week'].isin(shared_weeks)]
promotion = 1.05 # assume 5% increase in sales for Superman from Princess
comparison = {}

for region in regions:
    comparison[region] = (dwarf_shared[region].values / princess_shared[region].values).mean()

def get_sales(toy):
    # Prevent injection
    assert toy in toys
    
    if toy == toys[-1]:
        return _get_superman()
    if toy == 'Dwarf':
        data = dwarf
    else:
        data = princess
    fig = px.line(data, x='week', y=regions, markers='lines+markers', title=f'{toy} Plus Sales (Year - {2 - toys.index(toy)})')
    fig.update_layout(
        yaxis_title='sales',
    )
    fig.update_legends(title_text='region')
    return fig

def get_comparison(region):
    # Prevent injection
    assert region in regions

    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Scatter(x=princess_shared['week'].values, y=princess_shared[region].values, name='Princess Plus'))
    fig.add_trace(go.Scatter(x=dwarf_shared['week'].values, y=dwarf_shared[region].values, name='Dwarf Plus'))
    fig.add_trace(go.Scatter(x=dwarf_shared['week'].values, 
                            y=dwarf_shared[region].values / princess_shared[region].values, 
                            name='Dwarf Plus / Princess Plus',
                            mode='markers',
                            visible='legendonly',
                            marker=dict(
                                symbol='circle',
                                size=10, 
                                color='green'
                            )),
                secondary_y=True)
    fig.add_trace(go.Scatter(x=dwarf_shared['week'].values, 
                            y=[comparison[region]] * len(dwarf_shared[region]), 
                            name='Dwarf Plus / Princess Plus average',
                            mode='lines',
                            visible='legendonly',
                            line=dict(
                                dash='dash', 
                                color='green'
                            )),
                secondary_y=True)
    fig.update_layout(
        title_text=f'{region} Region Sales Comparison',
        xaxis_title='week',
        yaxis_title='sales',
        yaxis2_title='Dwarf Plus / Princess Plus',
    )
    fig.update_legends(title_text='toy')
    return fig
    
def _get_superman():
    idx = 5
    princess_short = dwarf.iloc[:idx].copy()
    for region in regions:
        princess_short[region] = princess_short[region] / comparison[region]
    princess_long = pd.concat([princess_short, princess.iloc[:-idx]], axis=0)

    superman_long = princess_long.copy()
    for region in regions:
        superman_long[region] = superman_long[region] * promotion
    
    # smooth AMR Oct wk4, treat it as anomaly
    superman_long.loc[superman_long['week'] == 'Oct wk4', 'AMR'] = ((superman_long.loc[superman_long['week'] == 'Oct wk3', 'AMR'].values + 
                                                                     superman_long.loc[superman_long['week'] == 'Oct wk5', 'AMR'].values) / 2)

    fig = px.line(superman_long, x='week', y=regions, markers='lines+markers', title='Superman Plus Sales (Predicted)')
    fig.update_layout(
        yaxis_title='sales',
    )
    fig.update_legends(title_text='region')
    return fig

def get_superman_all(models):
    # Prevent injection
    assert set(models).issubset(set(superman_models))

    traces_demand = [go.Scatter(x=superman[(superman['model'] == model) & (superman['type'] == 'demand')]['week'].values,
                                y=superman[(superman['model'] == model) & (superman['type'] == 'demand')]['amount'].values,
                                name=model + '-demand',
                                marker=dict(
                                    symbol='cross',
                                    size=10,
                                    color=colors[i]
                                )) for i, model in enumerate(models)]
    traces_supply = [go.Scatter(x=superman[(superman['model'] == model) & (superman['type'] == 'supply')]['week'].values,
                                y=superman[(superman['model'] == model) & (superman['type'] == 'supply')]['amount'].values,
                                name=model + '-supply',
                                marker=dict(
                                    symbol='circle',
                                    size=10,
                                    color=colors[i]
                                )) for i, model in enumerate(models)]
    fig = go.Figure(data=traces_demand + traces_supply)
    fig.update_layout(
        yaxis_title='amount',
        title='Superman Model Supply VS. Demand'
    )
    fig.update_legends(title_text='type')
    fig.update_layout(barmode='group')
    return fig

def get_superman_plus(channels):
    # Prevent injection
    assert set(channels).issubset(set(superman_plus_channels))

    traces_demand = [go.Scatter(x=superman_plus[(superman_plus['channel'] == channel) & (superman_plus['type'] == 'demand')]['week'].values,
                                y=superman_plus[(superman_plus['channel'] == channel) & (superman_plus['type'] == 'demand')]['amount'].values,
                                name=channel + '-demand',
                                marker=dict(
                                    symbol='cross',
                                    size=10,
                                    color=colors[i]
                                )) for i, channel in enumerate(channels)]
    traces_supply = [go.Scatter(x=superman_plus[(superman_plus['channel'] == channel) & (superman_plus['type'] == 'supply')]['week'].values,
                                y=superman_plus[(superman_plus['channel'] == channel) & (superman_plus['type'] == 'supply')]['amount'].values,
                                name=channel + '-supply',
                                marker=dict(
                                    symbol='circle',
                                    size=10,
                                    color=colors[i]
                                )) for i, channel in enumerate(channels)]
    fig = go.Figure(data=traces_demand + traces_supply)
    fig.update_layout(
        yaxis_title='amount',
        title='Superman Plus Channels Supply VS. Demand'
    )
    fig.update_legends(title_text='type')
    fig.update_layout(barmode='group')
    return fig
    
if __name__ == '__main__':
    # get_comparison('AMR').show()
    pass
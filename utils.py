import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


princess = pd.read_csv('PrincessPlusSales.csv')
dwarf = pd.read_csv('DwarfPlusSales.csv')
regions = ['AMR', 'Europe', 'PAC']
toys = ['Dwarf', 'Princess', 'Superman (Predicted)']
shared_weeks = dwarf['week'][dwarf['week'].isin(princess['week'])].values
princess_shared = princess[princess['week'].isin(shared_weeks)]
dwarf_shared = dwarf[dwarf['week'].isin(shared_weeks)]
promotion = 1.05 # assume 5% increase in sales for Superman from Princess
comparison = {}

for region in regions:
    comparison[region] = (dwarf_shared[region].values / princess_shared[region].values).mean()

def get_sales(toy):
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

    
if __name__ == '__main__':
    # get_comparison('AMR').show()
    pass
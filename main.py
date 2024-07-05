import os
import sys
os.chdir(sys.path[0])
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from utils import get_comparison, get_sales, get_superman_all, get_superman_plus, regions, toys, superman_models, superman_plus_channels


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        [html.H1('SUPERMAN DASHBOARD')],
        style={'textAlign': 'center'}
    ),
    html.Div([
        html.H2('Please select a toy type from dropdown.'),
        dcc.Dropdown(
            id='dropdown-sales',
            options=toys,
            value=toys[1]
        ),
        dcc.Graph(
            id='graph-sales',
            figure=get_sales(toys[1])
        )
    ], style={'width': '44%', 'display': 'inline-block', 'vertical-align': 'top', 'marginRight': '2%', 'marginLeft': '2%'}),
    html.Div([
        html.H2('Please select a region from dropdown.'),
        dcc.Dropdown(
            id='dropdown-comparison',
            options=regions,
            value=regions[0]
        ),
        dcc.Graph(
            id='graph-comparison',
            figure=get_comparison(regions[0])
        )
    ], style={'width': '44%', 'display': 'inline-block', 'vertical-align': 'top', 'marginRight': '2%', 'marginLeft': '2%'}),
    html.Div([
        html.H2('Please select 1 to 3 superman models from dropdown.'),
        dcc.Dropdown(
            id='dropdown-superman',
            options=superman_models,
            value=superman_models[:1],
            multi=True
        ),
        dcc.Graph(
            id='graph-superman',
            figure=get_superman_all(superman_models)
        )
    ], style={'width': '44%', 'display': 'inline-block', 'vertical-align': 'top', 'marginRight': '2%', 'marginLeft': '2%'}),
    html.Div([
        html.H2('Please select 1 to 5 Superman Plus channels from dropdown.'),
        dcc.Dropdown(
            id='dropdown-superman-plus',
            options=superman_plus_channels,
            value=superman_plus_channels[:1],
            multi=True
        ),
        dcc.Graph(
            id='graph-superman-plus',
            figure=get_superman_plus(superman_plus_channels)
        )
    ], style={'width': '44%', 'display': 'inline-block', 'vertical-align': 'top', 'marginRight': '2%', 'marginLeft': '2%'}),
])

@app.callback(
    Output('graph-comparison', 'figure'),
    Input('dropdown-comparison', 'value')
)
def update_comparison(input_value):
    return get_comparison(input_value)

@app.callback(
    Output('graph-sales', 'figure'),
    Input('dropdown-sales', 'value')
)
def update_sales(input_value):
    return get_sales(input_value)


@app.callback(
    Output('graph-superman', 'figure'),
    Input('dropdown-superman', 'value')
)
def update_superman_all(input_value):
    return get_superman_all(input_value)

@app.callback(
    Output('graph-superman-plus', 'figure'),
    Input('dropdown-superman-plus', 'value')
)
def update_superman_plus(input_value):
    return get_superman_plus(input_value)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
import os
import sys
os.chdir(sys.path[0])
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from utils import get_comparison, get_sales, regions, toys


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        [html.H1('SUPERMAN DASHBOARD')],
        style={'textAlign': 'center'}
    ),
    html.Div([
        html.H2('Please select a toy type from drop down.'),
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
        html.H2('Please select a region from drop down.'),
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


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
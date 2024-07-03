import os
import sys
os.chdir(sys.path[0])
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

# 创建一个Dash应用实例
app = dash.Dash(__name__)

# 定义应用的布局
app.layout = html.Div([
    html.H1('Hello, Dash!'),
    html.Div('This is a simple Dash app')
])

# 运行应用
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
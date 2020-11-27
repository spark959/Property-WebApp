import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime as dt

def MainTabHtml(width):
    main_tab_html = html.Div([
                         html.H3('Main Tab')
    ])
    return main_tab_html
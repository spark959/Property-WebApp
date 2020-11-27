import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime as dt


def InvestmentTabHtml(width):       
    investment_tab_html = html.Div([
            html.H1('Investment Calculator'),
            html.H2('Investment Calculator Inputs'),
            html.H2('Mortgage Calculator Outputs')])

    return investment_tab_html



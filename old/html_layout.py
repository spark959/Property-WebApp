import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import flask
import pandas as pd
import time
import os
import numpy as np
import datetime as dt

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button("Search", color="primary", className="ml-2"),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

def HtmlLayout():
    input_html = html.Div([
                
                dbc.Navbar(
                        [
                                html.A(
                                # Use row and col to control vertical alignment of logo / brand
                                dbc.Row(
                                        [
                                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                                        dbc.Col(dbc.NavbarBrand("Navbar", className="ml-2")),
                                        ],
                                        align="center",
                                        no_gutters=True,
                                ),
                                href="https://plot.ly",
                                ),
                                dbc.NavbarToggler(id="navbar-toggler"),
                                dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
                        ],
                        color="dark",
                        dark=True),
                dcc.Tabs(id='all_tabs', value='main_tab', children=[
                        
                        dcc.Tab(label='Main', value='main_tab'),
                        dcc.Tab(label='Debits', value='debit_tab', children=[
                                dcc.Tabs(id='debit_tabs', value='debit1', children=[
                                        dcc.Tab(label='Debit 1', value='debit1'),
                                        dcc.Tab(label='Debit 2', value='debit2'),
                                        dcc.Tab(label='Debit 3', value='debit3'),
                                        dcc.Tab(label='Add Debit', value='add_debit')
                                ]),
                                html.Div(id='current_debit_tab_content')
                        ]),
                        dcc.Tab(label='Credits', value='credit_tab', children=[
                                dcc.Tabs(id='credit_tabs', value='credit1', children=[
                                        dcc.Tab(label='Credit 1', value='credit1'),
                                        dcc.Tab(label='Credit 2', value='credit2'),
                                        dcc.Tab(label='Credit 3', value='credit3'),
                                        dcc.Tab(label='Add Credit', value='add_credit')
                                ]),
                                html.Div(id='current_credit_tab_content')
                        ]),
                        dcc.Tab(label='Investments', value='investment_tab', children=[
                                dcc.Tabs(id='investment_tabs', value='investment1', children=[
                                        dcc.Tab(label='Investment 1', value='investment1'),
                                        dcc.Tab(label='Investment 2', value='investment2'),
                                        dcc.Tab(label='Investment 3', value='investment3'),
                                        dcc.Tab(label='Add Investment', value='add_investment')
                                ]),
                                html.Div(id='current_investment_tab_content')
                        ]),
                        dcc.Tab(label='Debts', value='debt_tab', children=[
                                dcc.Tabs(id='debt_tabs', value='debt1', children=[
                                        dcc.Tab(label='Debt 1', value='debt1'),
                                        dcc.Tab(label='Debt 2', value='debt2'),
                                        dcc.Tab(label='Debt 3', value='debt3'),
                                        dcc.Tab(label='Add Debt', value='add_debt')
                                ]),
                                html.Div(id='current_debt_tab_content')
                        ]),
                html.Div(id='current_tab_content')
                ])
        ])
    return input_html
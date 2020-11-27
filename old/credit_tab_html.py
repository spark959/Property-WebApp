import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime as dt


def CreditTabHtml(width):       
    credit_tab_html = html.Div([
        html.H1('Credit'),
        html.H2('Credit Inputs'),

        html.Div([html.Label('Credit Start Date: '),
                dcc.DatePickerSingle(id='credit_start_date',
                date=dt.datetime.now().date())
                ],
                style={'width':width,'display':'inline-block','padding':10}),
        html.Div([html.Label('Credit End Date: '),
                dcc.DatePickerSingle(id='credit_end_date',
                date=dt.datetime.now().date())
                ],
                style={'width':width,'display':'inline-block','padding':10}),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("$", addon_type="prepend"),
                dbc.Input(id='credit_amount', placeholder="Credit Amount", type="number"),
            ],
            className="mb-3",
        ),
        
        dbc.InputGroup(
        [
                dbc.InputGroupAddon("Frequency", addon_type="prepend"),
                dbc.Select(id='credit_frequency',
                        options=[
                                {"label":"One time only", "value":"One time only"},
                                {"label":"Daily", "value":"Daily"},
                                {"label":"Weekly", "value":"Weekly"},
                                {"label":"Every 2 Weeks", "value":"Every 2 Weeks"},
                                {"label":"Monthly", "value":"Monthly"},
                                {"label":"Quarterly", "value":"Quarterly"},
                                {"label":"Semi-Annually", "value":"Semi-Annually"},
                                {"label":"Annually", "value":"Annually"},
                                {"label":"Custom", "value":"Custom"}
                        ]
                ),
                

        ]
        ),
        html.Br(),
        html.Div([html.Button(id='update-graph', n_clicks=0, children='Update Graph')]),
        html.H2('Credit Outputs')])

    return credit_tab_html


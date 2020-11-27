import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime as dt



def DebitTabHtml(width):       
    debit_tab_html = html.Div([
        html.H1('Debit'),
        html.Br(),
        html.H2('Debit Inputs'),
        html.Br(),
        html.Div([html.Label('Debit Start Date: '),
                dcc.DatePickerSingle(id='debit_start_date',
                date=dt.datetime.now().date())
                ],
                style={'width':width,'display':'inline-block','padding':10}),
        html.Div([html.Label('Debit End Date: '),
                dcc.DatePickerSingle(id='debit_end_date',
                date=dt.datetime.now().date())
                ],
                style={'width':width,'display':'inline-block','padding':10}),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("$", addon_type="prepend"),
                dbc.Input(placeholder="Debit Amount", type="number"),
                dbc.InputGroupAddon(".00", addon_type="append"),
            ],
            className="mb-3",
        ),
        
        dbc.InputGroup(
        [
                dbc.InputGroupAddon("Frequency", addon_type="prepend"),
                dbc.Select(id='debit_frequency_selection',
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
        html.Div([html.Button(id='debit-update-graph', n_clicks=0, children='Update Graph')]),
        html.Br(),
        html.H2('Debit Outputs'),
        html.Br(),
        dcc.Graph(id='debit_amortization_graph')])

    return debit_tab_html


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import datetime as dt


def DebtTabHtml(width):       
    debt_tab_html = html.Div([
            html.H1('Debt Calculator'),
            html.H2('Debt Calculator Inputs'),

            html.Div([html.Label('Debt Start Date: '),
                    dcc.DatePickerSingle(id='debt_start_date',
                    date=dt.datetime.now().date())
                    ],
                    style={'width':width,'display':'inline-block','padding':10}),
            html.Div([html.Label('Debt Length (years): '),
                    dcc.Input(id='debt_length',
                    placeholder='Enter Debt length...',
                    type='number'
                    )
                    ],
                    style={'width':width,'display':'inline-block','padding':10}),
            html.Div([html.Label('Payments per Year: '),
                    dcc.Input(id='number_of_payments_per_year',
                    placeholder='Enter the number of payments per year...',
                    type='number'
                    )
                    ],
                    style={'width':width,'display':'inline-block','padding':10}),
            html.Div([html.Label('Debt Interest Rate per Year (0.0 - 1.0): '),
                    dcc.Input(id='debt_interest_per_year',
                    placeholder='Enter yearly Debt interest rate (0.0 - 1.0)...',
                    type='number'
                    )
                    ],
                    style={'width':width,'display':'inline-block','padding':10}),
            html.Div([html.Label('Property Value ($): '),
                    dcc.Input(id='property_value',
                    placeholder='Enter the property value ($)...',
                    type='number'
                    )
                    ],
                    style={'width':width,'display':'inline-block','padding':10}),
            html.Div([html.Label('Downpayment ($): '),
                    dcc.Input(id='downpayment',
                    placeholder='Enter downpayment value ($)...',
                    type='number',
                    )
                    ],
                    style={'width':width,'display':'inline-block','padding':10}),
            html.Button(id='update-graph', n_clicks=0, children='Update Graph'),
            html.H2('Debt Calculator Outputs'),
            html.Div([html.Label('Total Monthly Payment: '),
                    html.Label(id='total_monthly_debt_payment')
                    ],
                    style={'width':width,'display':'inline-block','padding':10}),
            html.Div([html.Label('Total Interest Paid: '),
                    html.Label(id='total_interest_paid')
                    ],
                    style={'width':width,'display':'inline-block','padding':10}),
            html.Div([html.Label('Total Amount Paid: '),
                    html.Label(id='total_amount_paid')
                    ],
                    style={'width':width,'display':'inline-block','padding':10}),
            
            html.H2('Debt Calculator Graph'),
            dcc.Graph(id='amortization_graph')])

    return debt_tab_html



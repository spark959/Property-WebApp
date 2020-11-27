import dash_core_components as dcc
import dash_html_components as html
import datetime as dt

class Debt:
    def __init__(self):
        pass

    def DebtTabChildren(self, width):       
        debt_tab_html = html.Div([
            html.H1('Mortgage Calculator'),
            html.H2('Mortgage Calculator Inputs'),

            html.Div([html.Label('Mortgage Start Date: '),
                    dcc.DatePickerSingle(id='mortgage_start_date',
                    date=dt.datetime.now().date())
                    ],
                    style={'width':width,'display':'inline-block','padding':10}),
            html.Div([html.Label('Mortgage Length (years): '),
                    dcc.Input(id='mortgage_length',
                    placeholder='Enter mortgage length...',
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
            html.Div([html.Label('Mortgage Interest Rate per Year (0.0 - 1.0): '),
                    dcc.Input(id='mortgage_interest_per_year',
                    placeholder='Enter yearly mortgage interest rate (0.0 - 1.0)...',
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
            html.H2('Mortgage Calculator Outputs'),
            html.Div([html.Label('Total Monthly Payment: '),
                    html.Label(id='total_monthly_mortgage_payment')
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
            
            html.H2('Mortgage Calculator Graph'),
            dcc.Graph(id='amortization_graph')])

        return debt_tab_html




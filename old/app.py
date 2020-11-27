# public libraries
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# personal libraries
from equations import SimpleAmortization, Annuity
from html_layout import HtmlLayout
from ouput_html import MortgageOuputHtml
from main_tab_html import MainTabHtml
from debit_tab_html import DebitTabHtml
from credit_tab_html import CreditTabHtml
from investment_tab_html import InvestmentTabHtml
from debt_tab_html import DebtTabHtml

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = HtmlLayout()

width = '100%'

# Updating html based on tab type selected

@app.callback(Output('current_debit_tab_content', 'children'),
              [Input('debit_tabs', 'value')])
def RenderDebitTabFormat(tab):
    if 'debit' in tab:
        return DebitTabHtml(width)

@app.callback(Output('current_credit_tab_content', 'children'),
              [Input('credit_tabs', 'value')])
def RenderCreditTabFormat(tab):
    if 'credit' in tab:
        return CreditTabHtml(width)

@app.callback(Output('current_investment_tab_content', 'children'),
              [Input('investment_tabs', 'value')])
def RenderInvestmentTabFormat(tab):
    if 'investment' in tab:
        return InvestmentTabHtml(width)

@app.callback(Output('current_debt_tab_content', 'children'),
              [Input('debt_tabs', 'value')])
def RenderDebtTabFormat(tab):
    if 'debt' in tab:
        return DebtTabHtml(width)

# updating frequency options in frequency dropdown based on start date (DEBIT)

# updating amortization for debit objects

@app.callback(Output(component_id='debit_amortization_graph',component_property='figure'),
              [Input('debit-update-graph', 'n_clicks')],
              [State(component_id='debit_start_date',component_property='date')])
def UpdateDebitAmortization():
    return 0


# updating amortization for credit objects

        
# updating amortization for debt objects

@app.callback(Output(component_id='amortization_graph', component_property='figure'),
              [Input('update-graph', 'n_clicks')],
              [State(component_id='debt_start_date',component_property='date'),
              State(component_id='debt_length', component_property='value'),
              State(component_id='number_of_payments_per_year', component_property='value'),
              State(component_id='debt_interest_per_year', component_property='value'),
              State(component_id='property_value', component_property='value'),
              State(component_id='downpayment', component_property='value')])
def update_graph(n_clicks, mortgage_start_date,
                mortgage_length,
                number_of_payments_per_year,
                mortgage_interest_per_year,
                property_value,
                downpayment):

    result_data = SimpleAmortization(mortgage_start_date,
                                    mortgage_length,
                                    number_of_payments_per_year,
                                    mortgage_interest_per_year,
                                    property_value,
                                    downpayment)
    return MortgageOuputHtml(result_data)

application = app.server


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port='8080')
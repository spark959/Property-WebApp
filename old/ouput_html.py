import plotly.graph_objs as go

def MortgageOuputHtml(result_data):

    total_monthly_payments = go.Bar(x=result_data[1],
                                    y=result_data[2],
                                    name='Total Monthly Payments')

    monthly_insurance_payments = go.Bar(x=result_data[1],
                                    y=result_data[3],
                                    name='Monthly Insurance Payments')

    monthly_principle_payments = go.Bar(x=result_data[1],
                                    y=result_data[4],
                                    name='Monthly Principle Payments')
    
    figure = go.Figure(
                        data=[
                        monthly_insurance_payments,
                        monthly_principle_payments],
                        layout=go.Layout(barmode='stack')
    )
                
    return figure
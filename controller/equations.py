# Function to generate data for plots
import numpy as np
import datetime as dt
import calendar
from datetime import date
import re

def Annuity(n, m, i, P, downpayment):
    value = (P-downpayment)*i/m*(1+i/m)**(n*m)/((1+i/m)**(n*m)-1)
    return value

def SimpleAmortization(mortgage_start_date, n, m, i, P, downpayment):
    # calculating payments
    calculated_mortgage_payment = Annuity(n,m,i,P,downpayment)
    
    # static variables
    number_of_payments = n*m
    i = i/m

    # other variables
    payment_number = []
    payment_dates = []
    mortgage_payment_per_period = []
    money_to_insurance_per_period = []
    money_to_principle_per_period = []
    total_insurance_paid = []
    total_principle_owned = []
    total_mortgage_left = []
    
    ##Calculating each monthly payment and components of payments, this is truncated when the loan_principle falls below 0
    for j in range(number_of_payments):
        payment_number.append(j)
        # initial_date = dt.datetime.strptime(re.split('T| ', mortgage_start_date)[0], '%Y-%m-%d')
        initial_date = mortgage_start_date
        initial_date_year = initial_date.year
        initial_date_month = initial_date.month
        initial_date_day = initial_date.day
        payment_year = initial_date_year
        if (j + initial_date_month)//12 > 0 and (j + initial_date_month)%12 == 0:
            payment_year = (j + initial_date_month)//12 + initial_date_year - 1
        elif (j + initial_date_month)//12 > 0 and (j + initial_date_month)%12 != 0:
            payment_year = (j + initial_date_month)//12 + initial_date_year
        else:
            payment_year = (j + initial_date_month)//12 + initial_date_year 
        payment_month = (j + initial_date_month)%12
        if payment_month == 0:
            payment_month = 12
        payment_day = initial_date_day
        payment_date = date(payment_year, payment_month, payment_day)
        payment_dates.append(payment_date)
        if j == 0: #initial values  
            mortgage_payment_per_period.append(calculated_mortgage_payment)
            total_mortgage_left.append(P-downpayment)
            money_to_insurance_per_period.append(i*total_mortgage_left[-1])
            money_to_principle_per_period.append(calculated_mortgage_payment-money_to_insurance_per_period[-1])
            total_insurance_paid.append(money_to_insurance_per_period[-1])
            total_principle_owned.append(money_to_principle_per_period[-1])
        else:
            mortgage_payment_per_period.append(calculated_mortgage_payment)
            money_to_insurance_per_period.append(i*total_mortgage_left[-1])
            money_to_principle_per_period.append(calculated_mortgage_payment-money_to_insurance_per_period[-1])
            total_insurance_paid.append(total_insurance_paid[-1]+money_to_insurance_per_period[-1])
            total_principle_owned.append(total_principle_owned[-1]+money_to_principle_per_period[-1])
            total_mortgage_left.append(total_mortgage_left[-1]-money_to_principle_per_period[-1])

    return payment_number,\
           payment_dates,\
           mortgage_payment_per_period,\
           money_to_insurance_per_period,\
           money_to_principle_per_period,\
           total_insurance_paid,\
           total_principle_owned,\
           total_mortgage_left
           

def CombineSimpleAmortization(*args):
    '''
    Building a plan timeline (includes multiple amortizations)
    1. take all amortizations and find the earliest date and latest date
    2. build complete timeline from earliest to latest date 
    3. iterate through amortizations and append values if date == date in complete timeline
    4. Combine values for same days (also combining values for months)
    '''

    # 1
    earliest_date_list = []
    latest_date_list = []

    for amortization in args:
        # print(amortization[1])
        # earliest_date_list_converted = [x.date() for x in amortization[1]]
        earliest_date_list.append(min(amortization[1]))
        latest_date_list.append(max(amortization[1]))

    earliest_date = min(earliest_date_list)
    latest_date = max(latest_date_list)
    
    # 2
    delta = latest_date - earliest_date
    number_of_days = delta.days
    plan_dates = []
    plan_monthly_dates = []

    for i in range(number_of_days):
        new_date = earliest_date+dt.timedelta(days=i)
        plan_dates.append(new_date)
        if new_date.day == 1:
            # print(new_date)
            plan_monthly_dates.append(new_date)


    # 3 and 4
    number_of_args = len(args)
    number_of_vars_per_arg = len(args[0])
    plan_payments = [[] for x in range(len(plan_dates))]

    for amortization in args:
        for i in range(len(plan_dates)):
            for j in range(len(amortization[1])):
                if amortization[1][j] == plan_dates[i]:
                    plan_payments[i].append(amortization[2][j])
                else:
                    plan_payments[i].append(0)

    plan_payments = [sum(x) for x in plan_payments]

    plan_monthly_payments = [[] for x in plan_monthly_dates]
    for j in range(len(plan_monthly_dates)):
        for i in range(len(plan_dates)):
            if plan_dates[i].year == plan_monthly_dates[j].year and plan_dates[i].month == plan_monthly_dates[j].month:
                plan_monthly_payments[j].append(plan_payments[i])
    
    plan_monthly_payments = [sum(x) for x in plan_monthly_payments]

    return plan_dates,\
           plan_payments,\
           plan_monthly_dates,\
           plan_monthly_payments
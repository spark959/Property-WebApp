# Function to generate data for plots
import numpy as np
import datetime as dt
import calendar
from datetime import date
import re

def Annuity(n, m, i, P, downpayment):
    '''
    Function calculates the monthly payment cost
    '''
    value = (P-downpayment)*i/m*(1+i/m)**(n*m)/((1+i/m)**(n*m)-1)
    return value

def SimpleAmortization(mortgage_start_date, n, m, interest_rate_year, P, downpayment):
    '''
    Function takes 7 inputs and outputs 9 lists/values
    Outputs include a list of timestamps for each mortgage payment (currently limited to monthly payments)
    and a list of the cost of the monthly payment and lists of the cost breakdown
    '''
    # calculating payments
    calculated_mortgage_payment = Annuity(n,m,interest_rate_year,P,downpayment)
    
    # static variables
    number_of_payments = n*m
    interest_rate = interest_rate_year/m

    # other variables
    payment_number = []
    payment_dates = []
    mortgage_payment_per_period = []
    money_to_insurance_per_period = []
    money_to_principle_per_period = []
    total_interest_paid = []
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
            mortgage_payment_per_period.append(calculated_mortgage_payment+downpayment)
            total_mortgage_left.append(P-downpayment)
            money_to_insurance_per_period.append(interest_rate*total_mortgage_left[-1])
            money_to_principle_per_period.append(calculated_mortgage_payment-money_to_insurance_per_period[-1])
            total_interest_paid.append(money_to_insurance_per_period[-1])
            total_principle_owned.append(downpayment+money_to_principle_per_period[-1])
        else:
            mortgage_payment_per_period.append(calculated_mortgage_payment)
            money_to_insurance_per_period.append(interest_rate*total_mortgage_left[-1])
            money_to_principle_per_period.append(calculated_mortgage_payment-money_to_insurance_per_period[-1])
            total_interest_paid.append(total_interest_paid[-1]+money_to_insurance_per_period[-1])
            total_principle_owned.append(total_principle_owned[-1]+money_to_principle_per_period[-1])
            total_mortgage_left.append(total_mortgage_left[-1]-money_to_principle_per_period[-1])

    return payment_number,\
           payment_dates,\
           mortgage_payment_per_period,\
           money_to_insurance_per_period,\
           money_to_principle_per_period,\
           total_interest_paid,\
           total_principle_owned,\
           total_mortgage_left,\
           P,\
           downpayment
           

def CombineSimpleAmortization(*args):
    '''
    Building a plan timeline (includes multiple amortizations)
    1. take all amortizations and find the earliest date and latest date 
    2. build complete timeline from earliest to latest date 
    3. iterate through amortizations and append values if date == date in complete timeline
    4. Combine values for same days 
    5. combining values for months
    '''

    # 1
    earliest_date_list = []
    latest_date_list = []

    for amortization in args: 
        earliest_date_list.append(min(amortization[1]))
        latest_date_list.append(max(amortization[1]))

    earliest_date = min(earliest_date_list)
    latest_date = max(latest_date_list)
    
    # 2
    delta = latest_date - earliest_date
    number_of_days = delta.days # number of days between the latest and earliest date
    plan_dates = [] # every day between the latest and earliest date (payments will fall on a subset of this list)
    plan_monthly_dates = []

    for amortization in args:
        for i in range(number_of_days):
            new_date = earliest_date+dt.timedelta(days=i) # generate each day between last and first date
            for j in range(len(amortization[1])):
                if amortization[1][j] == new_date: # if date exists in amortization lists then save it
                    plan_dates.append(new_date)
                if i == 0 and new_date.day != 1: # if date is the beginning of the month or very first date save it
                    plan_monthly_dates.append(new_date)
                elif new_date.day == 1:
                    plan_monthly_dates.append(new_date)

    plan_dates = list(set(plan_dates)) # removing duplicate timestamps 
    plan_monthly_dates = list(set(plan_monthly_dates)) # removing duplicate timestamps 
    plan_dates.sort() # because duplicate timestamps are removed at random, this resorts the timestamps
    plan_monthly_dates.sort()

    # 3 and 4
    plan_payments = [[] for x in range(len(plan_dates))]
    plan_interest = [[] for x in range(len(plan_dates))]
    plan_principle = [[] for x in range(len(plan_dates))]
    plan_total_interest = [[] for x in range(len(plan_dates))]
    plan_total_principle = [[] for x in range(len(plan_dates))]

    

    for amortization in args:
        for i in range(len(plan_dates)):
            for j in range(len(amortization[1])):
                if plan_dates[i] == amortization[1][j]:
                    plan_payments[i].append(amortization[2][j])
                    plan_interest[i].append(amortization[3][j])
                    plan_principle[i].append(amortization[4][j])
                    plan_total_interest[i].append(amortization[5][j])
                    plan_total_principle[i].append(amortization[6][j])
            if plan_dates[i] > max(amortization[1]):
                plan_payments[i].append(0)
                plan_interest[i].append(0)
                plan_principle[i].append(0)
                plan_total_interest[i].append(0)
                plan_total_principle[i].append(amortization[8])

    print(plan_total_principle)

    plan_payments = [sum(x) for x in plan_payments]
    plan_interest = [sum(x) for x in plan_interest]
    plan_principle = [sum(x) for x in plan_principle]
    plan_total_interest = [sum(x) for x in plan_total_interest]
    plan_total_principle = [sum(x) for x in plan_total_principle]

    # 5
    plan_monthly_payments = [[] for x in plan_monthly_dates]
    plan_monthly_interest = [[] for x in plan_monthly_dates]
    plan_monthly_principle = [[] for x in plan_monthly_dates]
    plan_monthly_total_interest = [[] for x in plan_monthly_dates]
    plan_monthly_total_principle = [[] for x in plan_monthly_dates]
    for i in range(len(plan_dates)):
        for j in range(len(plan_monthly_dates)):
            if plan_dates[i].year == plan_monthly_dates[j].year and plan_dates[i].month == plan_monthly_dates[j].month:
                plan_monthly_payments[j].append(plan_payments[i])
                plan_monthly_interest[j].append(plan_interest[i])
                plan_monthly_principle[j].append(plan_principle[i])
                plan_monthly_total_interest[j].append(plan_total_interest[i])
                plan_monthly_total_principle[j].append(plan_total_principle[i])
    
    plan_monthly_payments = [sum(x) for x in plan_monthly_payments]
    plan_monthly_interest = [sum(x) for x in plan_monthly_interest]
    plan_monthly_principle = [sum(x) for x in plan_monthly_principle]
    plan_monthly_total_interest = [sum(x) for x in plan_monthly_total_interest]
    plan_monthly_total_principle = [sum(x) for x in plan_monthly_total_principle]

    return plan_dates,\
           plan_monthly_dates,\
           plan_payments,\
           plan_monthly_payments,\
           plan_interest,\
           plan_monthly_interest,\
           plan_principle,\
           plan_monthly_principle,\
           plan_total_interest,\
           plan_monthly_total_interest,\
           plan_total_principle,\
           plan_monthly_total_principle
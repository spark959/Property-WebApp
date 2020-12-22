# Function to generate data for plots
import numpy as np
import datetime as dt
import calendar
import datetime
from datetime import datetime as dt
import re
import logging 
import sys

# Create and configure logger
log_level = 'DEBUG' # NOTSET = 0, DEBUG = 10, INFO = 20, WARNING = 30, ERROR = 40, CRITICAL = 50
log_format = '%(levelname)s %(asctime)s , %(message)s'
logging.basicConfig(filename = 'C:\\Users\christian.abbott\\Desktop\\Personal\\Projects\\Property_Web_APP\\Property-WebApp\\app_log_{lev}.log'.format(lev=log_level),\
                    level=log_level,\
                    format = log_format,\
                    filemode = 'w')
logger = logging.getLogger()


def PeriodicPayment(*args,**kwargs):
    '''
    Function calculates the monthly payment cost
    ((P-downpay)*i/m*(1+i/m)^(n*m)) / ((1+i/m)^(n*m)-1)
    Requires a property object with AT LEAST the following parameters:
    1. loan_length_year
    2. loan_pay_freq_year
    3. loan_int_rate_year
    4. property_price
    5. loan_downpay
    '''
    loan_length_year = int(kwargs['loan_length_year'])
    loan_pay_freq_year = int(kwargs['loan_pay_freq_year'])
    loan_int_rate_year = float(kwargs['loan_int_rate_year'])
    property_price = float(kwargs['property_price'])
    loan_downpay = float(kwargs['loan_downpay'])

    logger.debug('INPUT PeriodicPayment({n},{m},{i},{P},{downpay})'.format(n=loan_length_year,m=loan_pay_freq_year,i=loan_int_rate_year,P=property_price,downpay=loan_downpay))

    value = (property_price-loan_downpay)*loan_int_rate_year/loan_pay_freq_year*(1+loan_int_rate_year/loan_pay_freq_year)**(loan_length_year*loan_pay_freq_year)/((1+loan_int_rate_year/loan_pay_freq_year)**(loan_length_year*loan_pay_freq_year)-1)

    # FUNCTION RESULT LOGGING
    logger.debug('  OUTPUT PeriodicPayment: {answer}'.format(answer=value))
    return value


def SimpleAmortization(*args,**kwargs):
    '''
    Building a property timeline (builds 1 amortization schedule)
    Requires a property object with AT LEAST the following parameters:
    1. loan_start_date
    2. loan_length_year
    3. loan_pay_freq_year
    4. loan_int_rate_year
    5. property_price
    6. loan_downpay
    '''

    loan_start_date = dt.strptime(kwargs['loan_start_date'],'%m/%d/%Y')
    loan_length_year = int(kwargs['loan_length_year'])
    loan_pay_freq_year = int(kwargs['loan_pay_freq_year'])
    loan_int_rate_year = float(kwargs['loan_int_rate_year'])
    property_price = float(kwargs['property_price'])
    loan_downpay = float(kwargs['loan_downpay'])

    property_data = {} # property data (keys reflect what is in the database)

    logger.debug('INPUT SimpleAmortization({sd},{n},{m},{i},{P},{downpay})'.format(sd=loan_start_date,n=loan_length_year,m=loan_pay_freq_year,i=loan_int_rate_year,P=property_price,downpay=loan_downpay))
    
    # calculating payment
    calculated_mortgage_payment = PeriodicPayment(**kwargs)
    
    # initializing variables
    number_of_payments = loan_length_year*loan_pay_freq_year
    interest_rate = loan_int_rate_year/loan_pay_freq_year
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
        # initial_date = dt.datetime.strptime(re.split('T| ', loan_start_date)[0], '%Y-%loan_pay_freq_year-%d')
        initial_date = loan_start_date
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
        if payment_month in [4,6,9,11] and initial_date_day == 31: # How to handle payments that are on days that not all months have (ex. 31 for Feb)
            payment_day = 30
        elif payment_month == 2 and initial_date_day > 28:
            payment_day = 28
        else:
            payment_day = initial_date_day
        payment_date = datetime.date(payment_year, payment_month, payment_day)
        payment_dates.append(payment_date)
        if j == 0: #initial values  
            mortgage_payment_per_period.append(calculated_mortgage_payment+loan_downpay)
            total_mortgage_left.append(property_price-loan_downpay)
            money_to_insurance_per_period.append(interest_rate*total_mortgage_left[-1])
            money_to_principle_per_period.append(calculated_mortgage_payment-money_to_insurance_per_period[-1])
            total_interest_paid.append(money_to_insurance_per_period[-1])
            total_principle_owned.append(loan_downpay+money_to_principle_per_period[-1])
        else:
            mortgage_payment_per_period.append(calculated_mortgage_payment)
            money_to_insurance_per_period.append(interest_rate*total_mortgage_left[-1])
            money_to_principle_per_period.append(calculated_mortgage_payment-money_to_insurance_per_period[-1])
            total_interest_paid.append(total_interest_paid[-1]+money_to_insurance_per_period[-1])
            total_principle_owned.append(total_principle_owned[-1]+money_to_principle_per_period[-1])
            total_mortgage_left.append(total_mortgage_left[-1]-money_to_principle_per_period[-1])

    property_data = {
        'payment_number':payment_number,
        'payment_dates':payment_dates,
        'mortgage_payment_per_period':mortgage_payment_per_period,
        'money_to_insurance_per_period':money_to_insurance_per_period,
        'money_to_principle_per_period':money_to_principle_per_period,
        'total_interest_paid':total_interest_paid,
        'total_principle_owned':total_principle_owned,
        'total_mortgage_left':total_mortgage_left,
        'property_price':property_price,
        'loan_downpay':loan_downpay
    }

    # FUNCTION RESULT LOGGING
    for item in property_data:
        logger.debug('  OUTPUT SimpleAmortizations: {item_name} - {item}'.format(item_name=item,item=property_data[item]))

    return property_data



def CombineSimpleAmortizations(*args,**kwargs):
    '''
    Building a plan timeline (includes multiple amortizations)
    Requires SimpleAmortization output with AT LEAST the following parameters:
    1. payment_number
    2. payment_dates
    3. mortgage_payment_per_period
    4. money_to_insurance_per_period
    5. money_to_principle_per_period
    6. total_interest_paid
    7. total_principle_owned
    8. total_mortgage_left
    9. property_price
    10. loan_downpay

    1. take all amortizations and find the earliest date and latest date 
    2. build complete timeline from earliest to latest date 
    3. iterate through amortizations and append values if date == date in complete timeline
    4. Combine values for same days 
    5. combining values for months
    '''
    logger.debug('STARTING CombineSimpleAmortizations')

    # for debugging inputs
    for amortization in kwargs:
        for item in kwargs[amortization]:
            logger.debug('INPUT CombineSimpleAmortizations({item_name} : {item})'.format(item_name=item,item=kwargs[amortization][item]))

    # 1
    earliest_date_list = []
    latest_date_list = []

    for amortization in kwargs:
        earliest_date_list.append(min(kwargs[amortization]['payment_dates']))
        latest_date_list.append(max(kwargs[amortization]['payment_dates']))

    earliest_date = min(earliest_date_list)
    latest_date = max(latest_date_list)
    logger.debug('  Determined earliest/latest dates')
    logger.debug('  Earliest Date: {date}'.format(date=earliest_date))
    logger.debug('  Latest Date:   {date}'.format(date=latest_date))
    
    # 2
    delta = latest_date - earliest_date
    number_of_days = delta.days # number of days between the latest and earliest date
    plan_monthly_dates = [] # every 1st day of a month between the latest and earliest dates (for making sense of payments graphically)

    for amortization in kwargs:
        for i in range(number_of_days):
            new_date = earliest_date+datetime.timedelta(days=i) # generate each day between last and first date
            
            if i == 0 and new_date.day != 1: # if date is the beginning of the month or very first date save it
                plan_monthly_dates.append(new_date)
            elif new_date.day == 1:
                plan_monthly_dates.append(new_date)

    plan_dates = [] # every day there is a payment AND every monthly date
    plan_dates.extend(plan_monthly_dates) # adding all monthly dates
    for amortization in kwargs:
        for i in range(len(kwargs[amortization]['payment_dates'])):
            if kwargs[amortization]['payment_dates'][i] not in plan_dates: # if date exists in amortization lists then save it
                plan_dates.append(kwargs[amortization]['payment_dates'][i])
    
    plan_dates = list(set(plan_dates)) # removing duplicate timestamps 
    plan_monthly_dates = list(set(plan_monthly_dates)) # removing duplicate timestamps 
    plan_dates.sort() # because duplicate timestamps are removed at random, this resorts the timestamps
    plan_monthly_dates.sort()

    logger.debug('  Built plan date list')
    logger.debug('  Plan date list: {list}'.format(list=plan_dates))
    logger.debug('  Plan monthly date list: {list}'.format(list=plan_monthly_dates))

    # 3 and 4
    plan_payments = [[] for x in range(len(plan_dates))]
    plan_interest = [[] for x in range(len(plan_dates))]
    plan_principle = [[] for x in range(len(plan_dates))]
    plan_total_interest = [[] for x in range(len(plan_dates))]
    plan_total_principle = [[] for x in range(len(plan_dates))]

    for amortization in kwargs:
        for i in range(len(plan_dates)):
            for j in range(len(kwargs[amortization]['payment_dates'])):
                if plan_dates[i] == kwargs[amortization]['payment_dates'][j]:
                    plan_payments[i].append(kwargs[amortization]['mortgage_payment_per_period'][j])
                    plan_interest[i].append(kwargs[amortization]['money_to_insurance_per_period'][j])
                    plan_principle[i].append(kwargs[amortization]['money_to_principle_per_period'][j])
                    plan_total_interest[i].append(kwargs[amortization]['total_interest_paid'][j])
                    plan_total_principle[i].append(kwargs[amortization]['total_principle_owned'][j])
            if plan_dates[i] > max(kwargs[amortization]['payment_dates']) and plan_dates[i] in plan_monthly_dates: # case when plan_date > amort date
                plan_payments[i].append(0)
                plan_interest[i].append(0)
                plan_principle[i].append(0)
                plan_total_interest[i].append(kwargs[amortization]['total_interest_paid'][-1])
                plan_total_principle[i].append(kwargs[amortization]['property_price'])

    plan_payments = [sum(x) for x in plan_payments]
    plan_interest = [sum(x) for x in plan_interest]
    plan_principle = [sum(x) for x in plan_principle]
    plan_total_interest = [sum(x) for x in plan_total_interest]
    plan_total_principle = [sum(x) for x in plan_total_principle]

    logger.debug('  Calculated Plan Values')

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

    logger.debug('  Calculated Monthly Plan Values')

    # plan data (keys reflect what is in the database)
    plan_data = {  
        'plan_dates':plan_dates,
        'plan_monthly_dates':plan_monthly_dates,
        'plan_payments':plan_payments,
        'plan_monthly_payments':plan_monthly_payments,
        'plan_interest':plan_interest,
        'plan_monthly_interest':plan_monthly_interest,
        'plan_principle':plan_principle,
        'plan_monthly_principle':plan_monthly_principle,
        'plan_total_interest':plan_total_interest,
        'plan_monthly_total_interest':plan_monthly_total_interest,
        'plan_total_principle':plan_total_principle,
        'plan_monthly_total_principle':plan_monthly_total_principle
    }

    for item in plan_data:
        logger.debug('  OUTPUT CombineSimpleAmortizations: {item_name} - {item}'.format(item_name=item,item=plan_data[item]))

    return plan_data
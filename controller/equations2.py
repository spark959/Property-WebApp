# Function to generate data for plots
import numpy as np
import datetime as dt
import calendar
import datetime
from datetime import datetime as dt
import re
import logging 
import sys
import fnmatch

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
    loan_pay_freq_year = str(kwargs['loan_pay_freq_year'])
    loan_int_rate_year = float(kwargs['loan_int_rate_year'])
    property_price = float(kwargs['property_price'])
    loan_downpay = float(kwargs['loan_downpay'])

    if loan_pay_freq_year == 'daily':
        loan_pay_freq_year = 365
    elif loan_pay_freq_year == 'weekly':
        loan_pay_freq_year = 52
    elif loan_pay_freq_year == 'bimonthly':
        loan_pay_freq_year = 26
    elif loan_pay_freq_year == 'monthly':
        loan_pay_freq_year = 12
    elif loan_pay_freq_year == 'quarterly':
        loan_pay_freq_year = 4
    elif loan_pay_freq_year == 'semiannually':
        loan_pay_freq_year = 2
    elif loan_pay_freq_year == 'annually':
        loan_pay_freq_year = 1

    logger.debug('INPUT PeriodicPayment({n},{m},{i},{P},{downpay})'.format(n=loan_length_year,m=loan_pay_freq_year,i=loan_int_rate_year,P=property_price,downpay=loan_downpay))

    value = (property_price-loan_downpay)*loan_int_rate_year/loan_pay_freq_year*(1+loan_int_rate_year/loan_pay_freq_year)**(loan_length_year*loan_pay_freq_year)/((1+loan_int_rate_year/loan_pay_freq_year)**(loan_length_year*loan_pay_freq_year)-1)

    output = {
        'periodic_payment':value,
        'periodic_interest_rate': loan_int_rate_year/loan_pay_freq_year
    }
    # FUNCTION RESULT LOGGING
    logger.debug('  OUTPUT PeriodicPayment: {answer}'.format(answer=output))
    return output

def CalculateTimeline(var_name,var_yes_no,var_start_date,var_end_date,var_freq_year,var_price,escrow_yes_no):
    '''
    Calculates timeline list and value list given the following property variables:
    0. <variable>_name
    1. <variable>_yes_no
    2. <variable>_start_date
    3. <variable>_end_date
    4. <variable>_freq_year
    5. <variable>_price
    for the following variables (don't need escrow):
        - loan
        - rent
        - homestead_exempt
        - security_system
        - landscape
        - bug
        - solar
        - property_man

    6. escrow_yes_no (needed for the following variables)
        - county_tax_year
        - school_tax_year
        - mud_tax_year
        - hoa_fees_year
        - homeown_insure_year
        - flood_insure_year
        - mortgage_insure_year
        - title_insure_year
        - ** secondary_water
    '''

    inputs = {
        'var_name':str(var_name),
        'var_yes_no':str(var_yes_no),
        'var_start_date':var_start_date,
        'var_end_date':var_end_date,
        'var_freq_year':str(var_freq_year),
        'var_price':float(var_price),
        'escrow_yes_no':str(escrow_yes_no)
    }

    for item in inputs:
        logger.debug('INPUT CalculateTimeline   {item}: {value}'.format(item=item,value=inputs[item]))

    counter = []
    var_dates = []
    var_values = []

    delta = inputs['var_end_date'] - inputs['var_start_date']
    number_of_days = delta.days # number of days between the latest and earliest date
    start_date_year = inputs['var_start_date'].year
    start_date_month = inputs['var_start_date'].month
    start_date_day = inputs['var_start_date'].day
    start_date_weekday = inputs['var_start_date'].weekday()
    start_date_monthrange = calendar.monthrange(start_date_year,start_date_month)[1]

    i = 0
    if inputs['var_freq_year'] == 'daily':
        for i in range(number_of_days):
            counter.append(i)
            new_date = inputs['var_start_date']+datetime.timedelta(days=i) # generate each day between last and first date
            var_dates.append(new_date)
            var_values.append(inputs['var_price'])
            i += 1

    elif inputs['var_freq_year'] == 'weekly':
        for i in range(number_of_days):
            new_date = inputs['var_start_date']+datetime.timedelta(days=i) # generate each day between last and first date
            if new_date.weekday() == start_date_weekday:
                counter.append(i)
                var_dates.append(new_date)
                var_values.append(inputs['var_price'])
                i += 1

    elif inputs['var_freq_year'] == 'bimonthly':
        for i in range(number_of_days):
            new_date = inputs['var_start_date']+datetime.timedelta(days=i) # generate each day between last and first date
            new_date_year = new_date.year
            new_date_month = new_date.month
            new_date_day = new_date.day
            new_date_month_length = calendar.monthrange(new_date_year,new_date_month)[1]
            new_date_mid_day = new_date_month_length//2
        
            if new_date_day == new_date_mid_day or new_date_day == new_date_month_length:
                counter.append(i)
                var_dates.append(new_date)
                var_values.append(inputs['var_price'])
                i += 1

    elif inputs['var_freq_year'] == 'monthly':
        for i in range(number_of_days):
            new_date = inputs['var_start_date']+datetime.timedelta(days=i) # generate each day between last and first date
            new_date_year = new_date.year
            new_date_month = new_date.month
            new_date_day = new_date.day
            new_date_month_length = calendar.monthrange(new_date_year,new_date_month)[1]

            if start_date_day == 31: # How to handle payments that are on days that not all months have (ex. 31 for Feb)
                if new_date_day == start_date_monthrange:
                    counter.append(i)
                    var_dates.append(new_date)
                    var_values.append(inputs['var_price'])
            elif start_date_day in [29,30]:
                if new_date_month == 2 and new_date_day == new_date_month_length:
                    counter.append(i)
                    var_dates.append(new_date)
                    var_values.append(inputs['var_price'])
            elif start_date_day == new_date_day:
                counter.append(i)
                var_dates.append(new_date)
                var_values.append(inputs['var_price'])
                i += 1

    elif inputs['var_freq_year'] == 'quarterly':
        pass
    elif inputs['var_freq_year'] == 'semiannually':
        pass
    elif inputs['var_freq_year'] == 'annually':
        pass
    
    list_of_var_name = [str(var_name) for x in var_dates] # to make as keys in output
    output = dict(zip(var_dates,zip(list_of_var_name,var_values)))
    logger.debug('  OUTPUT CalculateTimeline: {answer}'.format(answer=len(output.keys())))
    
    output = {**inputs,**output}

    return output


def AllExtraPeriodicCashFlow(*args,**kwargs):
    '''
    Calculating all non loan cash flows (results are added in the ComplexAmortization function)
    Requires a property object with the following:
    1. rent_yes_no
    2. own_yes_no
    3.
    4.
    5.
    6.
    7.
    8.
    9.
    10.
    11.
    12.
    13.
    14.
    15. 
    '''

def ComplexAmortization(*args,**kwargs):
    '''
    Building a property timeline (builds 1 amortization schedule)
    Requires a property object with AT LEAST the following parameters:
    1. loan_start_date
    2. loan_length_year
    3. loan_pay_freq_year
    4. loan_int_rate_year
    5. property_price
    6. loan_downpay
    7. rent_price
    '''

    loan_start_date = dt.strptime(kwargs['loan_start_date'],'%m/%d/%Y')
    loan_end_date = dt.strptime(kwargs['loan_end_date'],'%m/%d/%Y')
    loan_length_year = int(kwargs['loan_length_year'])
    loan_pay_freq_year = str(kwargs['loan_pay_freq_year'])
    loan_int_rate_year = float(kwargs['loan_int_rate_year'])
    property_price = float(kwargs['property_price'])
    loan_downpay = float(kwargs['loan_downpay'])
    rent_price = float(kwargs['rent_price'])

    property_data = {} # property data (keys reflect what is in the database)

    logger.debug('INPUT ComplexAmortization({sd},{n},{m},{i},{P},{downpay},{rent})'.format(\
        sd=loan_start_date,n=loan_length_year,m=loan_pay_freq_year,i=loan_int_rate_year,P=property_price,downpay=loan_downpay,rent=rent_price))
    
    # calculating payment
    calculated_mortgage_payment = PeriodicPayment(**kwargs)['periodic_payment']
    interest_rate = PeriodicPayment(**kwargs)['periodic_interest_rate']
    calc_payment_dates = CalculateTimeline('loan','yes',loan_start_date,loan_end_date,loan_pay_freq_year,calculated_mortgage_payment,'yes')
    payment_dates = [x for x in calc_payment_dates.keys() if 'var' not in str(x) and 'escrow' not in str(x)]
    # payment_values = [calc_payment_dates[x][1] for x in payment_dates]
    # print(payment_values)
    # return

    # initializing variables
    payment_number = []
    payment_dates = []
    mortgage_payment_per_period = []
    money_to_insurance_per_period = []
    money_to_principle_per_period = []
    total_interest_paid = []
    total_principle_owned = []
    total_mortgage_left = []
    
    ##Calculating each monthly payment and components of payments, this is truncated when the loan_principle falls below 0
    for j in range(len(payment_dates)):
        payment_number.append(j)
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

    # calculating all extra cash flows #########################################################
    all_extra_cash_flows = {}

    property_variables = {
        # 'loan',
        'rent',
        # 'tax',
        # 'mortgage_insure',
        # 'title_insure',
        # 'homestead_exempt',
        'security_system',
        'landscape',
        'bug',
        'solar',
        'property_man'
    }

    for var in property_variables:
        variable_keys = [x for x in kwargs if var in x]
        variable_keys.append('escrow_yes_no')
        variable_dict = {x:kwargs[x] for x in variable_keys}
        var_yes_no = variable_dict[var+'_yes_no']
        var_start = dt.strptime(variable_dict[var+'_start_date'],'%m/%d/%Y')
        var_end = dt.strptime(variable_dict[var+'_end_date'],'%m/%d/%Y')
        var_freq = variable_dict[var+'_freq_year']
        var_price = variable_dict[var+'_price']
        escrow = variable_dict['escrow_yes_no']
        var_dates = CalculateTimeline(var,var_yes_no,var_start,var_end,var_freq,var_price,escrow)['var_dates']
        var_values = CalculateTimeline(var,var_yes_no,var_start,var_end,var_freq,var_price,escrow)['var_values']

        all_extra_cash_flows[var+'_timeline'] = var_dates
        all_extra_cash_flows[var+'_values'] = var_values
    
    all_extra_timelines = [x for x in all_extra_cash_flows.keys() if '_timeline' in x]
    for timeline in all_extra_timelines:
        payment_dates.extend(all_extra_cash_flows[timeline])
    payment_dates = set(payment_dates)

    #######################################################################################

    # ouput object
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
        logger.debug('  OUTPUT ComplexAmortization: {item_name} - {item}'.format(item_name=item,item=property_data[item]))

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
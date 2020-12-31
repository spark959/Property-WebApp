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
from prettyprinter import pprint
import collections

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
    logging.debug('Executing: PeriodicPayment')
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

    logger.debug('  INPUT PeriodicPayment({n},{m},{i},{P},{downpay})'.format(n=loan_length_year,m=loan_pay_freq_year,i=loan_int_rate_year,P=property_price,downpay=loan_downpay))

    value = (property_price-loan_downpay)*loan_int_rate_year/loan_pay_freq_year*(1+loan_int_rate_year/loan_pay_freq_year)**(loan_length_year*loan_pay_freq_year)/((1+loan_int_rate_year/loan_pay_freq_year)**(loan_length_year*loan_pay_freq_year)-1)

    output = {
        'periodic_payment':value,
        'periodic_interest_rate': loan_int_rate_year/loan_pay_freq_year
    }
    # FUNCTION RESULT LOGGING
    logger.debug('      OUTPUT PeriodicPayment: {answer}'.format(answer=output))
    logging.debug('Finishing: PeriodicPayment')
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
    logging.debug('Executing: CalculateTimeline')
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
        logger.debug('  INPUT CalculateTimeline   {item}: {value}'.format(item=item,value=inputs[item]))

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
                    i += 1
            elif start_date_day in [29,30]:
                if new_date_month == 2 and new_date_day == new_date_month_length:
                    counter.append(i)
                    var_dates.append(new_date)
                    var_values.append(inputs['var_price'])
                    i += 1
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
        for i in range(number_of_days):
            new_date = inputs['var_start_date']+datetime.timedelta(days=i) # generate each day between last and first date
            new_date_year = new_date.year
            new_date_month = new_date.month
            new_date_day = new_date.day
            new_date_month_length = calendar.monthrange(new_date_year,new_date_month)[1]

            if start_date_day == 29 and start_date_month == 2: # How to handle payments that are on leap years (Feb 29)
                if new_date_month == 2 and new_date_day == new_date_month_length:
                    counter.append(i)
                    var_dates.append(new_date)
                    var_values.append(inputs['var_price'])
                    i += 1
            elif start_date_day == new_date_day and start_date_month == new_date_month: 
                counter.append(i)
                var_dates.append(new_date)
                var_values.append(inputs['var_price'])
                i += 1
    
    list_of_var_name = [str(var_name) for x in var_dates] # to make as keys in output
    var_name_and_values = [dict(zip(list_of_var_name,var_values)) for x in var_dates]
    output = dict(zip(var_dates,var_name_and_values))
    
    logger.debug('      OUTPUT CalculateTimeline: {answer}'.format(answer=len(output.keys())))
    logging.debug('Finishing: CalculateTimeline')
    return output


def CalculatePropertyPI(*args,**kwargs):
    '''
    Building 1 property PI (principle,interest) schedule
    Requires a property object with AT LEAST the following parameters:
    0. u_id
    1. pl_id
    2. p_id
    3. loan_start_date ('%m/%d/%Y')
    4. loan_end_date ('%m/%d/%Y')
    5. loan_length_year
    6. loan_pay_freq_year
    7. loan_int_rate_year
    8. property_price
    9. loan_downpay
    10. rent_price
    '''
    logging.debug('Executing: CalculatePropertyPI')
    inputs = {
        'u_id':str(kwargs['u_id']),
        'pl_id':str(kwargs['pl_id']),
        'p_id':str(kwargs['p_id']),
        'loan_start_date':dt.strptime(kwargs['loan_start_date'],'%m/%d/%Y'),
        'loan_end_date':dt.strptime(kwargs['loan_end_date'],'%m/%d/%Y'),
        'loan_length_year':int(kwargs['loan_length_year']),
        'loan_pay_freq_year':str(kwargs['loan_pay_freq_year']),
        'loan_int_rate_year':float(kwargs['loan_int_rate_year']),
        'property_price':float(kwargs['property_price']),
        'loan_downpay':float(kwargs['loan_downpay']),
        'rent_price':float(kwargs['rent_price'])
    }
    
    for item in inputs:
        logger.debug('  INPUT CalculatePropertyPI   {item}: {value}'.format(item=item,value=inputs[item]))

    # calculating payment and timeline for loan
    calculated_mortgage_payment = PeriodicPayment(**kwargs)['periodic_payment']
    interest_rate = PeriodicPayment(**kwargs)['periodic_interest_rate']
    calc_payment_dates = CalculateTimeline('loan','yes',inputs['loan_start_date'],inputs['loan_end_date'],inputs['loan_pay_freq_year'],calculated_mortgage_payment,kwargs['escrow_yes_no'])
    payment_dates = [x for x in calc_payment_dates.keys() if 'var' not in str(x) and 'escrow' not in str(x)]

    # initializing variables
    payment_number = []
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
            mortgage_payment_per_period.append(calculated_mortgage_payment+inputs['loan_downpay'])
            total_mortgage_left.append(inputs['property_price']-inputs['loan_downpay'])
            money_to_insurance_per_period.append(interest_rate*total_mortgage_left[-1])
            money_to_principle_per_period.append(calculated_mortgage_payment-money_to_insurance_per_period[-1])
            total_interest_paid.append(money_to_insurance_per_period[-1])
            total_principle_owned.append(inputs['loan_downpay']+money_to_principle_per_period[-1])
        else:
            mortgage_payment_per_period.append(calculated_mortgage_payment)
            money_to_insurance_per_period.append(interest_rate*total_mortgage_left[-1])
            money_to_principle_per_period.append(calculated_mortgage_payment-money_to_insurance_per_period[-1])
            total_interest_paid.append(total_interest_paid[-1]+money_to_insurance_per_period[-1])
            total_principle_owned.append(total_principle_owned[-1]+money_to_principle_per_period[-1])
            total_mortgage_left.append(total_mortgage_left[-1]-money_to_principle_per_period[-1])

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
        'property_price':[inputs['property_price'] for x in payment_dates],
        'loan_downpay':[inputs['loan_downpay'] for x in payment_dates]
    }

    # Building output
    '''
    output:{
        set_name:{
            date[i]:{
                var_name[j]: var_value[i,j]
                }
            }
        }
    }
    '''
    var_dictionaries = {var:{} for var in property_data}
    date_dictionaries = {date:var_dictionaries for date in payment_dates}
    set_name = inputs['u_id']+'|'+inputs['pl_id']+'|'+inputs['p_id']+'|'+'principle_interest'
    output = {set_name:date_dictionaries}

    for var1 in property_data:
        date_value_set = dict(zip(property_data['payment_dates'],property_data[var1]))
        for date in payment_dates:
            for var2 in property_data:
                output[set_name][date][var1] = date_value_set[date]

    # FUNCTION RESULT LOGGING
    for item in output:
        logger.debug('      OUTPUT CalculatePropertyPI: {item_name} - {item}'.format(item_name=item,item=len(output[item])))
    logging.debug('Finishing: CalculatePropertyPI')
    return output

def CalculatePropertyTI(*args,**kwargs):
    '''
    Building 1 property TI (taxes,insurance) schedule
    Requires a property object with AT LEAST the following parameters:
    0. u_id
    1. pl_id
    2. p_id
    3. loan_start_date ('%m/%d/%Y')
    4. loan_end_date ('%m/%d/%Y')
    5. loan_length_year
    6. loan_pay_freq_year
    7. loan_int_rate_year
    8. property_price
    9. loan_downpay
    10. rent_price
    11. escrow_yes_no
        if 'no' ---------
        a. county_tax_year
        b. school_tax_year
        c. mud_tax_year
        d. hoa_fees_year
        e. homeown_insure_year
        f. flood_insure_year
        g. mortgage_insure_rate_year
        h. title_insure_year
        i. ** secondary_water -- not built yet
    '''
    logging.debug('Executing: CalculatePropertyTI')
    for item in kwargs:
        logger.debug('  INPUT CalculatePropertyTI   {item}: {value}'.format(item=item,value=kwargs[item]))

    # percent vars
    percent_var_total = (float(kwargs['county_tax_year'])+\
        float(kwargs['school_tax_year'])+\
        float(kwargs['mud_tax_year']))*\
        float(kwargs['property_price'])

    # $ vars
    cash_var_total = float(kwargs['hoa_fees_year'])+\
        float(kwargs['homeown_insure_year'])+\
        float(kwargs['flood_insure_year'])+\
        float(kwargs['title_insure_year'])

    # mortgage insurance
    mortgage_insure_total = float(kwargs['mortgage_insure_rate_year'])

    all_var_total = cash_var_total + percent_var_total + mortgage_insure_total
    
    # Building output
    '''
    output:{
        set_name:{
            date[i]:{
                var_name[j]: var_value[i,j]
                }
            }
        }
    }
    '''
    output = {}
    # calculating esrow (using mortgage payment schedule) if escrow_yes_no is 'true'
    if str(kwargs['escrow_yes_no']).lower() == 'true':
        var_being_calculated = 'escrow_tax_insure_cash_flow'
        escrow_timeline = CalculateTimeline(var_being_calculated,\
                                'yes',\
                                dt.strptime(kwargs['loan_start_date'],'%m/%d/%Y'),\
                                dt.strptime(kwargs['property_sell_date'],'%m/%d/%Y'),\
                                str(kwargs['loan_pay_freq_year']),\
                                all_var_total,
                                str(kwargs['escrow_yes_no']))

        var_dictionaries = {var_being_calculated:{}}
        date_dictionaries = {date:var_dictionaries for date in escrow_timeline}
        set_name = kwargs['u_id']+'|'+kwargs['pl_id']+'|'+kwargs['p_id']+'|'+'taxes_insurance'
        output = {set_name:date_dictionaries}

        for date in output[set_name]:
            date_values = escrow_timeline[date][var_being_calculated]
            output[set_name][date][var_being_calculated] = date_values

        # for date in output[set_name]:
        #     logger.debug('{date}   |   {value}'.format(date=output[set_name][date],value=output[set_name][date]['escrow_tax_insure_cash_flow']))

    # calculating one time payment (last day of year) if escrow_yes_no is 'false'
    elif str(kwargs['escrow_yes_no']).lower() == 'false':
        loan_start_date = dt.strptime(kwargs['loan_start_date'],'%m/%d/%Y')
        end_of_year_date = dt(loan_start_date.year,12,31)
        number_of_days_until_EOY = (end_of_year_date-loan_start_date).days
        fraction_of_first_year_escrow = number_of_days_until_EOY/365
        fraction_of_last_year_escrow = 1-fraction_of_first_year_escrow
        var_being_calculated = 'no_escrow_tax_insure_cash_flow'
        no_escrow_timeline = CalculateTimeline(var_being_calculated,\
                                'yes',\
                                end_of_year_date,\
                                dt.strptime(kwargs['property_sell_date'],'%m/%d/%Y'),\
                                'annually',\
                                all_var_total,
                                str(kwargs['escrow_yes_no']))
                                
        date_dictionaries = {date:{var_being_calculated:{}} for date in no_escrow_timeline}
        set_name = kwargs['u_id']+'|'+kwargs['pl_id']+'|'+kwargs['p_id']+'|'+'taxes_insurance'
        output = {set_name:date_dictionaries}         

        for date in output[set_name]:
            date_values = no_escrow_timeline[date][var_being_calculated]
            output[set_name][date][var_being_calculated] = date_values

        # changing the first and last payments to reflect the amount of the year paid 
        first_date_of_escrow = min(no_escrow_timeline.keys())
        last_date_of_escrow = max(no_escrow_timeline.keys())
        output[set_name][first_date_of_escrow][var_being_calculated] = all_var_total*fraction_of_first_year_escrow
        output[set_name][last_date_of_escrow][var_being_calculated] = all_var_total*fraction_of_last_year_escrow

        # for date in output[set_name]:
        #     print('{date}   |   {value}'.format(date=output[set_name][date],value=output[set_name][date]['no_escrow_tax_insure_cash_flow']))
    
    # FUNCTION RESULT LOGGING
    for item in output:
        logger.debug('      OUTPUT CalculatePropertyTI: {item_name} - {item}'.format(item_name=item,item=len(output[item])))
    logging.debug('Finishing: CalculatePropertyTI')
    return output

def CalculatePropertyExtraCashFlows(*args,**kwargs):
    '''
        for the following variables (don't need escrow):
        - loan
        - rent
        - homestead_exempt
        - security_system
        - landscape
        - bug
        - solar
        - property_man
    '''
    logging.debug('Executing: CalculatePropertyExtraCashFlows')
    for item in kwargs:
        logger.debug('  INPUT CalculatePropertyExtraCashFlows   {item}: {value}'.format(item=item,value=kwargs[item]))

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

    # var_timelines 
    output = {}
    set_name = kwargs['u_id']+'|'+kwargs['pl_id']+'|'+kwargs['p_id']+'|'+'all_other_cash'
    output[set_name] = {}

    for var in property_variables:
        if kwargs[var+'_yes_no'].lower() == 'true':                 
            var_yes_no = kwargs[var+'_yes_no']
            var_start = dt.strptime(kwargs[var+'_start_date'],'%m/%d/%Y')
            var_end = dt.strptime(kwargs[var+'_end_date'],'%m/%d/%Y')
            var_freq = kwargs[var+'_freq_year']
            var_price = kwargs[var+'_price']
            escrow = kwargs['escrow_yes_no']

            var_timeline = CalculateTimeline(var,var_yes_no,var_start,var_end,var_freq,var_price,escrow)
            
            for date in var_timeline:
                if date in output[set_name]: # if the date already exists append new vars and values to date
                    output[set_name][date][var] = var_timeline[date][var]
                else: # if the date does not already exists append new date and all values
                    output[set_name][date] = var_timeline[date]

    # FUNCTION RESULT LOGGING
    for item in output:
        logger.debug('      OUTPUT CalculatePropertyExtraCashFlows: {item_name} - {item}'.format(item_name=item,item=len(output[item])))
    logging.debug('Finishing: CalculatePropertyExtraCashFlows')
    return output

def Combine_PI_TI_ExtraCash(*args,**kwargs):
    '''
    Requires output from the following equations given the same property (<property_a>)
    1. CalculatePropertyPI(<property_a>)
    2. CalculatePropertyTI(<property_a>)
    3. CalculatePropertyExtraCashFlows(<property_a>)
    '''

    logging.debug('Executing: Combine_PI_TI_ExtraCash')
    for item in kwargs:
        logger.debug('  INPUT Combine_PI_TI_ExtraCash   {item}: {value}'.format(item=item,value=kwargs[item]))

    pprint(kwargs)
    output = {}
    logging.debug('Finishing: Combine_PI_TI_ExtraCash')
    return output


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
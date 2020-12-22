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

def CalculateTimeline(var_yes_no,var_start_date,var_end_date,var_freq_year,var_price,escrow_yes_no):
    '''
    Calculates timeline list and value list given the following property variables:
    0. <variable>_yes_no
    1. <variable>_start_date
    2. <variable>_end_date
    3. <variable>_freq_year
    4. <variable>_price
    for the following variables (don't need escrow):
        - loan
        - rent
        - homestead_exempt
        - security_system
        - landscape
        - bug
        - solar
        - property_man

    5. escrow_yes_no (needed for the following variables)
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

    for item in kwargs:
        print(item)
    return 


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
    loan_length_year = int(kwargs['loan_length_year'])
    loan_pay_freq_year = int(kwargs['loan_pay_freq_year'])
    loan_int_rate_year = float(kwargs['loan_int_rate_year'])
    property_price = float(kwargs['property_price'])
    loan_downpay = float(kwargs['loan_downpay'])
    rent_price = float(kwargs['rent_price'])

    property_data = {} # property data (keys reflect what is in the database)

    logger.debug('INPUT SimpleAmortization({sd},{n},{m},{i},{P},{downpay},{rent})'.format(\
        sd=loan_start_date,n=loan_length_year,m=loan_pay_freq_year,i=loan_int_rate_year,P=property_price,downpay=loan_downpay,rent=rent_price))
    
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
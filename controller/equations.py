# Function to generate data for plots
import numpy as np
import datetime as dt
import calendar
from datetime import date
import re
import logging 

# Create and configure logger
log_level = 'DEBUG' # NOTSET = 0, DEBUG = 10, INFO = 20, WARNING = 30, ERROR = 40, CRITICAL = 50
log_format = '%(levelname)s %(asctime)s , %(message)s'
logging.basicConfig(filename = 'C:\\Users\christian.abbott\\Desktop\\Personal\\Projects\\Property_Web_APP\\Property-WebApp\\app_log_level_{lev}.log'.format(lev=log_level),\
                    level=log_level,\
                    format = log_format,\
                    filemode = 'w')
logger = logging.getLogger()

def PeriodicPayment(n, m, i, P, downpayment):
    '''
    Function calculates the monthly payment cost
    '''
    logger.debug('INPUT PeriodicPayment({n},{m},{i},{P},{downpayment})'.format(n=n,m=m,i=i,P=P,downpayment=downpayment))

    value = (P-downpayment)*i/m*(1+i/m)**(n*m)/((1+i/m)**(n*m)-1)

    # FUNCTION RESULT LOGGING
    logger.debug('  OUTPUT PeriodicPayment: {answer}'.format(answer=value))
    return value


def SimpleAmortization(mortgage_start_date, n, m, interest_rate_year, P, downpayment):
    '''
    Building a property timeline (includes 1 amortization)
    Function takes 7 inputs and outputs 10 lists/values
    
    '''
    property_data = {} # property data (reflects what is in the database)

    logger.debug('INPUT SimpleAmortization({start},{n},{m},{i},{P},{downpayment})'.format(start=mortgage_start_date,n=n,m=m,i=interest_rate_year,P=P,downpayment=downpayment))
    
    # calculating payments
    calculated_mortgage_payment = PeriodicPayment(n,m,interest_rate_year,P,downpayment)
    
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
        if payment_month in [4,6,9,11] and initial_date_day == 31: # How to handle payments that are on days that not all months have (ex. 31 for Feb)
            payment_day = 30
        elif payment_month == 2 and initial_date_day > 28:
            payment_day = 28
        else:
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

    # FUNCTION RESULT LOGGING
    for i in range(len(payment_number)):
        logger.debug('  OUTPUT SimpleAmortization: {one},{two},{three},{four},{five},{six},{seven},{eight},{nine},{ten}'.format(one=payment_number[i],\
                                                                                                                        two=payment_dates[i],\
                                                                                                                        three=mortgage_payment_per_period[i],\
                                                                                                                        four=money_to_insurance_per_period[i],\
                                                                                                                        five=money_to_principle_per_period[i],\
                                                                                                                        six=total_interest_paid[i],\
                                                                                                                        seven=total_principle_owned[i],\
                                                                                                                        eight=total_mortgage_left[i],\
                                                                                                                        nine=P,\
                                                                                                                        ten=downpayment))
    # logger.debug('  SimpleAmortization: {answer}'.format(answer=payment_number))
    # logger.debug('  SimpleAmortization: {answer}'.format(answer=payment_dates))
    # logger.debug('  SimpleAmortization: {answer}'.format(answer=mortgage_payment_per_period))
    # logger.debug('  SimpleAmortization: {answer}'.format(answer=money_to_insurance_per_period))
    # logger.debug('  SimpleAmortization: {answer}'.format(answer=money_to_principle_per_period))
    # logger.debug('  SimpleAmortization: {answer}'.format(answer=total_interest_paid))
    # logger.debug('  SimpleAmortization: {answer}'.format(answer=total_principle_owned))
    # logger.debug('  SimpleAmortization: {answer}'.format(answer=total_mortgage_left))
    # logger.debug('  SimpleAmortization: {answer}'.format(answer=P))
    # logger.debug('  SimpleAmortization: {answer}'.format(answer=downpayment))
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
    plan_data = {} # plan data (reflects what is in the database)

    for amortization in args:
        for item in amortization:
            logger.debug('INPUT CombineSimpleAmortization({item})'.format(item = item))

    # 1
    earliest_date_list = []
    latest_date_list = []

    for amortization in args: 
        earliest_date_list.append(min(amortization[1]))
        latest_date_list.append(max(amortization[1]))

    earliest_date = min(earliest_date_list)
    latest_date = max(latest_date_list)
    
    # 2
    plan_dates = [] # every day there is a payment
    for amortization in args:
        for i in range(len(amortization[1])):
            if amortization[1][j] not in plan_dates: # if date exists in amortization lists then save it
                plan_dates.append(amortization[1][j])
    
    delta = latest_date - earliest_date
    number_of_days = delta.days # number of days between the latest and earliest date
    plan_monthly_dates = [] # every 1st day of a month between the latest and earliest dates (for making sense of payments graphically)

    for amortization in args:
        for i in range(number_of_days):
            new_date = earliest_date+dt.timedelta(days=i) # generate each day between last and first date
            # for j in range(len(amortization[1])):
            
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

    # print(plan_total_principle)

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
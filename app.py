from controller.equations import *
import matplotlib.pyplot as plt 
import numpy as np
import datetime as dt

# defining data from user about user #1
u_id = 'user_1'
u_id_created = dt.date.today()
u_password = 'password123'


# defining data from user about plan #1
pl_id = 'my_first_plan'
pl_id_created = dt.date.today()
u_id = u_id
plan_length_year = 50
plan_length_month = plan_length_year*12
plan_length_day = plan_length_year*365
plan_initial_cash = 50000
plan_initial_invest = 25000
salary_year = 75000
bonus_perc_salary_year = 5
bonus_freq_year = 1
market_rate_year = 9
income_tax_rate_year = 15
donations_perc_year = 10
donations_freq_year = 24
inflation_rate_year = 3

cash_on_hand = .5*salary_year
save_above_cash_on_hand = True 


# defining data from user about property #1
u_id = u_id
pl_id = pl_id
p_id = 'my_first_property'
pi_created = dt.date.today()

house_price = 250000
loan_downpay = 50000
loan_amount = house_price - loan_downpay
loan_start_date = dt.date.today()
loan_length_year = 30
loan_end_date = loan_start_date + dt.timedelta(days=365*loan_length_year)
loan_length_month = loan_length_year*12
loan_length_day = (loan_start_date - loan_end_date).days
loan_pay_year = 12
loan_int_rate_year = .04
loan_lender_cred = 0
loan_orig_costs = 0
escrow_yes_no = True

rent_yes_no = True
own_yes_no = False
rent_freq_year = 12
rent_price = 2000
county_tax_year = .01
school_tax_year = .01
mud_tax_year = .01
hoa_fees_year = 1500
homeown_insure_year = 1500
flood_insure_year = 750
mortgage_insure_yes_no = False
mortgage_insure_rate_year = 0
title_insure_yes_no = True
title_insure_year = 500
homestead_exempt_yes_no = True
homestead_exempt_year = 2000
home_apprec_rate_year = .02
security_system_yes_no = True
security_system_freq_year = 12
security_system_price = 75
landscape_yes_no = False
landscape_freq_year = 12
landscape_price = 50
bug_yes_no = True
bug_freq_year = 4
bug_price = 100
solar_yes_no = True
solar_freq_year = 12
solar_price = 115
solar_savings = 80
property_manage_yes_no = True
property_man_freq_year = 12
property_man_price = 200
home_avg_energy_freq_year = 12
home_avg_energy_price = 200

inspection_fees = 800
home_warranties = 2000
title_co_closing_costs = 2000
realtor_buy_fee_rate = .03*house_price
realtor_sell_fee_rate = .03*house_price
realtor_fees_periodic = 0

custom_ext_pay_yes_no = False
custom_ext_pay = []
fixed_ext_pay_yes_no = False
fixed_ext_pay_freq_year = 12
fixed_ext_pay_price = 100

start_date_1 = dt.date.today()
n_1 = 30
m_1 = 12
i_1 = .04
p_1 = 250000
downpayment_1 = 50000


















start_date_2 = dt.date.today()+dt.timedelta(days=365*3)
n_2 = 15
m_2 = 12
i_2 = .035
p_2 = 300000
downpayment_2 = 60000

start_date_3 = dt.date.today()+dt.timedelta(days=365*20)
n_3 = 30
m_3 = 12
i_3 = .03
p_3 = 600000
downpayment_3 = 120000

start_date_4 = dt.date.today()+dt.timedelta(days=365*10)
n_4 = 20
m_4 = 12
i_4 = .045
p_4 = 435000
downpayment_4 = p_4*.2

answer1 = SimpleAmortization(start_date_1,n_1, m_1, i_1, p_1, downpayment_1)
answer2 = SimpleAmortization(start_date_2,n_2, m_2, i_2, p_2, downpayment_2)
answer3 = SimpleAmortization(start_date_3,n_3, m_3, i_3, p_3, downpayment_3)
answer4 = SimpleAmortization(start_date_4,n_4, m_4, i_4, p_4, downpayment_4)

inputs = [answer1, answer2, answer3, answer4]
answer = CombineSimpleAmortization(*inputs)

# print(answer[0])
# print(answer[1])
# print(answer[2])
# print(answer[3])
# print(answer[4])
# print(answer[5])
# print(answer[6])

# plt.plot(answer[1],answer[3])
# plt.plot(answer[1],answer[4])
# plt.plot(answer1[1],answer1[3])
# plt.plot(answer1[1],answer1[4])


# plt.plot(answer[0],answer[10])
# plt.plot(answer[1],answer[11])
# plt.show()
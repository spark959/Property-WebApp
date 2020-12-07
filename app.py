from controller.equations import *
import matplotlib.pyplot as plt 
import numpy as np
import datetime as dt


days2 = 365*3
days3 = 365*20
days4 = 365*10

start_date_1 = dt.date.today()
n_1 = 30
m_1 = 12
i_1 = .04
p_1 = 250000
downpayment_1 = 50000

start_date_2 = dt.date.today()+dt.timedelta(days=days2)
n_2 = 15
m_2 = 12
i_2 = .035
p_2 = 300000
downpayment_2 = 60000

start_date_3 = dt.date.today()+dt.timedelta(days=days3)
n_3 = 30
m_3 = 12
i_3 = .03
p_3 = 600000
downpayment_3 = 120000

start_date_4 = dt.date.today()+dt.timedelta(days=days4)
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
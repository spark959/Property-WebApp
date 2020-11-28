from equations import *
import matplotlib.pyplot as plt 
import numpy as np
import datetime as dt

days = 365*3

start_date_1 = dt.date.today()
n_1 = 30
m_1 = 12
i_1 = .04
p_1 = 250000
downpayment_1 = 50000

start_date_2 = dt.date.today()+dt.timedelta(days=days)
n_2 = 15
m_2 = 12
i_2 = .035
p_2 = 300000
downpayment_2 = 60000

answer = SimpleAmortization(start_date_1,n_1, m_1, i_1, p_1, downpayment_1)
answer1 = SimpleAmortization(start_date_2,n_2, m_2, i_2, p_2, downpayment_2)

inputs = [answer, answer1]

new_times = CombineSimpleAmortization(*inputs)
print(new_times)

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
# plt.show()
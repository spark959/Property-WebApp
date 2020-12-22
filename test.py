from controller.equations import *
from controller.equations2 import *
from temp_app_import import ImportCSVData
import matplotlib.pyplot as plt 
import numpy as np
import datetime as dt
import time

print('Running: test.py')
execution_start_time = dt.datetime.now()

##############################################################################################################
data = ImportCSVData()
##############################################################################################################

# print(data['properties']['property_1']['rent_price'])

# amortization_1 = SimpleAmortization(**data['properties']['property_1'])
# amortization_2 = SimpleAmortization(**data['properties']['property_2'])
# amortization_3 = SimpleAmortization(**data['properties']['property_3'])

# amortizations = (
#     amortization_1,
#     amortization_2,
#     amortization_3
# )

# amortization_names = [x for x in data['properties']]


# inputs = dict(zip(amortization_names,amortizations))
# answers = CombineSimpleAmortizations(**inputs)


# plt.plot(answers['plan_monthly_dates'],answers['plan_monthly_payments'])

# plt.plot(answers['plan_monthly_dates'],answers['plan_monthly_interest'])
# plt.plot(answers['plan_monthly_dates'],answers['plan_monthly_principle'])

# plt.plot(answers['plan_monthly_dates'],answers['plan_monthly_total_interest'])
# plt.plot(answers['plan_monthly_dates'],answers['plan_monthly_total_principle'])
# plt.show()
property_variables = [
    'loan',
    'rent',
    'tax',
    'mortgage_insure',
    'title_insure',
    'homestead_exempt',
    'security_system',
    'landscape',
    'bug',
    'solar',
    'property_man'
]
rent_variable_keys = [x for x in data['properties']['property_1'].keys() if 'rent' in x]
print(rent_variable_keys)

# test_time_line = CalculateTimeline(**data['properties']['property_1'])


execution_end_time = dt.datetime.now()
execution_time = execution_end_time - execution_start_time

print('Finishing: test.py')
print('Execution Time (sec): {sec}.{msec}'.format(sec=execution_time.seconds,msec=execution_time.microseconds))


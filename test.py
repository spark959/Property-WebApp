# from controller.equations import *
# from controller.equations2 import *
from controller.equations3 import *
from temp_data.temp_app_import import ImportCSVData
import matplotlib.pyplot as plt 
import numpy as np
import datetime as dt
import time
from prettyprinter import pprint


print('Running: test.py')
execution_start_time = dt.datetime.now()
print('..................')

##############################################################################################################
data = ImportCSVData()
##############################################################################################################
# counter = 0
# numbers = {
#     'one':1,
#     'two':2,
#     'three':3
# }
# for thing in list(numbers):
#     print('pass'+str(counter))
#     if counter == 1:
#         numbers['thing'] = 'thing'
#     counter += 1

# pprint(numbers)


# amortization_3b = CalculatePropertyTI(**data['properties']['property_3'])
# amortization_3c = CalculatePropertyExtraCashFlows(**data['properties']['property_3'])
# pprint(amortization_3c)



amortization_1a = CalculatePropertyPI(**data['properties']['property_1'])
amortization_1b = CalculatePropertyTI(**data['properties']['property_1'])
amortization_1c = CalculatePropertyExtraCashFlows(**data['properties']['property_1'])
amortization_1 = Combine_PI_TI_ExtraCash(**amortization_1a,**amortization_1b,**amortization_1c)

amortization_2a = CalculatePropertyPI(**data['properties']['property_2'])
amortization_2b = CalculatePropertyTI(**data['properties']['property_2'])
amortization_2c = CalculatePropertyExtraCashFlows(**data['properties']['property_2'])
amortization_2 = Combine_PI_TI_ExtraCash(**amortization_2a,**amortization_2b,**amortization_2c)

amortization_3a = CalculatePropertyPI(**data['properties']['property_3'])
amortization_3b = CalculatePropertyTI(**data['properties']['property_3'])
amortization_3c = CalculatePropertyExtraCashFlows(**data['properties']['property_3'])
amortization_3 = Combine_PI_TI_ExtraCash(**amortization_3a,**amortization_3b,**amortization_3c)


var_time_list = []
worth_value_list = []
cashflow_value_list = []

# for month in amortization_1['monthly']

for month in amortization_1['u_id_1|pl_id_1|property_1|Combined_PITIEC']['monthly']['u_id_1|pl_id_1|property_1|Combined_PITIEC_Monthly']:
    var_time_list.append(amortization_1['u_id_1|pl_id_1|property_1|Combined_PITIEC']['monthly']['u_id_1|pl_id_1|property_1|Combined_PITIEC_Monthly'][month]['payment_number'])
    worth_value_list.append(amortization_1['u_id_1|pl_id_1|property_1|Combined_PITIEC']['monthly']['u_id_1|pl_id_1|property_1|Combined_PITIEC_Monthly'][month]['sum_property_total_worth'])
    cashflow_value_list.append(amortization_1['u_id_1|pl_id_1|property_1|Combined_PITIEC']['monthly']['u_id_1|pl_id_1|property_1|Combined_PITIEC_Monthly'][month]['sum_property_total_cashflow'])
plt.plot(var_time_list,worth_value_list)
plt.plot(var_time_list,cashflow_value_list)
plt.show()

# processed_data = CombineProperties(**amortization_1)

# pprint(amortization_1)


execution_end_time = dt.datetime.now()
execution_time = execution_end_time - execution_start_time

print('..................')
print('Finishing: test.py')
print('Execution Time (sec): {sec}.{msec}'.format(sec=execution_time.seconds,msec=execution_time.microseconds))


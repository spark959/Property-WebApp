from controller.equations import *
from temp_app_import import ImportCSVData
import matplotlib.pyplot as plt 
import numpy as np
import datetime as dt


##############################################################################################################
data = ImportCSVData()
##############################################################################################################

# print(data['properties']['property_1'])

amortization_1 = SimpleAmortization(**data['properties']['property_1'])
amortization_2 = SimpleAmortization(**data['properties']['property_2'])
amortization_3 = SimpleAmortization(**data['properties']['property_3'])

amortizations = (
    amortization_1,
    amortization_2,
    amortization_3
)


# plt.plot(amortization_1['payment_dates'],amortization_1['money_to_principle_per_period'])
# plt.plot(amortization_1['payment_dates'],amortization_1['money_to_insurance_per_period'])
# plt.show()

answers = CombineSimpleAmortizations(amortizations)




import Property

class Plan:
    propertyList = []

    pl_id = ""
    pl_id_created = ""
    u_id = ""

    plan_length_year = ""
    plan_initial_cash = ""
    plan_initial_invest = ""

    salary = ""

    bonus_perc_year = ""
    market_rate_year = ""
    income_tax_rate_year = ""
    donations_perc_year = ""
    cash_on_hand = ""
    save_above_cash_on_hand = ""

    def __init__(self, pl_id, u_id):
        self.pl_id = pl_id
        self.u_id = u_id

    def addProperty(self, property):
        self.propertyList.append(property)

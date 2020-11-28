class Property:
    u_id = ""
    pl_id = ""
    p_id = ""
    p_id_created = ""

    house_price = "" ###

    loan_amount = "" ###
    loan_start_date = "" ###
    loan_end_date = "" 
    loan_length_year = "" ###
    loan_pay_per_year = "" ###
    loan_int_rate_year = "" ###
    loan_downpay = "" ###
    loan_lender_cred = ""
    loan_orig_costs = ""

    rent_yes_no = ""
    own_yes_no = ""

    rent_freq = ""
    rent_price = ""

    county_tax_year = ""
    school_tax_year = ""
    mud_tax_year = ""
    hoa_fees_year = ""
    homeown_insure_year = ""
    homestead_exempt_year = ""
    inflation_rate_year = ""
    home_apprec_rate_year = ""

    security_system_freq = ""
    security_system_price = ""

    landscape_freq = ""
    landscape_price = ""

    home_avg_energy_freq = ""
    home_avg_energy_price = ""

    inspection_fees = ""

    home_warranties = ""
    title_co_closing_costs = ""
    realtor_fees = ""
    custom_ext_pay = ""
    fixed_ext_pay = ""

    # Minimum constructor
    def __init__(self, house_price, loan_amount, loan_start_date, loan_length_year, loan_pay_per_year, loan_int_rate_year, loan_downpay):
        self.house_price = house_price
        self.loan_amount = loan_amount
        self.loan_start_date = loan_start_date
        self.loan_length_year = loan_length_year
        self.loan_pay_per_year = loan_pay_per_year
        self.loan_int_rate_year = loan_int_rate_year
        self.loan_downpay = loan_downpay

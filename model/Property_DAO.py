from .Property import Property
class Property_DAO:
    dbConn = ""

    def __init__ (self, dbConn, *args, **kwargs):
        self.dbConn = dbConn

    # queryString (string) = An SQL statement
    # commit (boolean) = If the SQL statement from the queryString should persist or not
    def doQuery(self, queryString, commit) :
        cur = self.dbConn.cursor()

        cur.execute(queryString)

        # If you want changes to persist in DB use:
        if (commit == True) :
            self.dbConn.commit()

        return cur.fetchall()

    def test(self):
        queryString = "SELECT U_ID, PL_ID FROM \"POTATO\";"
        for U_ID, PL_ID in self.doQuery(queryString, False) :
            print(U_ID, PL_ID)

    def getAll(self):
        queryString = "SELECT * FROM \"PROPERTY\";"
        return self.doQuery(queryString, False)

    def insert(self, property): #Still in progress (need to pass in values and put them into the queryString)
        if(isinstance(property, Property)):
            queryString = "INSERT INTO \"PROPERTY\" (u_id, pl_id, p_id, p_id_created, house_price, loan_amount, loan_start_date, loan_end_date, loan_length_year, loan_pay_per_year, loan_int_rate_year, loan_downpay, loan_lender_cred, loan_orig_costs, rent_yes_no, own_yes_no, rent_freq, rent_price, county_tax_year, school_tax_year, mud_tax_year, hoa_fees_year, homeown_insure_year, homestead_exempt_year, inflation_rate_year, home_apprec_rate_year, security_system_freq, security_system_price, landscape_freq, landscape_price, home_avg_energy_freq, home_avg_energy_price, inspection_fees, home_warranties, title_co_closing_costs, realtor_fees, custom_ext_pay, fixed_ext_pay, custom1, custom2, custom3, custom4, custom5, custom6, custom7, custom8, custom9, custom0) + VALUES('', '', '', now(), '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');"
            return self.doQuery(queryString, True)
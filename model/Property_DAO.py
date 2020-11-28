class Property_DAO:
    dbConn = ""

    def __init__ (self, dbConn):
        self.dbConn = dbConn

    # conn (connection) = connection to the database
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
        qsGetAllPotato = "SELECT U_ID, PL_ID FROM \"POTATO\";"
        for U_ID, PL_ID in self.doQuery(qsGetAllPotato, False) :
            print(U_ID, PL_ID)
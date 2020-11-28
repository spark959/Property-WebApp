class Plan_DAO:
    dbConn = ""

    def __init__ (self, dbConn):
        self.dbConn = dbConn
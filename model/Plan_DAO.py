class Plan_DAO:
    dbConn = ""

    def __init__ (self, dbConn, *args, **kwargs):
        self.dbConn = dbConn
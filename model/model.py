import psycopg2

hostname = 'localhost'
username = 'spark959'
password = 'potato'
database = 'propertywebapp'

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database ) # Make sure the connection is eventually closed

# conn (connection) = connection to the database
# queryString (string) = An SQL statement
# commit (boolean) = If the SQL statement from the queryString should persist or not
def doQuery(conn, queryString, commit) :
    cur = conn.cursor()

    cur.execute(queryString)

    # If you want changes to persist in DB use:
    if (commit == True) :
        conn.commit()

    return cur.fetchall()

qsGetAllPotato = "SELECT U_ID, PL_ID FROM \"POTATO\";"
for U_ID, PL_ID in doQuery(myConnection, qsGetAllPotato, False) :
    print(U_ID, PL_ID)
myConnection.close()

hostname = 'localhost'
username = 'spark959'
password = 'potato'
database = 'propertywebapp'

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT U_ID, PL_ID FROM \"USERS\";" )

    # for "columns in order in row" in cur.fetchall() :
    for U_ID, PL_ID in cur.fetchall() :
        print( U_ID, PL_ID )

    # If you want changes to persist in DB use:
    # conn.commit();


print( "Using psycopg2:" )
import psycopg2
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
doQuery( myConnection )
myConnection.close()
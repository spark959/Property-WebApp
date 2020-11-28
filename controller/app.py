import psycopg2
#import model.Property_DAO
#import model.Plan_DAO

hostname = 'localhost'
username = 'spark959'
password = 'potato'
database = 'propertywebapp'

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database ) # Make sure the connection is eventually closed
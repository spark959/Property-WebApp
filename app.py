import psycopg2
from model.Property_DAO import Property_DAO
from model.Plan_DAO import Plan_DAO

hostname = 'localhost'
username = 'spark959'
password = 'potato'
database = 'propertywebapp'

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database ) # Make sure the connection is eventually closed

currProp_DAO = Property_DAO(myConnection)
currPlan_DAO = Plan_DAO(myConnection)

currProp_DAO.test()

myConnection.close()
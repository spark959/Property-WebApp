import csv

def ImportCSVData():

    user_file_path = 'C:\\Users\\christian.abbott\\Desktop\\Personal\\Projects\\Property_Web_APP\\Property-WebApp\\temp_data\\USER.csv'
    plan_file_path = 'C:\\Users\\christian.abbott\\Desktop\\Personal\\Projects\\Property_Web_APP\\Property-WebApp\\temp_data\\PLAN.csv'
    property_file_path = 'C:\\Users\\christian.abbott\\Desktop\\Personal\\Projects\\Property_Web_APP\\Property-WebApp\\temp_data\\PROPERTY.csv'

    # def ImportDataFromExcel(file_path):
    data = {
        'users':{},
        'plans':{},
        'properties':{}
    }


    # Extracting USER data
    with open(user_file_path,'r') as user_data:
        csv_reader = csv.reader(user_data,delimiter=',')

        columns = next(csv_reader)

        for row in csv_reader:
            data['users'][str(row[0])] = dict(zip(columns, row))

    # Extracting PLAN data
    with open(plan_file_path,'r') as plan_data:
        csv_reader = csv.reader(plan_data,delimiter=',')

        columns = next(csv_reader)

        for row in csv_reader:
            data['plans'][str(row[0])] = dict(zip(columns, row))

    # Extracting PROPERTY data
    with open(property_file_path,'r') as property_data:
        csv_reader = csv.reader(property_data,delimiter=',')

        columns = next(csv_reader)

        for row in csv_reader:
            data['properties'][str(row[2])] = dict(zip(columns, row))

    # print(data['users'])
    # print(data['plans'])
    # print(data['properties'])

    return data
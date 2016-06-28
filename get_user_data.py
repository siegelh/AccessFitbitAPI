import pandas as pd
from access_api import *
import sys
from datetime import datetime, timedelta as td

# get the users arguments by looping through users
users = pd.read_csv(r'data\user_info.csv')

def retrieve_data(row, date):            
    data = access_api(row['username'], row['password'], row['OAuthTwoClientID'], row['ClientOrConsumerSecret'], date)
    heart = get_heart_rate_data(data, row['username'], date)
    calories = get_calories_data(data, row['username'], date)
    distance = get_distance_data(data, row['username'], date)
    floors = get_floors_data(data, row['username'], date)
    steps = get_steps_data(data, row['username'], date)
    sleep = get_sleep_data(data, row['username'], date)
    if (heart is None) and (calories is None) and (distance is None) and (floors is None) and (steps is None) and (sleep is None):
        print "No data retrieved for %s on date %s" % (row['username'], date)    
    all_data = [heart, calories, distance, floors, steps, sleep]
    real_data = [d for d in all_data if isinstance(d, pd.DataFrame)]
    out = real_data[0]
    for i in range(1, len(real_data)):
        out = out.merge(real_data[i], on=['datetime','username'], how="outer")	
    return out
	
def enforce_column_schema(table):
	column_schema = ['username','datetime','heart_rate_value','calories_value','calories_level','calories_mets',
	                 'distance_value','floors_value','steps_value','sleep_value']
	columns_with_data = table.columns
	missing_columns = [d for d in column_schema if d not in columns_with_data]
	for col in missing_columns:
		table[col] = None
	table = table[['username','datetime','heart_rate_value','calories_value','calories_level','calories_mets',
	               'distance_value','floors_value','steps_value','sleep_value']]
	return table

if len(sys.argv) == 2:
    date = sys.argv[1]
else:
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    if datetime.strptime(start_date, "%Y-%m-%d") > datetime.strptime(start_date, "%Y-%m-%d"):
        print "Start date must be before end date."
    else:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        delta = end_datetime - start_datetime
        dates = []
        for i in range(delta.days + 1):
            dates.append(str((start_datetime + td(days=i)).date()))
            
for index, row in users.iterrows():
    if 'date' in locals():
        out = retrieve_data(row, date)
        if not os.path.exists('data\\%s' % row['username']):
			os.makedirs('data\\%s' % row['username'])
        out = enforce_column_schema(out)
        out.to_csv('data\\%s\\%s.csv' % (row['username'], date), index=False)
    else:
        days_data = []
        for day in dates:
            day_data = retrieve_data(row, day)
            days_data.append(day_data)
        out = pd.concat(days_data)
        if not os.path.exists('data\\%s' % row['username']):
            os.makedirs('data\\%s' % row['username'])
	    out = enforce_column_schema(out)
        out.to_csv('data\\%s\\%s_%s.csv' % (row['username'], start_date, end_date), index=False)
		
		
		

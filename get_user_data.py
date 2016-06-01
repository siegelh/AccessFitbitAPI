import pandas as pd
from access_api import *
import sys

# get the users arguments by looping through users
users = pd.read_csv(r'data\user_info.csv')

date = sys.argv[1]

for index, row in users.iterrows():
    data = access_api(row['username'], row['password'], row['OAuthTwoClientID'], row['ClientOrConsumerSecret'], date)
    get_heart_rate_data(data, row['username'], date)
    get_calories_data(data, row['username'], date)
    get_distance_data(data, row['username'], date)
    get_floors_data(data, row['username'], date)
    get_steps_data(data, row['username'], date)
    get_sleep_data(data, row['username'], date)

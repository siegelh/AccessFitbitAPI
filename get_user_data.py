import pandas as pd
import sys
from subprocess import call

date = sys.argv[1]
users = pd.read_csv(r'data\user_info.csv')

for row in users.iterrows():
    data = row[1]
    username = data['username']
    password = data['password']
    OAuthTwoClientID = data['OAuthTwoClientID']
    ClientOrConsumerSecret = data['ClientOrConsumerSecret']
    call(
        "python access_api.py %s %s %s %s %s" % (username, password, OAuthTwoClientID, ClientOrConsumerSecret, date))

import urllib
import urllib2
import base64
import fitbit
import urlparse
import sqlite3

import os
from selenium import webdriver

chromedriver = r"requirements\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

date = '2016-05-10'

# These are the secrets etc from Fitbit developer
username = 'harrisried@gmail.com'
password = 'harrison17171'
OAuthTwoClientID = "227LLT"
ClientOrConsumerSecret = "561f3b8f1120cef9e105dd0cb22df45f"

# This is the Fitbit URL
TokenURL = "https://api.fitbit.com/oauth2/token"
redirectURL = "http://localhost:9090/register_user"

# Get Authorization
authorizationURL = "https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=" + OAuthTwoClientID + "&redirect_uri=" + urllib.quote_plus(
    redirectURL) + "&expires_in=31536000&scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight"
driver.get(authorizationURL)

with open(r'requirements\jquery-1.12.3.min.js', 'r') as jquery_js:
    jquery = jquery_js.read() #read the jquery from a file
    driver.execute_script(jquery) #active the jquery lib
    driver.execute_script("$('input.field.email').val('%s')" % username)
    driver.execute_script("$('input.field.password').val('%s')" % password)
    driver.execute_script("$('#loginForm').submit()")

while not driver.current_url.startswith('http://localhost:9090'):
    pass

parsed_url = urlparse.urlparse(driver.current_url)
AuthorisationCode = urlparse.parse_qs(parsed_url.query)['code'][0]

driver.close()

# Form the data payload
BodyText = {'code': AuthorisationCode,
            'redirect_uri': redirectURL, #'https://github.com/siegelh/FitbitAPITesting',
            'client_id': OAuthTwoClientID,
            'grant_type': 'authorization_code'}

BodyURLEncoded = urllib.urlencode(BodyText)

# Start the request
req = urllib2.Request(TokenURL, BodyURLEncoded)

# Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
req.add_header('Authorization', 'Basic ' + base64.b64encode(OAuthTwoClientID + ":" + ClientOrConsumerSecret))
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

# Fire off the request
try:
    response = urllib2.urlopen(req)
    FullResponse = response.read()
    authd_client = fitbit.Fitbit(OAuthTwoClientID, ClientOrConsumerSecret, access_token=(eval(FullResponse))['access_token'])
	# At this point, we have instantiated authd_client, which contains many methods that are useful for us.
	# Example, getting intraday heart rate data
    d = authd_client.intraday_time_series('activities/heart', base_date=date, detail_level="1sec")
    intraday_heart_rate_data = d['activities-heart-intraday']['dataset']
    intraday_heart_rate_data_list = [(username, date+'T'+d['time'], d['value']) for d in intraday_heart_rate_data]
except urllib2.URLError as e:
    print e.code
    print e.read()
	
# Save heartrate data to a database
conn = sqlite3.connect('example.db')
c = conn.cursor()
try:
    c.executemany('''INSERT INTO intraday_heartrate VALUES (?,?,?)''', intraday_heart_rate_data_list)
    conn.commit()
    print "Inserting data for %s from %s." % (username, date)
except sqlite3.OperationalError as err:
    print "Table does not exist, creating now."
    c.execute('''CREATE TABLE intraday_heartrate 
	            (username TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, value INTEGER)''')
    print "Inserting data for %s from %s." % (username, date)
    c.executemany('''INSERT INTO intraday_heartrate VALUES (?,?,?)''', intraday_heart_rate_data_list)
    conn.commit()

import urllib
import urllib2
import base64
import fitbit
import urlparse
import os
from selenium import webdriver
import pandas as pd
from datetime import datetime, timedelta

def access_api(username, password, OAuthTwoClientID, ClientOrConsumerSecret, date):
    '''
    Accesses the Fitbit API for the given user plus parameter info and returns a list of the raw API responses for:
    - Intraday heart rate data
    - Intraday calorie data
    - Intraday distance data
    - Intraday floors data
    - Intraday steps data
    - Intraday sleep data
    '''

    # Authorization
    TokenURL = "https://api.fitbit.com/oauth2/token"
    redirectURL = "http://localhost:9090/register_user"
    chromedriver = r"requirements\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    authorizationURL = "https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=" + str(OAuthTwoClientID) + "&redirect_uri=" + str(urllib.quote_plus(
        redirectURL)) + "&expires_in=31536000&scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight"
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
                'redirect_uri': redirectURL,
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

        # Heart rate data
        intraday_heart_rate_data_conn = authd_client.intraday_time_series('activities/heart', base_date=date, detail_level="1sec")

        # Calories data
        intraday_calories_data_conn = authd_client.intraday_time_series("activities/calories", base_date=date, detail_level="1min")

        # Distance data
        intraday_distance_data_conn = authd_client.intraday_time_series("activities/distance", base_date=date,  detail_level="1min")

        # Floors data
        intraday_floors_data_conn = authd_client.intraday_time_series("activities/floors", base_date=date, detail_level="1min")

        # Steps data
        intraday_steps_data_conn = authd_client.intraday_time_series("activities/steps", base_date=date, detail_level="1min")

        # Sleep data
        intraday_sleep_data_conn = authd_client.sleep(date)

    except urllib2.URLError as e:
        print e.code
        print e.read()

    return [intraday_heart_rate_data_conn, intraday_calories_data_conn, intraday_distance_data_conn,
            intraday_floors_data_conn, intraday_steps_data_conn, intraday_sleep_data_conn]
            
# Heart rate data
def get_heart_rate_data(access_api_object, username, date):
    heart_rate_data_raw = access_api_object[0]
    if "activities-heart-intraday" in heart_rate_data_raw.keys():
        intraday_heart_rate_data = heart_rate_data_raw['activities-heart-intraday']['dataset']
        intraday_heart_rate_data_list = [(username, date+'T'+d['time'], d['value']) for d in intraday_heart_rate_data]
        intraday_heart_rate_data_df = pd.DataFrame(intraday_heart_rate_data_list,columns=["username","datetime","value"])
        if not os.path.exists('data\\%s\\heart_rate' % username):
            os.makedirs('data\\%s\\heart_rate' % username)
        intraday_heart_rate_data_df.to_csv('data\\%s\\heart_rate\\%s.csv' % (username, date), index=False)
        print("Intraday heart rate data for %s on date %s saved." % (username, date))
    else:
        print("Intraday heart rate data missing for %s on date %s. Available keys are: %s" % (username, date, heart_rate_data_raw.keys()))
        print("Skipping.")

# Calories data
def get_calories_data(access_api_object, username, date):
    calories_data_raw = access_api_object[1]
    if "activities-calories-intraday" in calories_data_raw.keys():
        intraday_calories_rate_data = calories_data_raw['activities-calories-intraday']['dataset']
        intraday_calories_rate_data_list = [(username, d["level"], d["mets"], date+'T'+d['time'], d['value']) for d in intraday_calories_rate_data]
        intraday_calories_rate_data_df = pd.DataFrame(intraday_calories_rate_data_list,columns=["username","level","mets","datetime","value"])
        if not os.path.exists('data\\%s\\calories' % username):
            os.makedirs('data\\%s\\calories' % username)
        intraday_calories_rate_data_df.to_csv('data\\%s\\calories\\%s.csv' % (username, date), index=False)
        print("Intraday calorie data for %s on date %s saved." % (username, date))
    else:
        print("Intraday calorie data missing for %s on date %s. Available keys are: %s" % (username, date, calories_data_raw.keys()))
        print("Skipping.")
    
# Distance data
def get_distance_data(access_api_object, username, date):
    distance_data_raw = access_api_object[2]
    if "activities-distance-intraday" in distance_data_raw.keys():
        intraday_distance_rate_data = distance_data_raw['activities-distance-intraday']['dataset']
        intraday_distance_rate_data_list = [(username, date+'T'+d['time'], d['value']) for d in intraday_distance_rate_data]
        intraday_distance_rate_data_df = pd.DataFrame(intraday_distance_rate_data_list,columns=["username","datetime","value"])
        if not os.path.exists('data\\%s\\distance' % username):
            os.makedirs('data\\%s\\distance' % username)
        intraday_distance_rate_data_df.to_csv('data\\%s\\distance\\%s.csv' % (username, date), index=False)
        print("Intraday distance data for %s on date %s saved." % (username, date))
    else:
        print("Intraday distance data missing for %s on date %s. Available keys are: %s" % (username, date, distance_data_raw.keys()))
        print("Skipping.")   
    
# Floors data
def get_floors_data(access_api_object, username, date):
    floors_data_raw = access_api_object[3]
    if "activities-floors-intraday" in floors_data_raw.keys():
        intraday_floors_rate_data = floors_data_raw['activities-floors-intraday']['dataset']
        intraday_floors_rate_data_list = [(username, date+'T'+d['time'], d['value']) for d in intraday_floors_rate_data]
        intraday_floors_rate_data_df = pd.DataFrame(intraday_floors_rate_data_list,columns=["username","datetime","value"])
        if not os.path.exists('data\\%s\\floors' % username):
            os.makedirs('data\\%s\\floors' % username)
        intraday_floors_rate_data_df.to_csv('data\\%s\\floors\\%s.csv' % (username, date), index=False)
        print("Intraday floors data for %s on date %s saved." % (username, date))
    else:
        print("Intraday floors data missing for %s on date %s. Available keys are: %s" % (username, date, floors_data_raw.keys()))
        print("Skipping.")   
    
# Steps data
def get_steps_data(access_api_object, username, date):
    steps_data_raw = access_api_object[4]
    if "activities-steps-intraday" in steps_data_raw.keys():
        intraday_steps_rate_data = steps_data_raw['activities-steps-intraday']['dataset']
        intraday_steps_rate_data_list = [(username, date+'T'+d['time'], d['value']) for d in intraday_steps_rate_data]
        intraday_steps_rate_data_df = pd.DataFrame(intraday_steps_rate_data_list,columns=["username","datetime","value"])
        if not os.path.exists('data\\%s\\steps' % username):
            os.makedirs('data\\%s\\steps' % username)
        intraday_steps_rate_data_df.to_csv('data\\%s\\steps\\%s.csv' % (username, date), index=False)
        print("Intraday steps data for %s on date %s saved." % (username, date))
    else:
        print("Intraday steps data missing for %s on date %s. Available keys are: %s" % (username, date, steps_data_raw.keys()))
        print("Skipping.")  

# Sleep data
def get_sleep_data(access_api_object, username, date):
    sleep_data_raw = access_api_object[5]
    if "sleep" in sleep_data_raw.keys():
        if len(sleep_data_raw['sleep']) > 0:
            intraday_sleep_rate_data = sleep_data_raw['sleep'][0]['minuteData']
            start_date_datetime = datetime.strptime(sleep_data_raw['sleep'][0]['startTime'], '%Y-%m-%dT%H:%M:%S.000')
            if str(start_date_datetime.date()) == date:
                intraday_sleep_rate_data_list = [(username, date+'T'+d['dateTime'], d['value']) for d in intraday_sleep_rate_data]
                intraday_sleep_rate_data_df = pd.DataFrame(intraday_sleep_rate_data_list,columns=["username","datetime","value"])
                if not os.path.exists('data\\%s\\sleep' % username):
                    os.makedirs('data\\%s\\sleep' % username)
                intraday_sleep_rate_data_df.to_csv('data\\%s\\sleep\\%s.csv' % (username, date), index=False)
                print("Intraday sleep data for %s on date %s saved." % (username, date))
            else:
                for value in intraday_sleep_rate_data:
                    if datetime.strptime(value['dateTime'], "%H:%M:%S").time() >= start_date_datetime.time():
                        value['date'] = str(start_date_datetime.date())
                    else:
                        value['date'] = str((start_date_datetime + timedelta(days=1)).date())
                intraday_sleep_rate_data_list = [(username, d['date']+'T'+d['dateTime'], d['value']) for d in intraday_sleep_rate_data]
                intraday_sleep_rate_data_df = pd.DataFrame(intraday_sleep_rate_data_list,columns=["username","datetime","value"])
                if not os.path.exists('data\\%s\\sleep' % username):
                    os.makedirs('data\\%s\\sleep' % username)
                intraday_sleep_rate_data_df.to_csv('data\\%s\\sleep\\%s.csv' % (username, date), index=False)
                print("Intraday sleep data for %s on date %s saved." % (username, date))
                
        else:
            print("Intraday sleep data missing for %s on date %s." % (username, date))
    else:
        print("Intraday sleep data missing for %s on date %s. Available keys are: %s" % (username, date, sleep_data_raw.keys()))
        print("Skipping.")  

# FitbitAPITesting

This is the code to connect to the Fitbit API and extract intraday heart rate data.

### Requirements

* Python 2.7
* Requires the login, password, client_id, and client_secret, which should be added to the "data\user_info.csv"
* To install Python package requirements, run "pip install -r requirements/packages.txt"

### Instructions

* Set up access to personal data through the Fitbit api by visiting `www.dev.fitbit.com` and registering an app
  * After clicking `Register An App`, sign in with the account you wish to registering
  * Fill in the fields in `Register an application` with the following:
    * Application Name:  "Accessing Personal Data"
	* Description:  "Logging my personal data"
	* Application Website: "http://github.com/siegelh/FitbitAPITesting"
	* Organization:  "Not applicable"
	* Organization Website: "http://github.com/siegelh/FitbitAPITesting"
	* OAuth 2.0 Application Type: "Personal"
	* Callback URL: "http://localhost:9090/register_user"
	* Default Access Type: "Read-Only"
	* Save
  * You have now set up a personal application to access your data in read-only mode from the Fitbit API.
* Clone the repo and update the `data\user_info.csv` with user information (see requirements above)
* Run `get_user_data.py YYYY-MM-DD` with the date that you wish to access data
* Data will be gathered for each user in the user_info.csv and saved to the SQLite `data\user_data.db` database.
* Currently the `access_api.py` script will gather and store intraday heartrate data, accurate to 5 second intervals.

### Database Schema

The `data\user_data.db` file contains one table `intraday_heartrate` with the following schema:

username|timestamp|value
--------|---------|-----
useremail@example.com|2015-05-10T10:30:00|75
useremail@example.com|2015-05-10T10:30:05|78
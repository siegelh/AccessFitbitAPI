# Access Fitbit API for Personal Data

This is the code to connect to the Fitbit API and extract available intraday data.

### Requirements

* Python 2.7
* Requires the login, password, client_id, and client_secret, which should be added to the `data\user_info.csv`
* To install Python package requirements, run `pip install -r requirements/packages.txt` from `cmd`

### Instructions

* Set up access to personal data through the Fitbit api by visiting `www.dev.fitbit.com` and registering an app
  * After clicking `Register An App`, sign in with the account you wish to register
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
  * To access the client_id and client_secret, click `Manage My Apps` on dev.fitbit.com, and select the personal application you created.
  * The Client Secret and Client ID will be available, add these along with the login email and password to "data\user_info.csv"
* Run `get_user_data.py YYYY-MM-DD` with the date that you wish to access data
* Data will be gathered for each user in the user_info.csv and saved as .CSV files `data\username\data_source\data.csv`.

### Database Schema

The data files contains one days data for the given intraday field with the following schema:

* If heartrate, distance, floors, or sleep

username|timestamp|value
--------|---------|-----
useremail@example.com|2015-05-10T10:30:00|75
useremail@example.com|2015-05-10T10:30:05|78

* If calories

username|level|mets|timestamp|value
--------|-----|----|---------|-----
useremail@example.com|1|5|2015-05-10T10:30:00|75
useremail@example.com|2|10|2015-05-10T10:30:05|78
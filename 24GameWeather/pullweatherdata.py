from __future__ import print_function
import weatherapi
from weatherapi.rest import ApiException
import json
from datetime import datetime, timedelta


# Configure API key authorization: ApiKeyAuth
configuration = weatherapi.Configuration()
configuration.api_key['key'] = 'a6ebbf8a25f649d785c155643240711'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'

api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))
q = '01608' # str | Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name. Visit [request parameter section](https://www.weatherapi.com/docs/#intro-request) to learn more.
dt = '2024-10-18' # date | Date should be between today and next 14 day in yyyy-MM-dd format. e.g. '2015-01-01' (optional)
#unixdt = 56 # int | Please either pass 'dt' or 'unixdt' and not both in same request. unixdt should be between today and next 14 day in Unix format. e.g. 1490227200 (optional)
hour = 15 # int | Must be in 24 hour. For example 5 pm should be hour=17, 6 am as hour=6 (optional)
lang = '' # str | Returns 'condition:text' field in API in the desired language.<br /> Visit [request parameter section](https://www.weatherapi.com/docs/#intro-request) to check 'lang-code'. (optional)
alerts = 'no' # str | Enable/Disable alerts in forecast API output. Example, alerts=yes or alerts=no. (optional)
aqi = 'yes' # str | Enable/Disable Air Quality data in forecast API output. Example, aqi=yes or aqi=no. (optional)


try:
    # Forecast API
    #All days between first and last home games of the 2024 Season
    start_date = datetime(2023, 3, 31)
    end_date = datetime(2023, 9, 17)
    responses = []
    #Iterate through each day between start_date and end_date
    current_date = start_date
    while current_date <= end_date:
        dt = current_date.strftime('%Y-%m-%d')  # Format the date as 'YYYY-MM-DD'
        api_response = api_instance.history_weather(q, dt=current_date, end_dt = current_date)
        responses.append(api_response)
        current_date += timedelta(days=1)
    
    #dump all api_responses into one json file
    with open('api_responses23.json', 'w') as json_file:
        json.dump(responses, json_file, indent=4)
    
    

except ApiException as e:
    print("Exception when calling APIsApi->forecast_weather: %s\n" % e)
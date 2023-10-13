from twilio_config import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,API_KEY_WAPI
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from tqdm import tqdm
from utils import request_wapi,get_forecast,create_df,send_message,get_date

api_key = API_KEY_WAPI

# Location for which you want to check the forecast
query = 'YOUR LOCATION'

input_date= get_date()

# Getting the JSON after the request to the WeatherApi AP
response = request_wapi(api_key,query)

# Create data list
data = []

# Fetches the forecast for every hour of the day
for i in tqdm(range(24),colour = 'green'):

    data.append(get_forecast(response,i))

# Creates the dataframe only with the hours of the day when it will rain
df_rain = create_df(data)

# Send message
message_id = send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,input_date,df_rain,query)


print('Message sent successfully ' + message_id)

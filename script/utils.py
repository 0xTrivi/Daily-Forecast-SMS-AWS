
import pandas as pd
from twilio.rest import Client
from twilio_config import PHONE_NUMBER
from datetime import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

def get_date():
    """
    Retrieves the current date in the format 'YYYY-MM-DD'.

    Returns:
        str: The current date in the 'YYYY-MM-DD' format.
    """
    input_date = datetime.now()
    input_date = input_date.strftime("%Y-%m-%d")

    return input_date

def request_wapi(api_key,query):
    """
    Makes a request to the WeatherApi API to retrieve the weather forecast.

    Args:
        api_key (str): The API key for accessing the WeatherApi API.
        query (str): The location for which the forecast is requested.

    Returns:
        dict: A dictionary containing the API response in JSON format.
    """
    url = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

    try :
        response = requests.get(url).json()
    except Exception as e:
        print(e)

    return response

def get_forecast(response,i):
    """
    Extracts weather forecast information for a specific hour from the API response.

    Args:
        response (dict): The API response in JSON format.
        i (int): The index of the hour for which you want to extract the forecast data.

    Returns:
        tuple: A tuple containing the extracted weather forecast information, including date,
        time, condition, temperature, rain, and chance of rain.
    """
    date = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    time = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condition = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = response['forecast']['forecastday'][0]['hour'][i]['temp_c']
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    chance_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']

    return date,time,condition,tempe,rain,chance_rain

def create_df(data):
    """
    Creates a DataFrame with weather forecast data and filters it for rainy hours between 6 AM and 10 PM.

    Args:
        data (list): A list containing weather forecast data, including date, time, condition, 
        temperature, rain indicator, and chance of rain.

    Returns:
        DataFrame: A pandas DataFrame containing filtered weather forecast data.
    """
    col = ['Date','Time','Condition','Temperature','Rain','Chance_of_rain']
    df = pd.DataFrame(data,columns=col)
    df = df.sort_values(by = 'Time',ascending = True)

    df_rain = df[(df['Rain']==1) & (df['Time']>=6) & (df['Time']<= 22)]
    df_rain = df_rain[['Time','Condition']]
    df_rain.set_index('Time', inplace = True)

    return df_rain

def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,input_date,df,query):
    """
    Sends a weather forecast message via Twilio SMS.

    Args:
        TWILIO_ACCOUNT_SID (str): Twilio account SID for authentication.
        TWILIO_AUTH_TOKEN (str): Twilio authentication token.
        input_date (str): The date for the weather forecast.
        df (DataFrame): A pandas DataFrame containing weather forecast data.
        query (str): The location for which the weather forecast is sent.

    Returns:
        str: The Twilio message SID.
    """
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body='Hi! \n\n\nToday\'s '+ input_date +
                        ' rain forecast in ' + query +' is:\n\n\n' + str(df),
                        from_=PHONE_NUMBER,
                        to='+YOUR TWILIO NUMBER'
                    )

    return message.sid

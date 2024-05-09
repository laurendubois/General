#!/usr/bin/env python3
import requests
import pendulum

url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact'

headers = {}
headers['User-Agent'] = 'Testing out forecasting API'

params = {}
params['lat'] = 29.717394
params['lon'] = 95.401833

response = requests.get(url, headers=headers, params=params)
forecast = response.json()['properties']['timeseries'][0]
time = pendulum.parse(forecast['time'])
localtime = time.in_timezone('America/Chicago')
celsius = forecast['data']['instant']['details']['air_temperature']
fahrenheit = (celsius * 9/5) +  32

print(f"At {localtime.format('dddd Do [of] MMMM YYYY h:mm A')} it was {round(fahrenheit,2)} degrees F (that's {round(celsius, 2)} degrees C)")

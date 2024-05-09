#!/usr/bin/env python3
import requests
import pendulum

def convert_to_fahrenheit(celsius):
    # converts temp from C to F
    return (celsius * 9/5) + 32

# API endpoint and parameters
url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact'
headers = {'User-Agent': 'Testing out forecasting API'}
params = {'lat': 29.717394, 'lon': -95.401833}

# Make HTTP request
try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise exception for bad status codes
except requests.RequestException as e:
    print("Error fetching data:", e)
    exit(1)

    # Parse JSON response
data = response.json()

# Extract forecast data
forecast = data['properties']['timeseries'][0]
celsius = forecast['data']['instant']['details']['air_temperature']
fahrenheit = convert_to_fahrenheit(celsius)

# Convert time to local timezone
time = pendulum.parse(forecast['time'])
localtime = time.in_timezone('America/Chicago')  # Change timezone as needed

# Print forecast information
print(localtime)
print(
    f"At {localtime.format('dddd Do [of] MMMM YYYY h:mm A')} it was {celsius} degrees Celsius (that's {round(fahrenheit, 2)} degrees Fahrenheit)")
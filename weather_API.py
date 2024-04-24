import requests
import pendulum

# Set up the API request stuff, sometimes API wrappers can do some of this for you
url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact'

headers = {}
headers['User-Agent'] = 'Testing out forecasting API'

params = {}
params['lat'] = 29.717101  # change this to your local lat
params['lon'] = -95.404587  # change this to your local lon

response = requests.get(url, headers=headers, params=params) # FYI this is simpilar to my API statement for WorldCat

# Define the json output
forecast = response.json()['properties']['timeseries'][0]

# Define time and convert to local time
time = pendulum.parse(forecast['time'])
localtime = time.in_timezone('America/Chicago')  # remember to change this value! find https://pendulum.eustace.io/docs

print(f"The local date and time is {localtime}.")  # LD added extra text for clarity

# Convert temp to Celsius and then round it when you print it out
celsius = forecast['data']['instant']['details']['air_temperature']
fahrenheit = (celsius * 9/5) + 32

print(f"The rounded Fahrenheit temperature is {round(fahrenheit, 2)}.")  # LD added extra text for clarity

# Format all the info into a nice sentence
print(f"At {localtime.format('dddd Do [of] MMMM YYYY h:mm A')}, it was {celsius} C° ({round(fahrenheit, 2)} F°.)")

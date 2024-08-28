import requests

def feels_like(temp, humidity):
    return temp - ((0.55 - 0.0055 * humidity) * (temp - 14.5))

def celcius_to_kelvin(temp):
    return temp + 273.15

LAT = -30.03283000
LONG = -51.23019000
API_KEY = "3b6f2edd765dd6fc88169a6d75586b96"
EXCLUDE = "minutely,hourly,daily,alerts"

url = f"https://api.openweathermap.org/data/3.0/onecall" 
payload = {'lat': LAT, 'lon': LONG, 'appid': API_KEY, 'units': 'metric', 'exclude': EXCLUDE}
headers = {'user-agent': 'weather-cli/0.0.1'}

try:
    r = requests.get(url, headers=headers, params=payload)
    # print(r.headers['Content-Type'])
    # print(r.json())

    fl = feels_like(r.json()['current']['temp'], r.json()['current']['humidity'])
    flk = celcius_to_kelvin(fl)

    print('Temperature: %.2f' % r.json()['current']['temp'])
    print('Feels like (C): %.2f' % fl)
    print('Feels like (K): %.2f' % flk)
# except Exception as e:
#     print(e)
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
# finally:
#     print('finally')

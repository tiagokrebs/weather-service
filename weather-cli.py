import requests
import logging
logger = logging.getLogger(__name__)

def feels_like(temp, humidity):
    return temp - ((0.55 - 0.0055 * humidity) * (temp - 14.5))

def celcius_to_kelvin(temp):
    return temp + 273.15

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, filename='weather-cli.log', level=logging.INFO)

LAT = -30.03283000
LONG = -51.23019000
API_KEY = ""
EXCLUDE = "minutely,hourly,daily,alerts"

url = f"https://api.openweathermap.org/data/3.0/onecall" 
payload = {'lat': LAT, 'lon': LONG, 'appid': API_KEY, 'units': 'metric', 'exclude': EXCLUDE}
headers = {'user-agent': 'weather-cli/0.0.1'}

try:
    r = requests.get(url, headers=headers, params=payload)
    # print(r.headers['Content-Type'])
    # print(r.json())
    r.raise_for_status()

    data = r.json()

    fl = feels_like(data['current']['temp'], data['current']['humidity'])
    flk = celcius_to_kelvin(fl)

    print('Temperature: %.2f' % data['current']['temp'])
    print('Feels like (C): %.2f' % fl)
    print('Feels like (K): %.2f' % flk)

except requests.exceptions.InvalidJSONError as e:
    print(f"Invalid JSON: {e}")
    logger.error(f"Invalid JSON: {e}")
except requests.exceptions.ConnectionError as e:
    print(f"Connection error: {e}")
    logger.error(f"Connection error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
    logger.error(f"Request error: {e}")
except requests.exceptions.HTTPError as e:
    status_code = e.response.status_code
    if status_code >= 401 and status_code <= 403:
        print("Authentication error: Invalid API key or insufficient permissions.")
    elif status_code == 429:
        print("Too many requests error: Slow down.")
    else:
        print(f"HTTP error: {e}")
    logger.error(f"Authentication error: {status_code}")
except Exception as e:
    print(f"An error occurred: {e.with_traceback()}")
    logger.error(f"An error occurred: {e.with_traceback()}")
# finally:
#     print('finally')

print("The end.s")
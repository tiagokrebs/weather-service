import requests
import logging
import sys
import json
import time
import daemon
from cache import get_cache, set_cache

logger = logging.getLogger(__name__)
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, filename='weather-cli.log', level=logging.INFO)

API_KEY = "ab01497b830feef11e1577ad2adcdfbb"
USER_AGENT = "weather-cli/0.0.1"

def feels_like(temp, humidity):
    return temp - ((0.55 - 0.0055 * humidity) * (temp - 14.5))

def celcius_to_kelvin(temp):
    return temp + 273.15

def get_long_lat(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct" 
    payload = {'q': city, 'appid': API_KEY, 'LIMIT': '1'}
    headers = {'user-agent': USER_AGENT}

    cache_key = f"geo_{city}"

    data = get_cache(cache_key)

    if data:
        logger.info(f"Using cached data - City {city}")
    else:
        try:
            r = requests.get(url, headers=headers, params=payload)
            logger.info(f"Request {r.status_code} {url} {headers} {payload}")
            r.raise_for_status()
            data = r.json()
            set_cache(cache_key, data, expire=60)
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            logger.error(f"Request error: {e}")
    
    return data[0]['name'], data[0]['lat'], data[0]['lon']

def get_weather(long, lat):
    url = f"https://api.openweathermap.org/data/3.0/onecall" 
    exclude = "minutely,hourly,daily,alerts"
    payload = {'lat': lat, 'lon': long, 'appid': API_KEY, 'units': 'metric', 'exclude': exclude}
    headers = {'user-agent': USER_AGENT}
    cache_key = f"weather_{lat}_{long}_{exclude}"

    # get from cache
    data = get_cache(cache_key)

    if data:
        logger.info(f"Using cached data - Weather {lat} {long}")
    else:
        try:
            r = requests.get(url, headers=headers, params=payload)
            logger.info(f"Request {r.status_code} {url} {headers} {payload}")
            # print(r.headers['Content-Type'])
            # print(r.json())
            
            # in case of error, raise the exception
            r.raise_for_status()

            data = r.json()

            # cache the response
            set_cache(cache_key, data, expire=10)

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

    return data

def show_weather(weather, city_name, output_format='text'):
    if weather:
        fl = feels_like(weather['current']['temp'], weather['current']['humidity'])
        flk = celcius_to_kelvin(fl)

        if output_format == 'json':
            print(json.dumps({"city_name": city_name, 
                              "temperature": f'%.2f' % weather['current']['temp'],
                              "feels_like_C": f'%.2f' % fl, 
                              "feels_like_K": f'%.2f' % flk}))
        elif output_format == 'text':
            print(f'City: {city_name}')
            print('Temperature: %.2f' % weather['current']['temp'])
            print('Feels like (C): %.2f' % fl)
            print('Feels like (K): %.2f' % flk)
    else:
        print("No weather data available.")
        logger.error("No weather data available.")

# def run_daemon(city, output_format, interval):
#     while True:
#         city_name, long, lat = get_long_lat(city)
#         weather = get_weather(long, lat)
#         show_weather(weather, city_name, output_format)
#         time.sleep(interval)

def main():
    if len(sys.argv) < 2:
        print("Usage: python weather-cli.py <city> <output_format>")
        print("Example: python weather-cli.py Sao_Paulo json")
        print("Output format: json, text")
        sys.exit(1)
    
    city = sys.argv[1]

    if len(sys.argv) == 3:
        output_format = sys.argv[2]
    else:
        output_format = 'text'

    if output_format not in ['json', 'text']:
        print("Invalid output format. Please use 'json' or 'text'.")
        logger.error("Invalid output format. Please use 'json' or 'text'.")
        sys.exit(1)

    # interval = 30
    # with daemon.DaemonContext():
    #     run_daemon(city, output_format, interval)

    city_name, long, lat = get_long_lat(city)
    weather = get_weather(long, lat)
    show_weather(weather, city_name, output_format)

if __name__ == "__main__":
    main()
import unittest
import sys
import os
from unittest.mock import patch
# need to add the parent directory to the sys path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from weather_cli import feels_like, celcius_to_kelvin, get_long_lat, get_weather

# python -m unittest test_weather_cli.py -v

class TestWeatherCLI(unittest.TestCase):

    def test_feels_like(self):
        self.assertAlmostEqual(feels_like(30, 50), 25.737, places=2)
        self.assertAlmostEqual(feels_like(20, 80), 19.395, places=2)

    def test_celcius_to_kelvin(self):
        self.assertEqual(celcius_to_kelvin(0), 273.15)
        self.assertEqual(celcius_to_kelvin(100), 373.15)

    @patch('weather_cli.get_cache')
    @patch('weather_cli.set_cache')
    @patch('weather_cli.requests.get')
    def test_get_long_lat(self, mock_get, mock_set_cache, mock_get_cache):
        mock_get_cache.return_value = None
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'name': 'Test City', 'lat': 10.0, 'lon': 20.0}]
        
        city_name, lat, lon = get_long_lat('Test City')
        self.assertEqual(city_name, 'Test City')
        self.assertEqual(lat, 10.0)
        self.assertEqual(lon, 20.0)

    @patch('weather_cli.get_cache')
    @patch('weather_cli.set_cache')
    @patch('weather_cli.requests.get')
    def test_get_weather(self, mock_get, mock_set_cache, mock_get_cache):
        mock_get_cache.return_value = None
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'current': {'temp': 25.0, 'humidity': 60}}
        
        weather = get_weather(20.0, 10.0)
        self.assertIn('current', weather)
        self.assertEqual(weather['current']['temp'], 25.0)
        self.assertEqual(weather['current']['humidity'], 60)

if __name__ == '__main__':
    unittest.main()
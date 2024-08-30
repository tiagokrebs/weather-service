from behave import given, when, then
import unittest
import sys
import os
# need to add the parent directory to the sys path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from weather_cli import feels_like, celcius_to_kelvin, get_long_lat, get_weather

# behave

@given('the temperature is {temp:d} degrees Celsius')
def step_given_temperature(context, temp):
    context.temp = temp

@given('the humidity is {humidity:d} percent')
def step_given_humidity(context, humidity):
    context.humidity = humidity

@when('I calculate the feels like temperature')
def step_when_calculate_feels_like(context):
    context.result = feels_like(context.temp, context.humidity)

@then('the result should be {expected_result:f} degrees Celsius')
def step_then_check_feels_like(context, expected_result):
    assert context.result == expected_result, f"Expected {expected_result}, but got {context.result}"

@when('I convert the temperature to Kelvin')
def step_when_convert_to_kelvin(context):
    context.result = celcius_to_kelvin(context.temp)

@then('the result should be {expected_result:f} Kelvin')
def step_then_check_kelvin(context, expected_result):
    assert context.result == expected_result, f"Expected {expected_result}, but got {context.result}"
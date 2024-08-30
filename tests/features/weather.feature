    Feature: Weather CLI

      Scenario: Calculate feels like temperature
        Given the temperature is 30 degrees Celsius
        And the humidity is 50 percent
        When I calculate the feels like temperature
        Then the result should be 25.737 degrees Celsius

      Scenario: Convert Celsius to Kelvin
        Given the temperature is 0 degrees Celsius
        When I convert the temperature to Kelvin
        Then the result should be 273.15 Kelvin
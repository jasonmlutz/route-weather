# route-weather
CLI tools for combining travel directions with weather forecasts

Powered by Darksky (https://darksky.net/poweredby/)

Map data from Mapbox (https://www.mapbox.com/)

Note: Weather data for trips more than 10 days in the future will be based on
historical trends.

## Instructions
1. Download `route_weather.py` and `Credentials_template.py` to the same folder; rename the latter to `Credentials.py`.

1. 2. Obtain API keys from [Mapbox](https://www.mapbox.com/) and [Dark Sky](https://darksky.net/dev). Enter these keys in `Credentials.py`.

1. Install necessary third-party libraries:
```
pip3 install pandas mapbox darkskylib
```

1. Run route-weather:
```python3 route-weather.py
```

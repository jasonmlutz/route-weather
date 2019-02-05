"""This is the first attempt at combining all the necessary methods to fetch
    and display directions paired with weather data.
    """
# local imports
from Credentials import mapbox_token, darksky_token
from fetch_departure_time import get_departure_time
from fetch_directions import fetch_directions_summary
from fetch_weather import fetch_weather_summary
from input_verification import location_candidates, display_and_verify
# non-standard package imports
from mapbox import Geocoder, Directions
from darksky import forecast
# standard imports
import copy
import time
from datetime import datetime as dt

print('\n\n\nWelcome to Route Weather!')
print('\nMap data from Mapbox (mapbox.com)')
print('Powered by Dark Sky (darksky.net/poweredby/)')
time.sleep(2)
print('\nTo begin, let\'s get your starting point:')
raw_origin = input('Starting location: ')
print('\nLet\'s make sure we understood that location correctly.\n')
origin_dict = location_candidates(raw_origin, mapbox_token)
origin_checked = display_and_verify(origin_dict)
print('\nNext, let\'s get your destination:')
raw_destination = input('Destination: ')
print('\nAgain, let\'s doubld check.\n')
destination_dict = location_candidates(raw_destination, mapbox_token)
destination_checked = display_and_verify(destination_dict)

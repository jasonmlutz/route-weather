"""This is the first attempt at combining all the necessary methods to fetch
    and display directions paired with weather data.
    """
# standard imports
import copy
import time
import subprocess as sp
from datetime import datetime as dt
# non-standard package imports
from mapbox import Geocoder, Directions
from darksky import forecast
# local imports
from Credentials import mapbox_token, darksky_token
from fetch_departure_time import get_departure_time
from fetch_directions import fetch_directions_summary
from fetch_weather import fetch_weather_summary
from input_verification import location_candidates, display_and_verify

#def route_weather():
# opening
sp.call('clear',shell=True)
print('Welcome to Route Weather!')
print('\nMap data from Mapbox (mapbox.com)')
print('Powered by Dark Sky (darksky.net/poweredby/)')
time.sleep(2)

# fetch & verify starting point and destionation
print('\nTo begin, let\'s get your starting point:')
raw_origin = input('Starting location: ')
print('\nLet\'s make sure we understood that location correctly.\n')
origin_dict = location_candidates(raw_origin, mapbox_token)
origin_checked = display_and_verify(origin_dict)
print('\nNext, let\'s get your destination:')
raw_destination = input('Destination: ')
print('\nAgain, let\'s double check.\n')
destination_dict = location_candidates(raw_destination, mapbox_token)
destination_checked = display_and_verify(destination_dict)

# fetch departure time
print('\nNow for information about your departure time:\n')
departure_time = get_departure_time()

# fetch directions
directions_summary = fetch_directions_summary(origin_checked, destination_checked, mapbox_token)

#create the output dictionary
directions_output = copy.deepcopy(directions_summary)
for i in range(1, len(directions_summary)+1):
    del directions_output[i][-1]

# fetch weather at starting point & departure time
coords = list(reversed(origin_checked['center']))
wx = fetch_weather_summary(coords[0], coords[1], departure_time, darksky_token)
directions_output[1].extend((wx[0], wx[1]))

#fetch the rest of the weather data
waypoint_time = wx[2] #posix departure_time, timezone aware
for i in range (2, len(directions_summary)+1):
    waypoint_time += round(directions_summary[i][1])
    waypoint_coords = list(reversed(directions_summary[i][3]))
    waypoint_wx = fetch_weather_summary(waypoint_coords[0], waypoint_coords[1], waypoint_time, darksky_token)
    directions_output[i].extend((waypoint_wx[0], waypoint_wx[1]))

print('\nStep #: instruction, time (sec) to next step, distance (meters) to next step, wx, temp')
print("\n".join("{}: {}".format(k, v) for k, v in directions_output.items()))

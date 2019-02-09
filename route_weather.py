""" The combined version of route_weather.
    """
# standard imports
import copy
import time
import sys
import subprocess as sp
from datetime import datetime as dt
# third-party package imports
from mapbox import Geocoder, Directions
from darksky import forecast
# API credentials imports
from Credentials import mapbox_token, darksky_token

# Print iterations progress --
# from https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar_graphic = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar_graphic, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def fetch_departure_time():
    """ Get user's departure time; either now or in the future.

    This information will be passed to Dark Sky to fetch weather information
    at origin + departure time; Dark Sky accepts either a Unix time or a string
    of the form [YYYY]-[MM]-[DD]T[HH]:[MM]. In the latter case, if no timezone
    information is included, the time is interpreted (by Dark Sky)
    as local time with respect to the location given.

    Future feature: limit return to one form.

    Parameters:
    none

    Returns:
    dept_time (int or str): Current Unix time or a .isoformat() style string
    [YYYY]-[MM]-[DD]T[HH]:[MM]
    """
    print('\n1. Leave now. \n2. Specify future departure time.')
    while True:
        try:
            depart_now = int(input())
        except ValueError:
            print('Oops! That was not a valid choice. Try again...')
        else:
            if depart_now in [1, 2]:
                break
            else:
                print('Oops! That was not a valid choice. Try again...')
                continue
    if depart_now == 1:
        print('Weather data will be based on an immediate departure.')
        departure_datetime = int(time.time())
    if depart_now == 2:
        print("Let's get your departure date and time.")
        departure_date = input('Please enter your departure date as MM/DD/YY ... ')
        departure_time = input('Please enter your departure time as HH:MM ... ')
        departure_datetime_raw = dt.strptime(departure_date+departure_time, "%m/%d/%y%H:%M")
        departure_datetime_printable = departure_datetime_raw.strftime("%A, %B %d %Y, %I:%M%p")
        print("\nLocal departure time recorded as {}".format(departure_datetime_printable))
        departure_datetime = departure_datetime_raw.isoformat()
    return departure_datetime

def fetch_directions_summary(origin, destination, key):
    """
    Fetch driving directions using Mapbox api.

    Parameters:
    origin (dict): The origin (starting position) of the desired directions.
    destination (dict): The destination of the desired directions.
        Both parameters are of the form obtained by
        geocoder.forward(str(origin_raw)).json()['features'][0], where origin_raw
        is a string corresponding to the origin. This is compatible with the
        returns of the 'input_verification.py' methods.

    Returns:
    directions_summary (dict): keys are integers 0, 1, 2, ... n-1, where n is the
    number of steps in the directions (arriving at the destination counts
    as one step); values are lists (four items) of the form instruction, duration
    to next route step (in seconds), distance to next route step (in meters),
    location of current step.
    """
    service = Directions(access_token=key)
    response = service.directions([origin, destination], profile='mapbox/driving', steps=True)
    route = response.json()
    route_steps = route['routes'][0]['legs'][0]['steps']
    num_steps = len(route_steps)
    keys = range(num_steps)
    directions_summary = []
    for i in keys:
        instruction = route_steps[i]['maneuver']['instruction']
        duration = route_steps[i]['duration'] # in seconds
        distance = route_steps[i]['distance'] # in meters
        location = route_steps[i]['maneuver']['location']
        directions_summary.append([instruction, duration, distance, location])
    return directions_summary

def fetch_weather_summary(latitude, longitude, time, key):
    """
    Returns summary and temperature for a location at a specified time in the
    past or future.

    Parameters:
    latitude (float): The latitide of the location.
    longitude (float): The longitude of the location.
    time (int/str): The time of the forecast/recorded weather. Either be a UNIX
        time (that is, seconds since midnight GMT on 1 Jan 1970) or a string
        formatted as follows: [YYYY]-[MM]-[DD]T[HH]:[MM]:[SS]. The former
        option is of the structure optained from int(time.time()); the latter
        as could be obtained from from datetime.datetime(YYYY, MM, DD,
        HH, MM, SS).isoformat().

    Returns:
    A tuple. The first element is a short summary of the weather conditions
        (e.g. sunny, partly cloudy, rain); the second the integer-valued
        temperature in Fahrenheit (as dictated by the variable units = 'us').
    """
    inputs = key, latitude, longitude
    weather_full = forecast(*inputs, time=time, units='us')
    weather_current = weather_full['currently']
    return weather_current['summary'], int(weather_current['temperature']), weather_full.time

def fetch_location_candidates(raw_location, key):
    """
    Returns a dictionary of possible locations.

    With the goal of correctly interpreting a user's location input, this
    function utilizes the Geocoder feature of Mapbox to return a dictionary of
    possible candidates for the users intended input location.

    Parameters:
    user_input (str): A location, such as street address or landmark.

    Returns:
    candidates (list): A list encoding the responses from Mapbox based on
    the user's input.
    """
    geocoder = Geocoder(access_token=key)
    response = geocoder.forward(str(raw_location), limit=10)
    collection = response.json()
    # The 'features' key tracks the returned data for each possible location.
    num_features = len(collection['features'])
    candidates = []
    for i in range(num_features):
        candidates.append(collection['features'][i])
    return candidates

def verify_input_location(candidates):
    """
    Presents a dictionary of potential locations to the user.
    """
    print('The following locations were returned based on your entry:\n')
    for counter, value in enumerate(candidates, 1):
        # In particular, the 'place_name' of a feature houses the address, and
        # will be used to display back the user for verification.
        print("{}: {}".format(counter, value['place_name']))
    while True:
        try:
            user_choice = int(input('\nWhich option best reflects your intended location? '))
        except ValueError:
            print('Oops! That was not a valid choice. Try again...')
        else:
            if user_choice - 1 in range(len(candidates)):
                break
            else:
                print('Oops! That was not a valid choice. Try again...')
                continue
    return candidates[user_choice-1]

def route_weather():
    """ Method for obtaining driving directions paired with weather conditions
    at each route step.
    """
    # opening
    sp.call('clear', shell=True)
    print('Welcome to Route Weather!')
    print('\nMap data from Mapbox (mapbox.com)')
    print('Powered by Dark Sky (darksky.net/poweredby/)')
    time.sleep(1)

    # fetch & verify starting point and destionation
    print('\nTo begin, let\'s get your starting point:')
    raw_origin = input('Starting location: ')
    print('\nLet\'s make sure we understood that location correctly.\n')
    origin_cand_list = fetch_location_candidates(raw_origin, mapbox_token)
    origin_checked = verify_input_location(origin_cand_list)
    print('\nNext, let\'s get your destination:')
    raw_destination = input('Destination: ')
    print('\nAgain, let\'s double check.\n')
    destination_cand_list = fetch_location_candidates(raw_destination, mapbox_token)
    destination_checked = verify_input_location(destination_cand_list)

    # fetch departure time
    print('\nNow for information about your departure time:')
    departure_time = fetch_departure_time()

    print('\nFetching directions...')
    # fetch directions
    directions_summary = fetch_directions_summary(origin_checked, destination_checked, mapbox_token)

    #create the output dictionary
    directions_output = copy.deepcopy(directions_summary)
    for i in range(len(directions_summary)):
        del directions_output[i][-1]
    print("\nFetching weather data at each route step...")

    # fetch weather at starting point & departure time
    coords = list(reversed(origin_checked['center']))
    departure_weather = fetch_weather_summary(coords[0], coords[1], departure_time, darksky_token)
    directions_output[0].extend((departure_weather[0], departure_weather[1]))

    #fetch the rest of the weather data
    waypoint_time = departure_weather[2] #posix time
    for counter, value in enumerate(directions_summary, 1):
        print_progress(counter, len(directions_summary))
        #print(counter, len(directions_summary))
        waypoint_time += round(value[1])
        waypoint_coords = list(reversed(value[3]))
        waypoint_weather = fetch_weather_summary(waypoint_coords[0], waypoint_coords[1], waypoint_time, darksky_token)
        directions_output[counter-1].extend([waypoint_weather[0], waypoint_weather[1]])

    print('\nStep #: instruction, time (sec) to next step, distance (meters) to next step, weather, temp')
    for counter, value in enumerate(directions_output, 1):
        print("{}: {}".format(counter, value))

route_weather()

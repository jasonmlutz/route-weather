""" The combined version of route_weather.
    """
# standard imports
import copy
import time
import calendar
import subprocess as sp
# third-party package imports
from mapbox import Geocoder, Directions
from darksky import forecast
# credential imports
from Credentials import darksky_token, mapbox_token

def get_departure_time():
    """ Get user's departure time; either now or in the future.

    Parameters:
    none

    Returns:
    dept_time (str): A .isoformat() style string [YYYY]-[MM]-[DD]T[HH]:[MM]
    """
    print('\n 1. Leave now. \n 2. Specify future departure time.')
    while True:
        try:
            depart_now = int(input())
        except ValueError:
            print('Oops! That was not a valid choice. Try again...')
        else:
            if depart_now in range(1, 3):
                break
            else:
                print('Oops! That was not a valid choice. Try again...')
                continue
    if depart_now == 1:
        print('Thanks! Weather data will be based on an immediate departure.')
        departure_datetime = int(time.time())
    if depart_now == 2:
        print('Thanks! Let\'s get your departure date and time.')
        departure_year = input('Please enter your departure year YYYY: ')
        departure_month = input('Please enter your departure month MM: ')
        departure_day = input('Please enter your departure day DD: ')
        departure_hour = input('Please enter your departure hour HH, [0,23]: ')
        departure_minute = input('Please enter your departure day MM: ')
        departure_date = departure_year+'-'+departure_month+'-'+departure_day
        departure_time = departure_hour+':'+departure_minute
        departure_datetime = departure_date+'T'+departure_time+':00'
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
    directions_summary (dict): keys are integers 1, 2, 3 corresponding to the
    number of steps in the fetched directions (arriving at the destination counts
    as one step); values are lists (triples) of the form instruction, duration to next
    route step (in seconds), distance to next route step (in meters).
    """
    service = Directions(access_token=key)
    response = service.directions([origin, destination], profile='mapbox/driving', steps=True)
    route = response.json()
    route_steps = route['routes'][0]['legs'][0]['steps']
    num_steps = len(route_steps)
    keys = range(1, num_steps+1)
    directions_summary = {}
    for i in keys:
        instruction = route_steps[i-1]['maneuver']['instruction']
        duration = route_steps[i-1]['duration'] # in seconds
        distance = route_steps[i-1]['distance'] # in meters
        location = route_steps[i-1]['maneuver']['location']
        directions_summary[i] = [instruction, duration, distance, location]
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
        formatted as follows: [YYYY]-[MM]-[DD]T[HH]:[MM]:[SS][timezone]. The former
        option is of the structure optained from int(time.time()); the latter
        as could be obtained from from datetime.datetime(YYYY, MM, DD,
        HH, MM, SS).isoformat(). To avoid issues with timezones, we will use the
        former option to represent time.

    Returns:
    A tuple. The first element is a short summary of the weather conditions
        (e.g. sunny, partly cloudy, rain); the second the integer-valued
        temperature in Fahrenheit (as dictated by the variable units = 'us').
    """
    inputs = key, latitude, longitude
    wx_full = forecast(*inputs, time=time, units='us')
    wx_current = wx_full['currently']
    return wx_current['summary'], int(wx_current['temperature']), wx_full.time

def location_candidates(raw_location, key):
    """
    Returns a dictionary of possible locations.

    With the goal of correctly interpreting a user's input location input, this
    function utilizes the Geocoder feature of Mapbox to return a dictionary of
    possible candidates for the users intended input locationself.

    Parameters:
    user_input (str): A location, such as street address or landmark.

    Returns:
    candidates (dict): A dictionary encoding the responses from Mapbox based on
    the user's input. Keys are integers 1, 2, ...; values are the precise place
    names for the fetched locations.
    """
    geocoder = Geocoder(access_token=key)
    response = geocoder.forward(str(raw_location), limit=10)
    collection = response.json()
    # The 'features' key tracks the returned data for each possible location.
    # In particular, the 'place_name' of a feature houses the address, and
    # will be used to display back the the user for verification.  We construct
    # a dictionary to meaningfully display each place_name to the user.
    #
    # For conveinence, the dictionary keys begin at 1; this seems more
    # intuitive from a ui perspective.
    num_features = len(collection['features'])
    candidates = {}
    keys = range(1, num_features+1)
    for i in keys:
        candidates[i] = collection['features'][i-1]
    return candidates

def display_and_verify(candidate_dict):
    """
    Presents a dictionary of potential locations to the user.
    """
    print('The following locations were returned based on your entry.')
    # We create a copy of the candidate dictionary to display to the user,
    # appending an option to indicate that no option best meets the user's
    # intended location.
    displayed_candidate_dict = copy.copy(candidate_dict)
    # Removing these next line for now;  No need display a different dictionary.
    # I will adjust this once I know how
    # the final veresion will handle needing the user to add more specificity
    # to the location information.
    #displayed_candidate_dict[str(len(candidate_dict)+1)] = 'None of these are right.'
    print("\n".join("{}: {}".format(k, v['place_name']) for k, v in displayed_candidate_dict.items()))
    print('\n')
    while True:
        try:
            user_choice = int(input('Which option best reflects your intended location? '))
        except ValueError:
            print('Oops! That was not a valid choice. Try again...')
        else:
            if user_choice in range(1, len(displayed_candidate_dict)+1):
                break
            else:
                print('Oops! That was not a valid choice. Try again...')
                continue
    return candidate_dict[user_choice]

def get_departure_time():
    """ Get user's departure time; either now or in the future.

    Parameters:
    none

    Returns:
    dept_time (str): A .isoformat() style string [YYYY]-[MM]-[DD]T[HH]:[MM]
    """
    print('\n 1. Leave now. \n 2. Specify future departure time.')
    while True:
        try:
            depart_now = int(input())
        except ValueError:
            print('Oops! That was not a valid choice. Try again...')
        else:
            if depart_now in range(1, 3):
                break
            else:
                print('Oops! That was not a valid choice. Try again...')
                continue
    if depart_now == 1:
        departure_datetime = int(time.time())
    if depart_now == 2:
        print('Thanks! Let\'s get your departure date and time.')
        departure_year = input('Please enter your departure year YYYY: ')
        departure_month = input('Please enter your departure month MM: ')
        departure_day = input('Please enter your departure day DD: ')
        departure_hour = input('Please enter your departure hour HH, [0,23]: ')
        departure_minute = input('Please enter your departure day MM: ')
        departure_date = departure_year+'-'+departure_month+'-'+departure_day
        departure_time = departure_hour+':'+departure_minute
        departure_datetime = departure_date+'T'+departure_time+':00'
    return departure_datetime

#create calendar month number -> name dictionary
month_names = dict((v,k) for v,k in enumerate(calendar.month_abbr))

def route_weather():
    # opening
    sp.call('clear',shell=True)
    print('Welcome to Route Weather!')
    print('\nMap data from Mapbox (mapbox.com)')
    print('Powered by Dark Sky (darksky.net/poweredby/)')
    time.sleep(1)

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
    if isinstance(departure_time, int):
        print('Immediate departure time recorded.')
    else:
        departure_month_name = month_names[int(departure_time[5:7])]
        print('\nLocal departure time recorded as {} {}, {} at {}'.format(departure_month_name, int(departure_time[8:10]), departure_time[0:4], departure_time[11:16]))

    print('\nFetching directions and weather data at each step...')
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

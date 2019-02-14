""" The combined version of route_weather.
    """
# standard imports
import time
import sys
import datetime
import subprocess as sp
import pandas as pd
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

    Parameters:
    iteration (int): current iteration, required
    total (int): total iterations, required
    prefix (str): prefix string, optional
    suffix (str): suffix string, optional
    decimals (int): positive number of decimals in percent complete, optional
    bar_length (int): character length of bar, optional
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar_graphic = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar_graphic, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def print_ds(printed_string):
    """
    Print an input string in double-space (ds) format, i.e. new lines before
    and after.
    """
    print("\n"+str(printed_string)+"\n")

def fetch_departure_time(is_debug=False):
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
    print("\n1. Leave now. \n2. Specify future departure time.")
    while True:
        try:
            depart_now = int(input())
        except ValueError: # if, for example, user doesn't enter an integer
            print("Oops! That was not a valid choice. Try again...")
        else:
            if depart_now in [1, 2]:
                break
            else: # if, for example, user enters an integer outside [1,2]
                print("Oops! That was not a valid choice. Try again...")
                continue
    if depart_now == 1:
        print("Weather data will be based on an immediate departure.")
        departure_datetime = int(time.time())
    if depart_now == 2:
        print("Let's get your departure date and time.")
        if is_debug:
            departure_date = input("Please enter your departure date as MM/DD/YY ... ")
            departure_time = input("Please enter your departure time as HH:MM ... ")
            departure_datetime_raw = datetime.datetime.strptime(departure_date+departure_time, "%m/%d/%y%H:%M")
        else:
            while True:
                try:
                    departure_date = input("Please enter your departure date as MM/DD/YY ... ")
                    departure_time = input("Please enter your departure time as HH:MM ... ")
                    departure_datetime_raw = datetime.datetime.strptime(departure_date+departure_time, "%m/%d/%y%H:%M")
                    break
                except ValueError: # bad input format for date and/or time
                    print("Something went wrong with your date/time input(s). Let's try again...")
        departure_datetime_printable = departure_datetime_raw.strftime("%A, %B %d %Y, %I:%M%p")
        print("\nLocal departure time recorded as {}".format(departure_datetime_printable))
        departure_datetime = departure_datetime_raw.isoformat()
    return departure_datetime

def fetch_directions_summary(origin, destination, key, is_debug=False):
    """
    Fetch driving directions using Mapbox api.

    Parameters:
    origin (dict): The origin (starting position) of the desired directions.
    destination (dict): The destination of the desired directions.
        Both parameters are of the form obtained by
        geocoder.forward(str(origin_raw)).json()['features'][0], where origin_raw
        is a string corresponding to the origin. This is compatible with the
        returns of the 'input_verification.py' methods.
    key (str): Mapbox api token. More info about the necessary token at
        https://docs.mapbox.com/help/glossary/access-token/

    Returns:
    directions_summary (list): a list of length n-1, where n is the
    number of steps in the directions (arriving at the destination counts
    as one step); list elements are lists (of length 4) of the form
        [instruction,
        duration to next route step (in seconds),
        distance to next route step (in meters),
        location of current step].
    """
    service = Directions(access_token=key)
    response = service.directions([origin, destination], profile='mapbox/driving', steps=True)
    route = response.json()
    if is_debug:
        route_steps = route['routes'][0]['legs'][0]['steps']
    else:
        try:
            route_steps = route['routes'][0]['legs'][0]['steps']
        except IndexError: # if, for example, driving directions requested from
                           # Boston to London
            print("\nSomething went wrong when fetching directions ....")
            return
    directions_summary = []
    for step in route_steps:
        instruction = step['maneuver']['instruction']
        duration = step['duration'] # in seconds
        distance = step['distance'] # in meters
        location = step['maneuver']['location']
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
    key (str): Dark Sky api token. More info at https://darksky.net/dev

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
    candidates = []
    for location in collection['features']:
        candidates.append(location)
    return candidates

def verify_input_location(candidates):
    """
    Presents a list of potential locations to the user.
    """
    print("The following locations were returned based on your entry:\n")
    for counter, value in enumerate(candidates, 1):
        # In particular, the 'place_name' of a feature houses the address, and
        # will be used to display back the user for verification.
        print("{}: {}".format(counter, value['place_name']))
    while True:
        try:
            user_choice = int(input("\nWhich option best reflects your intended location? "))
        except ValueError: # input not an integer
            print("Oops! That was not a valid choice. Try again...")
        else:
            if user_choice - 1 in range(len(candidates)):
                break
            else: # input is an integer but outside of valid range
                print("Oops! That was not a valid choice. Try again...")
                continue
    return candidates[user_choice-1]

def convert_distance(meters):
    """ Converts distance in meters to miles or feet, depending on whether the
    distance is above 1 mile.
    """
    feet = int(meters*3.281)
    miles = round(feet/5280, 1)
    if miles < 0.1:
        output = (feet, 'feet')
    else: output = (miles, 'mile(s)')
    return output

def route_weather(is_debug=False, verbose=True, csv_output=True):
    """ Method for obtaining driving directions paired with weather conditions
    at each route step.

    Parameters:
    is_debug (boolean): optional parameter for debugging; if True, try/except
        calls are skipped in favor of printing the relevant stack trace
    verbose (boolean): optional; if True, prints the directions/weather
        in addition to returning the output of the function
    csv_output (boolean): optional; if True, directions_output is written to a
        csv file in the cwd. File name formatted as route_weather+timestamp.csv

    Returns:
    directions_df (pandas dataframe): columns are
        [driving instruction (str),
         time to next step (str, in the form HH:MM:SS),
         distance to the next step (str, in miles or feet, given by convert_distance)
         weather conditions at the step (str)
         temperature at the step (int, in degrees Fahrenheit)].
    """
    # opening
    sp.call('clear', shell=True)
    print("Welcome to Route Weather!")
    print("\nMap data from Mapbox (mapbox.com)")
    print("Powered by Dark Sky (darksky.net/poweredby/)")
    time.sleep(1)
    print("\nBased on your inputs of origin, destination, and departure time,")
    print("Route Weather will generate driving directions paired with the weather conditions")
    print("you can expect at the time and location for each step in the directions!")
    time.sleep(2)

    # fetch & verify starting point and destionation
    print("\nTo begin, let's get your starting point:")
    if is_debug:
        raw_origin = input("Starting location: ")
        origin_cand_list = fetch_location_candidates(raw_origin, mapbox_token)
    else:
        while True:
            try:
                raw_origin = input("Starting location: ")
                origin_cand_list = fetch_location_candidates(raw_origin, mapbox_token)
                break
            except KeyError: # if, for example, the user presses enter without
                             # entering a location
                print("\nSomething went wrong interpreting your location input. Let's try again...")
    print_ds("Let's make sure we understood that location correctly.")
    origin_checked = verify_input_location(origin_cand_list)
    print("\nNext, let's get your destination:")
    if is_debug:
        raw_destination = input("Destination: ")
        destination_cand_list = fetch_location_candidates(raw_destination, mapbox_token)
    else:
        while True:
            try:
                raw_destination = input("Destination: ")
                destination_cand_list = fetch_location_candidates(raw_destination, mapbox_token)
                break
            except KeyError: # if, for example, the user presses enter without
                             # entering a location
                print_ds("Something went wrong interpreting your location input. Let's try again...")
    print_ds("Again, let's double check.")
    destination_checked = verify_input_location(destination_cand_list)

    # fetch departure time
    print("\nNow for information about your departure time:")
    departure_time = fetch_departure_time(is_debug=is_debug)

    # fetch directions
    print("\nFetching directions...")
    directions_summary = fetch_directions_summary(origin_checked, destination_checked, mapbox_token, is_debug=is_debug)

    # fetch weather at starting point & departure time
    print("\nFetching weather data at each route step...")
    print_progress(0, len(directions_summary))
    coords = list(reversed(origin_checked['center']))
    departure_weather = fetch_weather_summary(coords[0], coords[1], departure_time, darksky_token)
    directions_summary[0].extend((departure_weather[0], departure_weather[1]))

    #fetch the remaining weather data
    waypoint_time = departure_weather[2] #posix time
    for counter, step in enumerate(directions_summary[1:], 1):
        print_progress(counter, len(directions_summary))
        waypoint_time += round(step[1])
        waypoint_coords = list(reversed(step[3]))
        waypoint_weather = fetch_weather_summary(waypoint_coords[0], waypoint_coords[1], waypoint_time, darksky_token)
        directions_summary[counter].extend([waypoint_weather[0], waypoint_weather[1]])
    print_progress(1, 1) # to print 100% progress

    #change the time format to HH:MM:SS and convert meters to miles, feet
    for step in directions_summary:
        step[1] = str(datetime.timedelta(seconds=int(step[1])))
        (distance, units) = convert_distance(step[2])
        step[2] = '{} {}'.format(distance, units)

    # build the data frame output
    column_names = ['instruction', 'duration', 'distance', 'location', 'wx conditions', 'temperature']
    directions_df = pd.DataFrame(directions_summary, columns=column_names)
    del directions_df['location'] # this was used for fetching weather, not ui friendly

    # optionally output the navigation + weather info to a csv file
    if csv_output:
        unix_timestamp = str(int(time.time()))
        file_name = "rw_"+unix_timestamp+".csv"
        print("\nWriting data to {} ...".format(file_name))
        print_progress(0, 1)
        directions_df.to_csv(file_name)
        print_progress(1, 1)

    # optionally print
    if verbose:
        print(directions_df)

    # and we're done!
    return directions_df

route_weather()

"""This is the first attempt at combining all the necessary methods to fetch
    and display directions paired with weather data.
    """
import copy
from mapbox import Geocoder, Directions
from darksky import forecast
from Credentials import *
def location_candidates(user_input):
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
    geocoder = Geocoder(access_token=str(mapbox_token))
    response = geocoder.forward(str(user_input), limit=10)
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
        candidates[i] = collection['features'][i-1]['place_name']
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
    print("\n".join("{}: {}".format(k, v) for k, v in displayed_candidate_dict.items()))
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

def fetch_directions_summary(origin, destination):
    """
    Fetch driving directions using Mapbox api.

    Parameters:
    origin (dict): The origin (starting position) of the desired directions.
    destination (dict): The destination of the desired directions.
        Both parameters are of the form obtained by
        geocoder.forward(str(origin_raw)).json()['features'][0], where origin_raw
        is a string corresponding to the origin. This is compatible with the
        returns of the 'input verification' methods.

    Returns:
    directions_summary (dict): keys are integers 1, 2, 3 corresponding to the
    number of steps in the fetched directions (arriving at the destination counts
    as one step); values are tuples (triples) of the form instruction, duration to next
    route step (in seconds), distance to next route step (in meters).
    """
    service = Directions(access_token=str(mapbox_token))
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
        directions_summary[i] = (instruction, duration, distance)
    return directions_summary

def fetch_weather_summary(latitude, longitude, time):
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
    inputs = darksky_token, latitude, longitude
    wx_full = forecast(*inputs, time=time, units='us')
    wx_current = wx_full['currently']
    return wx_current['summary'], int(wx_current['temperature'])

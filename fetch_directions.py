"""This module takes user input origin and destination
    and fetches directions using the mapbox cli api.
    """
from mapbox import Directions
from Credentials import mapbox_token

def fetch_directions_summary(origin, destination):
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

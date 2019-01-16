"""This module takes user input location (origin/destination)
    and calls mapbox geocoder based on user input. Response
    is then returned to the user for verification."""
from mapbox import Geocoder
from Credentials import mapbox_token
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
    the user's input. Keys are integers 0, 1, ...; values are the precise place
    names for the fetched locations.
    """
    geocoder = Geocoder(access_token=str(mapbox_token))
    response = geocoder.forward(str(user_input))
    collection = response.json()
    num_features = len(collection['features'])
    candidates = {}
    keys = range(num_features)
    for i in keys:
        candidates[i] = collection['features'][i]['place_name']
    return candidates

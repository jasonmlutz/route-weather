""" This module contains functions which will allow a user's input location
    (origin/destination) to be communicated to Mapbox and then verified by the
    user.
    """
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

def choose_location(candidate_dict):
    """
    Presents a dictionary of potential locations to the user, then takes user
    input to confirm correct choice.
    """

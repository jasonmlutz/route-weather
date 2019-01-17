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
    keys = range(1, num_features+1)
    for i in keys:
        candidates[i] = collection['features'][i-1]['place_name']
    return candidates

def display_and_verify(candidate_dict):
    """
    Presents a dictionary of potential locations to the user.
    """
    print('The following locations were returned based on your entry.')
    displayed_candidate_dict = candidate_dict
    displayed_candidate_dict[str(len(candidate_dict)+1)] = 'None of these are right.'
    print("\n".join("{}: {}".format(k, v) for k, v in displayed_candidate_dict.items()))
    user_choice = input('Which option best reflects your intended location? ')
    #if type(user_choice) -- try/except? still want to catch a need to restart
    return user_choice

def user_location_selection(candidate_dict):
    """
    Takes a numerical input from the user for the purpose of verifying
    location input.
    """
    return candidate_dict
    # maybe this isn't needed? display_and_verify is looking promising

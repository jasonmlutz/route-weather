""" This module contains functions which will allow a user's input location
    (origin/destination) to be communicated to Mapbox and then verified by the
    user.
    """
import copy
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

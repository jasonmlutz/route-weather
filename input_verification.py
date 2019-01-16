"""This module takes user input location (origin/destination)
    and calls mapbox geocoder based on user input. Response
    is then returned to the user for verification."""
from mapbox import Geocoder
from Credentials import mapbox_token
def verify_location(user_input):
    geocoder = Geocoder(access_token=str(mapbox_token))
    response = geocoder.forward(str(user_input))
    collection = response.json()
    n = len(collection['features'])
    for i in range(0,n):
        print(collection['features'][i]['place_name'])

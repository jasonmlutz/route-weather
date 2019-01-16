"""This module takes user input location (origin/destination)
    and calls mapbox geocoder based on user input. Response
    is then returned to the user for verification."""
from mapbox import Geocoder
from Credentials import mapbox_token

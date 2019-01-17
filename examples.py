""" Testing ground for route-weather fuctionallity.
    """
import copy
from mapbox import Geocoder
from Credentials import mapbox_token
from input_verification import location_candidates, display_and_verify
d = location_candidates('213 N Main, CA')
display_and_verify(d)

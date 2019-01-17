""" Testing ground for route-weather fuctionallity.
    """
#import json
from mapbox import Geocoder
from Credentials import mapbox_token
from input_verification import location_candidates, display_and_verify
d = location_candidates('213 N Main, CA')
display_and_verify(d)
#origin = '416 Sid Snyder Ave SW, Olympia, WA 98504'
#origin = 'Main St, CA'
#geocoder = geocoder = Geocoder(access_token=str(mapbox_token))
#response = geocoder.forward(origin, limit = 20)
#len(response.geojson()['features']) #in practice, limit <= 10 ?

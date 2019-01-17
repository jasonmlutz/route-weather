""" Testing ground for route-weather fuctionallity.
    """
import copy
from mapbox import Geocoder, Directions
from Credentials import mapbox_token
origin = '416 Sid Snyder Ave SW, Olympia, WA 98504'
destination = '1315 10th St Room B-27, Sacramento, CA 95814'
geocoder = Geocoder(access_token=str(mapbox_token))
service = Directions(access_token=str(mapbox_token))
response_origin = geocoder.forward(str(origin))
origin_proper = response_origin.json()['features'][0]
response_destination = geocoder.forward(str(destination))
destination_proper= response_destination.json()['features'][0]
response = service.directions([origin_proper, destination_proper], 'mapbox/driving', steps='true')
route = response.geojson()
route.keys()
route['type']
len(route['features'])
route['features'][0]
type(route['features'][0])
route['features'][0].keys()
len(route['features'][0]['geometry'])
route['features'][0]['geometry'].keys()
len(route['features'][0]['geometry']['coodinates'])
#from input_verification import location_candidates, display_and_verify
#d = location_candidates('213 N Main, CA')
#e = display_and_verify(d)

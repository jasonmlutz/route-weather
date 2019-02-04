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
destination_proper = response_destination.json()['features'][0]
response = service.directions([origin_proper, destination_proper], profile='mapbox/driving', steps=True)
route = response.json()
route.keys()
route['routes']
len(route['routes'])
type(route['routes'])
type(route['routes'][0])
route['routes'][0].keys()
route['routes'][0]['geometry']
type(route['routes'][0]['legs'])
len(route['routes'][0]['legs'])
type(route['routes'][0]['legs'][0])
route['routes'][0]['legs'][0].keys()
route['routes'][0]['legs'][0]['summary']
route['routes'][0]['legs'][0]['weight']
route['routes'][0]['legs'][0]['duration']
type(route['routes'][0]['legs'][0]['steps'])
len(route['routes'][0]['legs'][0]['steps'])
route['routes'][0]['legs'][0]['steps'][0]
route['routes'][0]['legs'][0]['steps'][0].keys()
for i in range(len(route['routes'][0]['legs'][0]['steps'])): print(route['routes'][0]['legs'][0]['steps'][i]['maneuver']['instruction'])
for i in range(len(route['routes'][0]['legs'][0]['steps'])): print(route['routes'][0]['legs'][0]['steps'][i]['duration'])
#from input_verification import location_candidates, display_and_verify
#d = location_candidates('213 N Main, CA')
#e = display_and_verify(d)

origin = '416 Sid Snyder Ave SW, Olympia, WA 98504'
geocoder = Geocoder(access_token=str(mapbox_token))
response_origin = geocoder.forward(str(origin))
coords = response_origin.json()['features'][0]['center']
#t = datetime.now()
#t = (t+timedelta(minutes = 120, microseconds = -t.microsecond)).isoformat()
s = dt(2019, 2, 10, 13, 45, 25)
a = int(dt.timestamp(s))
olympia = forecast(darksky_token, coords[1], coords[0], time = a, units = 'us')

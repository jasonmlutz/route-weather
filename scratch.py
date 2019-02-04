from mapbox import Geocoder
from Credentials import mapbox_token, darksky_token
from fetch_weather import fetch_weather_summary
#from datetime import datetime as dt
from fetch_directions import *
from fetch_departure_time import *
origin = '416 Sid Snyder Ave SW, Olympia, WA 98504'
#destination = '1315 10th St Room B-27, Sacramento, CA 95814'
geocoder = Geocoder(access_token=str(mapbox_token))
#service = Directions(access_token=str(mapbox_token))
response_origin = geocoder.forward(str(origin))
origin_proper = response_origin.json()['features'][0]
#response_destination = geocoder.forward(str(destination))
#destination_proper = response_destination.json()['features'][0]
#response = service.directions([origin_proper, destination_proper], profile='mapbox/driving', steps=True)
#a = fetch_directions_summary(origin_proper, destination_proper)
#print("\n".join("{}: {}, {}, {}".format(k, v[0], v[1], v[2]) for k, v in a.items()))

t = get_departure_time()
coords = list(reversed(origin_proper['center']))
wx = fetch_weather_summary(coords[0], coords[1], t)



### testint fetch_weather
#coords = response_origin.json()['features'][0]['center']
#t = datetime.now()
#t = (t+timedelta(minutes = 120, microseconds = -t.microsecond)).isoformat()
#s = dt(2019, 2, 10, 13, 45, 25)
#a = int(dt.timestamp(s))
#f = fetch_weather_summary(coords[1], coords[0], a)

from mapbox import Geocoder
from Credentials import mapbox_token
from fetch_weather import fetch_weather_summary
from datetime import datetime as dt

origin = '416 Sid Snyder Ave SW, Olympia, WA 98504'
geocoder = Geocoder(access_token=str(mapbox_token))
response_origin = geocoder.forward(str(origin))
coords = response_origin.json()['features'][0]['center']
#t = datetime.now()
#t = (t+timedelta(minutes = 120, microseconds = -t.microsecond)).isoformat()
s = dt(2019, 2, 10, 13, 45, 25)
a = int(dt.timestamp(s))

fetch_weather_summary(coords[1], coords[0], a)

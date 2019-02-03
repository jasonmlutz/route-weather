"""Methods for fetching weather data from Darksky api. The current goal is to
    make sure that the output from Mapbox can be made compatible with the
    inputs to the DarkSky api.
    """
from darksky import forecast
from mapbox import Geocoder
from Credentials import mapbox_token, darksky_token
origin = '416 Sid Snyder Ave SW, Olympia, WA 98504'
geocoder = Geocoder(access_token=str(mapbox_token))
response_origin = geocoder.forward(str(origin))
coords = response_origin.json()['features'][0]['center']
olympia = forecast(darksky_token, coords[1], coords[0], units = 'us')
a = olympia['currently']

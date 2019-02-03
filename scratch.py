from darksky import forecast
from mapbox import Geocoder
from Credentials import mapbox_token, darksky_token
geocoder = Geocoder(access_token=str(mapbox_token))
wx = forecast(darksky_token, 108.5007, -45.7833)

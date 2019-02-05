"""Method for fetching weather data from Darksky api. The current goal is to
    make sure that the output from Mapbox can be made compatible with the
    inputs to the DarkSky api.
    """
from darksky import forecast

def fetch_weather_summary(latitude, longitude, time, key):
    """
    Returns summary and temperature for a location at a specified time in the
    past or future.

    Parameters:
    latitude (float): The latitide of the location.
    longitude (float): The longitude of the location.
    time (int/str): The time of the forecast/recorded weather. Either be a UNIX
        time (that is, seconds since midnight GMT on 1 Jan 1970) or a string
        formatted as follows: [YYYY]-[MM]-[DD]T[HH]:[MM]:[SS][timezone]. The former
        option is of the structure optained from int(time.time()); the latter
        as could be obtained from from datetime.datetime(YYYY, MM, DD,
        HH, MM, SS).isoformat(). To avoid issues with timezones, we will use the
        former option to represent time.

    Returns:
    A tuple. The first element is a short summary of the weather conditions
        (e.g. sunny, partly cloudy, rain); the second the integer-valued
        temperature in Fahrenheit (as dictated by the variable units = 'us').
    """
    inputs = key, latitude, longitude
    wx_full = forecast(*inputs, time=time, units='us')
    wx_current = wx_full['currently']
    return wx_current['summary'], int(wx_current['temperature']), wx_full.time

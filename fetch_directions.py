"""This module takes user input origin and destination
    and fetches directions using the mapbox cli api.
    """
from mapbox import Directions, Geocoder
# example origin: 416 Sid Snyder Ave SW, Olympia, WA 98504
# example destination: 1315 10th St Room B-27, Sacramento, CA 95814
USER_ORIGIN = input("What is your starting point? ")
USER_DESTINATION = input("What is your destination? ")
# a short test print statement
#print("origin: {}".format(USER_ORIGIN))
#print("destination: {}".format(USER_DESTINATION))
geocoder = Geocoder()
response_origin = geocoder.forward(USER_ORIGIN)
response_destination = geocoder.forward(USER_DESTINATION)

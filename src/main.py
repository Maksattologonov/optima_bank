import random
from datetime import datetime

import googlemaps

API_KEY = 'AIzaSyB5psr6MUHGAkI5ywWNERlquUncZN3W29Q'
gmaps = googlemaps.Client(API_KEY)
geocode_result = gmaps.geocode('Bishkek')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Bishkek Isanova 37/1",
                                     "37 ул. Исанова, Бишкек/1",
                                     departure_time=now)
# place_1 = "Bishkek Isanova 37/1"
# place_2 = "37 ул. Исанова, Бишкек/1"
#
#
# response = map_client.geocode(place_1)
# dir = map_client.directions(place_1, place_2)
# # request = map_client.address(response[0]['place_id'])


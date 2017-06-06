import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyB04CkoEBSVeTs2eOLWxfhPhKULIF7CFow')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

directions_result = gmaps.directions(origin="4416 prince edward, Wichita Falls, Tx 76308",
                                     destination="3410 Taft Blvd, Wichita Falls Tx, 76308",
                                     mode="walking",
                                     departure_time=now)

print(directions_result)
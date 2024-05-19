from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="myGeocoder")
location = geolocator.geocode("Llinars del Valles")

print(location.latitude, location.longitude)
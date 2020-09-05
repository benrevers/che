#Che.py - The business search tool
#Copyright Benjamin Ross Evers, 2014

# Import the relevant libraries
import urllib2
import json
import time

# Define the Places API key
AUTH_KEY = 'INSERT_GOOGLE_API_AUTH_KEY'

# Grab the address to search and build ADDRESS string
ADDRESS = raw_input("Please input the address to search near: ").replace(' ', '+')

# Compose a url to query the Geocoding API and decode the JSON
url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s') % (ADDRESS, AUTH_KEY)
response = urllib2.urlopen(url)
geocode_raw = response.read()
geocode_data = json.loads(geocode_raw)

# Pull latitude and longitude coordinates from JSON data and build COORDINATES string
lat = str(geocode_data[u'results'][0][u'geometry'][u'location'][u'lat'])
lng = str(geocode_data[u'results'][0][u'geometry'][u'location'][u'lng'])
COORDINATES = lat + "," + lng
print "\nFound: " + geocode_data[u'results'][0][u'formatted_address'] + " @ " + COORDINATES

# Grab the radius (in meters) for the search
RADIUS = raw_input("Please input the search radius in meters (default 5000): ") or 5000

# Define supported Place types list (current as of 9/8/2014)
SUPPORTED_TYPES = ['accounting', 'airport', 'amusement_park', 'aquarium', 'art_gallery',
			'atm', 'bakery', 'bank', 'bar', 'beauty_salon', 'bicycle_store',
			'book_store', 'bowling_alley', 'bus_station', 'cafe', 'campground',
			'car_dealer', 'car_rental', 'car_repair', 'car_wash', 'casino',
			'cemetery', 'church', 'city_hall', 'clothing_store', 'convenience_store',
			'courthouse', 'dentist', 'department_store', 'doctor', 'electrician',
			'electronics_store', 'embassy', 'establishment', 'finance', 'fire_station',
			'florist', 'food', 'funeral_home', 'furniture_store', 'gas_station',
			'general_contractor', 'grocery_or_supermarket', 'gym', 'hair_care',
			'hardware_store', 'health', 'hindu_temple', 'home_goods_store', 'hospital',
			'insurance_agency', 'jewelry_store', 'laundry', 'lawyer', 'library',
			'liquor_store', 'local_government_office', 'locksmith', 'lodging', 'meal_delivery',
			'meal_takeaway', 'mosque', 'movie_rental', 'movie_theater', 'moving_company',
			'museum', 'night_club', 'painter', 'park', 'parking', 'pet_store', 'pharmacy',
			'physiotherapist', 'place_of_worship', 'plumber', 'police', 'post_office',
			'real_estate_agency', 'restaurant', 'roofing_contractor', 'rv_park', 'school',
			'shoe_store', 'shopping_mall', 'spa', 'stadium', 'storage', 'store', 'subway_station',
			'synagogue', 'taxi_stand', 'train_station', 'travel_agency', 'university',
			'veterinary_care', 'zoo']

# Grab TYPE input (default type "establishment")
TYPES = raw_input("Please input the Google type to search (default 'establishment'): ") or "establishment"

# Compose a URL to query the location
url = ('https://maps.googleapis.com/maps/api/place/radarsearch/json?location=%s'
		'&radius=%s&types=%s&sensor=false&key=%s') % (COORDINATES, RADIUS, TYPES, AUTH_KEY)

# Send the GET request to the Place details service (using url from above)
response = urllib2.urlopen(url)
print "\nREQUEST SENT..."
print "RESPONSE RETRIEVED..."

# Get the response and use the JSON library to decode the JSON
json_raw = response.read()
json_data = json.loads(json_raw)
print "JSON DECODED...\n"

# Loop through Place reference numbers and pull Place details
for place in json_data[u'results']:
	url = ('https://maps.googleapis.com/maps/api/place/details/json?'
				'reference=%s&sensor=false&key=%s' % (place[u'reference'], AUTH_KEY))
	response = urllib2.urlopen(url)
	details_raw = response.read()
	details_data = json.loads(details_raw)
	try:
		print details_data[u'result'][u'name'] + " * " + details_data[u'result'][u'formatted_phone_number'] + " * " + details_data[u'result'][u'formatted_address']
	except Exception:
		print "EXCEPTION THROWN"
		pass
	#time.sleep(1)

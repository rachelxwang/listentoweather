import requests, json
from datetime import datetime
from time import time
from ipstack import GeoLookup

# The API Key and base URL to access the API
api_key = "815896cb334c3837807948ed79b6d947"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# URL that combines base with API key
api_url = base_url + "appid=" + api_key

# Number of minutes between API updates
# OpenWeatherMap data only refreshes every 10 minutes or so
mins_between_updates = 10


# Dictionary to map location types to appropriate URL variables
location_type_switcher = {
	"city":    "q=%s",
	"city_id": "id=%s",
	"coords":  "lat=%s&lon=%s",
	"zipcode": "zip=%s,%s"
}


def current_location_weather():
	geo_lookup = GeoLookup("9ff825aee8c78758e19180acda87060c")
	location = geo_lookup.get_own_location()
	coords = (location["latitude"], location["longitude"])
	return WeatherData(coords, "coords")


class WeatherData:
	_prev_call = None
	_curr_call = None

	_last_updated = None

	_location = None
	_location_type = None

	def __init__(self, location, location_type):
		self._location = location
		self._location_type = location_type


	# Change to a different location
	def change_location(self, location, location_type):
		self._location = location
		self._location_type = location_type
		self._last_updated = None


	# Get the current weather
	def update_weather(self):

		# Get the current time - used to determine when to update
		curr_time = datetime.utcnow()

		# If enough time has passed since the last call, get an update
		if (self._last_updated == None or more_than_x_mins(self._last_updated, curr_time, mins_between_updates)):

			# Get the request from the server
			response = requests.get(self.get_complete_url())
			x = response.json();

			# If city is not found, return None
			if x["cod"] == "404":
				return None

			# Otherwise, update the object
			else:
				self._prev_call = self._curr_call
				self._curr_call = x
				self._last_updated = curr_time

		# Return the most recent weather call
		return self._curr_call

	def get_weather(self):

		self.update_weather()

		(daytime, percent) = self.get_daytime()

		return {
			"category": self.get_category(),

			"time": {
				"dayOrNight": daytime,
				"percent": percent,
				"hour": datetime.utcfromtimestamp(int(time()) + self._curr_call["timezone"]).hour,
				"sunrise": self._curr_call["sys"]["sunrise"],
				"sunset":  self._curr_call["sys"]["sunset"],
			},

			# Units: Kelvin
			"temp": self.get_temperature(),

			# Units: hectopascals (hPa) - range will be approximately 870 - 1085
			"pressure": self._curr_call["main"]["pressure"],

			# Units: Percentage
			"humidity": self._curr_call["main"]["humidity"],

			# Units:
			#   speed, gust:     meters per second (highest: ~113.3?)
			#   deg (direction): meteorological degrees (degrees clockwise starting at North,
			# 					 representing where the wind is COMING from)
			"wind": self._curr_call["wind"],

			# Units: Percentage
			"clouds": self._curr_call["clouds"]["all"],
		}


	def get_category(self):

		# Update the weather
		self.update_weather()

		# Get the weather ID
		return self._curr_call["weather"][0]["main"]


	def get_temperature(self):

		self.update_weather()

		return self._curr_call["main"]["feels_like"]



	def get_daytime(self):

		# Update the current weather
		self.update_weather()

		# Get sunrise, sunset, and current time
		sunrise = self._curr_call["sys"]["sunrise"]
		sunset = self._curr_call["sys"]["sunset"]
		current = int(time())

		# Calculate whether it's day or night
		day_time = ""
		if (sunrise < sunset):
			day_time = "night" if (current > sunset) else "day"
		else:
			day_time = "day" if (current > sunrise) else "night"

		# Calculate percentage into the day/night
		(last_time, next_time) = (sunrise, sunset) if (day_time == "day") else (sunset, sunrise + (24*60*60))
		percent = ((current - last_time) / (next_time - last_time))

		# Return these as a tuple
		return (day_time, percent)


	# Get the complete API URL to read data from
	def get_complete_url(self):
		return api_url + "&" + (location_type_switcher[self._location_type] % self._location)

	def get_location(self):
		return (self._location, self._location_type)

	def get_weather_id(self):
		self.update_weather()
		return self._curr_call["weather"][0]["id"]



def more_than_x_mins(t1, t2, mins):
	return abs(t1 - t2).seconds > (mins * 60)


test = WeatherData("chicago", "city")

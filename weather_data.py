import requests, json
from datetime import datetime

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


	# Get the current weather
	def get_weather(self):

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


	# Get the complete API URL to read data from
	def get_complete_url(self):
		return api_url + "&" + (location_type_switcher[self._location_type] % self._location)

	def get_location(self):
		return (self._location, self._location_type)



def more_than_x_mins(t1, t2, mins):
	return abs(t1 - t2).seconds > (mins * 60)


test = WeatherData("London", "city")

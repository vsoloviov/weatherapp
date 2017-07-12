import json, requests
import logging
import time, os, stat

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

def file_age_in_seconds(pathname):
    return time.time() - os.stat(pathname)[stat.ST_MTIME]

def GetCityID(city):
	with open("./citiesdatabase/citylist.json") as f:
		data = json.load(f)
		for key in data:
			if key["name"] == city and key["cc"] == "UA":
				return key["id"]
def GetFromCache(cityid, datafilename):
	try:
		with open(datafilename) as f:
			try:
				data = json.load(f)
				logging.debug('Loading JSON object from ' + datafilename)
				return data
				if data is None:
					logging.debug('JSON file loaded as None object.')
					return False
			except (EnvironmentError,ValueError) as e:
				return False

	except EnvironmentError as e:
		return False # return 'False' if no cache file found

def GetCurrentWheater(city):
	city_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=' + city

	unit_url = '&units=metric'
	unit = 'Celsius'

	type = 'accurate' # 'accurate' must be exact match of city name, 'like' serves up the closest match
	type_url = '&type=' + type

	count = 1
	count_url = '&cnt=' + str(count)

	APIKey = 'b139bdf8ae48e63b8155c4bf6d0a6807'
	API_url = '&APPID=' + APIKey

	url = city_url + unit_url + type_url + count_url + API_url
	weatherToday = dict()
	
	cityid = GetCityID(city)
	cachefilename = "./cache/" + str(cityid) + ".json"
	cache = GetFromCache(cityid, cachefilename)
	if cache is False or int(file_age_in_seconds(cachefilename)) > 300:
		logging.debug('No cache file or file too old (age is ' + str(file_age_in_seconds(cachefilename)) + ', working with API directly')
		try:
			response = requests.get(url)
			response.raise_for_status()
			weatherData = json.loads(response.text)
			weatherToday = weatherData['list'][0]
		except:
			raise ('Error: cannot find city, try using city id for precise location')
				
		try:
			with open(cachefilename, "w") as f:
				f.write(json.dumps(weatherToday))
				return weatherToday
		except EnvironmentError as e:
			print "Oops: " + e
	else:
		weatherToday = cache
		logging.debug('Got weather from cache file')
		return weatherToday

print GetCurrentWheater("Odessa")



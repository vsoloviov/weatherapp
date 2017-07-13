import json
import urllib2
import time, os, stat
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

def file_age_in_seconds(pathname):
    return time.time() - os.stat(pathname)[stat.ST_MTIME]

def DownloadNewDBFile(cityinfofile):
	logging.debug('File  ' + cityinfofile + ' is ' + str(file_age_in_seconds(cityinfofile)) + 'old. Downloading new one')
	try:
		response = urllib2.urlopen('http://openweathermap.org/help/city_list.txt')
		html = response.read()
		try:
			with open(cityinfofile, "w") as f:
				f.write(html)
		except EnvironmentError as e:
			print e
	except urllib2.HTTPError as e:
		print "City info file download error: " + str(e) 	

def UpdateDB():
	cityinfo = dict()
	cityinfomap = []
	cityinfofile = "./citiesdatabase/city_list.txt"
	if file_age_in_seconds(cityinfofile) > 86400:
		DownloadNewDBFile(cityinfofile)
	if os.stat(cityinfofile).st_size == 0:
		DownloadNewDBFile(cityinfofile)
	with open(cityinfofile) as f:
		logging.debug('File ' + cityinfofile + ' age ' + str(file_age_in_seconds(cityinfofile)))
		for line in f:
			tmp = line.split()
			if len(tmp) == 5:
				cityinfo["id"] = tmp[0]
				cityinfo["name"] = tmp[1]
				cityinfo["lat"] = tmp[2]
				cityinfo["lon"] = tmp[3]
				cityinfo["cc"] = tmp[4]
			
			try:
				json.dumps(cityinfo)
				cityinfomap.append(cityinfo.copy())
			except:
				logging.debug ("Some strange city %s. Skipping line" % tmp[1])

	with open("./citiesdatabase/citylist.json", "w") as f:
		f.write(json.dumps(cityinfomap))


UpdateDB()
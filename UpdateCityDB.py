import json
def UpdateDB():
	cityinfo = dict()
	cityinfomap = []
	with open("./citiesdatabase/city_list.txt") as f:
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
				print "Some strange city %s" % tmp[1]

	with open("./citiesdatabase/citylist.json", "w") as f:
		f.write(json.dumps(cityinfomap))


UpdateDB()
from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime
import pygeoip

import GetWeather

app = Flask(__name__)
geolocate = pygeoip.GeoIP('GeoLiteCity.dat')

@app.route("/", methods = ['POST', 'GET'])
def chart():

	ip_address = request.remote_addr
	#ip_address = "94.153.141.170"
	geo_data = geolocate.record_by_addr(ip_address)
	if request.method == 'POST':
		result = request.form
		default_city = result["Name"]
		if GetWeather.GetCityID(default_city) is None:
			return render_template('404.html', city=default_city), 404
	else:
		if not geo_data is None:
			default_city = geo_data["city"]
		else:
			default_city = "Odessa"


	data = GetWeather.GetCurrentWheater(default_city)
	usertime = datetime.now().strftime('%H:%M')


	return render_template('index.html', 
		clouds=data["clouds"], speed=data["speed"], 
		humidity=data["humidity"], eve_temp=int(data["temp"]["eve"]),
		weather_description=data["weather"][0]["description"],
		default_city=default_city, usertime=usertime,
		dayornight=data["weather"][0]["icon"], pressure=data["pressure"]
		) 




if __name__ == "__main__":
	#get_pbf_state()
	app.run(debug=True,host='0.0.0.0',port=5000)



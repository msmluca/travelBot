import googlemaps
from datetime import datetime
import time
import csv
import os
import json


class travelBotdistance():

	def setUp(self):
		#self.key = 'AIzaSyBUV64wz3G7-c-5Vgni9NpCrsKdi9Iw4S8'
		self.key = 'AIzaSyC0Na5lm99GZSQE7tVDWkf1jnFAnws_8hQ'
		self.client = googlemaps.Client(self.key)

	def timeDist(self, start_location, end_locations):

		now = datetime.now()
		matrix = self.client.distance_matrix(start_location, end_locations 
											,mode="driving"
											,avoid="tolls"
											,units="imperial")
		
		#print matrix
		results = {}
		dest_addresses = matrix["destination_addresses"]
		
		i=0
		for it in dest_addresses:
			duration_text 	= matrix["rows"][0]["elements"][i]["duration"]["text"]
			duration_value 	= matrix["rows"][0]["elements"][i]["duration"]["value"]
			distance_text 	= matrix["rows"][0]["elements"][i]["distance"]["text"]
			distance_value 	= matrix["rows"][0]["elements"][i]["distance"]["value"]
			
			temp = {end_locations[i][:-4]:[duration_text, duration_value, distance_text, distance_value, dest_addresses[i]]}
			i+=1
			results = dict(results.items()+temp.items())
			#results = {"York":["2h 3m",36185,"120km",120234,"York, UK"],"London":["1h 30m", 5432, "70km", 70123, "London, UK"]}
		return results
		
	
		
	def getWeather(self, destinations):
		def process_weather_file(file):
			fin = open(file, 'rb')
			
			weather = json.load(fin)
			fin.close()
			
			weather_list = []
			for i in range(1,4):
				#print "i=",i
				w_day 	= weather["list"][i]["temp"]["day"]
				w_min 	= weather["list"][i]["temp"]["min"]
				w_max 	= weather["list"][i]["temp"]["max"]
				w_night = weather["list"][i]["temp"]["night"]
				w_eve 	= weather["list"][i]["temp"]["eve"]
				w_morn 	= weather["list"][i]["temp"]["morn"]
				
				w_main 	= weather["list"][i]["weather"][0]["main"]
				w_desc 	= weather["list"][i]["weather"][0]["description"]
				
				w_speed = weather["list"][i]["speed"]
				w_deg 	= weather["list"][i]["deg"]
				w_clouds= weather["list"][i]["clouds"]
				
				try:
					w_rain = weather["list"][i]["rain"]
				except:
					w_rain = 0.0
				
				weather_list.extend([w_day, w_min, w_max, w_night, w_eve, w_morn, w_main, w_desc, w_speed, w_deg, w_clouds, w_rain])
				
			return weather_list
		# ------------------------------------------------------- #
		
		dir = "WeatherData"
		results = {}
		for dest in destinations:
			for root, subDirs, files in os.walk(dir):
				for f in files:
					if os.path.basename(f).replace('.json','').lower() == dest[:-4].lower():
						#print "match!"
						vals = process_weather_file(os.path.join(dir, f))
					
						temp = {dest[:-4]: vals}
						
						results = dict(results.items()+temp.items())
						break
		
		return results
						
					
	def getDestination(self):
		fileIn = os.path.join("csv","destinations.csv")
			
		fin = open(fileIn, 'rb')
		
		csvr = csv.reader(fin)
		
		dest = []
		for r in csvr:
			if "Destination" not in r[0]:
				dest.append(r[0]+', UK')
				
		
		fin.close()
		return dest

	def getCoordinates(self, place, city):
		coordinates = self.client.geocode(place+','+city)
		print coordinates
		lat = str(coordinates[0]["geometry"]["location"]["lat"])
		lng = str(coordinates[0]["geometry"]["location"]["lng"])
		
		
		return (lat, lng) 


if __name__ == "__main__":
	origin = "Coventry, UK"
	origin = {"lng":-3.51434,"lat":50.46384}
	
	tDD = travelBotdistance()
	tDD.setUp()
	end_locations = tDD.getDestination()

	end_locations = end_locations[:2]
	#print end_locations
	
	print "duration, distance"
	res = tDD.timeDist(origin, end_locations)
	for it in res:		print it, res[it]
		
	print "weather"
	res = tDD.getWeather(end_locations)	
	for it in res:		print it, res[it]
	
# a = travelBotdistance()
# a.setUp()
# print a.timeDist("london","manchester, UK")
import pandas as pd
import travelBotdestinations as da
import travelBotdistance as dd
import travelBothotels as dh

class travelBotrecommend():

	def top_hotels(self, dest_activities, dest_weather, dest_time):
		return




if __name__ == "__main__":

	# Load Destination Activities
	da_obj = da.travelBotdestinations()
	dest_activities = da_obj.load_destinations("./csv/destinations.csv")

	# Load Destination Weather
	# 0 = Fri Day Temp, 12 = Sat Day Temp, 24 = Sun Day Temp
	dd_obj = dd.travelBotdistance()
	dd_obj.setUp()
	dest_list = dd_obj.getDestination()
	dest_weather = dd_obj.getWeather(dest_list)

	# Load Destination Travel
	dest_time = dd_obj.timeDist('london, uk', dest_list)

	rec = travelBotrecommend()
	rec.top_hotels(dest_activities, dest_weather, dest_time)

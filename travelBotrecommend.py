import travelBotdestinations as da
import travelBotdistance as dd
import travelBothotels as dh
import operator

class travelBotrecommend():

	def __init__(self, start_position ):


		# Load Destination Activities
		self.da_obj = da.travelBotdestinations()
		self.dest_activities = self.da_obj.load_destinations("./csv/DestinationActivityFreqRank.csv")


		# Load Destination Weather
		# 0 = Fri Day Temp, 12 = Sat Day Temp, 24 = Sun Day Temp
		dd_obj = dd.travelBotdistance()
		dd_obj.setUp()
		self.dest_list = dd_obj.getDestination()
		self.dest_weather = dd_obj.getWeather(self.dest_list)

		# Load Destination Travel
		self.dest_time = dd_obj.timeDist(start_position, self.dest_list)

		# Load Destination Hotels
		dh_obj = dh.travelBothotels()
		self.dest_hotels = dh_obj.load_hotels('./csv/hotel_info.csv')

	def getCoordinates(self, place, city):
		return self.da_obj.getCoordinates(place,city)

	def top_hotels(self, activity, max_time, max_budget, nights=2):

		dh_obj = dh.travelBothotels()
		res = {}

		# Calculate ratings for each destination-hotel combination
		for dest_hotel, hotel_details in self.dest_hotels.iteritems():
			if float(hotel_details['Price'])*nights <= max_budget and self.dest_time[dest_hotel[0]][1] <= max_time:
				
				weather_temp_score_sat = 0
				if self.dest_weather[dest_hotel[0]][12] < 0:
					weather_temp_score_sat = 0
				elif self.dest_weather[dest_hotel[0]][12] < 10:
					weather_temp_score_sat = 0.25
				elif self.dest_weather[dest_hotel[0]][12] < 20:
					weather_temp_score_sat = 0.5
				elif self.dest_weather[dest_hotel[0]][12] < 30:
					weather_temp_score_sat = 0.75
				elif self.dest_weather[dest_hotel[0]][12] >= 30:
					weather_temp_score_sat = 1

				weather_rain_score_sat = 0
				if self.dest_weather[dest_hotel[0]][23] >= 50:
					weather_rain_score_sat = 0
				elif self.dest_weather[dest_hotel[0]][23] >= 7.6:
					weather_rain_score_sat = 0.25
				elif self.dest_weather[dest_hotel[0]][23] >= 2.5:
					weather_rain_score_sat = 0.5
				elif self.dest_weather[dest_hotel[0]][23] > 0:
					weather_rain_score_sat = 0.75
				elif self.dest_weather[dest_hotel[0]][23] == 0:
					weather_rain_score_sat = 1

				weather_wind_score_sat = 0
				if self.dest_weather[dest_hotel[0]][20] > 30:
					weather_wind_score_sat = 0
				elif self.dest_weather[dest_hotel[0]][20] > 13:
					weather_wind_score_sat = 0.25
				elif self.dest_weather[dest_hotel[0]][20] > 5:
					weather_wind_score_sat = 0.5
				elif self.dest_weather[dest_hotel[0]][20] > 0:
					weather_wind_score_sat = 0.75
				elif self.dest_weather[dest_hotel[0]][20] == 0:
					weather_wind_score_sat = 1

				weather_cloud_score_sat = 1-(float(self.dest_weather[dest_hotel[0]][22])/100.0)

				weather_temp_score_sun = 0
				if self.dest_weather[dest_hotel[0]][24] < 0:
					weather_temp_score_sun = 0
				elif self.dest_weather[dest_hotel[0]][24] < 10:
					weather_temp_score_sun = 0.25
				elif self.dest_weather[dest_hotel[0]][24] < 20:
					weather_temp_score_sun = 0.5
				elif self.dest_weather[dest_hotel[0]][24] < 30:
					weather_temp_score_sun = 0.75
				elif self.dest_weather[dest_hotel[0]][24] >= 30:
					weather_temp_score_sun = 1

				weather_rain_score_sun = 0
				if self.dest_weather[dest_hotel[0]][35] >= 50:
					weather_rain_score_sun = 0
				elif self.dest_weather[dest_hotel[0]][35] >= 7.6:
					weather_rain_score_sun = 0.25
				elif self.dest_weather[dest_hotel[0]][35] >= 2.5:
					weather_rain_score_sun = 0.5
				elif self.dest_weather[dest_hotel[0]][35] > 0:
					weather_rain_score_sun = 0.75
				elif self.dest_weather[dest_hotel[0]][35] == 0:
					weather_rain_score_sun = 1

				weather_wind_score_sun = 0
				if self.dest_weather[dest_hotel[0]][32] > 30:
					weather_wind_score_sun = 0
				elif self.dest_weather[dest_hotel[0]][32] > 13:
					weather_wind_score_sun = 0.25
				elif self.dest_weather[dest_hotel[0]][32] > 5:
					weather_wind_score_sun = 0.5
				elif self.dest_weather[dest_hotel[0]][32] > 0:
					weather_wind_score_sun = 0.75
				elif self.dest_weather[dest_hotel[0]][32] == 0:
					weather_wind_score_sun = 1

				weather_cloud_score_sun = 1-(float(self.dest_weather[dest_hotel[0]][34])/100.0)

				weather_score_final = float(weather_temp_score_sat + weather_rain_score_sat + weather_wind_score_sat + weather_cloud_score_sat \
										+ weather_temp_score_sun + weather_rain_score_sun + weather_wind_score_sun + weather_cloud_score_sun) / 8.0
				hotel_score_final = (float(hotel_details['Star Rating'])/5.0 + float(hotel_details['Review'])/100.0)/2.0
				activity_score_final = (1-(float(self.dest_activities[dest_hotel[0]][activity + ' Rank'])/40.0)) 

				res[dest_hotel] = weather_score_final + hotel_score_final + activity_score_final

		# # Top 3 results
		res_sorted = sorted(res.iteritems(), key=operator.itemgetter(1), reverse=True)
		res_top3 = [res_sorted[0]]
		city_top3 = [res_sorted[0][0][0]]
		for i in range(1,len(res_sorted)):
			city = res_sorted[i][0][0]
			if city not in city_top3:
				res_top3.append(res_sorted[i])
				city_top3.append(res_sorted[i][0][0])
				if len(res_top3) == 3:
					break

		# Repackage
		res_top3_final = {}
		for i in range(0,len(res_top3)):
			res_top3_final[res_top3[i][0]] = {
				'Position':i+1,
				'Total Price':float(self.dest_hotels[res_top3[i][0]]['Price'])*nights,
				'Star Rating':self.dest_hotels[res_top3[i][0]]['Star Rating'],
				'Review':self.dest_hotels[res_top3[i][0]]['Review'],
				'Time':self.dest_time[res_top3[i][0][0]][0],
				'Sat Temp':self.dest_weather[res_top3[i][0][0]][12],
				'Sun Temp':self.dest_weather[res_top3[i][0][0]][24],
				'Activity':self.dest_activities[res_top3[i][0][0]][activity]
			}

		return res_top3_final



if __name__ == "__main__":

	rec = travelBotrecommend("london, uk")
	res = rec.top_hotels('Museums', 10000, 1000)

	print(res)

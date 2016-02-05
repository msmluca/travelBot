import travelBotdestinations as da
import travelBotdistance as dd
import travelBothotels as dh
import operator

class travelBotrecommend():

	def __init__(self, start_position ):
			# Load Destination Activities
		da_obj = da.travelBotdestinations()
		self.dest_activities = da_obj.load_destinations("./csv/destinations2.csv")

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

	def top_hotels(self, activity, max_time, max_budget, nights=2):

		dh_obj = dh.travelBothotels()
		res = {}

		# Calculate ratings for each destination-hotel combination
		for dest_hotel, hotel_details in self.dest_hotels.iteritems():
			if float(hotel_details['Price'])*nights <= max_budget and self.dest_time[dest_hotel[0]][1] <= max_time:
				res[dest_hotel] = float(hotel_details['Star Rating'])/5.0 \
											+ float(hotel_details['Review'])/100.0 \
											+ (1-(float(self.dest_activities[dest_hotel[0]][activity])/40.0))

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
				'Position':i,
				'Price':self.dest_hotels[res_top3[i][0]]['Price'],
				'Star Rating':self.dest_hotels[res_top3[i][0]]['Star Rating'],
				'Review':self.dest_hotels[res_top3[i][0]]['Review'],
				'Time':self.dest_time[res_top3[i][0][0]][0],
				'Sat Temp':self.dest_weather[res_top3[i][0][0]][12],
				'Sun Temp':self.dest_weather[res_top3[i][0][0]][24]
			}

		return res_top3_final



if __name__ == "__main__":



	rec = travelBotrecommend("london, uk")
	res = rec.top_hotels('Museums', 10000, 1000)

	print(res)

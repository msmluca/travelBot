import travelBotdestinations as da
import travelBotdistance as dd
import travelBothotels as dh
import operator

class travelBotrecommend():

	def top_hotels(self, dest_activities, dest_weather, dest_time, activity, max_time, max_budget):

		dh_obj = dh.travelBothotels()
		res = {}

		# dest = [d[:-4] for d in dest_activities.keys()]

		# # activities
		# res = dict.fromkeys(dest)
		# print res
		# for d in dest:
		# 	val = dest_activities[d+', UK']

		# 	li = [(k,v) for (k,v) in val.iteritems()]

		# 	li = sorted(li)

		# 	#print li
		# 	ki = [it[1] for it in li]

		# 	#print "ki=",  ki
		# 	res[d]=ki
		                
		# # weather
		# for d in dest:
		# 	val_w = dest_weather[d]
		# 	val_t = dest_time[d]

		# 	old = res[d]
		# 	res[d] = old+val_w+val_t

		# Calculate ratings for each destination-hotel combination
		for destination, dest_details in dest_activities.iteritems():
			for hotel, hotel_details in dh_obj.load_hotels("./csv/hotel_info.csv", destination).iteritems():
				res[(destination,hotel)] = float(hotel_details['Star Rating'])/5.0 \
											+ float(hotel_details['Review'])/100.0 \
											+ (1-(float(dest_details[activity])/40.0))

		# Top 3 results
		res_sorted = sorted(res.iteritems(), key=operator.itemgetter(1), reverse=True)
		res_top3 = [res_sorted[0]]
		city_top3 = [res_sorted[0][0][0]]
		for i in range(1,len(res_sorted)):
			city = res_sorted[i][0][0]
			if city not in city_top3:
				res_top3.append(res_sorted[i])
				if len(res_top3) == 3:
					break

		return res_top3



if __name__ == "__main__":

	# Load Destination Activities
	da_obj = da.travelBotdestinations()
	dest_activities = da_obj.load_destinations("./csv/destinations2.csv")

	# Load Destination Weather
	# 0 = Fri Day Temp, 12 = Sat Day Temp, 24 = Sun Day Temp
	dd_obj = dd.travelBotdistance()
	dd_obj.setUp()
	dest_list = dd_obj.getDestination()
	dest_weather = dd_obj.getWeather(dest_list)

	# Load Destination Travel
	dest_time = dd_obj.timeDist('london, uk', dest_list)

	rec = travelBotrecommend()
	res = rec.top_hotels(dest_activities, dest_weather, dest_time, 'Museums', 0, 0)

	print(res)

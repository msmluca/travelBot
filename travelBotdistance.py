import googlemaps
from datetime import datetime
import time



class travelBotdistance():

	def setUp(self):
		self.key = 'AIzaSyBUV64wz3G7-c-5Vgni9NpCrsKdi9Iw4S8'
		self.client = googlemaps.Client(self.key)

	def timeDist(self, start_location, end_locations):

		now = datetime.now()
		matrix = self.client.distance_matrix(start_location, end_locations ,
											mode="driving",
											avoid="tolls",
											units="imperial"
											)
		return matrix


# a = travelBotdistance()
# a.setUp()
# print a.timeDist("london","manchester, UK")